import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def plot_vz_profiles(filename, y_target, x_start, x_end, x_step):
    """
    Plots Vz (Velocity w) as a function of z for a specific y-plane, 
    across a range of x positions, and calculates the line integral (∫ Vz dz).
    """
    print(f"Loading data from '{filename}'...")
    try:
        df = pd.read_csv(filename, skipinitialspace=True)
    except FileNotFoundError:
        print(f"Error: Could not find the file '{filename}'.")
        return

    # Clean column names
    df.columns = df.columns.str.strip()

    # Map your specific column names
    col_x = 'x [mm]'
    col_y = 'y [mm]'
    col_z = 'z [mm]'
    col_w = 'Velocity w [m/s]'

    # Verify columns exist
    for col in [col_x, col_y, col_z, col_w]:
        if col not in df.columns:
            print(f"Error: Column '{col}' not found in the dataset.")
            return

    # 1. Find the closest actual 'y' in the dataset
    actual_y = df.iloc[(df[col_y] - y_target).abs().argsort()[:1]][col_y].values[0]
    print(f"Target y = {y_target} mm | Using closest actual y = {actual_y} mm")

    df_y = df[df[col_y] == actual_y]

    if df_y.empty:
        print("No data found for this y-plane.")
        return

    # 2. Generate the list of target x values
    target_xs = np.arange(x_start, x_end + (x_step * 0.1), x_step)

    # Setup the plot
    plt.figure(figsize=(9, 8)) 
    
    colors = cm.viridis(np.linspace(0, 1, len(target_xs)))
    lines_plotted = 0

    # 3. Loop through x values, process data, calculate integral, and plot
    for tx, color in zip(target_xs, colors):
        actual_x = df_y.iloc[(df_y[col_x] - tx).abs().argsort()[:1]][col_x].values[0]
        
        if abs(actual_x - tx) > 2.0:
            continue

        df_x = df_y[df_y[col_x] == actual_x]
        
        # Sort by z to ensure clean plotting AND accurate integration
        df_x = df_x.sort_values(by=col_z)
        
        z_vals = df_x[col_z].values
        vz_vals = df_x[col_w].values

        # --- CALCULATE THE LINE INTEGRAL ---
        # np.trapz integrates the velocity (y-axis data) along the physical z-coordinates (x-axis data)
        integral_val = np.trapz(vz_vals, x=z_vals)
        
        # Create a detailed label showing the x-position and the calculated integral
        label_str = f"x ≈ {actual_x:.1f} mm  |  $I_{{VR}}$ = {integral_val:.2f}"

        # Plot the profile
        plt.plot(vz_vals, z_vals, label=label_str, color=color, linewidth=1.5)
        lines_plotted += 1

    if lines_plotted == 0:
        print("No valid lines were found to plot within the domain.")
        return

    # 4. Formatting the graph
    plt.title(f"Vertical Velocity ($V_z$) Profiles at $y \\approx {actual_y}$ mm", fontsize=14)
    plt.xlabel("Velocity $V_z$ (m/s)", fontsize=12)
    plt.ylabel("z (mm)", fontsize=12)
    
    plt.axvline(0, color='black', linewidth=1, linestyle='--', alpha=0.7)
    
    # Place the legend outside the plot area
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10, 
               title="Position & Integral", title_fontsize=11)
    
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()

    # Save and show
    output_filename = f"Vz_profiles_integrated_y{actual_y}_x{x_start}_to_{x_end}.png"
    plt.savefig(output_filename, dpi=150)
    print(f"Graph saved as: {output_filename}")
    plt.show()

def plot_upper_boundary_profiles(filename, y_target, x_min=0.0, x_max=130.0, z_start=0.0, z_end=-25.0, z_step=2.5):
    print(f"Loading data from '{filename}'...")
    try:
        df = pd.read_csv(filename, skipinitialspace=True)
    except FileNotFoundError:
        print(f"Error: Could not find the file '{filename}'.")
        return

    df.columns = df.columns.str.strip()

    col_x = 'x [mm]'
    col_y = 'y [mm]'
    col_z = 'z [mm]'
    col_u = 'Velocity u [m/s]'

    for col in [col_x, col_y, col_z, col_u]:
        if col not in df.columns:
            print(f"Error: Column '{col}' not found in the dataset.")
            return

    # 1. Find the closest actual 'y' in the dataset
    actual_y = df.iloc[(df[col_y] - y_target).abs().argsort()[:1]][col_y].values[0]
    print(f"Target y = {y_target} mm | Using closest actual y = {actual_y} mm")

    # Filter dataframe to this specific y-plane
    df_y = df[df[col_y] == actual_y]

    if df_y.empty:
        print("No data found for this y-plane.")
        return

    # 2. Generate the list of target z values
    # We use a negative step to go from 0 down to -25
    target_zs = np.arange(z_start, z_end - (z_step * 0.1), -z_step)

    # Setup the plot
    plt.figure(figsize=(8, 9)) # Made taller for vertical representation
    
    # Use a colormap to visualize distance from the airfoil
    colors = cm.plasma(np.linspace(0, 1, len(target_zs)))
    lines_plotted = 0

    # 3. Loop through z-slices, process data, and plot
    for tz, color in zip(target_zs, colors):
        # Find closest actual z in the dataset
        actual_z = df_y.iloc[(df_y[col_z] - tz).abs().argsort()[:1]][col_z].values[0]
        
        # Prevent plotting if the mesh node is too far from our target step
        if abs(actual_z - tz) > (z_step / 2):
            continue

        # Filter for this z-slice AND restrict to the x domain (0 to 130)
        df_z = df_y[(df_y[col_z] == actual_z) & 
                    (df_y[col_x] >= x_min) & 
                    (df_y[col_x] <= x_max)]
        
        # Sort by x to ensure the line is drawn smoothly from front to back
        df_z = df_z.sort_values(by=col_x)
        
        x_vals = df_z[col_x].values
        vx_vals = df_z[col_u].values

        if len(x_vals) < 2:
            print(f"Skipping z ≈ {actual_z:.1f} (Inside airfoil or insufficient data).")
            continue

        #CALCULATE THE LINE INTEGRAL 
        # Integrating Vx with respect to x
        integral_val = np.trapz(vx_vals, x=x_vals)
        
        label_str = f"z ≈ {actual_z:.1f} mm  |  $I_{{VR}}$ = {integral_val:.1f}"

        # PLOT AXES INVERTED: (Velocity on horizontal, x on vertical)
        plt.plot(vx_vals, x_vals, label=label_str, color=color, linewidth=1.5)
        lines_plotted += 1

    if lines_plotted == 0:
        print("No valid lines were found to plot within the domain.")
        return

    # 4. Formatting the graph
    plt.title(f"Horizontal Velocity ($V_x$) Profiles at $y \\approx {actual_y}$ mm", fontsize=14)
    
    # INVERTED LABELS
    plt.xlabel("Horizontal Velocity, $V_x$ (m/s)", fontsize=12)
    plt.ylabel("Chordwise Position, $x$ (mm)", fontsize=12)
    
    # Optional vertical line at V=0
    plt.axvline(0, color='black', linewidth=1, linestyle='--', alpha=0.7)
    
    # Enforce x-axis limits visually (now on the y-axis of the plot)
    plt.ylim(x_max, x_min)
    plt.xlim(6,7.5)
    
    # Place the legend outside the plot area
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10, 
               title="Height ($z$) & Integral", title_fontsize=11)
    
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()

    # Save and show
    output_filename = f"Upper_Boundary_Vx_inverted_y{actual_y}_x{x_min}to{x_max}.png"
    plt.savefig(output_filename, dpi=150)
    print(f"Graph successfully saved as: {output_filename}")
    plt.show()    

if __name__ == "__main__":
    DATA_FILE = "Dataset NACA0015 Velocity and Standard deviation.csv"
    
    plot_vz_profiles(
        filename=DATA_FILE, 
        y_target=300.0, 
        x_start=130.0, 
        x_end=175.0, 
        x_step=2.5
    )
    plot_upper_boundary_profiles(
        filename=DATA_FILE, 
        y_target=300.0, 
        x_min=0.0, 
        x_max=160.0, 
        z_start=-25, 
        z_end=-60.0, 
        z_step=2.5
    )
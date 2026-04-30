import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_spanwise_aoa(filename, y_targets, x_search_min=-160.0, x_search_max=-50.0):
    print(f"Loading data from '{filename}'...")
    df = pd.read_csv(filename, skipinitialspace=True)
    df.columns = df.columns.str.strip()

    # Define columns based on your dataset
    col_x = 'x [mm]'
    col_y = 'y [mm]'
    col_u = 'Velocity u [m/s]'
    col_w = 'Velocity w [m/s]'
    col_std_u = 'Standard deviation Vx [m/s]'
    col_std_w = 'Standard deviation Vz [m/s]'

    aoa_results = []
    
    # Optional: Setup a diagnostic plot for the first y-slice to visualize the noise
    plt.figure(figsize=(10, 5))
    diagnostic_plotted = False

    for y_target in y_targets:
        # 1. Isolate the target y-plane
        actual_y = df.iloc[(df[col_y] - y_target).abs().argsort()[:1]][col_y].values[0]
        df_y = df[df[col_y] == actual_y]

        # 2. Restrict to the upstream search window
        df_search = df_y[(df_y[col_x] >= x_search_min) & (df_y[col_x] <= x_search_max)]
        
        if df_search.empty:
            print(f"No data upstream for y ≈ {actual_y:.1f}")
            continue

        unique_xs = np.sort(df_search[col_x].unique())
        
        slice_vx = []
        slice_vz = []
        slice_variance = []

        # 3. Calculate mean velocities and total variance for each x-slice
        for tx in unique_xs:
            df_x = df_search[df_search[col_x] == tx]
            
            # Spatial average of velocity in this slice
            mean_u = np.nanmean(df_x[col_u].values)
            mean_w = np.nanmean(df_x[col_w].values)
            
            # Average measurement uncertainty in this slice
            # Variance = Standard Deviation squared
            mean_var_u = np.nanmean(df_x[col_std_u].values**2)
            mean_var_w = np.nanmean(df_x[col_std_w].values**2)
            
            # Total variance for the vector
            total_variance = mean_var_u + mean_var_w
            
            slice_vx.append(mean_u)
            slice_vz.append(mean_w)
            slice_variance.append(total_variance)

        slice_vx = np.array(slice_vx)
        slice_vz = np.array(slice_vz)
        slice_variance = np.array(slice_variance)

        # 4. Inverse-Variance Weighting
        # Prevent division by zero if variance is perfectly 0
        epsilon = 1e-9 
        weights = 1.0 / (slice_variance + epsilon)
        
        # Calculate the weighted average velocities
        weighted_vx = np.average(slice_vx, weights=weights)
        weighted_vz = np.average(slice_vz, weights=weights)
        
        # Calculate final flow angle
        flow_angle_rad = np.arctan2(weighted_vz, weighted_vx)
        flow_angle_deg = np.degrees(flow_angle_rad)
        
        aoa_results.append({
            'y_position': actual_y,
            'flow_angle_deg': flow_angle_deg,
            'weighted_Vx': weighted_vx,
            'weighted_Vz': weighted_vz
        })

        # --- Diagnostic Plotting (Just for the first y-slice) ---
        if not diagnostic_plotted:
            plt.plot(unique_xs, np.sqrt(slice_variance), 'r-', linewidth=2, label='Combined PIV Noise ($\sigma_{total}$)')
            
            # Find the single best slice just to show it on the graph
            best_idx = np.argmin(slice_variance)
            plt.axvline(unique_xs[best_idx], color='green', linestyle='--', label=f'Lowest Noise Slice (x={unique_xs[best_idx]:.1f})')
            
            plt.title(f"PIV Noise Profile Upstream of Airfoil (y ≈ {actual_y:.1f} mm)")
            plt.xlabel("Upstream Position, x (mm)")
            plt.ylabel("Velocity Standard Deviation (m/s)")
            plt.legend()
            plt.grid(True, alpha=0.5)
            plt.savefig("PIV_Noise_Diagnostic.png", dpi=150)
            diagnostic_plotted = True

    plt.show()

    # Print out the spanwise results
    #print("\n" + "="*50)
    #print("SPANWISE FREESTREAM ANGLE RESULTS")
    #print("="*50)
    #print(f"{'y position (mm)':<20} | {'Flow Angle (deg)':<20}")
    #print("-" * 50)
    #for res in aoa_results:
    #    print(f"{res['y_position']:<20.1f} | {res['flow_angle_deg']:<20.3f}")
    all_y = [res['y_position'] for res in aoa_results]
    all_angles = [res['flow_angle_deg'] for res in aoa_results]
    
    return np.array(all_y), np.array(all_angles) #Or pd.DataFrame(aoa_results) for more info

# =====================================================================
if __name__ == "__main__":
    DATA_FILE = "Dataset NACA0015 Velocity and Standard deviation.csv"
    
    # List the y-planes you want to analyze across the span
    target_spans = np.arange(101, 400, 2.5).tolist()
    
    # You can adjust the search window based on where your data starts
    y_pos_array, angle_array = calculate_spanwise_aoa(
        filename=DATA_FILE, 
        y_targets=target_spans,
        x_search_min=-170.0, # Push this to your outer boundary
        x_search_max=-50.0   # Stop before the airfoil upwash begins
    )
    plt.plot(y_pos_array, abs(angle_array - 15), 'r-', linewidth=2)
    plt.title("Angle of attack as a function of span position y")
    plt.xlabel("Span position y [mm]")
    plt.ylabel(r"Angle of attack $\alpha$ [deg]")
    plt.grid(True, alpha=0.5)
    plt.savefig("Angleofattack.png", dpi=150)
    plt.show()
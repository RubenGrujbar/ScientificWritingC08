import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# ==============================================================================
# 1. FLOW ANGLE ANALYSIS (Using the Velocity Dataset)
# ==============================================================================
# Load velocity data
try:
    df_vel = pd.read_csv("Dataset NACA0015 Velocity and Standard deviation.csv", skipinitialspace=True)
    df_vel.columns = df_vel.columns.str.strip()
    
    # Define exact column names based on your previous message
    col_x_vel = 'x [mm]'
    col_y_vel = 'y [mm]'
    col_u = 'Velocity u [m/s]'
    col_w = 'Velocity w [m/s]'

    y_target = 300.0
    calculated_slope = 0.2679492  # Default fallback slope

    # Filter for y ~ 300 mm
    df_vel_y = df_vel[np.abs(df_vel[col_y_vel] - y_target) <= 5.0]
    
    # Filter for the x range [-180, -50]
    df_vel_x_range = df_vel_y[(df_vel_y[col_x_vel] >= -180) & (df_vel_y[col_x_vel] <= 0)]

    if not df_vel_x_range.empty:
        # Target the middle of the range
        x_target = -187
        # Find the actual x value closest to our target in the velocity mesh
        actual_x = df_vel_x_range.iloc[(df_vel_x_range[col_x_vel] - x_target).abs().argsort()[:1]][col_x_vel].values[0]
        
        # Slice for that specific x location
        df_vel_slice = df_vel_x_range[df_vel_x_range[col_x_vel] == actual_x]
        
        # Calculate averages
        vx_avg = np.nanmean(df_vel_slice[col_u].values)
        vz_avg = np.nanmean(df_vel_slice[col_w].values)
        
        # Calculate angle and slope
        angle_rad = np.arctan2(vz_avg, vx_avg)
        angle_deg = np.degrees(angle_rad)
        calculated_slope = np.tan(angle_rad)
        
        print("-" * 50)
        print(f"Flow Analysis at y ≈ {y_target} mm, x = {actual_x} mm")
        print(f"Using file: 'Dataset NACA0015 Velocity and Standard deviation.csv'")
        print("-" * 50)
        print(f"Average Vx (u) : {vx_avg:.4f} m/s")
        print(f"Average Vz (w) : {vz_avg:.4f} m/s")
        print(f"Flow Angle     : {angle_deg:.2f}°")
        print(f"Line Slope     : {calculated_slope:.6f}")
        print("-" * 50)
    else:
        print("Notice: No data in x range [-180, -50] found in the velocity file.")

except FileNotFoundError:
    print("Notice: 'Dataset NACA0015 Velocity and Standard deviation.csv' not found. Using default slope.")
    calculated_slope = 0.2679492

# ==============================================================================
# 2. VORTICITY PLOTTING (Using the Gradient Dataset)
# ==============================================================================
# Load gradient data
df_grad = pd.read_csv("gradient_results.csv", skipinitialspace=True)
df_grad.columns = df_grad.columns.str.strip()

# Determine x, y, z column names in the gradient file
col_x_grad = 'x' if 'x' in df_grad.columns else 'x [mm]'
col_y_grad = 'y' if 'y' in df_grad.columns else 'y [mm]'
col_z_grad = 'z' if 'z' in df_grad.columns else 'z [mm]'

y_target = 300.0

# Slice the gradient dataset for plotting
df_plot = df_grad[np.abs(df_grad[col_y_grad] - y_target) <= 5.0]
df_plot = df_plot[(df_plot[col_z_grad] >= -50) & (df_plot[col_z_grad] <= 50)]

x = df_plot[col_x_grad].values
z = df_plot[col_z_grad].values

# ── Optional Overlays ──────────────────────────────────────────────────────
MARK_POINT = (96.3, 25.3)              # e.g. (120.0, -10.0) or None to disable
MARK_LABEL = "P1"
MARK_STYLE = dict(marker="o", color="black", markersize=3, zorder=5)

# The slope is now strictly driven by the velocity dataset calculation
LINE_SLOPE = calculated_slope        
LINE_STYLE = dict(color="yellow", linestyle="-", linewidth=2, zorder=10)
# ──────────────────────────────────────────────────────────────────────────

# Compute aspect ratio of the data
x_range = x.max() - x.min()
z_range = z.max() - z.min()
aspect = z_range / x_range

subplot_width = 5
subplot_height = subplot_width * aspect
fig_width = subplot_width * 3 + 1
fig_height = max(subplot_height, 3)

# Create a high-resolution regular grid
xi = np.linspace(x.min(), x.max(), 800)
zi = np.linspace(z.min(), z.max(), 400)
Xi, Zi = np.meshgrid(xi, zi)

fig, axes = plt.subplots(1, 3, figsize=(fig_width, fig_height),
                         constrained_layout=True)
fig.suptitle("Vorticity in the x-z plane (y ≈ 300 mm)", fontsize=14)

# Base colormap 
cmap = plt.get_cmap("RdBu_r").copy()

for ax, col, title in zip(axes,
                           ["omega_x", "omega_y", "omega_z"],
                           [r"$\omega_x$", r"$\omega_y$", r"$\omega_z$"]):
    omega = df_plot[col].values

    # Interpolate using the raw values first
    p_low  = np.percentile(omega, 1)
    p_high = np.percentile(omega, 90)

    Oi = griddata((x, z), omega, (Xi, Zi), method="linear")

    # Mask out-of-range values AFTER interpolation
    Oi = np.ma.masked_where((Oi < p_low) | (Oi > p_high), Oi)

    vmin, vmax = p_low, p_high
    if vmin < 0 < vmax:
        vabs = max(abs(vmin), abs(vmax))
        vmin, vmax = -vabs, vabs

    # Set the background color to green so transparent/masked areas show up green
    ax.set_facecolor("green")

    im = ax.pcolormesh(Xi, Zi, Oi, cmap=cmap, vmin=vmin, vmax=vmax,
                       shading="gouraud")

    cbar = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.04)
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label("s⁻¹", fontsize=9)

    # ── Draw the 10 cm (100 mm) circle ──────────────────────────────────────
    circle = plt.Circle((0, 0), radius=100, edgecolor='black', facecolor='none', 
                        linewidth=1.5, linestyle='--', zorder=10)
    ax.add_patch(circle)
    # ────────────────────────────────────────────────────────────────────────

    # ── Draw the adjustable slope line ──────────────────────────────────────
    line_x = np.array([x.min(), x.max()])
    line_z = LINE_SLOPE * line_x
    ax.plot(line_x, line_z, **LINE_STYLE)
    # ────────────────────────────────────────────────────────────────────────

    # ── Draw the optional point ────────────────────────────────────────────
    if MARK_POINT is not None:
        px, pz = MARK_POINT
        ax.plot(px, pz, **MARK_STYLE)
        if MARK_LABEL:
            ax.annotate(
                MARK_LABEL,
                xy=(px, pz),
                xytext=(6, 6),
                textcoords="offset points",
                fontsize=9,
                color=MARK_STYLE["color"],
                zorder=6,
            )
    # ──────────────────────────────────────────────────────────────────────

    ax.set_title(title, fontsize=13)
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("z (mm)")
    
    # Enforce strict limits so the line doesn't stretch the plot vertically
    ax.set_ylim(z.min(), z.max())
    
    ax.invert_yaxis()
    ax.set_aspect("equal")

plt.savefig("vorticity_xz_plane.png", dpi=150, bbox_inches="tight")
plt.show()
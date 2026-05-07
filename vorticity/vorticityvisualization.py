import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

#  CONFIGURATION

# ── Vorticity dataset
GRAD_CSV      = "gradient_results.csv"
VORT_Y_TARGET = 250              # mm — y-slice to plot
VORT_Z_MIN    = -50              # mm
VORT_Z_MAX    = 50               # mm

#  LOAD DATA

df = pd.read_csv(GRAD_CSV, skipinitialspace=True)
df.columns = df.columns.str.strip()

col_x = 'x' if 'x' in df.columns else 'x [mm]'
col_y = 'y' if 'y' in df.columns else 'y [mm]'
col_z = 'z' if 'z' in df.columns else 'z [mm]'

df_plot = df[np.abs(df[col_y] - VORT_Y_TARGET) <= 5.0]
df_plot = df_plot[(df_plot[col_z] >= VORT_Z_MIN) & (df_plot[col_z] <= VORT_Z_MAX)]

x = df_plot[col_x].values
z = df_plot[col_z].values

# =============================================================================
#  BUILD FIGURE
# =============================================================================

x_range = x.max() - x.min()
z_range = z.max() - z.min()

subplot_width  = 5
subplot_height = subplot_width * (z_range / x_range)
fig_width      = subplot_width * 3 + 1
fig_height     = max(subplot_height, 3)

xi = np.linspace(x.min(), x.max(), 800)
zi = np.linspace(z.min(), z.max(), 400)
Xi, Zi = np.meshgrid(xi, zi)

fig, axes = plt.subplots(1, 3, figsize=(fig_width, fig_height),
                         constrained_layout=True)
fig.suptitle(f"Vorticity in the x-z plane (y ≈ {VORT_Y_TARGET} mm)", fontsize=14)

cmap = plt.get_cmap("RdBu_r").copy()

for ax, col, title in zip(
    axes,
    ["omega_x", "omega_y", "omega_z"],
    [r"$\omega_x$", r"$\omega_y$", r"$\omega_z$"],
):
    omega  = df_plot[col].values
    p_low  = np.percentile(omega, 1)
    p_high = np.percentile(omega, 99)

    Oi = griddata((x, z), omega, (Xi, Zi), method="linear")

    vmin, vmax = p_low, p_high
    if vmin < 0 < vmax:
        vabs = max(abs(vmin), abs(vmax))
        vmin, vmax = -vabs, vabs

    im = ax.pcolormesh(Xi, Zi, Oi, cmap=cmap, vmin=vmin, vmax=vmax,
                       shading="gouraud")

    cbar = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.04)
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label("s⁻¹", fontsize=9)

    ax.set_title(title, fontsize=13)
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("z (mm)")
    ax.set_ylim(z.min(), z.max())
    ax.invert_yaxis()
    ax.set_aspect("equal")

plt.savefig("vorticity_xz_plane.png", dpi=150, bbox_inches="tight")
plt.show()
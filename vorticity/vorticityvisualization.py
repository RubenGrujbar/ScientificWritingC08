import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# =============================================================================
# SETTINGS
# =============================================================================

GRAD_CSV = "gradient_results.csv"

VORT_Y_TARGET = 250      # mm
VORT_Z_MIN = -50         # mm
VORT_Z_MAX = 50          # mm
VORT_X_MIN = -20         # mm

PERCENTILE = {
    "omega_x": 1,
    "omega_y": 1,
    "omega_z": 1,
}

# =============================================================================
# LOAD DATA
# =============================================================================

df = pd.read_csv(GRAD_CSV, skipinitialspace=True)
df.columns = df.columns.str.strip()

col_x = 'x' if 'x' in df.columns else 'x [mm]'
col_y = 'y' if 'y' in df.columns else 'y [mm]'
col_z = 'z' if 'z' in df.columns else 'z [mm]'

df_plot = df[np.abs(df[col_y] - VORT_Y_TARGET) <= 5]

df_plot = df_plot[
    (df_plot[col_z] >= VORT_Z_MIN) &
    (df_plot[col_z] <= VORT_Z_MAX) &
    (df_plot[col_x] >= VORT_X_MIN)
]

x = df_plot[col_x].values
z = df_plot[col_z].values

# =============================================================================
# INTERPOLATION GRID
# =============================================================================

xi = np.linspace(x.min(), x.max(), 800)
zi = np.linspace(z.min(), z.max(), 400)

Xi, Zi = np.meshgrid(xi, zi)

x_range = x.max() - x.min()
z_range = z.max() - z.min()

subplot_width = 5
subplot_height = subplot_width * (z_range / x_range)

fig_width = subplot_width * 3 + 1
fig_height = max(subplot_height, 4)

cmap = plt.get_cmap("RdBu_r")

components = ["omega_x", "omega_y", "omega_z"]
titles = [r"$\omega_x$", r"$\omega_y$", r"$\omega_z$"]

# =============================================================================
# FIGURE 1 → COLORBARS ON TOP
# =============================================================================

fig1, axes1 = plt.subplots(
    1, 3,
    figsize=(fig_width, fig_height),
    constrained_layout=True
)

for ax, col, title in zip(axes1, components, titles):

    omega = df_plot[col].values

    pct = PERCENTILE[col]
    low = np.percentile(omega, pct)
    high = np.percentile(omega, 100 - pct)

    Oi = griddata((x, z), omega, (Xi, Zi), method="linear")

    vmax = max(abs(low), abs(high))
    vmin = -vmax

    im = ax.pcolormesh(
        Xi, Zi, Oi,
        cmap=cmap,
        shading="gouraud",
        vmin=vmin,
        vmax=vmax
    )

    cbar = fig1.colorbar(
        im,
        ax=ax,
        location="top",
        fraction=0.05,
        pad=0.04
    )

    cbar.set_label("s⁻¹", fontsize=9)
    cbar.ax.tick_params(labelsize=8)

    ax.set_title(title, fontsize=13)
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("z (mm)")
    ax.set_aspect("equal")
    ax.invert_yaxis()

#fig1.suptitle(f"Vorticity in x-z plane (y ≈ {VORT_Y_TARGET} mm)\nColorbars on top",fontsize=14)
plt.savefig("vorticity_xz_plane.png", dpi=150, bbox_inches="tight")
plt.show()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Load and slice
df = pd.read_csv("gradient_results.csv", skipinitialspace=True)
df.columns = df.columns.str.strip()

y_target = 300.0
df = df[np.abs(df["y"] - y_target) <= 5.0]
df = df[(df["z"] >= -50) & (df["z"] <= 50)]

x = df["x"].values
z = df["z"].values

# Create a high-resolution regular grid
xi = np.linspace(x.min(), x.max(), 800)
zi = np.linspace(z.min(), z.max(), 400)
Xi, Zi = np.meshgrid(xi, zi)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Vorticity in the x-z plane (y ≈ 300 mm)", fontsize=14)

for ax, col, title in zip(axes,
                           ["omega_x", "omega_y", "omega_z"],
                           [r"$\omega_x$", r"$\omega_y$", r"$\omega_z$"]):
    omega = df[col].values

    # Clip outliers using percentile bounds before interpolating
    p_low  = np.percentile(omega, 1)
    p_high = np.percentile(omega, 99)
    omega_clipped = np.clip(omega, p_low, p_high)

    Oi = griddata((x, z), omega_clipped, (Xi, Zi), method="linear")

    vmin, vmax = np.nanmin(Oi), np.nanmax(Oi)
    if vmin < 0 < vmax:
        vabs = max(abs(vmin), abs(vmax))
        vmin, vmax = -vabs, vabs

    im = ax.pcolormesh(Xi, Zi, Oi, cmap="RdBu_r", vmin=vmin, vmax=vmax,
                       shading="gouraud")
    plt.colorbar(im, ax=ax, label="s⁻¹")
    ax.set_title(title, fontsize=13)
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("z (mm)")
    ax.set_ylim(z.min(), z.max())
    ax.invert_yaxis()

plt.tight_layout()
plt.savefig("vorticity_xz_plane.png", dpi=150, bbox_inches="tight")
plt.show()
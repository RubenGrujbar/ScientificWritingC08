import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
#Load and slice
df = pd.read_csv("vorticity\gradient_results.csv", skipinitialspace=True)
df.columns = df.columns.str.strip()
 
y_target = 300.0
df = df[np.abs(df["y"] - y_target) <= 5.0]
 
x = df["x"].values
z = df["z"].values
 
#Plot
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Vorticity in the x-z plane (y ≈ 300 mm)", fontsize=14)
 
for ax, col, title in zip(axes,
                           ["omega_x", "omega_y", "omega_z"],
                           [r"$\omega_x$", r"$\omega_y$", r"$\omega_z$"]):
    omega = df[col].values
    vmin, vmax = omega.min(), omega.max()
    # keep colormap symmetric around zero if data spans both signs
    if vmin < 0 < vmax:
        vabs = max(abs(vmin), abs(vmax))
        vmin, vmax = -vabs, vabs
    tc = ax.tricontourf(x, z, omega, levels=64, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    plt.colorbar(tc, ax=ax, label="s⁻¹")
    ax.set_title(title, fontsize=13)
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("z (mm)")
    ax.invert_yaxis()   # invert z-axis
 
plt.tight_layout()
plt.savefig("vorticity_xz_plane.png", dpi=150, bbox_inches="tight")
plt.show()
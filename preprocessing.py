import pandas as pd
import numpy as np

def load_velocity_arrays_fast(filepath):
    cols = [
        "x [mm]", "y [mm]", "z [mm]",
        "Velocity u [m/s]", "Velocity v [m/s]", "Velocity w [m/s]",
        "Standard deviation V [m/s]", "Standard deviation Vx [m/s]",
        "Standard deviation Vy [m/s]", "Standard deviation Vz [m/s]"
    ]
    df = pd.read_csv(filepath, index_col=0, delimiter=",", skipinitialspace=True)
    df.columns = df.columns.str.replace("\ufeff", "").str.strip()
    for col in cols:
        if col not in df.columns:
            df[col] = np.nan
    df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")
    df[cols] = df[cols].replace([np.inf, -np.inf], np.nan).fillna(0).astype("float32")
    return tuple(df[col].to_numpy() for col in cols)

url = "https://media.githubusercontent.com/media/RubenGrujbar/ScientificWritingC08/main/Dataset%20NACA0015%20Velocity%20and%20Standard%20deviation.csv"

x, y, z, u, v, w, std_V, std_Vx, std_Vy, std_Vz = load_velocity_arrays_fast(url)

import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import numpy as np

# Compute velocity magnitude
mag = np.sqrt(u**2 + v**2 + w**2)

# Subsample to avoid overplotting (3M points is too heavy for 3D scatter)
n = 100_000
idx = np.random.choice(len(x), n, replace=False)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

sc = ax.scatter(x[idx], y[idx], z[idx], c=u[idx], cmap='coolwarm', s=0.5, alpha=0.5)

plt.colorbar(sc, ax=ax, label="Velocity u [m/s]", shrink=0.5)
ax.set_xlabel("x [mm]")
ax.set_ylabel("y [mm]")
ax.set_zlabel("z [mm]")
ax.set_title("3D scatter — u velocity (colored), 100k sample")

plt.tight_layout()
plt.show()


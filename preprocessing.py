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
import numpy as np
import pandas as pd

mask = (u == 0) & (v == 0) & (w == 0)

df = pd.DataFrame({'x': x[mask], 'z': z[mask]})
counts = df.groupby(['x', 'z']).size().reset_index(name='count')

pivot = counts.pivot(index='z', columns='x', values='count').fillna(0)

plt.figure(figsize=(12, 6))
plt.pcolormesh(pivot.columns, pivot.index, pivot.values, cmap='hot_r')
plt.colorbar(label="Number of zero-velocity points")  
plt.xlabel("x [mm]")
plt.ylabel("z [mm]")
plt.title("Zero-velocity point count per (x, z) location")
plt.tight_layout()
plt.show()


df = pd.DataFrame({'x': x[mask], 'y': y[mask]})
counts = df.groupby(['x', 'y']).size().reset_index(name='count')   

pivot = counts.pivot(index='y', columns='x', values='count').fillna(0)
plt.figure(figsize=(12, 6))
plt.pcolormesh(pivot.columns, pivot.index, pivot.values, cmap='hot_r')
plt.colorbar(label="Number of zero-velocity points")
plt.xlabel("x [mm]")
plt.ylabel("z [mm]")
plt.title("Zero-velocity point count per (x, y) location")
plt.tight_layout()
plt.show()

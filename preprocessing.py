def load_velocity_arrays_fast(filepath):
    import pandas as pd

    dtype = {
        "x [mm]": "float32",
        "y [mm]": "float32",
        "z [mm]": "float32",
        "Velocity u [m/s]": "float32",
        "Velocity v [m/s]": "float32",
        "Velocity w [m/s]": "float32",
        "Standard deviation V [m/s]": "float32",
        "Standard deviation Vx [m/s]": "float32",
        "Standard deviation Vy [m/s]": "float32",
        "Standard deviation Vz [m/s]": "float32"
    }

    df = pd.read_csv(filepath, index_col=0, dtype=dtype)

    return {col: df[col].to_numpy() for col in df.columns}

url = "https://media.githubusercontent.com/media/RubenGrujbar/ScientificWritingC08/refs/heads/main/Dataset%20NACA0015%20Velocity%20and%20Standard%20deviation.csv"
data = load_velocity_arrays_fast(url)

x = data["x [mm]"]
y = data["y [mm]"]
z = data["z [mm]"]
u = data["Velocity u [m/s]"]
v = data["Velocity v [m/s]"]
w = data["Velocity w [m/s]"]
std_V = data["Standard deviation V [m/s]"]
std_Vx = data["Standard deviation Vx [m/s]"]
std_Vy = data["Standard deviation Vy [m/s]"]
std_Vz = data["Standard deviation Vz [m/s]"]
import numpy as np
import matplotlib.pyplot as plt

V = np.sqrt(u**2 + v**2 + w**2)

plt.tricontourf(x, y, u, levels=50)
plt.colorbar(label="Velocity u [m/s]")
plt.xlabel("x [mm]")
plt.ylabel("y [mm]")
plt.title("Velocity contour")
plt.show()

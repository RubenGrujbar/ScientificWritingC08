import pandas as pd
import numpy as np

def load_velocity_arrays_fast(url = "https://media.githubusercontent.com/media/RubenGrujbar/ScientificWritingC08/main/Dataset%20NACA0015%20Velocity%20and%20Standard%20deviation.csv"):
    cols = [
        "x [mm]", "y [mm]", "z [mm]",
        "Velocity u [m/s]", "Velocity v [m/s]", "Velocity w [m/s]",
        "Standard deviation V [m/s]", "Standard deviation Vx [m/s]",
        "Standard deviation Vy [m/s]", "Standard deviation Vz [m/s]"
    ]
    df = pd.read_csv(url, index_col=0, delimiter=",", skipinitialspace=True)
    df.columns = df.columns.str.replace("\ufeff", "").str.strip()
    for col in cols:
        if col not in df.columns:
            df[col] = np.nan
    df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")
    df[cols] = df[cols].replace([np.inf, -np.inf], np.nan).fillna(0).astype("float32")
    return tuple(df[col].to_numpy() for col in cols)



import matplotlib.pyplot as plt
import numpy as np

def plot_zero_velocity_heatmap():
    x, y, z, u, v, w, std_V, std_Vx, std_Vy, std_Vz = load_velocity_arrays_fast()
    mask = (u == 0) & (v == 0) & (w == 0)
    df = pd.DataFrame({'x': x[mask], 'y': y[mask], 'z': z[mask]})

    planes = [('x', 'z'), ('x', 'y'), ('y', 'z')]
    titles = ['x-z plane', 'x-y plane', 'y-z plane']

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    for i in range(len(planes)):
        col1, col2 = planes[i]
        counts = df.groupby([col1, col2]).size().reset_index(name='count')
        pivot = counts.pivot(index=col2, columns=col1, values='count').fillna(0)
        sc = axes[i].pcolormesh(pivot.columns, pivot.index, pivot.values, cmap='hot_r')
        plt.colorbar(sc, ax=axes[i], label="Zero-velocity points")
        axes[i].set_xlabel(f"{col1} [mm]")
        axes[i].set_ylabel(f"{col2} [mm]")
        axes[i].set_title(f"Zero-velocity count — {titles[i]}")
        axes[i].invert_yaxis()
    plt.tight_layout()
    plt.show()

#plot_zero_velocity_heatmap()

def airfoil_coords():
    x, y, z, u, v, w, std_V, std_Vx, std_Vy, std_Vz = load_velocity_arrays_fast()
    airfoil_x_coords = []
    airfoil_z_coords = []
    for i in range (len(x)):
        if (y[i]>150 and y[i]<300 and z[i] > -50 and z[i] < 50 and x[i] > -100 and x[i] < 200) : #limiting to a segment that we know for sure is within the span
            if (u[i] == 0 and v[i] == 0 and w[i] == 0): #if no velocities
                airfoil_x_coords.append(x[i]) 
                airfoil_z_coords.append(z[i])
    return airfoil_x_coords, airfoil_z_coords


#airfoil_x_coords, airfoil_z_coords = airfoil_coords()

#plt.scatter(airfoil_x_coords, airfoil_z_coords)
#plt.xlim(-200, 200)   # x axis limits
#plt.ylim(200, -200)
#plt.show()

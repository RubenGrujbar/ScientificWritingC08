import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#from preprocessing import load_velocity_arrays_fast
import os
import pyvista as pv

Xa = []
Ya = []


def Plt2DStreamVisu(X, Y, U, V, xa = Xa, ya = Ya):
    
    #X, Y = np.meshgrid(X, Y)
    #X = np.round(X,decimals=2)
    #Y = np.round(Y,decimals=2)
    #d = X[1] - Y[0]
    #X = np.linspace(X.size,)
    x_raw = X[0, :]
    y_raw = Y[:, 0]

    #print(x_raw)
    #print(y_raw)

    x = np.linspace(x_raw[0], x_raw[-1], len(x_raw))
    #y = np.linspace(y_raw[0], y_raw[-1], len(y_raw))
    dy = np.mean(np.diff(y_raw))  # average spacing
    y_uniform = y_raw[0] + dy * np.arange(len(y_raw))   

    #for i in range(y.size-1):
    #    print(y[i+1]-y[i])
    #print(x)
    #print(y)

    X, Y = np.meshgrid(x, y_uniform, indexing='ij')
    X = np.transpose(X)
    Y = np.transpose(Y)
    #print(X)
    #print(Y)

    U = np.flip(U, axis=0)
    V = np.flip(V, axis=0)
    Y = -1*np.flip(Y, axis=0)
    
    # plotting
    plt.figure(figsize=(8,4))
    speed = (U**2 + V**2)**0.5
    threshold = 1e-3
    speed_masked = np.ma.masked_where(speed < threshold, speed)
    #print(speed)



    # colored velocity magnitude
    #plt.contourf(X, Y, speed , levels=50, cmap='jet')

    cmap = plt.cm.jet
    cmap.set_bad('white')
    speed_plot = speed.copy()
    speed_plot[speed_plot < threshold] = np.nan  # instead of masked array

    cf = plt.contourf(X, Y, speed_plot, levels=50, cmap=cmap, vmin=speed.min(), vmax=speed.max())
    plt.colorbar(cf, label='Velocity magnitude')
    #plt.contourf(X, Y, speed_masked, levels=50, cmap=cmap,vmin=speed.min(), vmax=speed.max())
    #plt.contour(X, Y, speed, levels=[threshold], colors='k', linewidths=2)

    # streamlines
    #plt.quiver(X, Y, U, V, color='k', scale=50)  # adjust scale to suit

    plt.streamplot(X, Y, U, V,density=2,color='k',linewidth=0.8)

    # airfoil
    plt.fill(xa, ya, 'white')
    plt.plot(xa, ya, 'k', linewidth=2)
    print(speed.min(), speed.max())
    # formatting
    plt.axis('equal')
    plt.xlabel('x mm from LE')
    plt.ylabel('y mm from LE')
    plt.title('Flow field over airfoil')
    #plt.colorbar(label='Velocity magnitude')

    plt.show()
    return 'worked'

def load_velocity_arrays_fast(url = "https://media.githubusercontent.com/media/RubenGrujbar/ScientificWritingC08/main/Dataset%20NACA0015%20Velocity%20and%20Standard%20deviation.csv"):
    cols = [
        "x [mm]", "y [mm]", "z [mm]",
        "Velocity u [m/s]", "Velocity v [m/s]", "Velocity w [m/s]",
        "Standard deviation V [m/s]", "Standard deviation Vx [m/s]",
        "Standard deviation Vy [m/s]", "Standard deviation Vz [m/s]"
    ]
    df = pd.read_csv(r'C:\Users\alexa\OneDrive\Desktop\ScientificWritingC08\Dataset NACA0015 Velocity and Standard deviation.csv', index_col=0, delimiter=",", skipinitialspace=True)
    df.columns = df.columns.str.replace("\ufeff", "").str.strip()
    for col in cols:
        if col not in df.columns:
            df[col] = np.nan
    df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")
    df[cols] = df[cols].replace([np.inf, -np.inf], np.nan).fillna(0).astype("float32")
    return tuple(df[col].to_numpy() for col in cols)

def visualize_airfoil_piv(x, y, z, u, v, w, type,stl_path= r'C:\Users\alexa\OneDrive\Desktop\ScientificWritingC08\N15- Smooth 15 deg.stl'):

    # -----------------------------
    # 1. Load STL
    # -----------------------------
    mesh = pv.read(stl_path)

    # -----------------------------
    # 2. Build Structured Grid
    # -----------------------------
    # Your data is (Nz, Ny, Nx)
    Nz, Ny, Nx = x.shape

    # Stack coordinates properly
    points = np.stack((x, y, z), axis=-1)

    grid = pv.StructuredGrid()
    grid.points = points.reshape(-1, 3)
    grid.dimensions = (Nx, Ny, Nz)

    # Velocity field
    velocity = np.stack((u, v, w), axis=-1)
    grid["velocity"] = velocity.reshape(-1, 3)

    # Velocity magnitude
    speed = np.linalg.norm(velocity, axis=-1)
    grid["speed"] = speed.reshape(-1)

    # -----------------------------
    # 3. (Optional) Align STL to data
    # -----------------------------
    # Shift STL to match grid center
    grid_center = np.array(grid.center)
    mesh_center = np.array(mesh.center)

    mesh.translate(grid_center - mesh_center)

    # -----------------------------
    # 4. Create slices
    # -----------------------------

    #slice = grid.slice(normal='y', origin=[0,grid.center[1],0])
    min_val, max_val = y.min(), y.max()
    positions = np.linspace(min_val, max_val-80, 5)
    plotter = pv.Plotter()

    center = grid.center
    if type == 'v':
        slices = []

        for pos in positions:
            origin = list(center)
            origin[1] = pos

            slice_plane = grid.slice(normal='y', origin=origin)

            if slice_plane.n_points > 0:   # avoid empty slices
                slices.append(slice_plane)
        #slices = grid.slice_along_axis(n=5, axis='y')
        #slices = grid.slice_orthogonal(x=None, y=None, z=None)

        # -----------------------------
        # 5. Plot
        # -----------------------------

        # Airfoil surface
        plotter.add_mesh(mesh, color="lightgray")

        # Velocity slices
        for slice in slices:
            plotter.add_mesh(
                slice,
                scalars="speed",
                cmap="jet",
                opacity=0.9
            )
    #plotter.add_mesh(slice_plane, scalars='speed', cmap='jet', opacity=0.9)
    if type == 'q':
        #grid = grid.gaussian_smooth(radius_factor=1.5)
        # -----------------------------
        # 4. Compute velocity gradient
        # -----------------------------
        # Number of cells to remove from each boundary
        pad = 10   # try 2–5 depending on your grid

        mask = np.zeros_like(x, dtype=bool)

        mask[pad:-pad, pad:-pad, pad:-pad] = True

        # Flatten mask to match grid
        mask_flat = mask.reshape(-1)

        # Extract only interior points
        grid = grid.extract_points(mask_flat, adjacent_cells=True)
        deriv = grid.compute_derivative(scalars="velocity", gradient=True)
        grad = deriv["gradient"].reshape(-1, 3, 3)

        # -----------------------------
        # 5. Compute Q-criterion (vectorized)
        # -----------------------------
        S = 0.5 * (grad + np.transpose(grad, (0, 2, 1)))      # strain tensor
        Omega = 0.5 * (grad - np.transpose(grad, (0, 2, 1)))  # rotation tensor

        S2 = np.sum(S**2, axis=(1, 2))
        Omega2 = np.sum(Omega**2, axis=(1, 2))

        Q = 0.5 * (Omega2 - S2)
        Q = Q/1e6
        grid["Q"] = Q

        # -----------------------------
        # 6. Choose threshold (tunable!)
        # -----------------------------
        q_threshold = np.percentile(Q, 98)

        # -----------------------------
        # 7. Extract vortex structures
        # -----------------------------
        vortices = grid.contour(
            isosurfaces=[q_threshold],
            scalars="Q"
        )

        # -----------------------------
        # 8. Plot
        # -----------------------------
        plotter.add_mesh(mesh, color="lightgray", opacity=1.0)

        plotter.add_mesh(
            vortices,
            scalars="speed",
            cmap="plasma",
            opacity=1.0
        )

    # Add axes + better view
    plotter.add_axes()
    plotter.show_grid()

    # Nice camera angle
    plotter.camera_position = 'xy'

    plotter.show()

if __name__ == "__main__":

    
    #current_dir = os.path.dirname(__file__) #Check file path of this file
    #file_path = os.path.join(current_dir, 'Dataset NACA0015 Velocity and Standard deviation.csv') #Build the file path for the dataset

    #df = pd.read_csv(file_path, index_col=0, delimiter=",", skipinitialspace=True)
    a = np.array([0,1,2,3,0,1,2,3,0,1,2,3])
    b = np.array([0,0,0,0,1,1,1,1,2,2,2,2])
    c = np.array([20,20,20,20,20,20,20,20,20,20,20,20])
    #print(a.reshape(3,4,1))
    #print(b.reshape(3,4,1))
    #print(c.reshape(3,4,1))
    
    
    #data = pd.read_csv(r'C:\Users\alexa\OneDrive\Desktop\ScientificWritingC08\cleaned_dataset.csv')
    #x = data["x [mm]"].to_numpy()
    #y = data["y [mm]"].to_numpy()
    #z = data["z [mm]"].to_numpy()
    #u = data["Velocity u [m/s]"].to_numpy()
    #v = data["Velocity v [m/s]"].to_numpy()
    #w = data["Velocity w [m/s]"].to_numpy()
    #print(x[0])
    
    x, y, z, u, v, w, std_V, std_Vx, std_Vy, std_Vz = load_velocity_arrays_fast()
    print('hello')
    x = x.reshape(123,137,180)
    #print(x[0][0][0])
    y = y.reshape(123,137,180)
    z = z.reshape(123,137,180)
    u = u.reshape(123,137,180)
    v= v.reshape(123,137,180)
    w = w.reshape(123,137,180)
    #print(np.transpose(x[:,80,:]))
    #print(np.transpose(x[:,80,:]))

    #print(z)
    #print(x[:,70,:])

    #print(y[0,70,0])
    #print(x[:,70,:])
    #print(z[:,70,:])
    visualize_airfoil_piv(x,y,z,u,v,w,'q')
    #print(Plt2DStreamVisu(x[:,70,:],z[:,70,:],u[:,70,:],v[:,70,:]))
    



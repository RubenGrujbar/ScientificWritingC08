import numpy as np
import pandas as pd
import pyvista as pv


<<<<<<< HEAD

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

# def load_velocity_arrays_fast(url = "https://media.githubusercontent.com/media/RubenGrujbar/ScientificWritingC08/main/Dataset%20NACA0015%20Velocity%20and%20Standard%20deviation.csv"):
#     cols = [
#         "x [mm]", "y [mm]", "z [mm]",
#         "Velocity u [m/s]", "Velocity v [m/s]", "Velocity w [m/s]",
#         "Standard deviation V [m/s]", "Standard deviation Vx [m/s]",
#         "Standard deviation Vy [m/s]", "Standard deviation Vz [m/s]"
#     ]
#     df = pd.read_csv(r'C:\Users\alexa\OneDrive\Desktop\ScientificWritingC08\Dataset NACA0015 Velocity and Standard deviation.csv', index_col=0, delimiter=",", skipinitialspace=True)
#     df.columns = df.columns.str.replace("\ufeff", "").str.strip()
#     for col in cols:
#         if col not in df.columns:
#             df[col] = np.nan
#     df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")
#     df[cols] = df[cols].replace([np.inf, -np.inf], np.nan).fillna(0).astype("float32")
#     return tuple(df[col].to_numpy() for col in cols)



# def visualize_airfoil_piv(x, y, z, u, v, w, type,stl_path= r'C:\Users\alexa\OneDrive\Desktop\ScientificWritingC08\N15- Smooth 15 deg.stl'):

def load_velocity_arrays_fast(url = "https://media.githubusercontent.com/media/RubenGrujbar/ScientificWritingC08/main/Dataset%20NACA0015%20Velocity%20and%20Standard%20deviation.csv"):
=======
def load_velocity_arrays_fast(
        url="https://media.githubusercontent.com/media/RubenGrujbar/ScientificWritingC08/main/Dataset%20NACA0015%20Velocity%20and%20Standard%20deviation.csv"):
>>>>>>> e612c781f46beef2d09ec211122412a56a608dc3
    cols = [
        "x [mm]", "y [mm]", "z [mm]",
        "Velocity u [m/s]", "Velocity v [m/s]", "Velocity w [m/s]",
        "Standard deviation V [m/s]", "Standard deviation Vx [m/s]",
        "Standard deviation Vy [m/s]", "Standard deviation Vz [m/s]"
    ]
<<<<<<< HEAD
    df = pd.read_csv(url, index_col=0, delimiter=",", skipinitialspace=True)
=======
    df = pd.read_csv(
        r'C:\Users\Daria\Desktop\Test_AnalysisAndSimulation\ScientificWritingC08\Dataset NACA0015 Velocity and Standard deviation.csv',
        index_col=0, delimiter=",", skipinitialspace=True)
>>>>>>> e612c781f46beef2d09ec211122412a56a608dc3
    df.columns = df.columns.str.replace("\ufeff", "").str.strip()
    for col in cols:
        if col not in df.columns:
            df[col] = np.nan
    df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")
    df[cols] = df[cols].replace([np.inf, -np.inf], np.nan).fillna(0).astype("float32")
    return tuple(df[col].to_numpy() for col in cols)

<<<<<<< HEAD
def visualize_airfoil_piv(x, y, z, u, v, w, type,stl_path= 'N15- Smooth 15 deg.stl'):
=======

def compute_Q_field(grid):
    """
    Computes the Q-criterion field on the given structured PyVista grid
    (which must already have a 'velocity' point array).
    Returns Q as a 1-D numpy array aligned with grid points, in SI units (s^-2).
    """
    deriv = grid.compute_derivative(scalars="velocity", gradient=True)
    grad = deriv["gradient"].reshape(-1, 3, 3)

    S = 0.5 * (grad + np.transpose(grad, (0, 2, 1)))
    Omega = 0.5 * (grad - np.transpose(grad, (0, 2, 1)))

    S2 = np.sum(S ** 2, axis=(1, 2))
    Omega2 = np.sum(Omega ** 2, axis=(1, 2))

    Q = 0.5 * (Omega2 - S2)
    Q = Q / 1e6  # mm -> m unit correction
    return Q


def visualize_airfoil_piv(x, y, z, u, v, w, type,
                           stl_path=r"C:\Users\Daria\Desktop\Test_AnalysisAndSimulation\ScientificWritingC08\N15- Smooth 15 deg.stl",
                           plane_x=147.7, plane_z=-37.4, plane_y=None):
>>>>>>> e612c781f46beef2d09ec211122412a56a608dc3
    # -----------------------------
    # 1. Load STL
    # -----------------------------
    mesh = pv.read(stl_path)

    # -----------------------------
    # 2. Build Structured Grid
    # -----------------------------
    Nz, Ny, Nx = x.shape

    points = np.stack((x, y, z), axis=-1)
    grid = pv.StructuredGrid()
    grid.points = points.reshape(-1, 3)
    grid.dimensions = (Nx, Ny, Nz)

    velocity = np.stack((u, v, w), axis=-1)
    grid["velocity"] = velocity.reshape(-1, 3)

    speed = np.linalg.norm(velocity, axis=-1)
    grid["speed"] = speed.reshape(-1)

    # -----------------------------
    # 3. Align STL & Set Visual Crop Domain Bounds
    # -----------------------------
    grid_center = np.array(grid.center)
    mesh_center = np.array(mesh.center)
    mesh.translate(grid_center - mesh_center)

    xmin, xmax, ymin, ymax, zmin, zmax = grid.bounds
    
    # Redefine the minimum X window boundary for visual display items
    display_xmin = -50.0
    crop_bounds = [display_xmin, xmax, ymin, ymax, zmin, zmax]

    mesh_clipped = mesh.clip_box(bounds=crop_bounds, invert=False)

    # -----------------------------
    # 4. Plotter setup
    # -----------------------------
    plotter = pv.Plotter(off_screen=False)

    # Add the standard Spanwise Slice Plane if requested
    if plane_y is not None:
        xz_plane = pv.Plane(
            center=((display_xmin + xmax) / 2, plane_y, (zmin + zmax) / 2),
            direction=(0, 1, 0),
            i_size=(xmax - display_xmin),
            j_size=(zmax - zmin),
            i_resolution=1,
            j_resolution=1
        )
        plotter.add_mesh(xz_plane, color="red", opacity=0.4, show_edges=True, edge_color="red", label="Spanwise Cut")

    # -------------------------------------------------------------
    # Integration Boundaries as physical 3D Planes (Bounded at X = -50)
    # -------------------------------------------------------------
    # Wake Boundary Plane (Vertical cut along constant X value)
    if plane_x is not None and plane_x >= display_xmin:
        wake_plane = pv.Plane(
            center=(plane_x, (ymin + ymax) / 2, (zmin + zmax) / 2),
            direction=(1, 0, 0),  # Orthogonal to X-axis
            i_size=(ymax - ymin),
            j_size=(zmax - zmin),
            i_resolution=1,
            j_resolution=1
        )
        plotter.add_mesh(wake_plane, color="darkred", opacity=0.5, show_edges=True, edge_color="darkred")

    # Above Wing Boundary Plane (Horizontal cut along constant Z value)
    if plane_z is not None:
        above_wing_plane = pv.Plane(
            center=((display_xmin + xmax) / 2, (ymin + ymax) / 2, plane_z),
            direction=(0, 0, 1),  # Orthogonal to Z-axis
            i_size=(xmax - display_xmin),
            j_size=(ymax - ymin),
            i_resolution=1,
            j_resolution=1
        )
        plotter.add_mesh(above_wing_plane, color="green", opacity=0.5, show_edges=True, edge_color="green")

    if type == 'v':
        min_val, max_val = y.min(), y.max()
        positions = np.linspace(min_val, max_val - 80, 5)
        slices = []
        for pos in positions:
            origin = list(grid.center)
            origin[1] = pos
            slice_plane = grid.slice(normal='y', origin=origin)
            if slice_plane.n_points > 0:
                slices.append(slice_plane.clip_box(bounds=crop_bounds, invert=False))

        plotter.add_mesh(mesh_clipped, color="lightgray")
        for sl in slices:
            plotter.add_mesh(sl, scalars="speed", cmap="jet", opacity=0.9)

    if type == 'q':
        # -----------------------------
        # Compute Q
        # -----------------------------
        Q = compute_Q_field(grid)
        grid["Q"] = Q

        Q_3D = Q.reshape(Nz, Ny, Nx)

        pad = 15
        mask = np.zeros_like(Q_3D, dtype=bool)
        mask[pad:-pad, pad:-pad, pad:-pad] = True
        Q_3D_filtered = np.where(mask, Q_3D, 0.0)
        Q_filtered_flat = Q_3D_filtered.reshape(-1)
        grid["Q"] = Q_filtered_flat

        # Calculate absolute Q_max for fractional calculation scaling
        Q_positive = Q_filtered_flat[Q_filtered_flat > 0]
        Q_max = float(Q_positive.max()) if Q_positive.size > 0 else 1.0

        # -----------------------------
        # Fractional Selection Logic
        # -----------------------------
        print("\n" + "="*60)
        print(f"Calculated Maximum Positive Q (Q_max) = {Q_max:.4f} 1/s^2")
        print("Choose an alpha value (fraction of Q_max) for the 3D visualization.")
        print("="*60)
        
        while True:
            user_input = input("Enter alpha value as a fraction (e.g., 0.05 or 0.15): ").strip()
            try:
                alpha = float(user_input)
                q_threshold = alpha * Q_max
                print(f"-> Selected alpha: {alpha}")
                print(f"-> Resulting Threshold (alpha * Q_max): {q_threshold:.4f} 1/s^2\n")
                break
            except ValueError:
                print("Invalid input. Please enter a numerical fraction value.")

        # -----------------------------
        # Q vortex core extraction visualization
        # -----------------------------
        vortices = grid.contour(isosurfaces=[q_threshold], scalars="Q")
        vortices_clipped = vortices.clip_box(bounds=crop_bounds, invert=False)
        
        plotter.add_mesh(mesh_clipped, color="lightgray", opacity=1.0)
        plotter.add_mesh(vortices_clipped, scalars="speed", cmap="plasma", opacity=1.0)

    plotter.render()
    plotter.add_axes()
    plotter.show_grid()
    
    plotter.view_isometric()
    plotter.camera.up = (0, 0, -1)
    plotter.show()


if __name__ == "__main__":
    x, y, z, u, v, w, std_V, std_Vx, stdf_Vy, std_Vz = load_velocity_arrays_fast()
    print('hello')
    x = x.reshape(123, 137, 180)
    y = y.reshape(123, 137, 180)
    z = z.reshape(123, 137, 180)
    u = u.reshape(123, 137, 180)
    v = v.reshape(123, 137, 180)
    w = w.reshape(123, 137, 180)

    visualize_airfoil_piv(x, y, z, u, v, w, 'q', plane_y=None)
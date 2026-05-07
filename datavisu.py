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
    df = pd.read_csv(r'C:\Users\Daria\Desktop\Test_AnalysisAndSimulation\ScientificWritingC08\Dataset NACA0015 Velocity and Standard deviation.csv', index_col=0, delimiter=",", skipinitialspace=True)
    df.columns = df.columns.str.replace("\ufeff", "").str.strip()
    for col in cols:
        if col not in df.columns:
            df[col] = np.nan
    df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")
    df[cols] = df[cols].replace([np.inf, -np.inf], np.nan).fillna(0).astype("float32")
    return tuple(df[col].to_numpy() for col in cols)

def visualize_airfoil_piv(x, y, z, u, v, w, type,
                          stl_path=r"C:\Users\Daria\Desktop\Test_AnalysisAndSimulation\ScientificWritingC08\N15- Smooth 15 deg.stl",
                          plane_x=147.7, plane_z=-37.4, plane_y=250):

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


    # Get bounds of your data grid
    xmin, xmax, ymin, ymax, zmin, zmax = grid.bounds

    # Clip STL to match data volume
    mesh_clipped = mesh.clip_box(bounds=grid.bounds, invert=False)

    # -----------------------------
    # 4. Create slices
    # -----------------------------

    #slice = grid.slice(normal='y', origin=[0,grid.center[1],0])
    min_val, max_val = y.min(), y.max()
    positions = np.linspace(min_val, max_val-80, 5)
    plotter = pv.Plotter(off_screen=False)

    center = grid.center

    # -----------------------------
    # NEW: Add delimitation planes
    # -----------------------------
    '''
    if plane_x is not None:
        # YZ-plane at given X value
        yz_plane = pv.Plane(
            center=(plane_x, (ymin + ymax) / 2, (zmin + zmax) / 2),
            direction=(1, 0, 0),          # normal pointing in X
            i_size=(ymax - ymin),
            j_size=(zmax - zmin),
            i_resolution=1,
            j_resolution=1
        )
        plotter.add_mesh(yz_plane, color="red", opacity=0.6, show_edges=True, edge_color="red")

    if plane_z is not None:
        # XY-plane at given Z value
        xy_plane = pv.Plane(
            center=((xmin + xmax) / 2, (ymin + ymax) / 2, plane_z),
            direction=(0, 0, 1),          # normal pointing in Z
            i_size=(xmax - xmin),
            j_size=(ymax - ymin),
            i_resolution=1,
            j_resolution=1
        )
        plotter.add_mesh(xy_plane, color="red", opacity=0.6, show_edges=True, edge_color="red")
    '''
    # Added Plane at Y = 250
    if plane_y is not None:
        # XZ-plane at given Y value
        xz_plane = pv.Plane(
            center=((xmin + xmax) / 2, plane_y, (zmin + zmax) / 2),
            direction=(0, 1, 0),          # normal pointing in Y
            i_size=(xmax - xmin),
            j_size=(zmax - zmin),
            i_resolution=1,
            j_resolution=1
        )
        plotter.add_mesh(xz_plane, color="red", opacity=0.6, show_edges=True, edge_color="red")

    if type == 'v':
        slices = []

        for pos in positions:
            origin = list(center)
            origin[1] = pos

            slice_plane = grid.slice(normal='y', origin=origin)

            if slice_plane.n_points > 0:   # avoid empty slices
                slices.append(slice_plane)

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

    if type == 'q':
        # -----------------------------
        # 4. Compute velocity gradient
        # -----------------------------
        deriv = grid.compute_derivative(scalars="velocity", gradient=True)
        grad = deriv["gradient"].reshape(-1, 3, 3)

        # -----------------------------
        # 5. Compute Q-criterion
        # -----------------------------
        S = 0.5 * (grad + np.transpose(grad, (0, 2, 1)))
        Omega = 0.5 * (grad - np.transpose(grad, (0, 2, 1)))

        S2 = np.sum(S**2, axis=(1, 2))
        Omega2 = np.sum(Omega**2, axis=(1, 2))

        Q = 0.5 * (Omega2 - S2)

        # Unit correction (mm → m)
        Q = Q / 1e6

        # Store for PyVista
        grid["Q"] = Q


        # -----------------------------
        # 6. Reshape to structured grid
        # -----------------------------
        Q_3D = Q.reshape(Nz, Ny, Nx)

        # -----------------------------
        # 7. Mask boundaries (NO extraction!)
        # -----------------------------
        pad = 15

        mask = np.zeros_like(Q_3D, dtype=bool)
        mask[pad:-pad, pad:-pad, pad:-pad] = True

        Q_3D_filtered = np.where(mask, Q_3D, 0.0)

        # -----------------------------
        # 8. Spanwise Q integral
        # -----------------------------
        q_threshold = np.percentile(Q, 98)

        Q_span = np.sum(Q_3D_filtered, axis=(0, 2))
        Q_filtered_flat = Q_3D_filtered.reshape(-1)
        grid["Q"] = Q_filtered_flat
        z_span = y[0, :, 0]   # spanwise coordinate

        # -----------------------------
        # 9. Matplotlib plot (non-blocking)
        # -----------------------------

        plt.ion()
        plt.figure()

        plt.plot(z_span, Q_span, '-o')
        plt.xlabel('Spanwise location (mm)')
        plt.ylabel('Integrated Q')
        plt.title('Spanwise Q integral')
        plt.grid()

        plt.show()

        # -----------------------------
        # 10. 3D vortex visualization
        # -----------------------------

        vortices = grid.contour(
            isosurfaces=[q_threshold],
            scalars="Q"
        )

        # Airfoil
        plotter.add_mesh(mesh_clipped, color="lightgray", opacity=1.0)

        # Vortex structures
        plotter.add_mesh(
            vortices,
            scalars="speed",
            cmap="plasma",
            opacity=1.0
        )

    #plotter.camera_position =[(364.33454087406733, 1034.0624653533628, -116.72001792193413),
        #(44.89354705810547, 257.818603515625, -6.211048126220703),
        #(0.030984611829599613, -0.1533612512099731, -0.9876843020201751)]
    
    plotter.render()  # force render
    plotter.add_axes()
    plotter.show_grid()
    plotter.camera.up = (0, 0, -1)  # flip Z axis
    #plotter.screenshot(r"C:\Users\alexa\OneDrive\Desktop\airfoil_q.png")
    plotter.show()
    plt.plot()

def calcForces(x,y,z,u,v,w, x1,x2,z1,z2,y1,y2):
    x = 0.001*x.T
    y = 0.001*y.T
    z = 0.001*z.T
    u = u.T
    v = v.T
    w = w.T
    lens = []
    xs = []
    for i in range(y2-y1):
        c = 0
        #top
        c += calcLine(x[x1:x2,y1 + i,z1],u[x1:x2,y1 + i,z1])
        #bottom
        c -= calcLine(x[x1:x2,y1 + i,z2],u[x1:x2,y1 + i,z2])
        #left
        c += calcLine(y[x1,y1 + i,z1:z2],w[x1,y1 + i,z1:z2])
        #right
        c-= calcLine(y[x2,y1 + i,z1:z2],w[x2,y1 + i,z1:z2])
        lens.append(c)
        xs.append(y[0,y1+i,0])
            # -----------------------------
    #plt.ion()
    plt.figure()

    plt.plot(xs, lens, '-o')
    plt.xlabel('Spanwise location (mm)')
    plt.ylabel('Integrated Q')
    plt.title('Spanwise Q integral')
    plt.grid()

    plt.show()


def calcLine(LinX,LinV):
    x = (LinX[0:-2] + LinX[1:-1])/2
    v = (LinV[0:-2] + LinV[1:-1])/2
    dx = abs(x[1] - x[0])
    s = 0
    for i in range(len(x)):
        s += dx*v[i]
    return s

if __name__ == "__main__":

    x, y, z, u, v, w, std_V, std_Vx, std_Vy, std_Vz = load_velocity_arrays_fast()
    print('hello')
    x = x.reshape(123,137,180)
    y = y.reshape(123,137,180)
    z = z.reshape(123,137,180)
    u = u.reshape(123,137,180)
    v= v.reshape(123,137,180)
    w = w.reshape(123,137,180)

    visualize_airfoil_piv(x, y, z, u, v, w, 'q')
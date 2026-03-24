import pyvista as pv
import numpy as np
from preprocessing import load_velocity_arrays_fast

# Load STL
airfoil = pv.read("N15- Smooth 15 deg.stl")

# Valid velocity points (exclude zeros)
x, y, z, u, v, w, std_V, std_Vx, std_Vy, std_Vz = load_velocity_arrays_fast()
mask = ~((u == 0) & (v == 0) & (w == 0))

# Subsample for performance
n_samples = 200_000
idx = np.random.choice(mask.sum(), n_samples, replace=False)
points = np.column_stack([x[mask][idx], y[mask][idx], z[mask][idx]]) #getting a list of position vectors of selected points
vectors = np.column_stack([u[mask][idx], v[mask][idx], w[mask][idx]]) #getting a list of velocity vectors of selected points

# Build point cloud
cloud = pv.PolyData(points)
cloud['velocity'] = vectors
cloud['u'] = u[mask][idx]



# Interpolate onto a uniform grid for streamlines
bounds = [x[mask].min(), x[mask].max(),
          y[mask].min(), y[mask].max(),
          z[mask].min(), z[mask].max()]

grid = pv.ImageData()
grid.dimensions = [50, 50, 50]
grid.origin = [bounds[0], bounds[2], bounds[4]] #origin of the coordinate system is at the minimum value of x,y,z coordinates
grid.spacing = [                                #50x50x50 grid lattince for visualization
    (bounds[1] - bounds[0]) / 49,               #50 points (49 intervals) span each axis
    (bounds[3] - bounds[2]) / 49,
    (bounds[5] - bounds[4]) / 49
]


# Interpolate on grid
interpolated = grid.interpolate(cloud, radius=50, sharpness=5)

# Mask out points inside the airfoil
selection = interpolated.select_enclosed_points(airfoil, tolerance=0.001)
inside_mask = selection['SelectedPoints'].astype(bool)
interpolated['velocity'][inside_mask] = [0.0, 0.0, 0.0]

# Use the original streamlines call, not streamlines_from_source
streamlines = interpolated.streamlines(
    vectors='velocity',
    source_center=[-150, 278, 10],
    source_radius=80,
    n_points=100,
    max_steps=1000,
    integration_direction='forward'
)
# Compute streamlines — seed from a plane upstream of the airfoil
#streamlines = interpolated.streamlines(
    #vectors='velocity',
    #source_center=[-150, 278, 10],   # upstream, mid-span, mid-height
    #source_radius=80,                # streamlines come out of a defined circular region centered at source_center with radius source_radius
    #n_points=200,                    # number of streamlines
    #max_steps=2000,                  # max number of integration steps along each streamline
    #integration_direction='forward'  # moving downstream, in the direction instantaneous velocity points towards
#)


# Plot
plotter = pv.Plotter()
plotter.add_mesh(airfoil, color='lightgray', opacity=0.8, label='Airfoil')
plotter.add_mesh(cloud, scalars='u', cmap='coolwarm', point_size=2,
                 render_points_as_spheres=True, opacity=0.3, label='Velocity field')

if streamlines.n_points > 0:
    plotter.add_mesh(streamlines.tube(radius=0.5), color='white', label='Streamlines')
else:
    print("Streamlines are empty — try adjusting source_center or source_radius")

plotter.add_scalar_bar(title='u [m/s]')
plotter.show()
print("Airfoil bounds:", airfoil.bounds)
#(xmin, xmax, ymin, ymax, zmin, zmax)

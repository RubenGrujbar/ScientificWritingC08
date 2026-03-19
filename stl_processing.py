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
points = np.column_stack([x[mask][idx], y[mask][idx], z[mask][idx]])
vectors = np.column_stack([u[mask][idx], v[mask][idx], w[mask][idx]])

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
grid.origin = [bounds[0], bounds[2], bounds[4]]
grid.spacing = [
    (bounds[1] - bounds[0]) / 49,
    (bounds[3] - bounds[2]) / 49,
    (bounds[5] - bounds[4]) / 49
]

# Interpolate velocity onto grid
interpolated = grid.interpolate(cloud, radius=20, sharpness=2)

# Compute streamlines — seed from a plane upstream of the airfoil
streamlines = interpolated.streamlines(
    vectors='velocity',
    source_center=[-150, 278, 10],   # upstream, mid-span, mid-height
    source_radius=80,
    n_points=50,
    max_steps=1000,
    integration_direction='forward'
)

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
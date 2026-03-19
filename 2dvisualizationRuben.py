import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.interpolate import griddata

# 1. Load data
df = pd.read_csv('Dataset NACA0015 Velocity and Standard deviation.csv')

target_y = 114.435
slice_df = df[np.isclose(df['y [mm]'], target_y, atol=0.001)].copy()

# 2. Separate valid points
flow_points = slice_df.dropna(subset=['Velocity u [m/s]'])

# 3. Create Grid
xi = np.linspace(slice_df['x [mm]'].min(), slice_df['x [mm]'].max(), 500)
zi = np.linspace(slice_df['z [mm]'].min(), slice_df['z [mm]'].max(), 500)
xi, zi = np.meshgrid(xi, zi)

# 4. Interpolate
ui = griddata((flow_points['x [mm]'], flow_points['z [mm]']), 
              flow_points['Velocity u [m/s]'], (xi, zi), method='linear')

# --- THE FIX: MASKING THE INTERPOLATION ---
# Griddata naturally interpolates across the "hole"
# We define a mask where the distance to the nearest REAL point is too large
from scipy.spatial import cKDTree
tree = cKDTree(flow_points[['x [mm]', 'z [mm]']].values)
# If a grid point is further than 3mm from any data point, consider it "Inside the Airfoil"
dist, _ = tree.query(np.c_[xi.ravel(), zi.ravel()])
dist = dist.reshape(xi.shape)
ui[dist > 3.0] = np.nan  # Adjust 3.0 based on your point spacing

# 5. Plotting
fig, ax = plt.subplots(figsize=(12, 7))
ax.set_facecolor('gray') # This gray will now show through the "cut" hole

v_limit = max(abs(flow_points['Velocity u [m/s]'].min()), abs(flow_points['Velocity u [m/s]'].max()))
cf = ax.contourf(xi, zi, ui, levels=np.linspace(-v_limit, v_limit, 51), 
                 cmap=mcolors.LinearSegmentedColormap.from_list("", ["#b2182b", "white", "#2166ac"]), 
                 extend='both')

# Legend Formatting
ticks = np.linspace(-v_limit, v_limit, 11)
cbar = fig.colorbar(cf, ticks=ticks)
cbar.ax.set_yticklabels([f'{t:.1f}' for t in ticks])

ax.invert_yaxis()
plt.show()
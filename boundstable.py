import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

filename = "Dataset NACA0015 Velocity and Standard deviation.csv"
df = pd.read_csv(filename, skipinitialspace=True)
df.columns = df.columns.str.strip()

# Define columns based on your dataset
col_x = 'x [mm]'
col_y = 'y [mm]'
col_z = 'z [mm]'
col_u = 'Velocity u [m/s]'
col_v = 'Velocity v [m/s]'
col_w = 'Velocity w [m/s]'
col_std_u = 'Standard deviation Vx [m/s]'
col_std_v = 'Standard deviation Vy [m/s]'
col_std_w = 'Standard deviation Vz [m/s]'

df_box = df[(df[col_x] >= -189.746) & (df[col_x] <= 274.892) & (df[col_y] >= 101.457) & (df[col_y] <= 454.478) & (df[col_z] >= -148.98) & (df[col_z] <= 167.7)]

u_target = 8.97

df_clean = df_box.dropna(subset=[col_u])
df_u = df_clean.iloc[(df_clean[col_u] - u_target).abs().argsort()[:3]]

#print(f"u value found: {df_u[col_u].values[2]:.4f} m/s")
#print(f"std u: {df_u[col_std_u].values[2]:.4f} m/s")


u_vals    = df_box[col_u].dropna().values
v_vals    = df_box[col_v].dropna().values
w_vals    = df_box[col_w].dropna().values
stdu_vals = df_box[col_std_u].dropna().values
stdv_vals = df_box[col_std_v].dropna().values
stdw_vals = df_box[col_std_w].dropna().values

#print(f"The max u value is {max(u_vals)}")
#print(f"The min u value is {min(u_vals)}")
#print(f"The max v value is {max(v_vals)}")
#print(f"The min v value is {min(v_vals)}")
#print(f"The max w value is {max(w_vals)}")
#print(f"The min w value is {min(w_vals)}")

print(f"The max std u value is {max(stdu_vals)}")
print(f"The max std v value is {max(stdv_vals)}")
print(f"The max std w value is {max(stdw_vals)}")

#fig, ax = plt.subplots(figsize=(10, 6))
#
#ax.hist(df_box[col_std_u].dropna().values, bins=50, color='steelblue', edgecolor='white', linewidth=0.5)
#
#ax.set_xlabel('u [m/s]')
#ax.set_ylabel('Count')
#ax.set_title('Distribution of u velocities in Control Volume')
#ax.grid(axis='y', linestyle='--', alpha=0.5)
#ax.set_ylim(0, 2e4)
#
#plt.tight_layout()
#plt.savefig('u_distribution.png', dpi=150)
#plt.show()
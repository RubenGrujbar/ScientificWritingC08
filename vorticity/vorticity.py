import pandas as pd
import numpy as np

# reading the x,y,z coordinates
df = pd.read_csv('Vorticity/gradient_results.csv')

# reading the U_gradient
du_dx = df['du_dx'].values
du_dy = df['du_dy'].values
du_dz = df['du_dz'].values

# reading the V_gradient
dv_dx = df['dv_dx'].values
dv_dy = df['dv_dy'].values
dv_dz = df['dv_dz'].values

# reading the W_gradient
dw_dx = df['dw_dx'].values
dw_dy = df['dw_dy'].values
dw_dz = df['dw_dz'].values

# calculating the vorticity components
omega_x = dw_dy - dv_dz
omega_y = du_dz - dw_dx
omega_z = dv_dx - du_dy

# creating a dataframe to store the results
df_out = pd.DataFrame({
    'x': x,
    'y': y,
    'z': z,
    'omega_x': omega_x,
    'omega_y': omega_y,
    'omega_z': omega_z
})

df_out.to_csv('Vorticity/vorticity_xyz.csv', index=False)

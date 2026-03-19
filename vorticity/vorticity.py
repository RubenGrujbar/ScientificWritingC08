import pandas as pd
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
import numpy as np
=======
=======
>>>>>>> 039f6103187495b2d8f5f283efcca4c1702204be
=======
>>>>>>> 039f6103187495b2d8f5f283efcca4c1702204be
=======
>>>>>>> a61984d8df727e3054eaedafdbff4cfa773e02ca
>>>>>>> Stashed changes
import numpy as np


#reading the x,y,z coordinates
dfu = pd.read_csv('Vorticity/U_gradient_results.csv')
<<<<<<< Updated upstream
x = dfu['x_coords'].values
y = dfu['y_coords'].values
z = dfu['z_coords'].values

=======
<<<<<<< HEAD
x = dfu['x'].values
y = dfu['y'].values
z = dfu['z'].values
=======
x = dfu['x_coords'].values
y = dfu['y_coords'].values
z = dfu['z_coords'].values
>>>>>>> a61984d8df727e3054eaedafdbff4cfa773e02ca
>>>>>>> Stashed changes

#readig the U_gradient
du_dx = dfu['du_dx'].values
du_dy = dfu['du_dy'].values
du_dz = dfu['du_dz'].values


#readig the V_gradient
dfv = pd.read_csv('Vorticity/V_gradient_results.csv',usecols=[3,4,5], dtype=np.float32)
dv_dx = dfv['dv_dx'].values
dv_dy = dfv['dv_dy'].values
dv_dz = dfv['dv_dz'].values


#reading the W_gradient
dfw = pd.read_csv('Vorticity/W_gradient_results.csv', usecols=[3,4,5], dtype=np.float32)
dw_dx = dfw['dw_dx'].values
dw_dy = dfw['dw_dy'].values
dw_dz = dfw['dw_dz'].values


#calculating the vorticity components
omega_x = dw_dy - dv_dz
omega_y = du_dz - dw_dx
omega_z = dv_dx - du_dy


#creating a dataframe to store the results
df_out = pd.DataFrame({
    'x': x,
    'y': y,
    'z': z,
    'omega_x': omega_x,
    'omega_y': omega_y,
    'omega_z': omega_z
})

<<<<<<< Updated upstream
df_out.to_csv('Vorticity/vorticity_xyz.csv', index=False)
=======
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
df_out.to_csv('Vorticity/vorticity_xyz.csv', index=False)
>>>>>>> 039f6103187495b2d8f5f283efcca4c1702204be
=======
df_out.to_csv('Vorticity/vorticity_xyz.csv', index=False)
>>>>>>> 039f6103187495b2d8f5f283efcca4c1702204be
=======
df_out.to_csv('Vorticity/vorticity_xyz.csv', index=False)
>>>>>>> 039f6103187495b2d8f5f283efcca4c1702204be
=======
df_out.to_csv('Vorticity/vorticity_xyz.csv', index=False)
>>>>>>> a61984d8df727e3054eaedafdbff4cfa773e02ca
>>>>>>> Stashed changes

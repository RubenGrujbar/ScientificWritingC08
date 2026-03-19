import pandas as pd
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
import numpy as np
=======
=======
>>>>>>> 039f6103187495b2d8f5f283efcca4c1702204be
=======
>>>>>>> 039f6103187495b2d8f5f283efcca4c1702204be
import numpy as np

#reading the x,y,z coordinates
dfu = pd.read_csv('Vorticity/U_gradient_results.csv')
x = dfu['x'].values
y = dfu['y'].values
z = dfu['z'].values

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

omega_x = dw_dy - dv_dz
omega_y = du_dz - dw_dx
omega_z = dv_dx - du_dy

df_out = pd.DataFrame({
    'x': x,
    'y': y,
    'z': z,
    'omega_x': omega_x,
    'omega_y': omega_y,
    'omega_z': omega_z
})

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

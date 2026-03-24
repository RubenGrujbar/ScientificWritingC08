import pandas as pd
import numpy as np

# reading the x,y,z coordinates
df = pd.read_csv('Vorticity/gradient_results_backup.csv')

# reading the U_gradient
du_dx = df.iloc[:, 3]
du_dy = df.iloc[:, 4]
du_dz = df.iloc[:, 5]

# reading the V_gradient
dv_dx = df.iloc[:, 6]
dv_dy = df.iloc[:, 7]
dv_dz = df.iloc[:, 8]

# reading the W_gradient
dw_dx = df.iloc[:, 9]
dw_dy = df.iloc[:, 10]
dw_dz = df.iloc[:, 11]

# calculating the vorticity components
omega_x = dw_dy - dv_dz
omega_y = du_dz - dw_dx
omega_z = dv_dx - du_dy

# adding the collumns to the dataframe
df['omega_x2'] = dw_dy - dv_dz
df['omega_y2'] = du_dz - dw_dx
df['omega_z2'] = dv_dx - du_dy

#saving the results to a new csv file
df.to_csv('Vorticity/gradient_results_backup.csv', index=False)

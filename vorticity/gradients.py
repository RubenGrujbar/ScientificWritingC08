import numpy as np
from pathlib import Path
import sys
import os

# Adds the parent directory to the search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from preprocessing import load_velocity_arrays_fast
url = "https://media.githubusercontent.com/media/RubenGrujbar/ScientificWritingC08/main/Dataset%20NACA0015%20Velocity%20and%20Standard%20deviation.csv"

#current_dir = Path(__file__).parent
#file_path = current_dir.parent /  "cleaned_dataset.csv"
#data = np.genfromtxt(file_path, delimiter=',', skip_header=1)
# x-coord, y-coord,z-coord,x-velocity,x-stan.dev.,y-velocity,y-stan.dev.,z-velocity,z-stan.dev.
#0   ,        1,      2,       3,           4,       5,          6,          7,          8

x_coords, y_coords, z_coords, u, v, w, std_V, std_Vx, std_Vy, std_Vz = load_velocity_arrays_fast(url)

y_jump = 180
z_jump = 180*137


def calculate_gradients(x_coords, y_coords, z_coords, u, v, w, std_V, std_Vx, std_Vy, std_Vz,y_jump,z_jump):

    du_dx = np.zeros_like(x_coords)
    du_dy = np.zeros_like(x_coords)
    du_dz = np.zeros_like(x_coords)

    # X-Gradients
    du_dx[1:-1] = (u[2:] - u[:-2]) / (x_coords[2:] - x_coords[:-2])*1000 #mm to m conversion
    du_dx[0] = (u[1] - u[0]) / (x_coords[1] - x_coords[0])*1000
    du_dx[-1] = (u[-1] - u[-2]) / (x_coords[-1] - x_coords[-2])*1000

    # Y-Gradients
    du_dy[y_jump:-y_jump] = (u[2*y_jump:] - u[:-2*y_jump]) / (y_coords[2*y_jump:] - y_coords[:-2*y_jump])*1000
    
    # Z-Gradients
    du_dz[z_jump:-z_jump] = (u[2*z_jump:] - u[:-2*z_jump]) / (z_coords[2*z_jump:] - z_coords[:-2*z_jump])*1000
    



    dv_dx = np.zeros_like(x_coords)
    dv_dy = np.zeros_like(x_coords)
    dv_dz = np.zeros_like(x_coords)

    # X-Gradients
    dv_dx[1:-1] = (v[2:] - v[:-2]) / (x_coords[2:] - x_coords[:-2])*1000
    dv_dx[0] = (v[1] - v[0]) / (x_coords[1] - x_coords[0])*1000
    dv_dx[-1] = (v[-1] - v[-2]) / (x_coords[-1] - x_coords[-2])*1000

    # Y-Gradients
    dv_dy[y_jump:-y_jump] = (v[2*y_jump:] - v[:-2*y_jump]) / (y_coords[2*y_jump:] - y_coords[:-2*y_jump])*1000
    
    # Z-Gradients
    dv_dz[z_jump:-z_jump] = (v[2*z_jump:] - v[:-2*z_jump]) / (z_coords[2*z_jump:] - z_coords[:-2*z_jump])*1000
   

    dw_dx = np.zeros_like(x_coords)
    dw_dy = np.zeros_like(x_coords)
    dw_dz = np.zeros_like(x_coords)

    # X-Gradients
    dw_dx[1:-1] = (w[2:] - w[:-2]) / (x_coords[2:] - x_coords[:-2]) * 1000 
    dw_dx[0] = (w[1] - w[0]) / (x_coords[1] - x_coords[0]) *1000
    dw_dx[-1] = (w[-1] - w[-2]) / (x_coords[-1] - x_coords[-2]) *1000

    # Y-Gradients
    dw_dy[y_jump:-y_jump] = (w[2*y_jump:] - w[:-2*y_jump]) / (y_coords[2*y_jump:] - y_coords[:-2*y_jump])*1000

    # Z-Gradients
    dw_dz[z_jump:-z_jump] = (w[2*z_jump:] - w[:-2*z_jump]) / (z_coords[2*z_jump:] - z_coords[:-2*z_jump])*1000
    
    omega_x = np.zeros_like(x_coords)
    omega_x[0:-1] = dw_dy[0:-1] - dv_dz[0:-1]

    omega_y = np.zeros_like(x_coords)
    omega_y[0:-1] = du_dz[0:-1] - dw_dx[0:-1]

    omega_z = np.zeros_like(x_coords)
    omega_z[0:-1] = dv_dx[0:-1] - du_dy[0:-1]


    res = np.nan_to_num(np.column_stack((x_coords, y_coords, z_coords, du_dx,du_dy,du_dz,dv_dx,dv_dy,dv_dz,dw_dx, dw_dy, dw_dz,omega_x,omega_y,omega_z)))
    np.savetxt('vorticity/gradient_results.csv', res, delimiter=',', header='x,y,z,du_dx,du_dy,du_dz,dv_dx,dv_dy,dv_dz,dw_dx, dw_dy, dw_dz, omega_x, omega_y, omega_z', comments='')

print("test1")

calculate_gradients(x_coords, y_coords, z_coords, u, v, w, std_V, std_Vx, std_Vy, std_Vz,y_jump,z_jump)


print("done")
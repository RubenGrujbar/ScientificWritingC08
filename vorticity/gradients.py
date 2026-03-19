import numpy as np
from pathlib import Path
current_dir = Path(__file__).parent
file_path = current_dir.parent /  "cleaned_dataset.csv"
data = np.genfromtxt(file_path, delimiter=',', skip_header=1)
# x-coord, y-coord,z-coord,x-velocity,x-stan.dev.,y-velocity,y-stan.dev.,z-velocity,z-stan.dev.
#0   ,        1,      2,       3,           4,       5,          6,          7,          8

y_jump = 180
z_jump = 180*137


def calculate_gradients(data,y_jump,z_jump):
    x_coords = data[:, 0]
    y_coords = data[:, 1]
    z_coords = data[:, 2]
    u = data[:, 3]

    du_dx = np.zeros_like(x_coords)
    du_dy = np.zeros_like(y_coords)
    du_dz = np.zeros_like(z_coords)

    # X-Gradients
    du_dx[1:-1] = (u[2:] - u[:-2]) / (x_coords[2:] - x_coords[:-2])
    du_dx[0] = (u[1] - u[0]) / (x_coords[1] - x_coords[0])
    du_dx[-1] = (u[-1] - u[-2]) / (x_coords[-1] - x_coords[-2])

    # Y-Gradients
    du_dy[y_jump:-y_jump] = (u[2*y_jump:] - u[:-2*y_jump]) / (y_coords[2*y_jump:] - y_coords[:-2*y_jump])
    
    # Z-Gradients
    du_dz[z_jump:-z_jump] = (u[2*z_jump:] - u[:-2*z_jump]) / (z_coords[2*z_jump:] - z_coords[:-2*z_jump])
    

    v = data[:, 5]

    dv_dx = np.zeros_like(x_coords)
    dv_dy = np.zeros_like(y_coords)
    dv_dz = np.zeros_like(z_coords)

    # X-Gradients
    dv_dx[1:-1] = (v[2:] - v[:-2]) / (x_coords[2:] - x_coords[:-2])
    dv_dx[0] = (v[1] - v[0]) / (x_coords[1] - x_coords[0])
    dv_dx[-1] = (v[-1] - v[-2]) / (x_coords[-1] - x_coords[-2])

    # Y-Gradients
    dv_dy[y_jump:-y_jump] = (v[2*y_jump:] - v[:-2*y_jump]) / (y_coords[2*y_jump:] - y_coords[:-2*y_jump])
    
    # Z-Gradients
    dv_dz[z_jump:-z_jump] = (v[2*z_jump:] - v[:-2*z_jump]) / (z_coords[2*z_jump:] - z_coords[:-2*z_jump])
   
    w = data[:, 7]

    dw_dx = np.zeros_like(x_coords)
    dw_dy = np.zeros_like(y_coords)
    dw_dz = np.zeros_like(z_coords)

    # X-Gradients
    dw_dx[1:-1] = (w[2:] - w[:-2]) / (x_coords[2:] - x_coords[:-2])
    dw_dx[0] = (w[1] - w[0]) / (x_coords[1] - x_coords[0])
    dw_dx[-1] = (w[-1] - w[-2]) / (x_coords[-1] - x_coords[-2])

    # Y-Gradients
    dw_dy[y_jump:-y_jump] = (w[2*y_jump:] - w[:-2*y_jump]) / (y_coords[2*y_jump:] - y_coords[:-2*y_jump])

    # Z-Gradients
    dw_dz[z_jump:-z_jump] = (w[2*z_jump:] - w[:-2*z_jump]) / (z_coords[2*z_jump:] - z_coords[:-2*z_jump])
    
    res = np.nan_to_num(np.column_stack((x_coords, y_coords, z_coords, du_dx,du_dy,du_dz,dv_dx,dv_dy,dv_dz,dw_dx, dw_dy, dw_dz)))
    np.savetxt('vorticity/gradient_results.csv', res, delimiter=',', header='x,y,z,du_dx,du_dy,du_dz,dv_dx,dv_dy,dv_dz,dw_dx, dw_dy, dw_dz', comments='')
    

print("test1")

calculate_gradients(data,y_jump,z_jump)

print("done")

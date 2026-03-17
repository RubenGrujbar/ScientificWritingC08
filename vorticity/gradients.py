
import numpy as np
from pathlib import Path

current_dir = Path(__file__).parent
file_path = current_dir.parent /  "Dataset NACA0015 Velocity and Standard deviation.csv"
data = np.genfromtxt(file_path, delimiter=',', skip_header=1)
#number, x-coord, y-coord,z-coord,x-velocity,x-stan.dev.,y-velocity,y-stan.dev.,z-velocity,z-stan.dev.
#0,         1   ,   2,      3,      4,             5,       6,          7,          8,          9

x_coords = data[:,1] #all rows in 1st column
x_velocity = data[:,4]

y_coords = data[:,2]
y_velocity = data[:,6]

z_coords = data[:,3]
z_velocity = data[:,8]


def du_gradients():
    du_dx = np.zeros_like(x_velocity)
    # Central Difference: Change in x_velocity over change in y_coords
    # (Using indices 1:-1 for the middle of the array)
    du_dx[1:-1] = (x_velocity[2:]-x_velocity[:-2]) / (x_coords[2:]-x_coords[:-2]) 
    # Forward difference for the first point
    du_dx[0]  = (x_velocity[1] - x_velocity[0]) / (x_coords[1] - x_coords[0])
    # Backward difference for the last point
    du_dx[-1] = (x_velocity[-1] - x_velocity[-2]) / (x_coords[-1] - x_coords[-2])


    du_dy = np.zeros_like(x_velocity)
    du_dy[1:-1] = (x_velocity[2:] - x_velocity[:-2]) / (y_coords[2:] - y_coords[:-2])
    du_dy[0] = (x_velocity[1] - x_velocity[0]) / (y_coords[1] - y_coords[0])
    du_dy[-1] = (x_velocity[-1] - x_velocity[-2]) / (y_coords[-1] - y_coords[-2])

    du_dz = np.zeros_like(x_velocity)
    du_dz[1:-1] = (x_velocity[2:] - x_velocity[:-2]) / (z_coords[2:] - z_coords[:-2])
    du_dz[0] = (x_velocity[1] - x_velocity[0]) / (z_coords[1] - z_coords[0])
    du_dz[-1] = (x_velocity[-1] - x_velocity[-2]) / (z_coords[-1] - z_coords[-2])

    du_dx = np.nan_to_num(du_dx, nan=0.0, posinf=0.0, neginf=0.0) #clamps divide by zero errors to 0.
    du_dy = np.nan_to_num(du_dy, nan=0.0, posinf=0.0, neginf=0.0)
    du_dz = np.nan_to_num(du_dz, nan=0.0, posinf=0.0, neginf=0.0)

    du_write = np.column_stack((x_coords, y_coords, z_coords, du_dx, du_dy, du_dz))

    np.savetxt('vorticity/U_gradient_results.csv', du_write, delimiter=',', header='x_coords,y_coords,z_coords,du_dx,du_dy,du_dz', comments='')

def dv_gradients():
    dv_dx = np.zeros_like(y_velocity)
    dv_dx[1:-1] = (y_velocity[2:] - y_velocity[:-2]) / (x_coords[2:] - x_coords[:-2])
    dv_dx[0] = (y_velocity[1] - y_velocity[0]) / (x_coords[1] - x_coords[0])
    dv_dx[-1] = (y_velocity[-1] - y_velocity[-2]) / (x_coords[-1] - x_coords[-2])

    dv_dy = np.zeros_like(y_velocity)
    dv_dy[1:-1] = (y_velocity[2:] - y_velocity[:-2]) / (y_coords[2:] - y_coords[:-2])
    dv_dy[0] = (y_velocity[1] - y_velocity[0]) / (y_coords[1] - y_coords[0])
    dv_dy[-1] = (y_velocity[-1] - y_velocity[-2]) / (y_coords[-1] - y_coords[-2])

    dv_dz = np.zeros_like(y_velocity)
    dv_dz[1:-1] = (y_velocity[2:] - y_velocity[:-2]) / (z_coords[2:] - z_coords[:-2])
    dv_dz[0] = (y_velocity[1] - y_velocity[0]) / (z_coords[1] - z_coords[0])
    dv_dz[-1] = (y_velocity[-1] - y_velocity[-2]) / (z_coords[-1] - z_coords[-2])

    dv_write = np.column_stack((x_coords, y_coords, z_coords, dv_dx, dv_dy, dv_dz))

    np.savetxt('vorticity/V_gradient_results.csv', dv_write, delimiter=',', header='x_coords,y_coords,z_coords,dv_dx,dv_dy,dv_dz', comments='')

def dw_gradients():
    dw_dx = np.zeros_like(z_velocity)
    dw_dx[1:-1] = (z_velocity[2:] - z_velocity[:-2]) / (x_coords[2:] - x_coords[:-2])
    dw_dx[0] = (z_velocity[1] - z_velocity[0]) / (x_coords[1] - x_coords[0])
    dw_dx[-1] = (z_velocity[-1] - z_velocity[-2]) / (x_coords[-1] - x_coords[-2])

    dw_dy = np.zeros_like(z_velocity)
    dw_dy[1:-1] = (z_velocity[2:] - z_velocity[:-2]) / (y_coords[2:] - y_coords[:-2])
    dw_dy[0] = (z_velocity[1] - z_velocity[0]) / (y_coords[1] - y_coords[0])
    dw_dy[-1] = (z_velocity[-1] - z_velocity[-2]) / (y_coords[-1] - y_coords[-2])

    dw_dz = np.zeros_like(z_velocity)
    dw_dz[1:-1] = (z_velocity[2:] - z_velocity[:-2]) / (z_coords[2:] - z_coords[:-2])
    dw_dz[0] = (z_velocity[1] - z_velocity[0]) / (z_coords[1] - z_coords[0])
    dw_dz[-1] = (z_velocity[-1] - z_velocity[-2]) / (z_coords[-1] - z_coords[-2])

    dw_dx = np.nan_to_num(dw_dx, nan=0.0, posinf=0.0, neginf=0.0)
    dw_dy = np.nan_to_num(dw_dy, nan=0.0, posinf=0.0, neginf=0.0)
    dw_dz = np.nan_to_num(dw_dz, nan=0.0, posinf=0.0, neginf=0.0)

    dw_write = np.column_stack((x_coords, y_coords, z_coords, dw_dx, dw_dy, dw_dz))

    np.savetxt('vorticity/W_gradient_results.csv', dw_write, delimiter=',', header='x_coords,y_coords,z_coords,dw_dx,dw_dy,dw_dz', comments='')

print("start!")
dv_gradients()
print("50percent")
dw_gradients()
print("done!")
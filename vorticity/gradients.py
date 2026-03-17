
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

du_dx = np.zeros_like(x_velocity)
du_dx[1:-1] = (x_velocity[2:]-x_velocity[:-2]) / (x_coords[2:]-x_coords[:-2])  #central difference 

du_dx[0]  = (x_velocity[1] - x_velocity[0]) / (x_coords[1] - x_coords[0])
du_dx[-1] = (x_velocity[-1] - x_velocity[-2]) / (x_coords[-1] - x_coords[-2])


np.savetxt('vorticity/gradient_results.csv', du_dx, delimiter=',', header='du_dx', comments='')
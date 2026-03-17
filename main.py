import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt
from preprocessing import wall_derivative
from preprocessing import transform_to_wall_coords
from processing import finding_zero

#mat = loadmat('C:\\School\\project 2\\small_data2.mat')
mat = loadmat('small_data2.mat')
data = mat['small']
temp_X = data['v1']
X = temp_X[0,0]
X=X[30:200][30:200]
temp_Y = data['v2']
Y = temp_Y[0,0]
Y = Y[30:200][30:200]
temp_U = data['v3']
U = temp_U[0,0]
U = U[30:200][30:200]
temp_V= data['v4']
V = temp_V[0,0]
V = V[30:200][30:200]



def finding_zero():
    hits = np.zeros((139, 226))
    for i in range(0,len(X)-1):

        for j in range(0,len(Y)-1):

            if np.isnan(U[j, i]):
                hits[j, i] = -1
            elif U[j, i] * U[j, i + 1] > 300: #this is gonna be less than 0 for separation
                hits[j, i] = 1
    return hits #hits where the zeros are found 

hits = finding_zero()

def wall_derivative(x):  #somehow find wall geometry derivative, this is a placeholder
    return -3.141

def transform_to_wall_coords(X,Y,U,V): #transform from global x and y to wall normal to wall tangent
    U_local = np.zeros((139, 226))#this is hardcoded but it shouldnt be but im lazy!!!!!!!!!!!!!!!!!!
    V_local = np.zeros((139, 226))
    for x in range(0,len(X)-1):
        wall_derivative_val = wall_derivative(x)
        denom = np.sqrt(1+wall_derivative_val**2)
        for y in range(0,len(Y)-1):
            U_global = U[y,x]
            V_global = V[y,x]

            tangent_x = 1.0 / denom
            tangent_y = wall_derivative_val / denom

            normal_x = -wall_derivative_val/ denom
            normal_y = 1.0 / denom



            U_local[y,x] = (U_global*tangent_x + V_global*tangent_y)/(denom)
            V_local[y,x] = (U_global*normal_x + V_global*normal_y)/(denom)
    return U_local, V_local


U_local, V_local = transform_to_wall_coords(X,Y,U,V)



plt.figure(1)
plt.title("U")
plt.pcolormesh(X, Y, U, cmap='jet', vmin=7.5, vmax=18)
plt.colorbar(label='U velocity [m/s]') # Adds the color legend

plt.figure(2)
plt.title("V")
plt.pcolormesh(X, Y, V, cmap='jet', vmin=0, vmax=5)
plt.colorbar(label='V velocity [m/s]') # Adds the color legend

plt.figure(3)
plt.title("Separation")
plt.pcolormesh(X, Y, hits, cmap='jet', vmin=-1, vmax=1)
plt.colorbar(label='Separation ') # Adds the color legend

plt.figure(4)
plt.title("Rotated Velocity")
plt.pcolormesh(X, Y, U_local, cmap='jet', vmin=0, vmax=5)
plt.colorbar(label='Separation ') # Adds the color legend

plt.figure(5)
plt.title("Mean Velocity Profile")
plt.pcolormesh(X, Y, ((((U**2)*(V**2))**0.5)/14.8), cmap='jet', vmin=0, vmax=3)
plt.colorbar(label='Mean Velocity / Freestream velocity') # Adds the color legend
plt.show()



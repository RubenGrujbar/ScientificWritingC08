import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt

mat = loadmat('C:\\School\\project 2\\small_data2.mat')
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
            elif U[j, i] * U[j, i + 1] > 300:
                hits[j, i] = 1
    return hits

hits = finding_zero()




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
plt.title("Mean Velocity Profile")
plt.pcolormesh(X, Y, ((((U**2)*(V**2))**0.5)/14.8), cmap='jet', vmin=0, vmax=3)
plt.colorbar(label='Mean Velocity / FreeStream') # Adds the color legend
plt.show()
#rows between 70 and 170
#columns between 70 and 130




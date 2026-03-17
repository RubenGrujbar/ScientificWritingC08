import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
print('hello')
# grid
x = np.linspace(-1, 2, 200)
y = np.linspace(-1, 1, 150)
X, Y = np.meshgrid(x, y)

# synthetic vortex flow
U = 1 - Y
V = X

# velocity magnitude
speed = np.sqrt(U**2 + V**2)

# simple airfoil shape
theta = np.linspace(0, 2*np.pi, 200)
xa = 0.5*np.cos(theta) + 0.2
ya = 0.1*np.sin(theta)

# plotting
plt.figure(figsize=(8,4))

# colored velocity magnitude
plt.contourf(X, Y, speed, levels=50, cmap='jet')

# streamlines
plt.streamplot(X, Y, U, V,
               density=2,
               color='k',
               linewidth=0.8)

# airfoil
plt.fill(xa, ya, 'white')
plt.plot(xa, ya, 'k', linewidth=2)

# formatting
plt.axis('equal')
plt.xlabel('x/c')
plt.ylabel('y/c')
plt.title('Flow field over airfoil')
plt.colorbar(label='Velocity magnitude')

plt.show()
def Plt3DVisu():
    pass
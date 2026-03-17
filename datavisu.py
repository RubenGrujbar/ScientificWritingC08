import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
print('hello')
Xa = []
Ya = []


def Plt2DStreamVisu(X, Y, U, V, xa = Xa, ya = Ya):
    
    X, Y = np.meshgrid(X, Y)

    # plotting
    plt.figure(figsize=(8,4))

    speed = (U**2 + V**2)**0.5

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
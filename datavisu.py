import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
print('hello')
Xa = []
Ya = []


def Plt2DStreamVisu(X, Y, U, V, xa = Xa, ya = Ya):
    
    #X, Y = np.meshgrid(X, Y)
    #X = np.round(X,decimals=2)
    #Y = np.round(Y,decimals=2)
    #d = X[1] - Y[0]
    #X = np.linspace(X.size,)
    x_raw = X[0, :]
    y_raw = Y[:, 0]

    x = np.linspace(x_raw[0], x_raw[-1], len(x_raw))
    y = np.linspace(y_raw[0], y_raw[-1], len(y_raw))
    print(x)
    print(y)
    X, Y = np.meshgrid(x, y, indexing='ij')
    X = np.transpose(X)
    Y = np.transpose(Y)
    U = np.flip(U, axis=0)
    V = np.flip(V, axis=0)
    Y = -1*np.flip(Y, axis=0)
    # plotting
    plt.figure(figsize=(8,4))
    speed = (U**2 + V**2)**0.5
    threshold = 1e-3
    speed_masked = np.ma.masked_where(speed < threshold, speed)
    print(speed)



    # colored velocity magnitude
    #plt.contourf(X, Y, speed , levels=50, cmap='jet')

    cmap = plt.cm.jet
    cmap.set_bad('white')
    plt.contourf(X, Y, speed_masked, levels=50, cmap=cmap)
    #plt.contour(X, Y, speed, levels=[threshold], colors='k', linewidths=2)

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
    plt.xlabel('x mm from LE')
    plt.ylabel('y mm from LE')
    plt.title('Flow field over airfoil')
    plt.colorbar(label='Velocity magnitude')

    plt.show()
    return 'worked'


if __name__ == "__main__":
    #current_dir = os.path.dirname(__file__) #Check file path of this file
    #file_path = os.path.join(current_dir, 'Dataset NACA0015 Velocity and Standard deviation.csv') #Build the file path for the dataset

    #df = pd.read_csv(file_path, index_col=0, delimiter=",", skipinitialspace=True)
    a = np.array([0,1,2,3,0,1,2,3,0,1,2,3])
    b = np.array([0,0,0,0,1,1,1,1,2,2,2,2])
    c = np.array([20,20,20,20,20,20,20,20,20,20,20,20])
    #print(a.reshape(3,4,1))
    #print(b.reshape(3,4,1))
    #print(c.reshape(3,4,1))
    

    data = pd.read_csv(r'C:\Users\alexa\OneDrive\Desktop\ScientificWritingC08\cleaned_dataset.csv')
    x = data["x [mm]"].to_numpy()
    y = data["y [mm]"].to_numpy()
    z = data["z [mm]"].to_numpy()
    u = data["Velocity u [m/s]"].to_numpy()
    v = data["Velocity v [m/s]"].to_numpy()
    w = data["Velocity w [m/s]"].to_numpy()
    print(x[0])
    
    x = x.reshape(123,137,180)
    print(x[0][0][0])
    y = y.reshape(123,137,180)
    z = z.reshape(123,137,180)
    u = u.reshape(123,137,180)
    v= v.reshape(123,137,180)
    w = w.reshape(123,137,180)
    #print(np.transpose(x[:,80,:]))
    #print(np.transpose(x[:,80,:]))

    #print(z)
    #print(x[:,70,:])
    print(y[0,70,0])
    print(Plt2DStreamVisu(x[:,70,:],z[:,70,:],u[:,70,:],v[:,70,:]))
    
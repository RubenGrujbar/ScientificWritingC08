
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
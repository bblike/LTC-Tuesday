# In this section I am importing all the libraries I will need
import numpy as np
import matplotlib.pyplot as plt
import time


# In this section I am setting the domain of solution and the discretised grid

# Space step
h = 4.6 #mm
# Time step
t = 0.01 #s
# Size of the cross-sectional area of the steak
Lx = 23 #mm
Ly = 23 #mm
Heating_time = 60 #s

# Length of each side of the the cross-sectional area
Nx = int(Lx / h )
Ny = int(Ly / h )

# Length of time
Nt = int(Heating_time / t)

# Temperature at each point
T = np.zeros((Nx + 1,Ny + 1,Nt))
print(T.shape)

# In this section I am defining arrays I would need (if neeeded)

# T is initialized above for storing the temperature of the steak at each point


# In this section I am setting the boundary conditions/initial values

# Thermal diffusivity (Iron)
a = 23  # m^2/s

# Temperature initialization
# Bottom of the ribeye steak heated near the pan is 100 degrees
# Rest of the ribeye steak is as same as the temperature of the refrigerator where it stored
T[:,:,0] = 5
T[0,:,:] = 100


# In this section I am implementing the numerical method
r = a * t / h ** 2
print(r)
def ParaPDE(i,j,k):
    T[i,j,k+1] = r * (T[i+1,j,k] + T[i-1,j,k] + T[i,j+1,k] + T[i,j-1,k] - 4 * T[i,j,k]) + T[i,j,k]

for k in range(0,Nt - 1):
    for i in range(1,Nx):
        for j in range(0,Ny):
            ParaPDE(i,j,k)

# In this section I am showing the results
x = np.arange(0,Nx)
y = np.arange(0,Ny)
Xg,Yg = np.meshgrid(x,y)


plt.ion()
for k in range(0, Nt-1, 10):
    cntr1 = plt.contourf(Xg, Yg, T[:-1, :-1, k], levels = 20)
    plt.colorbar(cntr1)
    plt.title("{}".format(k))
    plt.show()
    time.pause(0.2)
    plt.clf()

# In this section I am celebrating
print('CW done: I deserve a good mark')
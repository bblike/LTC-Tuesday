import numpy as np
from matplotlib import pyplot as plt
f = open('T120I2.dat')
data = f.readlines()
length = len(data)

V = np.zeros((length))
I = np.zeros((length))
R = np.zeros((length)-1)

for i in range(0, length):
    string = data[i][26:]
    V[i], I[i] = string.split(" ")

for i in range(0, length-1):
    R[i] = (V[i+1]-V[i])/(I[i+1]-I[i])
    #R[i] = V[i]/I[i]
print(V)
print(I)
print(R)

fig1 = plt.figure()
ax1 = fig1.add_axes([0.1, 0.1, 0.8, 0.3])
ax2 = fig1.add_axes([0.1, 0.4, 0.8, 0.3])
ax3 = fig1.add_axes([0.1, 0.7, 0.8, 0.3])

ax1.plot(range(0, length), V, label = "voltage", color = "red")
#plt.legend()

ax2.plot(I, label = "current", color = "blue")
#plt.legend()

ax3.plot(R,  label = "resistance", color = "green")
plt.legend()
plt.show()
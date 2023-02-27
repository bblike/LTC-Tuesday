import numpy as np
from matplotlib import pyplot as plt
f = open('week4-semiC/T140V3.dat')
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
ax1 = fig1.add_axes([0.1, 0.1, 0.8, 0.4])
ax2 = fig1.add_axes([0.1, 0.5, 0.8, 0.4])
#ax3 = fig1.add_axes([0.1, 0.7, 0.8, 0.3])

#ax1.plot(range(0, length), V, label = "voltage", color = "red")
#plt.legend()

ax2.plot(R[0:30], I[1:30], label = "I-V", color = "blue")
plt.legend()

ax1.plot(R[20:50], label = "resistance", color = "green")
plt.legend()
plt.show()
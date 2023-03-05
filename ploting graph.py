import numpy as np
from matplotlib import pyplot as plt
f = open('week5/T80V3.dat')
k = open('week5/T200V3.dat')
data = f.readlines()
data2 = k.readlines()
length = len(data)
length2 = len(data)

T = np.zeros(length)
V = np.zeros(length)
I = np.zeros(length)
R = np.zeros(length-1)

T2 = np.zeros(length)
V2 = np.zeros(length)
I2 = np.zeros(length)
R2 = np.zeros(length-1)

for i in range(0, length-1):
    string = data[i]
    T[i], V[i], I[i], R[i] = string.split(" ")

for i in range(0, length2-1):
    string = data2[i]
    T2[i], V2[i], I2[i], R2[i] = string.split(" ")


#single graph plots
fig1 = plt.figure()
ax1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8])
#ax1.set_title("V-I graph")
ax1.plot(V[60:150], R[60:150], marker = "x", label = "V-R plot T80", color = "red")
ax1.plot(V2[50:150], R2[50:150], marker = "x", label = "V-R plot T200", color = "blue")
#ax1.plot(V, I, marker = "x", label = "I-V plot T80", color = "red")
#ax1.plot(V2, I2, marker = "x", label = "I-V plot T200", color = "blue")
plt.legend()


fig1.show()
"""
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
plt.show()"""
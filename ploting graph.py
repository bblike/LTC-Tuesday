import numpy as np
from matplotlib import pyplot as plt
import scipy.stats as scps
f = open('week6-super/T108V3.dat')
k = open('week6-super/T107V3.dat')
file = ["T80V1.dat", "T90V1.dat", "T100V1.dat", "T110V1.dat", "T120V1.dat", "T130V1.dat", "T140V1.dat", "T150V1.dat", "T160V1.dat", "T170V1.dat", "T180V1.dat","T190V1.dat","T200V1.dat"]
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

"""
#-V-R graph
fig1 = plt.figure()
ax1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8])
#ax1.set_title("V-I graph")
ax1.plot(V[60:150], R[60:150], marker = "x", label = "V-R plot T80", color = "red")
ax1.plot(V2[50:150], R2[50:150], marker = "x", label = "V-R plot T200", color = "blue")
#ax1.plot(V, I, marker = "x", label = "I-V plot T80", color = "red")
#ax1.plot(V2, I2, marker = "x", label = "I-V plot T200", color = "blue")
plt.legend()


fig1.show()"""


#I-V graph
fig1 = plt.figure()

#ax3 = fig1.add_axes([0.1, 0.7, 0.8, 0.3])

#ax1.plot(range(0, length), V, label = "voltage", color = "red")
#plt.legend()

#plt.plot(V, np.log(I), marker = "x", label = "I-V 80K", color = "blue")
#plt.plot(V2[20:40], np.log(I2[20:40]), marker = "x", label = "I-V 200K", color = "green")
plt.plot(I[:30], R[:30], marker = "x", label = "I-R 108K", color = "blue")
plt.plot(I2[:30], R2[:30], marker = "x", label = "I-R 107K", color = "green")
result = [1,2,3,4]
result2 = [1,2,3,4]

temp = scps.linregress(I[:30], R[:30])
result[0] = temp.slope
result[1] = temp.intercept
result[2] = temp.stderr
result[3] = temp.intercept_stderr

xe = np.arange(0, 0.06, 0.002)
ye = xe * result[0] + result[1]
plt.plot(xe, ye, color = "red")

temp2 = scps.linregress(I2[:30], R2[:30])
result2[0] = temp2.slope
result2[1] = temp2.intercept
result2[2] = temp2.stderr
result2[3] = temp2.intercept_stderr


xe2 = np.arange(0, 0.06, 0.002)
ye2 = xe2 * result2[0] + result2[1]
plt.plot(xe2, ye2, color = "black")

print(result)
print(result2)
plt.legend()
plt.show()

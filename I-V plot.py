import numpy as np
from matplotlib import pyplot as plt
import os
import scipy.stats as scps

path = r"C:\Users\Li Zhejun\Desktop\LTC-Tuesday\week5"
files = os.listdir(path)
files.sort(key=lambda x:int(x[1:-6]))
s = []
counter = 0
file_length = len(files)
data = []
fig1 = plt.figure(figsize=(8, 6))
ax1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8])
ax2 = fig1.add_axes([0.69, 0.2, 0.2, 0.25])
ax3 = fig1.add_axes([0.32, 0.6, 0.2, 0.2])
ax1.set_title("relations between voltage and current at different temperature")
ax1.set_xlabel("Voltage/V")
ax1.set_ylabel("Current/A")
ax2.set_xlabel("Voltage/V")
ax2.set_ylabel("Current/A")
ax3.set_xlabel("Temperature/K")
ax3.set_ylabel("critical voltage/V")
wide_select = [80, 90, 100, 120, 140, 200, 180, 160, 220, 240, 260]
semi_select = [80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260]
show_select = [80, 120, 160, 200, 240]

sign = 0
marker = 0
result = []
for l in [2]:
    for file in files:
        for s in semi_select:
            if file[1:-6] == "210" or file[1:-6] == "220" or file[1:-6] == "230" or file[1:-6] == "240" or file[1:-6] == "250" or file[1:-6] == "260":
                sign = -1
            else:
                sign = 1

            if file == "T{}V{}.dat".format(np.str_(s), l):
                f = open("week5./{}".format(file))
                data = f.readlines()
                counter += 1
                #print(counter)
                length = len(data)
                T = np.zeros(length)
                V = np.zeros(length)
                I = np.zeros(length)
                R = np.zeros(length)

                for i in range(0, length):
                    string = data[i]
                    T[i], V[i], I[i], R[i] = string.split(" ")


                T = T[T != 0]
                V = V[V != 0]
                I = I[I != 0]
                R = R[R != 0]
                V = V * sign
                R = R * sign

                for i in range(0, len(I)):
                    if I[i] < 0.000001:
                        marker = i
                print("marker = ", marker)
                for sh in wide_select:
                    if s == sh:
                        ax1.plot(V[:], I[:], marker="_", label="T = {}K".format(sh))

                if file[1:-6] == "100" or file[1:-6] == "120":
                    ax2.plot(V[45:60], I[45:60], label="T = {}K".format(s))


                print("At T = {}K, the x interception is {}V.".format(s, V[marker]))

                result.append([s, V[marker]])
                marker = 0

    rx = []
    ry = []

    for i in range(0, len(semi_select)):
        rx.append(result[i][0])
        ry.append(result[i][1])

ax3.plot(rx, ry)
temp = scps.linregress(rx, ry)
R3 = [1, 1]
R3[0]= temp.slope
R3[1] = temp.intercept
tx = np.arange(80, 280, 10)
ty = tx*R3[0] + R3[1]
ax3.plot(tx, ty)
print(R3)



ax1.legend()
ax2.legend()
fig1.show()
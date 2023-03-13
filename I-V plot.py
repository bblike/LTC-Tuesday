import numpy as np
from matplotlib import pyplot as plt
import os

path = r"C:\Users\Li Zhejun\Desktop\LTC-Tuesday\week5"
files = os.listdir(path)
files.sort(key=lambda x:int(x[1:-6]))
s = []
counter = 0
file_length = len(files)
data = []
fig1 = plt.figure(figsize=(8, 6))
wide_select = ["80", "90", "100", "110", "120", "130", "140", "200", "180", "160"]
narrow_select = ["80", "90", "100", "103", "105", "106", "107", "108", "109"]
semi_select = [80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260]
sign = 0
for file in files:
    for s in semi_select:
        if file[1:-6] == "210" or file[1:-6] == "220" or file[1:-6] == "230" or file[1:-6] == "240" or file[1:-6] == "250" or file[1:-6] == "260":
            sign = -1
        else:
            sign = 1

        if file == "T{}V1.dat".format(np.str_(s)):
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
            #I = I * sign
            V = V * sign
            R = R * sign

            print(V)
            """
            print(V)
            print(I)
            print(R)"""
            plt.plot(V[:], I[:], marker="_", label="T = {}K".format(s))

plt.title("relations between voltage and current under different temperature")
plt.xlabel("Voltage/V")
plt.ylabel("Current/A")
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

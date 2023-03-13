import numpy as np
from matplotlib import pyplot as plt
import os

path = r"C:\Users\Li Zhejun\Desktop\LTC-Tuesday\week5"
files = os.listdir(path)
s = []
counter = 0
file_length = len(files)
data = []
fig1 = plt.figure(figsize=(8,6))
file_length = len(files)
files.sort(key=lambda x:int(x[1:-6]))
flag = 1
select = [80,110,140,170,210,240,260]
for file in files:
    for s in select:
        if file == "T{}V1.dat".format(np.str(s)):
            if file[1:-6] == "210" or file[1:-6] == "220" or file[1:-6] == "230" or file[1:-6] == "240" or file[1:-6] == "250" or file[1:-6] == "260":
                flag = -1
            else:
                flag = 1
            f = open("week5./{}".format(file))
            data = f.readlines()
            counter += 1
            print(counter)

            length = len(data)

            T = np.zeros(length)
            V = np.zeros(length)
            I = np.zeros(length)
            R = np.zeros(length - 1)

            for i in range(0, length - 1):
                string = data[i]
                T[i], V[i], I[i], R[i] = string.split(" ")
            V = V * flag
            R = R * flag
            """print(T)
            print(V)
            print(I)
            print(R)"""


            plt.plot(V[60:150], R[60:150], marker="", label = "T = {}K".format(s))


            plt.title("relations between voltage and resistance under different temperature")
            plt.xlabel("voltage/V")
            plt.ylabel("Resistance/R")
            plt.legend()
        data = []

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
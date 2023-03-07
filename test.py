import numpy as np
from matplotlib import pyplot as plt
import os

path = r"C:\Users\Li Zhejun\Desktop\LTC-Tuesday\week5"
files = os.listdir(path)
s = []
counter = 0
file_length = len(files)
data = []
fig1 = plt.figure(figsize=(10,10))
file_length = len(files)
for file in files:
    if file[-6:] == "V1.dat":
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

        """print(T)
        print(V)
        print(I)
        print(R)"""


        plt.plot(V[60:150], R[60:150], marker="", label = "{}".format(counter*10+70))


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

import numpy as np
from matplotlib import pyplot as plt
import os
import scipy.stats as scps

path = r"C:\Users\Li Zhejun\Desktop\LTC-Tuesday\week6-super"
files = os.listdir(path)
files.sort(key=lambda x:int(x[1:-6]))
s = []
counter = 0
file_length = len(files)
data = []

fig1 = plt.figure(figsize=(6,4))
ax1 = fig1.add_axes([0.13, 0.12, 0.8, 0.8])
ax1.set_title("relation between the resistance and current")
ax1.set_xlabel("I/A")
ax1.set_ylabel(r"$R/Ω$")
#ax2 = fig1.add_axes([0.43, 0.7, 0.2, 0.2])


wide_select = ["80", "90", "100", "110", "120", "130", "140", "200", "180", "160"]
narrow_select = [80, 100, 103, 105, 106, 107, 108, 109, 110]
semi_select = [80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260]
super_select = [80,90,100,103,105,106,107,108,109,110,115,120,130,140,150,160,170,180,190,200]
sign = 0
hall_test = []

for l in [3]:
    for file in files:
        for s in narrow_select:
            if file[1:-6] == "210" or file[1:-6] == "220" or file[1:-6] == "230" or file[1:-6] == "240" or file[1:-6] == "250" or file[1:-6] == "260":
                sign = -1
            else:
                sign = 1

            if file == "T{}V{}.dat".format(np.str_(s), l):
                f = open("week6-super./{}".format(file))
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

                #print(V)
                """
                print(V)
                print(I)
                print(R)"""
                ax1.plot(I[1:], R[:],marker = "x", label="T = {}K".format(s))
                #if file[1:-6] == "108" or file[1:-6] == "110":
                #    ax2.plot(I[:], V[:], marker=".", label="T = {}K".format(s))

                # plot the least square fit line
                result = [1, 2, 3, 4]
                temp = scps.linregress(I[1:], R[:])
                result[0] = temp.slope
                result[1] = temp.intercept
                result[2] = temp.stderr
                result[3] = temp.intercept_stderr

                xe = np.arange(0, 0.10, 0.002)
                ye = xe * result[0] + result[1]
                plt.plot(xe, ye)
                print("At T = {}K, the gradient is {}±{}, the inteception is {}±{}".format(s, result[0], result[2], result[1], result[3]))
                hall_test.append([s, result[0], result[1], result[2], result[3]])
    hall_test = np.array(hall_test)

    hallx = []
    hally = []
    hall_slope_error = []
    hall_interc_error = []
    for i in range(0, len(narrow_select)):
        hallx.append(hall_test[i][0])
        hally.append(hall_test[i][2])
        hall_slope_error.append(np.abs(hall_test[i][3]))
        hall_interc_error.append(np.abs(hall_test[i][4]))
    #hallxx = np.array(hallx)
    #hallyy = np.array(hally)

    #print(hallxx)
    #print(hallyy)
    markers = ""
    if l == 1:
        markers = "x"
    if l == 2:
        markers = "o"
    if l == 3:
        markers = "."

    #ax1.errorbar(hallx, hally, marker = markers, yerr = hall_slope_error, capsize = 3, label = "experiment set: {}".format(l))
    hall_test = []
    Rresult = [1, 2, 3, 4]
    temp = scps.linregress(hallx[-8:], hally[-8:])
    Rresult[0] = temp.slope
    Rresult[1] = temp.intercept
    Rresult[2] = temp.stderr
    Rresult[3] = temp.intercept_stderr
    xt = np.arange(140, 300, 10)
    yt = xt * Rresult[0] + Rresult[1]
    yerror = xt * np.abs(Rresult[2]) + np.abs(Rresult[3])
    #ax1.plot(xt, yt)

    #plot interception
    #x = [290, 290]
    #y = [0, yt[-1]]
    #ax1.plot(x,y)
    #print("The resistance at 290K is {}±{}".format(yt[-1], yerror[-1]))

#plt.title("relations between current and resistance under different temperature")
#plt.xlabel("Current/A")
#plt.ylabel("Resisrance/Ω")
ax1.legend()

#calculate the gradient for linear part


"""
hyposysis on test
ax1.plot(hallxx, hallyy)

xt = np.arange(95, 200, 5)
yt = 0.0015 * np.exp(950/xt) / xt**(1.5)
print(xt)
print(yt)
ax1.plot(xt, yt)
"""
fig1.show()

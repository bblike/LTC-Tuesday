import numpy as np
from matplotlib import pyplot as plt
import os
import scipy.stats as scps
path = r"C:\Users\Li Zhejun\Desktop\LTC-Tuesday\week5"
files = os.listdir(path)
s = []
counter = 0
file_length = len(files)
data = []
fig1 = plt.figure()
ax1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8])
ax1.set_ylabel("Temperature/K")
ax1.set_xlabel("voltage/V")
ax1.set_title("T-V plot for silicon at I = 0.05A")
#ax1.set_xlabel("current/A")
#ax1.set_ylabel("band gap energy/eV")
#ax1.set_title("band gap energy relation to current")
use = np.zeros((2000,2))
sign = 0
flag = 0
semi_select = [80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260]
current_test = []
current_choose = [0.05]
for I_choose in current_choose:
    for l in [3]:
        for file in files:
            for s in semi_select:
                if file[-6:] == "V{}.dat".format(l):
                    if file[1:-6] == "210" or file[1:-6] == "220" or file[1:-6] == "230" or file[1:-6] == "240" or file[1:-6] == "250" or file[1:-6] == "260":
                        sign = -1
                    else:
                        sign = 1

                    if file =="T{}V{}.dat".format(np.str_(s), l):
                        f = open("week5./{}".format(file))
                        data = f.readlines()
                        counter += 1
                        print(counter)

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
                            if (I[i] - I_choose) < 0.002 and (I_choose - I[i]) < 0.002:
                                use[flag] += [T[i], V[i]]
                                flag += 1
        print(flag)

        xax = np.zeros(flag)
        yax = np.zeros(flag)

        for i in range(flag):
            xax[i] = use[i][0]
            yax[i] = use[i][1]

        for j in range(flag-1):
            for i in range(flag-1):

                if xax[i] > xax[i+1]:
                    xtemp = xax[i]
                    xax[i] = xax[i+1]
                    xax[i+1] = xtemp
                    ytemp = yax[i]
                    yax[i] = yax[i + 1]
                    yax[i + 1] = ytemp

        print(xax)
        print(yax)
        use = np.zeros((200, 2))
        flag = 0


        ax1.scatter(yax[:], xax[:], marker = "x", label = "I = {}0A".format(I_choose))

        temp = scps.linregress(yax, xax)

        print("The gradient is {}±{} and the y-interception is {}±{}.".format(temp.slope, temp.stderr, temp.intercept, temp.intercept_stderr))
        lsfy = np.arange(80, 270, 10)
        lsfx = (lsfy - temp.intercept)/temp.slope

        ax1.plot(lsfx, lsfy, label = "Least square fit", color = "green")

        e = 1.601 / 10**19
        eg = -(temp.intercept/temp.slope) * e / 1.601 * 10**19
        print(eg)
        egerr = eg * np.sqrt((temp.stderr/temp.slope)**2 + ((temp.intercept_stderr/temp.intercept)**2))
        print(egerr)
        current_test.append([I_choose, eg, egerr])



ix = []
iy = []
iyerr = []
for i in range(len(current_test)):
    ix.append(current_test[i][0])
    iy.append(current_test[i][1])
    iyerr.append(current_test[i][2])



#ax1.errorbar(ix, iy, xerr = 0.001, yerr = iyerr, capsize = 3, label = "experiment value")


temp = scps.linregress(ix, iy)
print(temp)
xt = [0, 0.1]
yt = [temp.intercept, temp.slope * 0.1 + temp.intercept]
#ax1.plot(xt, yt, label = "least square fit")
plt.legend()
plt.show()

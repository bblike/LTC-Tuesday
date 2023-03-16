import numpy as np
import matplotlib.pyplot as pl
def Lagrange(xp,x,j):
    # x, y are lists
    # xp is a specific point to interpolate
    # return L (Lagrange Number)
    L = 1
    for k in range(0,len(x)):
        if x[k] != x[j]:
            L = (xp-x[k])/(x[j]-x[k])
    return L

def LagrInterp(xp,xn,yn):
    # xn, yn are lists
    # xp is a specific point to inteprolate
    # return Interpolated value
    x = '80  90 100 110 120 130 140 150 160 170 180 190 200 210 220 230 240 250 260 270 280 290'
    y = ' 0.08521345  0.04629983  0.02718282  0.01695284  0.01109653  0.00755613 0.00531739  0.00384738  0.00285072  0.00215611  0.00166029  0.00129886 0.00103045  0.00082781 -0.00080693 -0.00103212 -0.00155228 -0.0038378  0.00534603  0.00142065  0.0007719  -0.00093054'
    xn = x.split(" ")
    yn = y.split(" ")
    print(xn)
    p = 0
    for i in range(0,len(xn)):
        p += Lagrange(xp,xn,i) * yn[i]
    return p
    print(p)


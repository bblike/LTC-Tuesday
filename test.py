import numpy as np
from matplotlib import pyplot as plt
x = np.arange(10, 300, 10)
y = 1/x**(1.5)
print(x)
print(y)
plt.figure()
plt.plot(x,y)
plt.show()

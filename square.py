import numpy as np
import matplotlib.pyplot as plt

#Teoricas
A =1
f = 100
DC = 0
T = 1/f
t = np.arange(0, 2 * T, T / 1000)
fase = 0
VT= A * np.sign(np.sin(2*np.pi*f*t+fase)) + DC 

plt.figure
plt.plot(t, VT)
plt.grid(True)
plt.show()

import numpy as np
import matplotlib.pyplot as plt

#Teoricas
A =1
f = 200
DC = 1.5
T = 1/f
t = np.arange(0, 2.2 * T, T / 1000)
fase = 3.8
VT= A * np.sin(2*np.pi*f*t+fase) + DC 

plt.figure
plt.plot(t, VT)
plt.grid(True)
plt.show()

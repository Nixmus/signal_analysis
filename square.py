import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Teoricas
A = 1
f = 100
DC = 0
T = 1/f
t = np.arange(0, 2 * T, T / 1000)
fase = 0
duty = 0.5  # Duty cycle (0 to 1)

# Generate rectangular signal
VT = A * signal.square(2 * np.pi * f * t + fase, duty=duty) + DC


plt.plot(t, VT)
plt.grid(True)
plt.title('Señal Rectangular')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Parámetros
fs = 1000000
t = np.arange(0, 0.0005, 1/fs)

# Señales
m = np.cos(2 * np.pi * 1000 * t)  # 1kHz
m1 = np.cos(5 * np.pi * 5000 * t)  # 5kHz
m2 = np.cos(10 * np.pi * 10000 * t)  # 10kHz
mt = m + m1 + m2

# Definir el filtro pasa baja
def filtro_pasa_baja(corte, fs, num_coeficiente):
    newf = 0.5 * fs
    normal_corte = corte / newf #normaliza la frecuencia de corte
    coeficiente = np.sinc(2 * normal_corte * (np.arange(num_coeficiente) - (num_coeficiente - 1) / 2))#crea un arreglo de ceros y lo centra en 0, ajusta el arreglo a la frecuencia normalizada
    #np.sinc calcula es la base de los filtros FIR 
    #filtros fir respuesta finita al impulso
    window = np.hamming(num_coeficiente)#ventana de hamming
    coeficiente *= window#suaviza el filtro
    coeficiente /= np.sum(coeficiente)#normaliza los coeficientes
    return coeficiente

# Aplicar el filtro
corte = 7500  # Frecuencia de corte
num_coeficiente = 101  # Número de coeficientes del filtro
coeficiente = filtro_pasa_baja(corte, fs, num_coeficiente)
mt_filtrada = np.convolve(mt, coeficiente, mode='same')

# Graficar las señales
fig, axs = plt.subplots(2, 2, figsize=(12, 12))
fig.suptitle('Señales de 1kHz, 5kHz y 10kHz')

axs[0, 0].plot(t, m)
axs[0, 0].set_title('1kHz')
axs[0, 0].set_xlabel('Tiempo')
axs[0, 0].set_ylabel('Amplitud')
axs[0, 0].grid(True)

axs[0, 1].plot(t, m1)
axs[0, 1].set_title('5kHz')
axs[0, 1].set_xlabel('Tiempo')
axs[0, 1].set_ylabel('Amplitud')
axs[0, 1].grid(True)

axs[1, 0].plot(t, m2)
axs[1, 0].set_title('10kHz')
axs[1, 0].set_xlabel('Tiempo')
axs[1, 0].set_ylabel('Amplitud')
axs[1, 0].grid(True)

axs[1, 1].plot(t, mt, label='Original')
axs[1, 1].plot(t, mt_filtrada, label='Filtrada', linestyle='--')
axs[1, 1].set_title('Señal Sumada y Filtrada')
axs[1, 1].set_xlabel('Tiempo')
axs[1, 1].set_ylabel('Amplitud')
axs[1, 1].grid(True)
axs[1, 1].legend()

plt.show()

plt.plot(t, mt, label='Original')
plt.plot(t, mt_filtrada, label='Filtrada')
plt.title('Señal Sumada y Filtrada')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.grid(True)
plt.show()

plt.plot(t, mt, label='Original')
plt.title('Señal Sumada y Filtrada')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.grid(True)
plt.show()

plt.plot(t, mt_filtrada, label='Filtrada')
plt.title('Señal Sumada y Filtrada')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.grid(True)
plt.show()

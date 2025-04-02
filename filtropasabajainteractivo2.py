import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

class FiltroInteractivo:
    def __init__(self, root):
        self.root = root
        self.root.title("Filtro Pasa Bajas Interactivo")
        self.root.geometry("1200x800")
        
        # Parámetros iniciales
        self.fs = 1000000  # Frecuencia de muestreo
        self.t = np.arange(0, 0.004, 1/self.fs)  # Vector de tiempo
        
        # Señales base
        self.m = np.cos(2 * np.pi * 1000 * self.t)    # 1kHz
        self.m1 = np.cos(2 * np.pi * 3000 * self.t)   # 3kHz
        self.m2 = np.cos(2 * np.pi * 5000 * self.t)   # 5kHz
        self.mt = self.m + self.m1 + self.m2          # Señal combinada
        
        # Parámetros iniciales del filtro
        self.corte = 1500      # Frecuencia de corte inicial
        self.num_coef = 201    # Número de coeficientes inicial
        
        # Crear figura de matplotlib con solo 2 subplots
        self.fig, self.axs = plt.subplots(3, 1, figsize=(10, 6))
        self.fig.subplots_adjust(hspace=0.4)
        
        # Crear el canvas de matplotlib
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Frame para los controles
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        # Slider para frecuencia de corte
        ttk.Label(control_frame, text="Frecuencia de corte (Hz):").pack()
        self.corte_var = tk.DoubleVar(value=self.corte)
        self.corte_slider = ttk.Scale(
            control_frame,
            from_=500,
            to=10000,
            orient=tk.HORIZONTAL,
            command=self.actualizar_filtro,
            variable=self.corte_var
        )
        self.corte_slider.pack(fill=tk.X)
        self.corte_label = ttk.Label(control_frame, text=f"Valor: {self.corte} Hz")
        self.corte_label.pack()
        
        # Slider para número de coeficientes
        ttk.Label(control_frame, text="Número de coeficientes:").pack()
        self.coef_var = tk.IntVar(value=self.num_coef)
        self.coef_slider = ttk.Scale(
            control_frame,
            from_=21,
            to=1501,
            orient=tk.HORIZONTAL,
            command=self.actualizar_filtro,
            variable=self.coef_var
        )
        self.coef_slider.pack(fill=tk.X)
        self.coef_label = ttk.Label(control_frame, text=f"Valor: {self.num_coef}")
        self.coef_label.pack()
        
        # Botón para actualizar
        ttk.Button(control_frame, text="Actualizar Gráficos", command=self.actualizar_filtro).pack(pady=5)
        
        # Dibujar gráficos iniciales
        self.actualizar_filtro()
    
    def filtro_pasa_baja(self, corte, fs, num_coeficiente):
        newf = 0.5 * fs
        normal_corte = corte / newf
        coeficiente = np.sinc(2 * normal_corte * (np.arange(num_coeficiente) - (num_coeficiente - 1) / 2))
        window = np.hamming(num_coeficiente)
        coeficiente *= window
        coeficiente /= np.sum(coeficiente)
        return coeficiente
    
    def actualizar_filtro(self, *args):
        # Obtener valores actuales
        self.corte = self.corte_var.get()
        self.num_coef = self.coef_var.get()
        
        # Actualizar etiquetas
        self.corte_label.config(text=f"Valor: {int(self.corte)} Hz")
        self.coef_label.config(text=f"Valor: {self.num_coef}")
        
        # Asegurarse que el número de coeficientes es impar
        if self.num_coef % 2 == 0:
            self.num_coef += 1
            self.coef_var.set(self.num_coef)
        
        # Aplicar el filtro
        coeficiente = self.filtro_pasa_baja(self.corte, self.fs, self.num_coef)
        self.mt_filtrada = np.convolve(self.mt, coeficiente, mode='same')
        
        # Actualizar gráficos
        self.actualizar_graficos()
    
    def actualizar_graficos(self):
        # Limpiar todos los subplots
        for ax in self.axs:
            ax.clear()
        
        # Graficar señal original en el primer subplot
        self.axs[0].plot(self.t, self.mt, label='Original', color='blue')
        self.axs[0].set_title('Señal Original (1kHz + 3kHz + 5kHz)')
        self.axs[0].set_xlabel('Tiempo (s)')
        self.axs[0].set_ylabel('Amplitud')
        self.axs[0].grid(True, linestyle='--', alpha=0.6)
        self.axs[0].legend()
        
        # Graficar señal filtrada en el segundo subplot
        self.axs[1].plot(self.t, self.mt_filtrada, label=f'Filtrada ({int(self.corte)} Hz)', color='red')
        self.axs[1].set_title('Señal Filtrada')
        self.axs[1].set_xlabel('Tiempo (s)')
        self.axs[1].set_ylabel('Amplitud')
        self.axs[1].grid(True, linestyle='--', alpha=0.6)
        self.axs[1].legend()
        
        self.axs[2].plot(self.t, self.mt, label='Original', color='blue')
        self.axs[2].plot(self.t, self.mt_filtrada, label=f'Filtrada ({int(self.corte)} Hz)', color='red')
        self.axs[2].set_title('Señal Filtrada y original')
        self.axs[2].set_xlabel('Tiempo (s)')
        self.axs[2].set_ylabel('Amplitud')
        self.axs[2].grid(True, linestyle='--', alpha=0.6)
        self.axs[2].legend()
        
        # Ajustar diseño y redibujar
        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = FiltroInteractivo(root)
    root.mainloop()

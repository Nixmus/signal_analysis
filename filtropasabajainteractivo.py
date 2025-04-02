import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

class FiltroInteractivo:
    def __init__(self, root):
        self.root = root
        self.root.title("Filtro Pasa Bajas Interactivo")
        self.root.geometry("1000x700")
        
        # Configuración inicial
        self.fs = 1e6  # Frecuencia de muestreo (1MHz)
        self.t = np.arange(0, 0.001, 1/self.fs)
        self.frecuencias = [1000, 3000, 5000]  # 1kHz, 3kHz, 5kHz
        
        # Generar señales
        self.senales = [np.cos(2*np.pi*f*self.t) for f in self.frecuencias]
        self.senal_combinada = sum(self.senales)
        
        # Parámetros del filtro
        self.corte = tk.DoubleVar(value=1500)
        self.num_coef = tk.IntVar(value=201)
        
        # UI Setup
        self.setup_ui()
        self.actualizar_filtro()
    
    def setup_ui(self):
        """Configura la interfaz gráfica"""
        # Figura y gráficos
        self.fig, (self.ax_original, self.ax_filtrada) = plt.subplots(2, 1, figsize=(9, 5))
        self.fig.tight_layout(pad=3.0)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Controles
        frame_controles = ttk.Frame(self.root)
        frame_controles.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        self.crear_slider(frame_controles, "Frecuencia de corte (Hz):", self.corte, 500, 10000)
        self.crear_slider(frame_controles, "Número de coeficientes:", self.num_coef, 21, 401, es_impar=True)
        
        ttk.Button(frame_controles, text="Actualizar", command=self.actualizar_filtro).pack(pady=5)
    
    def crear_slider(self, parent, texto, variable, min_val, max_val, es_impar=False):
        """Crea un slider con etiqueta descriptiva"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(frame, text=texto).pack(side=tk.TOP, anchor=tk.W)
        ttk.Scale(
            frame,
            from_=min_val,
            to=max_val,
            orient=tk.HORIZONTAL,
            command=lambda _: self.actualizar_filtro(es_impar),
            variable=variable
        ).pack(fill=tk.X)
        
        ttk.Label(frame, textvariable=variable).pack(side=tk.TOP)
    
    def filtro_pasa_baja(self, corte, num_coeficiente):
        """Diseña un filtro FIR pasa bajas"""
        normal_corte = corte / (0.5 * self.fs)
        coeficientes = np.sinc(2 * normal_corte * (np.arange(num_coeficiente) - (num_coeficiente-1)/2))
        coeficientes *= np.hamming(num_coeficiente)
        return coeficientes / coeficientes.sum()
    
    def actualizar_filtro(self, forzar_impar=False, *_):
        """Actualiza el filtro y los gráficos"""
        if forzar_impar and self.num_coef.get() % 2 == 0:
            self.num_coef.set(self.num_coef.get() + 1)
        
        # Aplicar filtro
        coef = self.filtro_pasa_baja(self.corte.get(), self.num_coef.get())
        senal_filtrada = np.convolve(self.senal_combinada, coef, mode='same')
        
        # Actualizar gráficos
        self.actualizar_graficos(self.senal_combinada, senal_filtrada)
    
    def actualizar_graficos(self, original, filtrada):
        """Dibuja las señales en los gráficos"""
        for ax in [self.ax_original, self.ax_filtrada]:
            ax.clear()
        
        # Gráfico de la señal original
        self.ax_original.plot(self.t, original, 'b', label='Original')
        self.configurar_ejes(self.ax_original, 'Señal Original (1k + 3k + 5kHz)')
        
        # Gráfico de la señal filtrada
        self.ax_filtrada.plot(self.t, filtrada, 'r', label=f'Filtrada ({int(self.corte.get())}Hz)')
        self.configurar_ejes(self.ax_filtrada, 'Señal Filtrada')
        
        self.canvas.draw()
    
    def configurar_ejes(self, ax, titulo):
        """Configuración común para ambos ejes"""
        ax.set_xlabel('Tiempo (s)')
        ax.set_ylabel('Amplitud')
        ax.set_title(titulo)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()

if __name__ == "__main__":
    root = tk.Tk()
    app = FiltroInteractivo(root)
    root.mainloop()


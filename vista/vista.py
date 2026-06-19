import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

class VistaMonteCarlo:
    """Vista - Interfaz gráfica para el método de Monte Carlo"""
    
    def __init__(self, root_or_controlador):
        # Si se pasa un controlador, crear la ventana
        if isinstance(root_or_controlador, tk.Tk) or isinstance(root_or_controlador, tk.Toplevel):
            self.root = root_or_controlador
            self.controlador = None
        else:
            # Si se pasa el controlador, crear la ventana
            self.root = tk.Tk()
            self.controlador = root_or_controlador
        
        self.font_label = ("Arial", 14)
        self.font_label2 = ("Arial", 12)
        self.font_entry = ("Arial", 13)
        self.font_entry2 = ("Arial", 11)
        # Crear estilo para los botones de funciones matemáticas
        estilo_func = ttk.Style()
        # Nombre del estilo: "BotonFunc.TButton"
        estilo_func.configure("BotonFunc.TButton", font=("Arial", 12))

        self.root.title("Simulación Monte Carlo - Integrales")
        self.root.geometry("1200x800")
        
        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame para integral 1D
        self.frame_1d = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_1d, text="Integral Simple (1D)")
        
        # Frame para integral 2D
        self.frame_2d = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_2d, text="Integral Doble (2D)")
        
        # Crear interfaz 1D
        self._crear_interfaz_1d()
        
        # Crear interfaz 2D
        self._crear_interfaz_2d()
        
        # Inicializar gráficos
        self.fig_1d = None
        self.canvas_1d = None
        self.fig_2d = None
        self.canvas_2d = None
    
    def _crear_interfaz_1d(self):
        """Crea la interfaz para integral 1D"""
        # Frame izquierdo - Entradas
        left_frame = ttk.Frame(self.frame_1d)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        # Título
        ttk.Label(left_frame, text="Integral Simple ∫f(x)dx", 
                font=("Arial", 15, "bold")).pack(pady=10)
        
        # Función
        ttk.Label(left_frame, text="Función f(x):", font=self.font_label).pack(anchor=tk.W, pady=5)
        self.func_1d = ttk.Entry(left_frame, width=30, font=self.font_entry)
        self.func_1d.pack(pady=5, padx=5, fill=tk.X)
        self.func_1d.insert(0, "x**2")
        ttk.Label(left_frame, text="Ejemplo: x**2, math.sin(x), math.exp(x)", 
                font=("Arial", 10)).pack(anchor=tk.W, padx=5)
        
        # Frame para botones de funciones matemáticas
        func_buttons_frame = ttk.Frame(left_frame)
        func_buttons_frame.pack(pady=5, padx=5, fill=tk.X)
        
        # Crear botones de funciones matemáticas
        self._crear_botones_funciones(func_buttons_frame, self.func_1d)
        
        # Límite a
        ttk.Label(left_frame, text="Límite inferior (a):", font=self.font_label).pack(anchor=tk.W, pady=5)
        self.a_1d = ttk.Entry(left_frame, width=30, font=self.font_entry)
        self.a_1d.pack(pady=5, padx=5, fill=tk.X)
        self.a_1d.insert(0, "0")
        
        # Límite b
        ttk.Label(left_frame, text="Límite superior (b):", font=self.font_label).pack(anchor=tk.W, pady=5)
        self.b_1d = ttk.Entry(left_frame, width=30, font=self.font_entry)
        self.b_1d.pack(pady=5, padx=5, fill=tk.X)
        self.b_1d.insert(0, "1")
        
        # Número de puntos
        ttk.Label(left_frame, text="Número de puntos (N):", font=self.font_label).pack(anchor=tk.W, pady=5)
        self.n_1d = ttk.Entry(left_frame, width=30, font=self.font_entry)
        self.n_1d.pack(pady=5, padx=5, fill=tk.X)
        self.n_1d.insert(0, "10000")
        
        # Botón calcular
        self.btn_calcular_1d = ttk.Button(left_frame, text="Calcular", style="BotonFunc.TButton",
                                        command=self._calcular_1d)
        self.btn_calcular_1d.pack(pady=20, padx=5, fill=tk.X)
        
        # Botones de ejemplo
        ttk.Label(left_frame, text="Ejemplos:", font=("Arial", 12, "bold")).pack(pady=(20,5))
        
        self.btn_ej1_1d = ttk.Button(left_frame, text="Ejemplo 1: x² en [0,1]", style="BotonFunc.TButton",
                                command=lambda: self._cargar_ejemplo_1d("x**2", 0, 1, 10000))
        self.btn_ej1_1d.pack(pady=2, padx=5, fill=tk.X)
        
        self.btn_ej2_1d = ttk.Button(left_frame, text="Ejemplo 2: sin(x) en [0,π]", style="BotonFunc.TButton",
                                command=lambda: self._cargar_ejemplo_1d("math.sin(x)", 0, math.pi, 10000))
        self.btn_ej2_1d.pack(pady=2, padx=5, fill=tk.X)
        
        self.btn_ej3_1d = ttk.Button(left_frame, text="Ejemplo 3: eˣ en [0,1]", style="BotonFunc.TButton",
                                command=lambda: self._cargar_ejemplo_1d("math.exp(x)", 0, 1, 10000))
        self.btn_ej3_1d.pack(pady=2, padx=5, fill=tk.X)
        
        # Frame derecho - Gráfico y resultados
        right_frame = ttk.Frame(self.frame_1d)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Área de gráfico
        graph_frame = ttk.LabelFrame(right_frame, text="Gráfico")
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Área de resultados
        result_frame = ttk.LabelFrame(right_frame, text="Resultados")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.texto_resultados_1d = scrolledtext.ScrolledText(result_frame, 
                                                            height=15, 
                                                            wrap=tk.WORD,
                                                            font=("Courier", 12))
        self.texto_resultados_1d.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para el gráfico (se creará cuando se calcule)
        self.graph_container_1d = ttk.Frame(graph_frame)
        self.graph_container_1d.pack(fill=tk.BOTH, expand=True)
    
    def _crear_interfaz_2d(self):
        """Crea la interfaz para integral 2D"""
        # Frame izquierdo - Entradas
        left_frame = ttk.Frame(self.frame_2d)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        # Título
        ttk.Label(left_frame, text="Integral Doble ∬f(x,y)dxdy", 
                font=("Arial", 15, "bold")).pack(pady=7)
        
        # Función
        ttk.Label(left_frame, text="Función f(x,y):", font=self.font_label2).pack(anchor=tk.W, pady=5)
        self.func_2d = ttk.Entry(left_frame, width=30, font=self.font_entry2)
        self.func_2d.pack(pady=5, padx=5, fill=tk.X)
        self.func_2d.insert(0, "x*y")
        ttk.Label(left_frame, text="Ejemplo: x*y, x**2 + y**2", 
                font=("Arial", 11)).pack(anchor=tk.W, padx=5)
        
        # Frame para botones de funciones matemáticas
        func_buttons_frame = ttk.Frame(left_frame)
        func_buttons_frame.pack(pady=5, padx=5, fill=tk.X)
        
        # Crear botones de funciones matemáticas
        self._crear_botones_funciones(func_buttons_frame, self.func_2d)
        
        # Límites X
        ttk.Label(left_frame, text="Intervalo X:", font=("Arial", 13, "bold")).pack(anchor=tk.W, pady=(10,5))
        ttk.Label(left_frame, text="Límite inferior (ax):", font=self.font_label2).pack(anchor=tk.W, pady=2)
        self.ax_2d = ttk.Entry(left_frame, width=30, font=self.font_entry2)
        self.ax_2d.pack(pady=2, padx=5, fill=tk.X)
        self.ax_2d.insert(0, "0")
        
        ttk.Label(left_frame, text="Límite superior (bx):", font=self.font_label2).pack(anchor=tk.W, pady=2)
        self.bx_2d = ttk.Entry(left_frame, width=30, font=self.font_entry2)
        self.bx_2d.pack(pady=2, padx=5, fill=tk.X)
        self.bx_2d.insert(0, "1")
        
        # Límites Y
        ttk.Label(left_frame, text="Intervalo Y:", font=("Arial", 13, "bold")).pack(anchor=tk.W, pady=(10,5))
        ttk.Label(left_frame, text="Límite inferior (cy):", font=self.font_label2).pack(anchor=tk.W, pady=2)
        self.cy_2d = ttk.Entry(left_frame, width=30, font=self.font_entry2)
        self.cy_2d.pack(pady=2, padx=5, fill=tk.X)
        self.cy_2d.insert(0, "0")
        
        ttk.Label(left_frame, text="Límite superior (dy):", font=self.font_label2).pack(anchor=tk.W, pady=2)
        self.dy_2d = ttk.Entry(left_frame, width=30, font=self.font_entry2)
        self.dy_2d.pack(pady=2, padx=5, fill=tk.X)
        self.dy_2d.insert(0, "1")
        
        # Número de puntos
        ttk.Label(left_frame, text="Número de puntos (N):", font=self.font_label).pack(anchor=tk.W, pady=5)
        self.n_2d = ttk.Entry(left_frame, width=30, font=self.font_entry2)
        self.n_2d.pack(pady=5, padx=5, fill=tk.X)
        self.n_2d.insert(0, "10000")
        
        # Botón calcular
        self.btn_calcular_2d = ttk.Button(left_frame, text="Calcular", style="BotonFunc.TButton", 
                                        command=self._calcular_2d)
        self.btn_calcular_2d.pack(pady=2, padx=5, fill=tk.X)
        
        # Botones de ejemplo
        ttk.Label(left_frame, text="Ejemplos:", font=("Arial", 12, "bold")).pack(pady=(5))
        
        self.btn_ej1_2d = ttk.Button(left_frame, text="Ejemplo 1: x*y en [0,1]×[0,1]", style="BotonFunc.TButton",
                                command=lambda: self._cargar_ejemplo_2d("x*y", 0, 1, 0, 1, 10000))
        self.btn_ej1_2d.pack(pady=2, padx=5, fill=tk.X)
        
        self.btn_ej2_2d = ttk.Button(left_frame, text="Ejemplo 2: x²+y² en [0,1]×[0,1]", style="BotonFunc.TButton",
                                command=lambda: self._cargar_ejemplo_2d("x**2 + y**2", 0, 1, 0, 1, 10000))
        self.btn_ej2_2d.pack(pady=2, padx=5, fill=tk.X)
        
        # Frame derecho - Gráfico y resultados
        right_frame = ttk.Frame(self.frame_2d)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Área de gráfico
        graph_frame = ttk.LabelFrame(right_frame, text="Gráfico")
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Área de resultados
        result_frame = ttk.LabelFrame(right_frame, text="Resultados")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.texto_resultados_2d = scrolledtext.ScrolledText(result_frame, 
                                                            height=15, 
                                                            wrap=tk.WORD,
                                                            font=("Courier", 12))
        self.texto_resultados_2d.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para el gráfico (se creará cuando se calcule)
        self.graph_container_2d = ttk.Frame(graph_frame)
        self.graph_container_2d.pack(fill=tk.BOTH, expand=True)
    
    def obtener_valores_1d(self):
        """Obtiene los valores de los campos 1D"""
        return {
            'func': self.func_1d.get(),
            'a': self.a_1d.get(),
            'b': self.b_1d.get(),
            'n': self.n_1d.get()
        }
    
    def obtener_valores_2d(self):
        """Obtiene los valores de los campos 2D"""
        return {
            'func': self.func_2d.get(),
            'ax': self.ax_2d.get(),
            'bx': self.bx_2d.get(),
            'cy': self.cy_2d.get(),
            'dy': self.dy_2d.get(),
            'n': self.n_2d.get()
        }
    
    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        messagebox.showerror("Error", mensaje)
    
    def mostrar_progreso(self, mensaje):
        """Muestra un mensaje de progreso"""
        # Actualizar el área de resultados con el progreso
        texto_widget = self.texto_resultados_1d if self.notebook.index(self.notebook.select()) == 0 else self.texto_resultados_2d
        texto_widget.delete(1.0, tk.END)
        texto_widget.insert(1.0, mensaje)
        self.root.update()
    
    def actualizar_grafico_1d(self, func, a, b, puntos):
        """Actualiza el gráfico 1D"""
        # Limpiar gráfico anterior
        for widget in self.graph_container_1d.winfo_children():
            widget.destroy()
        
        # Crear nuevo gráfico
        self.fig_1d, ax = plt.subplots(figsize=(2, 3))
        
        # Generar puntos para la función
        x_vals = np.linspace(a, b, 200)
        y_vals = []
        for x in x_vals:
            try:
                y = eval(func, {"x": x, "math": math, "np": np, "__builtins__": {}})
                y_vals.append(y)
            except:
                try:
                    y = eval(func, {"x": x, "math": math, "np": np})
                    y_vals.append(y)
                except:
                    y_vals.append(0)
        
        # Graficar función
        ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {func}')
        
        # Graficar puntos aleatorios
        if puntos:
            x_puntos = [p['x'] for p in puntos]
            y_puntos = [p['y'] for p in puntos]
            ax.scatter(x_puntos, y_puntos, color='red', s=20, alpha=0.6, label='Puntos aleatorios')
        
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title(f'Integral de f(x) = {func} en [{a}, {b}]')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Integrar en tkinter
        self.canvas_1d = FigureCanvasTkAgg(self.fig_1d, self.graph_container_1d)
        self.canvas_1d.draw()
        self.canvas_1d.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def actualizar_grafico_2d(self, func, ax_val, bx_val, cy_val, dy_val, puntos):
        """Actualiza el gráfico 2D"""
        # Limpiar gráfico anterior
        for widget in self.graph_container_2d.winfo_children():
            widget.destroy()
        
        # Crear nuevo gráfico
        self.fig_2d = plt.figure(figsize=(4, 4))
        ax = self.fig_2d.add_subplot(111, projection='3d')
        
        # Generar malla para la superficie
        x_vals = np.linspace(ax_val, bx_val, 30)
        y_vals = np.linspace(cy_val, dy_val, 30)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = np.zeros_like(X)
        
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                try:
                    z = eval(func, {"x": X[i,j], "y": Y[i,j], "math": math, "np": np, "__builtins__": {}})
                    Z[i,j] = z
                except:
                    try:
                        z = eval(func, {"x": X[i,j], "y": Y[i,j], "math": math, "np": np})
                        Z[i,j] = z
                    except:
                        Z[i,j] = 0
        
        # Graficar superficie
        ax.plot_surface(X, Y, Z, alpha=0.7, cmap='viridis')
        
        # Graficar puntos aleatorios
        if puntos:
            x_puntos = [p['x'] for p in puntos]
            y_puntos = [p['y'] for p in puntos]
            z_puntos = [p['z'] for p in puntos]
            ax.scatter(x_puntos, y_puntos, z_puntos, color='red', s=20, alpha=0.8)
        
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('f(x,y)')
        ax.set_title(f'Integral de f(x,y) = {func}')
        
        # Integrar en tkinter
        self.canvas_2d = FigureCanvasTkAgg(self.fig_2d, self.graph_container_2d)
        self.canvas_2d.draw()
        self.canvas_2d.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def mostrar_resultados(self, texto):
        """Muestra los resultados en el área de texto"""
        # Determinar qué área de resultados usar según la pestaña activa
        if self.notebook.index(self.notebook.select()) == 0:
            texto_widget = self.texto_resultados_1d
        else:
            texto_widget = self.texto_resultados_2d
        
        texto_widget.delete(1.0, tk.END)
        texto_widget.insert(1.0, texto)
    
    def establecer_controlador(self, controlador):
        """Establece el controlador después de la creación"""
        self.controlador = controlador
    
    def _calcular_1d(self):
        """Método auxiliar para calcular 1D"""
        if self.controlador:
            self.controlador.calcular_1d()
        else:
            self.mostrar_error("Controlador no inicializado")
    
    def _calcular_2d(self):
        """Método auxiliar para calcular 2D"""
        if self.controlador:
            self.controlador.calcular_2d()
        else:
            self.mostrar_error("Controlador no inicializado")
    
    def _cargar_ejemplo_1d(self, func, a, b, n):
        """Método auxiliar para cargar ejemplo 1D"""
        if self.controlador:
            self.controlador.cargar_ejemplo_1d(func, a, b, n)
        else:
            self.mostrar_error("Controlador no inicializado")
    
    def _cargar_ejemplo_2d(self, func, ax, bx, cy, dy, n):
        """Método auxiliar para cargar ejemplo 2D"""
        if self.controlador:
            self.controlador.cargar_ejemplo_2d(func, ax, bx, cy, dy, n)
        else:
            self.mostrar_error("Controlador no inicializado")
    
    def _crear_botones_funciones(self, parent_frame, entry_widget):
        """Crea los botones de funciones matemáticas"""
        # Primera fila: funciones trigonométricas básicas
        row1 = ttk.Frame(parent_frame)
        row1.pack(fill=tk.X, pady=2)
        
        btn_cos = ttk.Button(row1, text="cos", width=8, style="BotonFunc.TButton",
                            command=lambda: self._insertar_funcion(entry_widget, "math.cos("))
        btn_cos.pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        
        btn_sin = ttk.Button(row1, text="sin", width=8, style="BotonFunc.TButton",
                            command=lambda: self._insertar_funcion(entry_widget, "math.sin("))
        btn_sin.pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        
        btn_tan = ttk.Button(row1, text="tan", width=8, style="BotonFunc.TButton",
                            command=lambda: self._insertar_funcion(entry_widget, "math.tan("))
        btn_tan.pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        
        # Segunda fila: funciones trigonométricas inversas
        row2 = ttk.Frame(parent_frame)
        row2.pack(fill=tk.X, pady=2)
        
        btn_arcsin = ttk.Button(row2, text="arcsin", width=8, style="BotonFunc.TButton",
                            command=lambda: self._insertar_funcion(entry_widget, "math.asin("))
        btn_arcsin.pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        
        btn_arccos = ttk.Button(row2, text="arccos", width=8, style="BotonFunc.TButton",
                            command=lambda: self._insertar_funcion(entry_widget, "math.acos("))
        btn_arccos.pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        
        btn_arctan = ttk.Button(row2, text="arctan", width=8, style="BotonFunc.TButton",
                            command=lambda: self._insertar_funcion(entry_widget, "math.atan("))
        btn_arctan.pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        
        # Tercera fila: logaritmos
        row3 = ttk.Frame(parent_frame)
        row3.pack(fill=tk.X, pady=2)
        
        btn_log = ttk.Button(row3, text="log", width=8, style="BotonFunc.TButton",
                            command=lambda: self._insertar_funcion(entry_widget, "math.log10("))
        btn_log.pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        
        btn_ln = ttk.Button(row3, text="ln", width=8, style="BotonFunc.TButton",
                        command=lambda: self._insertar_funcion(entry_widget, "math.log("))
        btn_ln.pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
    
    def _insertar_funcion(self, entry_widget, funcion):
        """Inserta una función matemática en el Entry en la posición del cursor"""
        cursor_pos = entry_widget.index(tk.INSERT)
        texto_actual = entry_widget.get()
        nuevo_texto = texto_actual[:cursor_pos] + funcion + texto_actual[cursor_pos:]
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, nuevo_texto)
        # Mover el cursor después de la función insertada
        nueva_pos = cursor_pos + len(funcion)
        entry_widget.icursor(nueva_pos)
        entry_widget.focus_set()
    
    def ejecutar(self):
        """Inicia la aplicación (ya está ejecutándose si se pasó root)"""
        if self.controlador:
            # Si se creó desde el controlador, iniciar mainloop
            self.root.mainloop()

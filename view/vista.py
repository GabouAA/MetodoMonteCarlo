import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

COLORES = {
    'celeste': '#A8D8EA',
    'celeste_claro': '#D6EFF8',
    'verde': '#B5EAD7',
    'verde_claro': '#D7F5E9',
    'rojo': '#FFB7B2',
    'rojo_claro': '#FFD6D3',
    'blanco': '#FAFAFA',
    'texto': '#2C3E50',
    'texto_claro': '#5D6D7E',
    'borde': '#D5DBDB',
    'boton_calcular': '#7EC8E3',
    'boton_ejemplo': '#98D8C8',
    'boton_func': '#FFB7B2',
    'progreso_bg': '#E8F8F5',
    'progreso_fg': '#48C9B0',
    'panel_bg': '#EFF2F7',
    'toolbar_bg': '#DDE4EC',
    'toggle_on': '#5DADE2',
    'toggle_off': '#BDC3C7',
    'header_panel': '#A8D8EA',
}


class VistaMonteCarlo:
    """Vista - Interfaz gráfica Dashboard para el método de Monte Carlo"""

    def __init__(self, root_or_controlador):
        if isinstance(root_or_controlador, tk.Tk) or isinstance(root_or_controlador, tk.Toplevel):
            self.root = root_or_controlador
            self.controlador = None
        else:
            self.root = tk.Tk()
            self.controlador = root_or_controlador

        self.font_label = ("Segoe UI", 13)
        self.font_label2 = ("Segoe UI", 11)
        self.font_entry = ("Segoe UI", 12)
        self.font_entry2 = ("Segoe UI", 11)
        self.font_titulo = ("Segoe UI", 16, "bold")
        self.font_subtitulo = ("Segoe UI", 12, "bold")
        self.font_resultado = ("Consolas", 11)

        self.root.title("Monte Carlo Dashboard — Integrales")
        self.root.geometry("1450x900")
        self.root.minsize(950, 650)
        self.root.configure(bg=COLORES['celeste_claro'])

        self._configurar_estilos()

        self._panels = {}

        main_frame = tk.Frame(self.root, bg=COLORES['celeste_claro'])
        main_frame.pack(fill=tk.BOTH, expand=True)

        self._crear_barra_estado(main_frame)

        self.notebook = ttk.Notebook(main_frame, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=6, pady=(6, 0))

        self.frame_1d = tk.Frame(self.notebook, bg=COLORES['blanco'])
        self.notebook.add(self.frame_1d, text="  ∫  Integral Simple (1D)  ")

        self.frame_2d = tk.Frame(self.notebook, bg=COLORES['blanco'])
        self.notebook.add(self.frame_2d, text="  ∬  Integral Doble (2D)  ")

        self._crear_interfaz_1d()
        self._crear_interfaz_2d()

        self.fig_1d = None
        self.canvas_1d = None
        self.fig_2d = None
        self.canvas_2d = None

    def _configurar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use('clam')

        estilo.configure('Custom.TNotebook', background=COLORES['celeste_claro'])
        estilo.configure('Custom.TNotebook.Tab',
                         font=("Segoe UI", 12, "bold"),
                         padding=[16, 8],
                         background=COLORES['celeste'],
                         foreground=COLORES['texto'])
        estilo.map('Custom.TNotebook.Tab',
                    background=[('selected', COLORES['blanco'])],
                    foreground=[('selected', COLORES['texto'])])

        estilo.configure("Calcular.TButton",
                         font=("Segoe UI", 13, "bold"),
                         padding=[12, 8],
                         background=COLORES['boton_calcular'],
                         foreground=COLORES['texto'])
        estilo.map("Calcular.TButton",
                    background=[('active', COLORES['celeste'])])

        estilo.configure("Ejemplo.TButton",
                         font=("Segoe UI", 11),
                         padding=[8, 5],
                         background=COLORES['boton_ejemplo'],
                         foreground=COLORES['texto'])
        estilo.map("Ejemplo.TButton",
                    background=[('active', COLORES['verde'])])

        estilo.configure("Func.TButton",
                         font=("Segoe UI", 11),
                         padding=[6, 4],
                         background=COLORES['boton_func'],
                         foreground=COLORES['texto'])
        estilo.map("Func.TButton",
                    background=[('active', COLORES['rojo'])])

        estilo.configure("Green.Horizontal.TProgressbar",
                         troughcolor=COLORES['progreso_bg'],
                         background=COLORES['progreso_fg'],
                         thickness=18)

    # ── Status Bar (bottom) ──────────────────────────────────────────

    def _crear_barra_estado(self, parent):
        self.progreso_frame = tk.Frame(parent, bg=COLORES['verde_claro'],
                                       highlightbackground=COLORES['borde'],
                                       highlightthickness=1, bd=0)
        self.progreso_frame.pack(side=tk.BOTTOM, fill=tk.X)

        inner = tk.Frame(self.progreso_frame, bg=COLORES['verde_claro'])
        inner.pack(fill=tk.X, padx=12, pady=4)

        self.progreso_label = tk.Label(inner,
                                       text="Listo para calcular",
                                       font=("Segoe UI", 10),
                                       bg=COLORES['verde_claro'],
                                       fg=COLORES['texto'])
        self.progreso_label.pack(side=tk.LEFT)

        self.progreso_contador = tk.Label(inner,
                                          text="",
                                          font=("Segoe UI", 10, "bold"),
                                          bg=COLORES['verde_claro'],
                                          fg=COLORES['texto'])
        self.progreso_contador.pack(side=tk.RIGHT)

        self.progreso_bar = ttk.Progressbar(self.progreso_frame,
                                             style="Green.Horizontal.TProgressbar",
                                             mode='determinate',
                                             maximum=100)
        self.progreso_bar.pack(fill=tk.X, padx=12, pady=(0, 4))

    def _set_bg_recursivo(self, widget, color):
        if isinstance(widget, (tk.Frame, tk.Label)):
            widget.configure(bg=color)
        for child in widget.winfo_children():
            self._set_bg_recursivo(child, color)

    def actualizar_progreso(self, actual, total):
        porcentaje = (actual / total) * 100
        self.progreso_bar['value'] = porcentaje
        self.progreso_label.configure(text=f"Generando puntos aleatorios...")
        self.progreso_contador.configure(text=f"Punto {actual:,} / {total:,}")

        if actual >= total:
            self.progreso_label.configure(text="Cálculo completado")
            self._set_bg_recursivo(self.progreso_frame, COLORES['blanco'])
        else:
            self._set_bg_recursivo(self.progreso_frame, COLORES['verde_claro'])

        self.root.update_idletasks()

    def resetear_progreso(self):
        self.progreso_bar['value'] = 0
        self.progreso_label.configure(text="Listo para calcular")
        self.progreso_contador.configure(text="")
        self._set_bg_recursivo(self.progreso_frame, COLORES['verde_claro'])

    # ── Toolbar with toggle buttons ──────────────────────────────────

    def _crear_toolbar(self, parent, dimension):
        toolbar = tk.Frame(parent, bg=COLORES['toolbar_bg'], height=42)
        toolbar.pack(fill=tk.X, side=tk.TOP)
        toolbar.pack_propagate(False)

        btn_left = tk.Button(toolbar, text="◀ Resultados",
                             font=("Segoe UI", 10, "bold"),
                             bg=COLORES['toggle_on'], fg='white',
                             activebackground=COLORES['celeste'],
                             activeforeground='white',
                             relief=tk.FLAT, cursor='hand2', padx=10,
                             command=lambda: self._toggle_panel('left', dimension))
        btn_left.pack(side=tk.LEFT, padx=(8, 4), pady=6)

        btn_right = tk.Button(toolbar, text="Controles ▶",
                              font=("Segoe UI", 10, "bold"),
                              bg=COLORES['toggle_on'], fg='white',
                              activebackground=COLORES['celeste'],
                              activeforeground='white',
                              relief=tk.FLAT, cursor='hand2', padx=10,
                              command=lambda: self._toggle_panel('right', dimension))
        btn_right.pack(side=tk.RIGHT, padx=(4, 8), pady=6)

        formula_label = tk.Label(toolbar, text="",
                                 font=("Cambria Math", 13),
                                 bg=COLORES['toolbar_bg'],
                                 fg=COLORES['texto'])
        formula_label.pack(expand=True, fill=tk.X, padx=10)

        self._panels[f'{dimension}_btn_left'] = btn_left
        self._panels[f'{dimension}_btn_right'] = btn_right

        return formula_label

    def _toggle_panel(self, side, dimension):
        key = f'{dimension}_{side}'
        panel = self._panels[key]
        visible_key = f'{key}_visible'
        btn = self._panels[f'{dimension}_btn_{side}']

        if self._panels.get(visible_key, True):
            panel.grid_remove()
            self._panels[visible_key] = False
            btn.configure(bg=COLORES['toggle_off'])
            if side == 'left':
                btn.configure(text="▶ Resultados")
            else:
                btn.configure(text="◀ Controles")
        else:
            panel.grid()
            self._panels[visible_key] = True
            btn.configure(bg=COLORES['toggle_on'])
            if side == 'left':
                btn.configure(text="◀ Resultados")
            else:
                btn.configure(text="Controles ▶")

    # ── 1D Interface ─────────────────────────────────────────────────

    def _crear_interfaz_1d(self):
        self.formula_label_1d = self._crear_toolbar(self.frame_1d, '1d')

        content = tk.Frame(self.frame_1d, bg=COLORES['blanco'])
        content.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        content.grid_columnconfigure(0, weight=0)
        content.grid_columnconfigure(1, weight=1)
        content.grid_columnconfigure(2, weight=0)
        content.grid_rowconfigure(0, weight=1)

        # ── Left panel: Results ──
        left_panel = tk.Frame(content, bg=COLORES['panel_bg'], width=320,
                              highlightbackground=COLORES['borde'],
                              highlightthickness=1)
        left_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 3))
        left_panel.grid_propagate(False)
        self._panels['1d_left'] = left_panel
        self._panels['1d_left_visible'] = True

        header = tk.Frame(left_panel, bg=COLORES['header_panel'], height=34)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="☰  Resultados",
                 font=("Segoe UI", 11, "bold"),
                 bg=COLORES['header_panel'],
                 fg=COLORES['texto']).pack(side=tk.LEFT, padx=10, pady=5)

        self.texto_resultados_1d = scrolledtext.ScrolledText(
            left_panel, wrap=tk.WORD,
            font=self.font_resultado,
            bg=COLORES['blanco'], fg=COLORES['texto'],
            bd=0, relief=tk.FLAT, padx=10, pady=8)
        self.texto_resultados_1d.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # ── Center panel: Graph ──
        center_panel = tk.Frame(content, bg=COLORES['blanco'],
                                highlightbackground=COLORES['borde'],
                                highlightthickness=1)
        center_panel.grid(row=0, column=1, sticky='nsew', padx=3)

        self.graph_container_1d = tk.Frame(center_panel, bg=COLORES['blanco'])
        self.graph_container_1d.pack(fill=tk.BOTH, expand=True)

        # ── Right panel: Controls ──
        right_panel = tk.Frame(content, bg=COLORES['panel_bg'], width=290,
                               highlightbackground=COLORES['borde'],
                               highlightthickness=1)
        right_panel.grid(row=0, column=2, sticky='nsew', padx=(3, 0))
        right_panel.grid_propagate(False)
        self._panels['1d_right'] = right_panel
        self._panels['1d_right_visible'] = True

        header_r = tk.Frame(right_panel, bg=COLORES['header_panel'], height=34)
        header_r.pack(fill=tk.X)
        header_r.pack_propagate(False)
        tk.Label(header_r, text="⚙  Calculadora",
                 font=("Segoe UI", 11, "bold"),
                 bg=COLORES['header_panel'],
                 fg=COLORES['texto']).pack(side=tk.LEFT, padx=10, pady=5)

        ctrl = tk.Frame(right_panel, bg=COLORES['panel_bg'])
        ctrl.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        titulo_frame = tk.Frame(ctrl, bg=COLORES['blanco'],
                                highlightbackground=COLORES['borde'],
                                highlightthickness=1)
        titulo_frame.pack(fill=tk.X, pady=(4, 6))
        tk.Label(titulo_frame, text="Integral Simple",
                 font=("Segoe UI", 14, "bold"),
                 bg=COLORES['blanco'],
                 fg=COLORES['texto']).pack(pady=(6, 4))

        self._crear_campo(ctrl, "f(x) =", "func_1d", "x**2",
                          "Ej: x**2, math.sin(x), math.exp(x)")

        func_frame = tk.Frame(ctrl, bg=COLORES['panel_bg'])
        func_frame.pack(pady=(0, 4), fill=tk.X)
        self._crear_botones_funciones(func_frame, None, "1d")

        self._crear_campo(ctrl, "Límite inferior (a):", "a_1d", "0")
        self._crear_campo(ctrl, "Límite superior (b):", "b_1d", "1")
        self._crear_campo(ctrl, "Número de puntos (N):", "n_1d", "10000")

        self.btn_calcular_1d = ttk.Button(ctrl, text="Calcular Integral",
                                          style="Calcular.TButton",
                                          command=self._calcular_1d)
        self.btn_calcular_1d.pack(pady=(10, 8), padx=4, fill=tk.X)

        ej_frame = tk.LabelFrame(ctrl, text=" Ejemplos ",
                                  font=self.font_subtitulo,
                                  bg=COLORES['verde_claro'],
                                  fg=COLORES['texto'],
                                  bd=1, relief=tk.GROOVE)
        ej_frame.pack(fill=tk.X, pady=(6, 4))

        self.btn_ej1_1d = ttk.Button(ej_frame, text="x² en [0, 1]",
                                      style="Ejemplo.TButton",
                                      command=lambda: self._cargar_ejemplo_1d("x**2", 0, 1, 10000))
        self.btn_ej1_1d.pack(pady=3, padx=8, fill=tk.X)

        self.btn_ej2_1d = ttk.Button(ej_frame, text="sin(x) en [0, π]",
                                      style="Ejemplo.TButton",
                                      command=lambda: self._cargar_ejemplo_1d("math.sin(x)", 0, math.pi, 10000))
        self.btn_ej2_1d.pack(pady=3, padx=8, fill=tk.X)

        self.btn_ej3_1d = ttk.Button(ej_frame, text="eˣ en [0, 1]",
                                      style="Ejemplo.TButton",
                                      command=lambda: self._cargar_ejemplo_1d("math.exp(x)", 0, 1, 10000))
        self.btn_ej3_1d.pack(pady=(3, 8), padx=8, fill=tk.X)

        self.func_1d.bind('<KeyRelease>', lambda e: self._actualizar_formula_1d())
        self.a_1d.bind('<KeyRelease>', lambda e: self._actualizar_formula_1d())
        self.b_1d.bind('<KeyRelease>', lambda e: self._actualizar_formula_1d())
        self._actualizar_formula_1d()

    # ── 2D Interface ─────────────────────────────────────────────────

    def _crear_interfaz_2d(self):
        self.formula_label_2d = self._crear_toolbar(self.frame_2d, '2d')

        content = tk.Frame(self.frame_2d, bg=COLORES['blanco'])
        content.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        content.grid_columnconfigure(0, weight=0)
        content.grid_columnconfigure(1, weight=1)
        content.grid_columnconfigure(2, weight=0)
        content.grid_rowconfigure(0, weight=1)

        # ── Left panel: Results ──
        left_panel = tk.Frame(content, bg=COLORES['panel_bg'], width=320,
                              highlightbackground=COLORES['borde'],
                              highlightthickness=1)
        left_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 3))
        left_panel.grid_propagate(False)
        self._panels['2d_left'] = left_panel
        self._panels['2d_left_visible'] = True

        header = tk.Frame(left_panel, bg=COLORES['header_panel'], height=34)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="☰  Resultados",
                 font=("Segoe UI", 11, "bold"),
                 bg=COLORES['header_panel'],
                 fg=COLORES['texto']).pack(side=tk.LEFT, padx=10, pady=5)

        self.texto_resultados_2d = scrolledtext.ScrolledText(
            left_panel, wrap=tk.WORD,
            font=self.font_resultado,
            bg=COLORES['blanco'], fg=COLORES['texto'],
            bd=0, relief=tk.FLAT, padx=10, pady=8)
        self.texto_resultados_2d.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # ── Center panel: Graph ──
        center_panel = tk.Frame(content, bg=COLORES['blanco'],
                                highlightbackground=COLORES['borde'],
                                highlightthickness=1)
        center_panel.grid(row=0, column=1, sticky='nsew', padx=3)

        self.graph_container_2d = tk.Frame(center_panel, bg=COLORES['blanco'])
        self.graph_container_2d.pack(fill=tk.BOTH, expand=True)

        # ── Right panel: Controls ──
        right_panel = tk.Frame(content, bg=COLORES['panel_bg'], width=290,
                               highlightbackground=COLORES['borde'],
                               highlightthickness=1)
        right_panel.grid(row=0, column=2, sticky='nsew', padx=(3, 0))
        right_panel.grid_propagate(False)
        self._panels['2d_right'] = right_panel
        self._panels['2d_right_visible'] = True

        header_r = tk.Frame(right_panel, bg=COLORES['header_panel'], height=34)
        header_r.pack(fill=tk.X)
        header_r.pack_propagate(False)
        tk.Label(header_r, text="⚙  Calculadora",
                 font=("Segoe UI", 11, "bold"),
                 bg=COLORES['header_panel'],
                 fg=COLORES['texto']).pack(side=tk.LEFT, padx=10, pady=5)

        ctrl = tk.Frame(right_panel, bg=COLORES['panel_bg'])
        ctrl.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        titulo_frame = tk.Frame(ctrl, bg=COLORES['blanco'],
                                highlightbackground=COLORES['borde'],
                                highlightthickness=1)
        titulo_frame.pack(fill=tk.X, pady=(4, 6))
        tk.Label(titulo_frame, text="Integral Doble",
                 font=("Segoe UI", 14, "bold"),
                 bg=COLORES['blanco'],
                 fg=COLORES['texto']).pack(pady=(6, 4))

        self._crear_campo(ctrl, "f(x,y) =", "func_2d", "x*y",
                          "Ej: x*y, x**2 + y**2")

        func_frame = tk.Frame(ctrl, bg=COLORES['panel_bg'])
        func_frame.pack(pady=(0, 4), fill=tk.X)
        self._crear_botones_funciones(func_frame, None, "2d")

        tk.Label(ctrl, text="Intervalo X",
                 font=self.font_subtitulo,
                 bg=COLORES['panel_bg'],
                 fg=COLORES['texto']).pack(anchor=tk.W, pady=(4, 1))
        self._crear_campo(ctrl, "Límite inferior (ax):", "ax_2d", "0")
        self._crear_campo(ctrl, "Límite superior (bx):", "bx_2d", "1")

        tk.Label(ctrl, text="Intervalo Y",
                 font=self.font_subtitulo,
                 bg=COLORES['panel_bg'],
                 fg=COLORES['texto']).pack(anchor=tk.W, pady=(4, 1))
        self._crear_campo(ctrl, "Límite inferior (cy):", "cy_2d", "0")
        self._crear_campo(ctrl, "Límite superior (dy):", "dy_2d", "1")

        self._crear_campo(ctrl, "Número de puntos (N):", "n_2d", "10000")

        self.btn_calcular_2d = ttk.Button(ctrl, text="Calcular Integral",
                                          style="Calcular.TButton",
                                          command=self._calcular_2d)
        self.btn_calcular_2d.pack(pady=(8, 6), padx=4, fill=tk.X)

        ej_frame = tk.LabelFrame(ctrl, text=" Ejemplos ",
                                  font=self.font_subtitulo,
                                  bg=COLORES['verde_claro'],
                                  fg=COLORES['texto'],
                                  bd=1, relief=tk.GROOVE)
        ej_frame.pack(fill=tk.X, pady=(6, 4))

        self.btn_ej1_2d = ttk.Button(ej_frame, text="x·y en [0,1]×[0,1]",
                                      style="Ejemplo.TButton",
                                      command=lambda: self._cargar_ejemplo_2d("x*y", 0, 1, 0, 1, 10000))
        self.btn_ej1_2d.pack(pady=3, padx=8, fill=tk.X)

        self.btn_ej2_2d = ttk.Button(ej_frame, text="x²+y² en [0,1]×[0,1]",
                                      style="Ejemplo.TButton",
                                      command=lambda: self._cargar_ejemplo_2d("x**2 + y**2", 0, 1, 0, 1, 10000))
        self.btn_ej2_2d.pack(pady=(3, 8), padx=8, fill=tk.X)

        self.func_2d.bind('<KeyRelease>', lambda e: self._actualizar_formula_2d())
        self.ax_2d.bind('<KeyRelease>', lambda e: self._actualizar_formula_2d())
        self.bx_2d.bind('<KeyRelease>', lambda e: self._actualizar_formula_2d())
        self.cy_2d.bind('<KeyRelease>', lambda e: self._actualizar_formula_2d())
        self.dy_2d.bind('<KeyRelease>', lambda e: self._actualizar_formula_2d())
        self._actualizar_formula_2d()

    # ── Shared field creator ─────────────────────────────────────────

    def _crear_campo(self, parent, label_text, attr_name, default="", hint=None):
        try:
            bg = parent.cget('bg')
        except Exception:
            bg = COLORES['blanco']

        tk.Label(parent, text=label_text, font=self.font_label2,
                 bg=bg, fg=COLORES['texto'],
                 anchor=tk.W).pack(anchor=tk.W, pady=(4, 1))

        entry = tk.Entry(parent, width=28, font=self.font_entry2,
                         bg=COLORES['blanco'],
                         fg=COLORES['texto'],
                         relief=tk.FLAT,
                         highlightbackground=COLORES['borde'],
                         highlightthickness=1,
                         highlightcolor=COLORES['boton_calcular'],
                         insertbackground=COLORES['texto'])
        entry.pack(pady=(0, 1), padx=4, fill=tk.X, ipady=3)
        entry.insert(0, default)
        setattr(self, attr_name, entry)

        if hint:
            tk.Label(parent, text=hint, font=("Segoe UI", 8),
                     bg=bg, fg=COLORES['texto_claro'],
                     anchor=tk.W).pack(anchor=tk.W, padx=4)

    # ── Formula display ──────────────────────────────────────────────

    def _formato_funcion(self, func_str):
        f = func_str
        f = f.replace("math.sin", "sin")
        f = f.replace("math.cos", "cos")
        f = f.replace("math.tan", "tan")
        f = f.replace("math.asin", "arcsin")
        f = f.replace("math.acos", "arccos")
        f = f.replace("math.atan", "arctan")
        f = f.replace("math.exp", "exp")
        f = f.replace("math.log10", "log₁₀")
        f = f.replace("math.log", "ln")
        f = f.replace("math.pi", "π")
        f = f.replace("math.e", "e")
        f = f.replace("math.sqrt", "√")
        f = f.replace("np.sin", "sin")
        f = f.replace("np.cos", "cos")
        f = f.replace("np.exp", "exp")
        f = f.replace("np.log", "ln")
        f = f.replace("np.sqrt", "√")
        f = f.replace("**2", "²")
        f = f.replace("**3", "³")
        f = f.replace("**4", "⁴")
        f = f.replace("**", "^")
        f = f.replace("*", "·")
        return f

    def _actualizar_formula_1d(self):
        try:
            func = self.func_1d.get() or "f(x)"
            a = self.a_1d.get() or "a"
            b = self.b_1d.get() or "b"
            func_fmt = self._formato_funcion(func)
            formula = f"∫ [{a}, {b}]  {func_fmt}  dx"
            self.formula_label_1d.configure(text=formula)
        except Exception:
            pass

    def _actualizar_formula_2d(self):
        try:
            func = self.func_2d.get() or "f(x,y)"
            ax = self.ax_2d.get() or "a"
            bx = self.bx_2d.get() or "b"
            cy = self.cy_2d.get() or "c"
            dy = self.dy_2d.get() or "d"
            func_fmt = self._formato_funcion(func)
            formula = f"∬ [{ax},{bx}]×[{cy},{dy}]  {func_fmt}  dx dy"
            self.formula_label_2d.configure(text=formula)
        except Exception:
            pass

    # ── View interface methods (unchanged signatures) ────────────────

    def obtener_valores_1d(self):
        return {
            'func': self.func_1d.get(),
            'a': self.a_1d.get(),
            'b': self.b_1d.get(),
            'n': self.n_1d.get()
        }

    def obtener_valores_2d(self):
        return {
            'func': self.func_2d.get(),
            'ax': self.ax_2d.get(),
            'bx': self.bx_2d.get(),
            'cy': self.cy_2d.get(),
            'dy': self.dy_2d.get(),
            'n': self.n_2d.get()
        }

    def mostrar_error(self, mensaje):
        messagebox.showerror("Error", mensaje)

    def mostrar_progreso(self, mensaje):
        texto_widget = self.texto_resultados_1d if self.notebook.index(self.notebook.select()) == 0 else self.texto_resultados_2d
        texto_widget.delete(1.0, tk.END)
        texto_widget.insert(1.0, mensaje)
        self.root.update()

    def actualizar_grafico_1d(self, func, a, b, puntos):
        for widget in self.graph_container_1d.winfo_children():
            widget.destroy()

        self.fig_1d, ax = plt.subplots(figsize=(2, 3))
        self.fig_1d.patch.set_facecolor('#FAFAFA')
        ax.set_facecolor('#FAFAFA')

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

        func_fmt = self._formato_funcion(func)
        ax.plot(x_vals, y_vals, color='#2E86AB', linewidth=2.5, label=f'f(x) = {func_fmt}')

        if puntos:
            x_puntos = [p['x'] for p in puntos]
            y_puntos = [p['y'] for p in puntos]
            ax.scatter(x_puntos, y_puntos, color='#FF1744', s=25, alpha=0.7,
                       edgecolors='#B71C1C', linewidths=0.5,
                       label='Puntos aleatorios', zorder=3)

        ax.fill_between(x_vals, y_vals, alpha=0.15, color=COLORES['celeste'])
        ax.set_xlabel('x', fontsize=11)
        ax.set_ylabel('f(x)', fontsize=11)
        ax.set_title(f'f(x) = {func_fmt} en [{a}, {b}]', fontsize=12, fontweight='bold', color=COLORES['texto'])
        ax.grid(True, alpha=0.2, linestyle='--')
        ax.legend(fontsize=9)

        self.canvas_1d = FigureCanvasTkAgg(self.fig_1d, self.graph_container_1d)
        self.canvas_1d.draw()
        self.canvas_1d.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas_1d, self.graph_container_1d)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    def actualizar_grafico_2d(self, func, ax_val, bx_val, cy_val, dy_val, puntos):
        for widget in self.graph_container_2d.winfo_children():
            widget.destroy()

        self.fig_2d = plt.figure(figsize=(4, 4))
        self.fig_2d.patch.set_facecolor('#FAFAFA')
        ax = self.fig_2d.add_subplot(111, projection='3d')
        ax.set_facecolor('#FAFAFA')

        x_vals = np.linspace(ax_val, bx_val, 30)
        y_vals = np.linspace(cy_val, dy_val, 30)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = np.zeros_like(X)

        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                try:
                    z = eval(func, {"x": X[i, j], "y": Y[i, j], "math": math, "np": np, "__builtins__": {}})
                    Z[i, j] = z
                except:
                    try:
                        z = eval(func, {"x": X[i, j], "y": Y[i, j], "math": math, "np": np})
                        Z[i, j] = z
                    except:
                        Z[i, j] = 0

        ax.plot_surface(X, Y, Z, alpha=0.7, cmap='cool')

        if puntos:
            x_puntos = [p['x'] for p in puntos]
            y_puntos = [p['y'] for p in puntos]
            z_puntos = [p['z'] for p in puntos]
            ax.scatter(x_puntos, y_puntos, z_puntos, color='#FF1744', s=25, alpha=0.7,
                       edgecolors='#B71C1C', linewidths=0.5)

        ax.set_xlabel('x', fontsize=10)
        ax.set_ylabel('y', fontsize=10)
        ax.set_zlabel('f(x,y)', fontsize=10)
        func_fmt = self._formato_funcion(func)
        ax.set_title(f'f(x,y) = {func_fmt}', fontsize=12, fontweight='bold', color=COLORES['texto'])

        self.canvas_2d = FigureCanvasTkAgg(self.fig_2d, self.graph_container_2d)
        self.canvas_2d.draw()
        self.canvas_2d.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas_2d, self.graph_container_2d)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    def mostrar_resultados(self, texto):
        if self.notebook.index(self.notebook.select()) == 0:
            texto_widget = self.texto_resultados_1d
        else:
            texto_widget = self.texto_resultados_2d

        texto_widget.delete(1.0, tk.END)
        texto_widget.insert(1.0, texto)
        self._aplicar_formato_resultados(texto_widget)

    def _aplicar_formato_resultados(self, widget):
        widget.tag_configure("titulo", foreground="#2E86AB", font=("Segoe UI", 12, "bold"))
        widget.tag_configure("seccion", foreground="#27AE60", font=("Segoe UI", 11, "bold"))
        widget.tag_configure("resultado", foreground="#E74C3C", font=("Consolas", 12, "bold"))
        widget.tag_configure("valor", foreground="#8E44AD", font=("Consolas", 11))

        contenido = widget.get("1.0", tk.END)
        for i, linea in enumerate(contenido.split('\n'), 1):
            line_start = f"{i}.0"
            line_end = f"{i}.end"
            if '=' * 10 in linea or 'MÉTODO DE MONTE CARLO' in linea:
                widget.tag_add("titulo", line_start, line_end)
            elif linea.strip().startswith(('≈', '∫', '∬')):
                widget.tag_add("resultado", line_start, line_end)
            elif any(s in linea for s in ['INFORMACIÓN', 'RESULTADO', 'COMPARACIÓN', 'PUNTOS', 'EXPLICACIÓN']):
                widget.tag_add("seccion", line_start, line_end)
            elif 'Valor exacto:' in linea or 'Error' in linea:
                widget.tag_add("valor", line_start, line_end)

    def establecer_controlador(self, controlador):
        self.controlador = controlador

    def _calcular_1d(self):
        if self.controlador:
            self.controlador.calcular_1d()
        else:
            self.mostrar_error("Controlador no inicializado")

    def _calcular_2d(self):
        if self.controlador:
            self.controlador.calcular_2d()
        else:
            self.mostrar_error("Controlador no inicializado")

    def _cargar_ejemplo_1d(self, func, a, b, n):
        if self.controlador:
            self.controlador.cargar_ejemplo_1d(func, a, b, n)
            self._actualizar_formula_1d()
        else:
            self.mostrar_error("Controlador no inicializado")

    def _cargar_ejemplo_2d(self, func, ax, bx, cy, dy, n):
        if self.controlador:
            self.controlador.cargar_ejemplo_2d(func, ax, bx, cy, dy, n)
            self._actualizar_formula_2d()
        else:
            self.mostrar_error("Controlador no inicializado")

    def _crear_botones_funciones(self, parent_frame, entry_widget_unused, dimension):
        entry_attr = "func_1d" if dimension == "1d" else "func_2d"

        try:
            bg = parent_frame.cget('bg')
        except Exception:
            bg = COLORES['blanco']

        row1 = tk.Frame(parent_frame, bg=bg)
        row1.pack(fill=tk.X, pady=2)
        for text, func_str in [("cos", "math.cos("), ("sin", "math.sin("), ("tan", "math.tan(")]:
            btn = ttk.Button(row1, text=text, width=7, style="Func.TButton",
                             command=lambda f=func_str, a=entry_attr: self._insertar_funcion(getattr(self, a), f))
            btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

        row2 = tk.Frame(parent_frame, bg=bg)
        row2.pack(fill=tk.X, pady=2)
        for text, func_str in [("arcsin", "math.asin("), ("arccos", "math.acos("), ("arctan", "math.atan(")]:
            btn = ttk.Button(row2, text=text, width=7, style="Func.TButton",
                             command=lambda f=func_str, a=entry_attr: self._insertar_funcion(getattr(self, a), f))
            btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

        row3 = tk.Frame(parent_frame, bg=bg)
        row3.pack(fill=tk.X, pady=2)
        for text, func_str in [("log", "math.log10("), ("ln", "math.log("), ("exp", "math.exp(")]:
            btn = ttk.Button(row3, text=text, width=7, style="Func.TButton",
                             command=lambda f=func_str, a=entry_attr: self._insertar_funcion(getattr(self, a), f))
            btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

    def _insertar_funcion(self, entry_widget, funcion):
        cursor_pos = entry_widget.index(tk.INSERT)
        texto_actual = entry_widget.get()
        nuevo_texto = texto_actual[:cursor_pos] + funcion + texto_actual[cursor_pos:]
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, nuevo_texto)
        nueva_pos = cursor_pos + len(funcion)
        entry_widget.icursor(nueva_pos)
        entry_widget.focus_set()
        if entry_widget == self.func_1d:
            self._actualizar_formula_1d()
        elif entry_widget == self.func_2d:
            self._actualizar_formula_2d()

    def ejecutar(self):
        if self.controlador:
            self.root.mainloop()

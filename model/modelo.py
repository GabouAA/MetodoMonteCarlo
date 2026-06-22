import random
import math
import numpy as np
import sympy as sp
from typing import Tuple, List, Dict, Callable, Optional

class MonteCarloCalculator:
    """Modelo - Lógica de cálculo Monte Carlo"""

    @staticmethod
    def calcular_integral_1d(func_str: str, a: float, b: float, n: int,
                              progreso_callback: Optional[Callable] = None) -> Tuple[float, List[Dict]]:
        """Calcula integral simple usando Monte Carlo"""
        suma = 0
        puntos = []
        paso_progreso = max(1, n // 200)

        for i in range(n):
            x = random.uniform(a, b)
            try:
                y = eval(func_str, {"x": x, "math": math, "np": np, "__builtins__": {}})
            except:
                try:
                    y = eval(func_str, {"x": x, "math": math, "np": np})
                except:
                    y = 0
            suma += y

            if i < n:
                puntos.append({"x": x, "y": y})

            if progreso_callback and (i + 1) % paso_progreso == 0:
                progreso_callback(i + 1, n)

        if progreso_callback:
            progreso_callback(n, n)

        integral = (b - a) * suma / n
        return integral, puntos

    @staticmethod
    def calcular_integral_2d(func_str: str, a: float, b: float, c: float, d: float, n: int,
                              progreso_callback: Optional[Callable] = None) -> Tuple[float, List[Dict]]:
        """Calcula integral doble usando Monte Carlo"""
        suma = 0
        puntos = []
        paso_progreso = max(1, n // 200)

        for i in range(n):
            x = random.uniform(a, b)
            y = random.uniform(c, d)
            try:
                z = eval(func_str, {"x": x, "y": y, "math": math, "np": np, "__builtins__": {}})
            except:
                try:
                    z = eval(func_str, {"x": x, "y": y, "math": math, "np": np})
                except:
                    z = 0
            suma += z

            if i < n:
                puntos.append({"x": x, "y": y, "z": z})

            if progreso_callback and (i + 1) % paso_progreso == 0:
                progreso_callback(i + 1, n)

        if progreso_callback:
            progreso_callback(n, n)

        area = (b - a) * (d - c)
        integral = area * suma / n
        return integral, puntos

    @staticmethod
    def generar_puntos_funcion(func_str: str, a: float, b: float, num_puntos: int = 100) -> Tuple[List[float], List[float]]:
        """Genera puntos para graficar la función"""
        x_vals = np.linspace(a, b, num_puntos).tolist()
        y_vals = []

        for x in x_vals:
            try:
                y = eval(func_str, {"x": x, "math": math, "np": np, "__builtins__": {}})
                y_vals.append(y)
            except:
                y_vals.append(0)

        return x_vals, y_vals

    @staticmethod
    def calcular_valor_exacto_1d(func_str: str, a: float, b: float) -> float:
        """Calcula valor exacto para funciones conocidas"""
        try:
            x = sp.Symbol('x')

            reemplazos = {
                "math.sin": "sin",
                "math.cos": "cos",
                "math.tan": "tan",
                "math.asin": "asin",
                "math.acos": "acos",
                "math.atan": "atan",
                "math.exp": "exp",
                "math.log": "ln",
                "math.log10": "(log(x)/log(10))",
                "math.pi": "pi",
                "math.e": "E"
            }

            for k, v in reemplazos.items():
                func_str = func_str.replace(k, v)

            func = sp.sympify(func_str)
            resultado = sp.integrate(func, (x, a, b))
            resultado_simplificado = sp.simplify(resultado)

            return float(resultado_simplificado.evalf())

        except:
            return None

    @staticmethod
    def calcular_valor_exacto_2d(func_str: str, a: float, b: float, c: float, d: float) -> float:
        """Calcula valor exacto para integrales dobles usando SymPy"""
        try:
            x = sp.Symbol('x')
            y = sp.Symbol('y')

            reemplazos = {
                "math.sin": "sin",
                "math.cos": "cos",
                "math.tan": "tan",
                "math.asin": "asin",
                "math.acos": "acos",
                "math.atan": "atan",
                "math.exp": "exp",
                "math.log": "ln",
                "math.log10": "(log(x)/log(10))",
                "math.pi": "pi",
                "math.e": "E"
            }

            for k, v in reemplazos.items():
                func_str = func_str.replace(k, v)

            func = sp.sympify(func_str)
            resultado = sp.integrate(func, (x, a, b), (y, c, d))
            resultado_simplificado = sp.simplify(resultado)

            return float(resultado_simplificado.evalf())

        except:
            return None

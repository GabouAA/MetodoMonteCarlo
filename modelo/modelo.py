import random
import math
import numpy as np
import sympy as sp
from typing import Tuple, List, Dict

class MonteCarloCalculator:
    """Modelo - Lógica de cálculo Monte Carlo"""
    
    @staticmethod
    def calcular_integral_1d(func_str: str, a: float, b: float, n: int) -> Tuple[float, List[Dict]]:
        """Calcula integral simple usando Monte Carlo"""
        suma = 0
        puntos = []
        
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
        
        integral = (b - a) * suma / n
        return integral, puntos
    
    @staticmethod
    def calcular_integral_2d(func_str: str, a: float, b: float, c: float, d: float, n: int) -> Tuple[float, List[Dict]]:
        """Calcula integral doble usando Monte Carlo"""
        suma = 0
        puntos = []
        
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
            # Definimos variable simbólica
            x = sp.Symbol('x')

            # Reemplazamos prefijos 'math.' por versiones de SymPy
            reemplazos = {
                # Trigonométricas básicas
                "math.sin": "sin",
                "math.cos": "cos",
                "math.tan": "tan",
                # Trigonométricas inversas
                "math.asin": "asin",
                "math.acos": "acos",
                "math.atan": "atan",
                # Exponencial y logarítmica
                "math.exp": "exp",
                "math.log": "ln",  # logaritmo natural
                "math.log10": "(log(x)/log(10))", # logaritmo base 10 (clásico)
                # Constantes
                "math.pi": "pi",
                "math.e": "E"
            }

            for k, v in reemplazos.items():
                func_str = func_str.replace(k, v)

            # Convertimos a expresión simbólica
            func = sp.sympify(func_str)

            # Integramos analíticamente
            resultado = sp.integrate(func, (x, a, b))

            # Simplificamos
            resultado_simplificado = sp.simplify(resultado)

            return float(resultado_simplificado.evalf())

        except:
            return None
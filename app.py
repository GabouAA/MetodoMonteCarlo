# app.py
import tkinter as tk
import sys
import os
# Agregar el directorio actual al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from controlador.controller import Controlador
from modelo.modelo import MonteCarloCalculator     
from vista.vista import VistaMonteCarlo    

class MonteCarloApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulación Monte Carlo")
        self.root.geometry("800x600")
        
        # Inicializar MVC
        self.modelo = MonteCarloCalculator()
        self.vista = VistaMonteCarlo(self.root)
        self.controlador = Controlador(self.modelo, self.vista)
        # Conectar el controlador a la vista
        self.vista.establecer_controlador(self.controlador)
        
    def ejecutar(self):
        self.controlador.ejecutar()
        self.root.mainloop()

if __name__ == "__main__":
    app = MonteCarloApp()
    app.ejecutar()
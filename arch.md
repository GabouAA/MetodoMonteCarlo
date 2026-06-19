# arch.md - Arquitectura y Funcionamiento del Software

## Descripción General

Este software implementa el **Método de Monte Carlo** para calcular integrales definidas de forma numérica. En lugar de usar métodos analíticos exactos, estima el valor de la integral usando muestreo aleatorio dentro del intervalo de integración.

## Cómo Funciona el Método de Monte Carlo

### Concepto Básico

La integral definida `∫f(x)dx` de `a` a `b` representa el área bajo la curva de `f(x)` entre los puntos `a` y `b`.

El método de Monte Carlo estima esta área de la siguiente manera:

1. **Generar puntos aleatorios**: Se generan `N` valores `x` aleatorios dentro del intervalo `[a, b]`
2. **Evaluar la función**: Para cada punto `x`, se calcula `f(x)`
3. **Calcular el promedio**: Se obtiene el promedio de todos los valores `f(x)`
4. **Estimar el área**: Se multiplica el promedio por el ancho del intervalo `(b - a)`

**Fórmula:**
```
∫f(x)dx ≈ (b - a) × (1/N) × Σf(xᵢ)
```

---

## Ejemplo Práctico: f(x) = x³ + 2

Supongamos que queremos calcular:
```
∫₁³ (x³ + 2) dx
```

Con los parámetros:
- **Función**: `x**3 + 2`
- **Límite inferior (a)**: 1
- **Límite superior (b)**: 3
- **Número de puntos (N)**: 10,000

### Pasos de Ejecución

#### Paso 1: Generar 10,000 puntos aleatorios
Se generan valores `x` uniformemente distribuidos entre 1 y 3:
```
x₁ = 1.234, x₂ = 2.567, x₃ = 1.891, ..., x₁₀₀₀₀ = 2.456
```

#### Paso 2: Evaluar f(x) en cada punto
Para cada punto `xᵢ`, se calcula `f(xᵢ) = xᵢ³ + 2`:
```
f(x₁) = (1.234)³ + 2 = 1.877 + 2 = 3.877
f(x₂) = (2.567)³ + 2 = 16.885 + 2 = 18.885
f(x₃) = (1.891)³ + 2 = 6.755 + 2 = 8.755
...
f(x₁₀₀₀₀) = (2.456)³ + 2 = 14.819 + 2 = 16.819
```

#### Paso 3: Calcular el promedio
```
Promedio = (1/10000) × (3.877 + 18.885 + 8.755 + ... + 16.819)
Promedio ≈ 12.500  (valor aproximado)
```

#### Paso 4: Multiplicar por el ancho del intervalo
```
Ancho = b - a = 3 - 1 = 2

∫₁³ (x³ + 2) dx ≈ 2 × 12.500 = 25.000
```

### Valor Exacto (SymPy)

El software también calcula el valor exacto usando SymPy:
```
∫₁³ (x³ + 2) dx = [x⁴/4 + 2x]₁³
                = (81/4 + 6) - (1/4 + 2)
                = (20.25 + 6) - (0.25 + 2)
                = 26.25 - 2.25
                = 24.00
```

### Comparación de Resultados
- **Valor aproximado (Monte Carlo)**: 25.000
- **Valor exacto (Simbólico)**: 24.000
- **Error absoluto**: |25.000 - 24.000| = 1.000
- **Error relativo**: (1.000 / 24.000) × 100 = 4.17%

---

## Estructura del Proyecto

```
MonteCarlo/
│
├── main.py                 # Punto de entrada de la aplicación
├── app.py                  # Inicialización de la aplicación (MVC)
├── CLAUDE.md              # Documentación para Claude Code
├── arch.md                # Este archivo
├── dependencias.txt       # Lista de dependencias
│
├── modelo/                # Capa de lógica de negocios
│   ├── __init__.py
│   └── modelo.py          # MonteCarloCalculator (cálculos numéricos)
│
├── vista/                 # Capa de presentación (GUI)
│   ├── __init__.py
│   └── vista.py           # VistaMonteCarlo (interfaz Tkinter)
│
└── controlador/           # Capa de control
    ├── __init__.py
    └── controller.py      # ControladorMonteCarlo (coordinación)
```

---

## Arquitectura MVC (Modelo-Vista-Controlador)

### 1. **Modelo** (`modelo/modelo.py`)
**Responsabilidad**: Lógica pura de cálculo matemático

**Clase Principal**: `MonteCarloCalculator`

**Métodos:**
- `calcular_integral_1d(func_str, a, b, n)`: Calcula integral simple usando Monte Carlo
  - Genera `n` puntos aleatorios en `[a, b]`
  - Evalúa la función en cada punto
  - Retorna: integral aproximada y lista de puntos
  
- `calcular_integral_2d(func_str, a, b, c, d, n)`: Calcula integral doble
  - Similar a 1D, pero con dos variables `(x, y)`
  
- `calcular_valor_exacto_1d(func_str, a, b)`: Calcula el valor exacto
  - Usa SymPy para integración simbólica
  - Traduce funciones de `math.*` a notación de SymPy
  
- `generar_puntos_funcion(func_str, a, b, num_puntos)`: Genera puntos para graficar

**Características de Seguridad:**
- El método `eval()` usa un namespace restringido: `{"x": x, "math": math, "np": np, "__builtins__": {}}`
- Esto evita acceso a funciones peligrosas de Python

---

### 2. **Vista** (`vista/vista.py`)
**Responsabilidad**: Interfaz gráfica de usuario

**Clase Principal**: `VistaMonteCarlo`

**Componentes GUI:**
- **Notebook (pestañas)**: Dos tabs para integral 1D y 2D
  
- **Tab de Integral 1D:**
  - Campo de entrada para función: `f(x) = x**3 + 2`
  - Campos para límites: `a = 1`, `b = 3`
  - Campo para número de puntos: `N = 10000`
  - Botones de funciones matemáticas: sin, cos, log, exp, etc.
  - Botones de ejemplo
  - Gráfico con matplotlib
  - Área de resultados con scrollbars

- **Tab de Integral 2D:**
  - Similar a 1D, pero con dos variables y dos intervalos
  - Gráfico 3D de la superficie

**Flujo de Datos:**
1. Usuario ingresa datos en campos Entry
2. Usuario hace click en botón "Calcular"
3. Se llama `_calcular_1d()` que invoca al controlador

---

### 3. **Controlador** (`controlador/controller.py`)
**Responsabilidad**: Coordinación entre modelo y vista

**Clase Principal**: `ControladorMonteCarlo` (alias `Controlador`)

**Métodos Principales:**
- `calcular_1d()`:
  1. Obtiene valores de la vista
  2. Valida que `a < b`
  3. Llama al modelo: `modelo.calcular_integral_1d()`
  4. Actualiza el gráfico: `vista.actualizar_grafico_1d()`
  5. Formatea y muestra resultados: `mostrar_resultados_1d()`

- `calcular_2d()`: Similar para integrales dobles

- `mostrar_resultados_1d()`: Formatea la salida con:
  - Información del cálculo
  - Resultado de la aproximación
  - Comparación con valor exacto
  - Error absoluto y relativo
  - Explicación del método

- `cargar_ejemplo_1d()`: Llena los campos con valores de ejemplo

---

## Flujo Completo de la Aplicación

### Entrada del Usuario
El usuario ingresa en la GUI:
```
Función: x**3 + 2
a = 1
b = 3
N = 10000
```

### Flujo de Datos (MVC)

```
┌─────────────┐
│   USUARIO   │
│  (ingresa   │
│  datos)     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│    VISTA (vista.py)     │
│  - Recolecta datos      │
│  - Muestra GUI          │
└──────┬──────────────────┘
       │ (Usuario hace click en "Calcular")
       ▼
┌──────────────────────────┐
│ CONTROLADOR (controller) │
│ - Obtiene valores        │
│ - Valida datos           │
│ - Orquesta operación     │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│   MODELO (modelo.py)     │
│ - Genera 10000 puntos x  │
│ - Evalúa f(x) en c/punto │
│ - Calcula promedio       │
│ - Multiplica por (b-a)   │
│ - Retorna integral       │
└──────┬───────────────────┘
       │
       ▼ (Resultado: 25.000)
┌──────────────────────────┐
│  CONTROLADOR (formatter) │
│  - Formatea resultados   │
│  - Calcula error exacto  │
│  - Prepara texto explica │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│     VISTA (renderer)     │
│  - Dibuja gráfico        │
│  - Muestra resultados    │
│  - Visualiza puntos      │
└──────┬───────────────────┘
       │
       ▼
┌─────────────┐
│   PANTALLA  │
│   (Output)  │
└─────────────┘
```

---

## Detalle Técnico del Cálculo (x³ + 2)

### Código en `modelo.py` - `calcular_integral_1d()`

```python
def calcular_integral_1d(func_str: str, a: float, b: float, n: int):
    suma = 0
    puntos = []
    
    # Genera n puntos aleatorios
    for i in range(n):  # n = 10000
        x = random.uniform(a, b)  # x ∈ [1, 3]
        
        # Evalúa f(x) = x**3 + 2
        y = eval(func_str, {"x": x, "math": math, "np": np, ...})
        suma += y
        
        if i < n:
            puntos.append({"x": x, "y": y})
    
    # Calcula integral: (b - a) × (suma / n)
    integral = (b - a) * suma / n
    # integral = (3 - 1) × (suma / 10000) = 2 × promedio
    
    return integral, puntos
```

### Visualización Gráfica

El gráfico mostrado incluye:
1. **Línea azul**: La función `f(x) = x³ + 2` continua
2. **Puntos rojos**: Los 10,000 puntos aleatorios generados
3. **Eje X**: Valores de `x` de 1 a 3
4. **Eje Y**: Valores de `f(x)` calculados
5. **Área bajo la curva**: Representada visualmente

---

## Cálculo del Valor Exacto con SymPy

### Código en `modelo.py` - `calcular_valor_exacto_1d()`

```python
def calcular_valor_exacto_1d(func_str, a, b):
    x = sp.Symbol('x')
    
    # Traduce: x**3 + 2 → x**3 + 2 (sin cambios)
    func = sp.sympify(func_str)
    
    # Integra analíticamente: ∫(x³ + 2)dx = x⁴/4 + 2x
    resultado = sp.integrate(func, (x, a, b))
    
    # Evalúa en límites: [x⁴/4 + 2x] de 1 a 3
    # = (81/4 + 6) - (1/4 + 2)
    # = 26.25 - 2.25
    # = 24.0
    
    return float(resultado.evalf())
```

---

## Salida de Resultados

Cuando se ejecuta con los parámetros del ejemplo, el controlador genera:

```
============================================================
INTEGRAL SIMPLE - MÉTODO DE MONTE CARLO
============================================================

📊 INFORMACIÓN DEL CÁLCULO:
   Función: f(x) = x**3 + 2
   Intervalo: [1, 3]
   Puntos generados (N): 10,000

🎯 RESULTADO DE LA APROXIMACIÓN:
   ∫f(x)dx ≈ 25.000

📐 COMPARACIÓN CON VALOR EXACTO:
   Valor exacto: 24.000
   Error absoluto: 1.000
   Error relativo: 4.17%

🔢 PUNTOS ALEATORIOS UTILIZADOS (primeros 10):
   Punto 1: x = 1.234, f(x) = 3.877
   Punto 2: x = 2.567, f(x) = 18.885
   ...

📈 EXPLICACIÓN DEL MÉTODO:
   1. Se generan 10,000 puntos xᵢ aleatorios en [1, 3]
   2. Se evalúa f(xᵢ) en cada punto
   3. Se calcula el promedio: (1/10000) × Σ f(xᵢ)
   4. Se multiplica por el ancho del intervalo: (3-1)
   5. Fórmula: ∫f(x)dx ≈ (b-a) × (1/N) × Σ f(xᵢ)
```

---

## Dependencias

| Librería | Propósito |
|----------|-----------|
| `tkinter` | Interfaz gráfica (GUI) |
| `matplotlib` | Generación de gráficos |
| `numpy` | Operaciones numéricas y arrays |
| `sympy` | Integración simbólica exacta |
| `random` | Generación de números aleatorios |
| `math` | Funciones matemáticas |

---

## Configuración Recomendada

- **Python**: 3.6 o superior
- **numpy**: 1.19.0+
- **matplotlib**: 3.3.0+
- **SymPy**: 1.12+
- **Pillow**: 8.0.0+ (para matplotlib + tkinter)

---

## Notas de Implementación

### Precisión del Método
- **Más puntos (N)** = Mayor precisión pero más lento
- **Menos puntos (N)** = Menor precisión pero más rápido
- Típicamente 10,000 puntos dan buena aproximación

### Limitaciones
- No funciona bien con funciones muy oscilantes
- Requiere evaluación de función en cada punto
- El error disminuye con √N (convergencia lenta)

### Ventajas de Monte Carlo
- Funciona en cualquier dimensión
- No necesita derivadas
- Robusto con funciones discontinuas
- Fácil de paralelizar

---

## Ejemplo de Ejecución Completa

```bash
$ python3 main.py
# Se abre la ventana GUI
# Usuario ingresa: x**3 + 2, a=1, b=3, N=10000
# Usuario presiona "Calcular"
# App genera 10,000 puntos aleatorios
# App evalúa función en cada punto
# App muestra gráfico y resultados
# Resultado: ∫₁³ (x³ + 2)dx ≈ 25.0 (exacto: 24.0)
```

---

**Autor**: MonteCarlo Simulator  
**Versión**: 1.0  
**Año**: 2025

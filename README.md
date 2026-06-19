# Método de Monte Carlo — Calculadora de Integrales

## Parte 1: Objetivos

### Objetivo General

Comprender, explicar e implementar el Método de Monte Carlo como herramienta de integración numérica, demostrando su funcionamiento mediante una aplicación interactiva que permita visualizar el proceso de muestreo aleatorio y comparar los resultados aproximados con los valores exactos.

### Objetivos Específicos

1. **Definir el marco histórico:** Investigar los orígenes del método, sus creadores y el contexto científico-militar en el que surgió durante la década de 1940.
2. **Establecer el fundamento teórico:** Explicar los principios matemáticos y estadísticos que sustentan el método, incluyendo la Ley de los Grandes Números y la generación de números pseudoaleatorios.
3. **Identificar aplicaciones prácticas:** Analizar los campos modernos donde el método se aplica activamente, desde finanzas hasta física de partículas e inteligencia artificial.
4. **Desarrollar una implementación funcional:** Construir una aplicación con interfaz gráfica que permita calcular integrales simples y dobles, visualizar los puntos aleatorios y comparar con soluciones analíticas.

---

## Parte 2: Historia y Contexto

### Orígenes en el Proyecto Manhattan (1940s)

El Método de Monte Carlo nació en **1946** en el Laboratorio Nacional de Los Álamos, durante el desarrollo del **Proyecto Manhattan**, el programa secreto estadounidense para construir la primera bomba atómica.

**Stanislaw Ulam**, un matemático polaco-estadounidense, concibió la idea mientras jugaba solitario durante una convalecencia. Se preguntó: *"¿Cuál es la probabilidad de que un solitario Canfield salga bien?"* En lugar de calcular todas las combinatorias posibles (un problema enormemente complejo), pensó que sería más práctico simplemente **jugar muchas partidas y contar cuántas veces ganaba**. Esta intuición fue el germen del método.

Ulam compartió la idea con **John von Neumann**, quien inmediatamente reconoció su potencial para resolver las ecuaciones de transporte de neutrones que necesitaban para el diseño de armas nucleares. Von Neumann diseñó los algoritmos y los implementó en la computadora **ENIAC**, una de las primeras computadoras electrónicas del mundo.

### ¿Por qué "Monte Carlo"?

El nombre fue sugerido por **Nicholas Metropolis**, colega de Ulam y von Neumann en Los Álamos. El nombre hace referencia al famoso **Casino de Monte Carlo** en Mónaco, conocido mundialmente por sus juegos de azar y ruletas. La elección del nombre era una metáfora perfecta: al igual que en un casino, el método se basa en el **azar** y la **aleatoriedad** para obtener resultados. Además, el nombre servía como nombre en clave, dado que el trabajo se realizaba en un contexto de alto secreto militar.

### Evolución posterior

Tras la Segunda Guerra Mundial, el método se extendió rápidamente a otros campos. En los años 50 y 60, con la llegada de computadoras más potentes, se aplicó a problemas de física nuclear, termodinámica y estadística. Hoy en día, con la capacidad computacional moderna, el Método de Monte Carlo es una herramienta fundamental en ciencia, ingeniería y finanzas.

---

## Parte 3: Marco Teórico

### Definición del Método de Monte Carlo

El Método de Monte Carlo es una **técnica de simulación numérica** que utiliza la generación de **números aleatorios** para resolver problemas matemáticos que pueden ser deterministas en su naturaleza pero difíciles o imposibles de resolver analíticamente.

La idea central es transformar un problema determinista (como calcular una integral) en un problema probabilístico equivalente, y luego resolverlo mediante **muestreo aleatorio masivo**.

### Fundamento matemático

El método se basa en la **Ley de los Grandes Números**, que establece que:

> A medida que el número de muestras aleatorias tiende a infinito, el promedio de los resultados obtenidos converge al valor esperado teórico.

Para calcular una integral definida:

```
∫[a,b] f(x) dx
```

El método sigue estos pasos:

1. **Generar N puntos aleatorios** x₁, x₂, ..., xₙ uniformemente distribuidos en el intervalo [a, b].
2. **Evaluar la función** f(xᵢ) en cada punto aleatorio.
3. **Calcular el promedio** de los valores obtenidos.
4. **Multiplicar por la longitud del intervalo** (b - a).

La fórmula resultante es:

```
∫[a,b] f(x) dx  ≈  (b - a) × (1/N) × Σ f(xᵢ)
```

### Números pseudoaleatorios

Las computadoras no pueden generar números verdaderamente aleatorios; en su lugar, utilizan **generadores de números pseudoaleatorios (PRNG)**. Estos son algoritmos deterministas que producen secuencias de números que pasan pruebas estadísticas de aleatoriedad. Python utiliza el algoritmo **Mersenne Twister** como generador predeterminado, que tiene un período de 2¹⁹⁹³⁷ - 1, suficiente para cualquier simulación práctica.

### Convergencia y error

El error del método de Monte Carlo disminuye a una tasa de **1/√N**, donde N es el número de puntos muestreados. Esto significa que:

- Para **reducir el error a la mitad**, se necesita **cuadruplicar** el número de puntos.
- La tasa de convergencia es **independiente de la dimensionalidad** del problema, lo cual es una ventaja enorme frente a métodos como la regla del trapecio o Simpson en dimensiones altas.

---

## Parte 4: Casos de Uso

### Aplicaciones modernas del Método de Monte Carlo

#### Finanzas y gestión de riesgos
- **Valoración de opciones financieras:** El modelo de Black-Scholes y sus extensiones utilizan simulaciones Monte Carlo para estimar el precio de opciones exóticas donde no existen fórmulas cerradas.
- **Value at Risk (VaR):** Los bancos simulan miles de escenarios de mercado para estimar la máxima pérdida esperada en un portafolio de inversiones.
- **Planificación de retiro:** Se simulan diferentes escenarios de mercado para estimar la probabilidad de que un fondo de pensión sea suficiente.

#### Física de partículas
- **Simulación de colisiones:** En aceleradores como el CERN, se usa Monte Carlo para simular el comportamiento de partículas subatómicas tras colisiones a alta energía.
- **Transporte de radiación:** Modela cómo los neutrones y fotones se mueven a través de diferentes materiales, crucial para el diseño de reactores nucleares y blindaje de radiación.

#### Inteligencia artificial y machine learning
- **Métodos MCMC (Markov Chain Monte Carlo):** Utilizados en inferencia bayesiana para estimar distribuciones de probabilidad complejas en modelos de machine learning.
- **Aprendizaje por refuerzo:** El algoritmo Monte Carlo Tree Search (MCTS) es la base de programas como **AlphaGo**, que derrotó al campeón mundial de Go en 2016.

#### Gráficos por computadora y renderizado
- **Ray tracing estocástico:** Los motores de renderizado modernos (como los usados en Pixar o en videojuegos con ray tracing) utilizan Monte Carlo para simular cómo la luz rebota en las superficies, produciendo imágenes fotorrealistas.
- **Path tracing:** Técnica que traza miles de rayos de luz aleatorios por cada píxel para calcular la iluminación global de una escena.

#### Ingeniería y ciencias aplicadas
- **Análisis de confiabilidad:** Simula la probabilidad de fallo de sistemas complejos (puentes, aviones, circuitos electrónicos).
- **Predicción del clima:** Los modelos meteorológicos usan Monte Carlo para cuantificar la incertidumbre en sus pronósticos.

---

## Parte 5: Análisis Crítico

### Ventajas

| Ventaja | Descripción |
|---------|-------------|
| **Flexibilidad** | Puede aplicarse a prácticamente cualquier problema que pueda formularse de manera probabilística, sin importar la complejidad de la función o la geometría del dominio. |
| **Escalabilidad dimensional** | A diferencia de métodos como la regla del trapecio (cuyo costo crece exponencialmente con la dimensión), Monte Carlo mantiene una convergencia de O(1/√N) independientemente del número de dimensiones. |
| **Simplicidad de implementación** | El algoritmo básico es conceptualmente sencillo: generar puntos aleatorios, evaluar la función y promediar. |
| **Paralelizable** | Las muestras son independientes entre sí, lo que permite distribuir el cálculo en múltiples procesadores o GPUs. |
| **Manejo de geometrías complejas** | Puede integrar sobre regiones irregulares donde los métodos clásicos de cuadratura son difíciles de aplicar. |

### Limitaciones

| Limitación | Descripción |
|------------|-------------|
| **Convergencia lenta** | La tasa de 1/√N significa que para ganar un dígito extra de precisión se necesitan 100 veces más puntos. |
| **Resultados aproximados** | Cada ejecución produce un resultado diferente; nunca se obtiene un valor exacto, solo una estimación estadística. |
| **Costo computacional** | Para obtener alta precisión se requieren millones o miles de millones de muestras, lo que demanda gran capacidad de procesamiento. |
| **Dependencia del generador aleatorio** | La calidad de los resultados depende de la calidad del generador de números pseudoaleatorios utilizado. |
| **Ineficiente en dimensiones bajas** | Para problemas de 1 o 2 dimensiones, métodos clásicos como Simpson o cuadratura de Gauss son más precisos y rápidos. |

---

## Parte 6: Demostración

### Ejemplo: Estimación de π mediante Monte Carlo

El ejemplo más clásico y didáctico del método es la **estimación del número π** usando un cuadrado y un círculo inscrito.

#### Planteamiento

Consideremos un cuadrado de lado 2 centrado en el origen, con un círculo de radio 1 inscrito dentro de él:

- **Área del cuadrado** = (2)² = 4
- **Área del círculo** = π × r² = π × 1² = π

La razón entre las áreas es:

```
Área del círculo / Área del cuadrado = π / 4
```

#### Procedimiento paso a paso

1. **Generar puntos aleatorios:** Se generan N puntos (x, y) con coordenadas aleatorias en el rango [-1, 1].

2. **Clasificar cada punto:** Para cada punto, se verifica si cae **dentro del círculo** usando la condición:
   ```
   x² + y² ≤ 1  →  el punto está dentro del círculo
   x² + y² > 1  →  el punto está fuera del círculo
   ```

3. **Contar puntos interiores:** Se cuenta cuántos puntos cayeron dentro del círculo (N_dentro).

4. **Estimar π:** La proporción de puntos dentro del círculo aproxima la razón de áreas:
   ```
   N_dentro / N  ≈  π / 4
   ```
   Por lo tanto:
   ```
   π  ≈  4 × (N_dentro / N)
   ```

#### Ejemplo numérico

Con **N = 10,000** puntos:
- Supongamos que **7,856** puntos caen dentro del círculo.
- Entonces: π ≈ 4 × (7856 / 10000) = 4 × 0.7856 = **3.1424**
- El valor real de π = 3.14159... → Error ≈ 0.026%

#### Lógica del ejemplo

Este ejemplo ilustra la esencia del Método de Monte Carlo: **reemplazar un cálculo geométrico exacto por un experimento estadístico**. No se necesita conocer fórmulas de áreas de círculos; simplemente se "lanzan dardos" al azar y se observa qué fracción cae dentro. A medida que se lanzan más dardos (más puntos), la estimación se acerca más al valor verdadero.

---

## Parte 7: Conclusión y Proyecto

### Conclusión

El Método de Monte Carlo, nacido en el contexto del Proyecto Manhattan gracias a las mentes de Stanislaw Ulam y John von Neumann, ha trascendido su origen militar para convertirse en una de las herramientas computacionales más versátiles y poderosas de la ciencia moderna.

Su principio fundamental es elegantemente simple: utilizar el azar para resolver problemas deterministas. A través de la generación masiva de muestras aleatorias y la aplicación de la Ley de los Grandes Números, el método convierte problemas matemáticamente intratables en simulaciones computacionales accesibles.

Si bien presenta limitaciones inherentes como su convergencia lenta (O(1/√N)) y la naturaleza aproximada de sus resultados, sus ventajas lo hacen insustituible en contextos de alta dimensionalidad y geometrías complejas. Desde la valoración de derivados financieros hasta el entrenamiento de inteligencia artificial con AlphaGo, desde el renderizado de películas de Pixar hasta la simulación de reactores nucleares, Monte Carlo es un pilar de la computación científica contemporánea.

La implementación desarrollada en este proyecto demuestra de manera práctica cómo el método puede aplicarse al cálculo de integrales, permitiendo visualizar el proceso de muestreo, comparar con valores exactos y comprender intuitivamente por qué funciona.

---

### Proyecto: Calculadora Monte Carlo

Aplicación de escritorio con interfaz gráfica (GUI) que implementa el Método de Monte Carlo para el cálculo de integrales simples (1D) y dobles (2D), con visualización interactiva de los puntos aleatorios y comparación con valores exactos.

#### Prerrequisitos

- **Python** 3.6 o superior
- **Tkinter** (incluido con Python)
- Dependencias externas:

```bash
pip install numpy matplotlib sympy
```

| Paquete      | Versión mínima | Uso                                      |
|--------------|----------------|------------------------------------------|
| `numpy`      | 1.19.0         | Operaciones numéricas y generación de puntos |
| `matplotlib` | 3.3.0          | Gráficos y visualización interactiva     |
| `sympy`      | 1.12           | Cálculo simbólico de integrales exactas   |

#### Cómo ejecutar

```bash
git clone <url-del-repositorio>
cd MonteCarlo
pip install numpy matplotlib sympy
python main.py
```

#### Uso de la aplicación

1. Seleccionar la pestaña **Integral Simple (1D)** o **Integral Doble (2D)**.
2. Ingresar la función (ej: `x**2`, `math.sin(x)`, `x**3 + 4`).
3. Definir los límites de integración y el número de puntos.
4. Presionar **Calcular Integral**.
5. Usar la barra de herramientas del gráfico para hacer **zoom**, **pan** y explorar los puntos aleatorios a detalle.

#### Arquitectura (MVC)

El proyecto sigue el patrón **Modelo-Vista-Controlador**:

```
MonteCarlo/
├── main.py                  # Punto de entrada
├── app.py                   # Bootstrap MVC, crea la ventana Tkinter
├── model/
│   └── modelo.py            # Lógica de cálculo Monte Carlo y SymPy
├── view/
│   └── vista.py             # Interfaz gráfica Tkinter + Matplotlib
├── controller/
│   └── controller.py        # Validación, orquestación y formato de resultados
├── dependencias.txt         # Documentación de dependencias
└── README.md
```

| Componente     | Archivo                  | Responsabilidad                                                    |
|----------------|--------------------------|--------------------------------------------------------------------|
| **Modelo**     | `model/modelo.py`        | Algoritmos de muestreo Monte Carlo, evaluación de funciones, cálculo de integrales exactas con SymPy |
| **Vista**       | `view/vista.py`          | Interfaz gráfica con pestañas (1D/2D), gráficos Matplotlib embebidos con toolbar de zoom, panel de resultados |
| **Controlador** | `controller/controller.py` | Validación de entradas, coordinación modelo-vista, formateo de resultados con estadísticas y explicación |

#### Funcionalidades

- Cálculo de integrales simples (1D) y dobles (2D) por Monte Carlo
- Visualización de la función y los puntos aleatorios con colores llamativos
- Barra de herramientas interactiva para zoom, desplazamiento y guardado de gráficos
- Comparación automática con el valor exacto calculado por SymPy
- Barra de progreso en tiempo real durante la generación de puntos
- Botones de funciones matemáticas comunes (sin, cos, exp, log, etc.)
- Ejemplos precargados para pruebas rápidas
- Explicación paso a paso del método en cada resultado

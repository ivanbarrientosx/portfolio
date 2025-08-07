# portfolio Project 2 Quantum for Portfolio Optimization

## San Angel Digital

### Iván Barrientos Salas

Este proyecto utiliza algoritmos cuánticos para resolver un problema de optimización financiera: encontrar la combinación óptima de activos (bonos) cuya duración ponderada se acerque a un objetivo específico (target_duration = 1.0). El enfoque combina la librería PennyLane para computación cuántica y técnicas clásicas de optimización (VQE, Variational Quantum Eigensolver). A continuación, se detallan las cuatro secciones principales del programa:

#### 1. Definición del Problema
El objetivo es minimizar la diferencia entre la duración total de una cartera de  bonos y un valor objetivo (1.0). Los parámetros de entrada son:

    ° betas: Contribución de cada bono a la duración ([0.3, 0.5, 0.7]).
    ° x_vals: Valores de los activos (simplificados a [1.0, 1.0, 1.0]).
    ° target_duration: Duración deseada (1.0).

El problema se modela como un sistema de optimización cuadrática (QUBO), donde las variables binarias representan la inclusión (1) o exclusión (0) de cada bono.

#### 2. Conversión a Física Cuántica
Para resolver el problema con un circuito cuántico, se construye un Hamiltoniano QUBO que codifica la función de costo. Este Hamiltoniano se expresa como una combinación de operadores de Pauli (Z y ZZ), que representan interacciones entre qubits:

    ° Términos lineales: Corresponden a la contribución individual de cada bono (PauliZ).

    ° Términos cuadráticos: Capturan las interacciones entre pares de bonos (PauliZ @ PauliZ).

La función build_qubo_hamiltonian calcula los coeficientes del Hamiltoniano a partir de los parámetros del problema. Por ejemplo, el término lineal para el bono i incluye:
                coeffs.append(-Q[i,i]/2 - c[i]/2)  # Término Z (operador PauliZ)

#### 3. Entrenamiento del Circuito Cuántico
El circuito cuántico (ansatz) utiliza capas alternadas de rotaciones y entrelazamiento:

    1. Rotaciones Y (RY): Aplicadas a cada qubit con ángulos aleatorios iniciales.

    2. Entrelazamiento (CZ): Generado con compuertas controladas-Z entre qubits adyacentes.

El dispositivo cuántico simulado (default.qubit) evalúa el valor esperado del Hamiltoniano mediante la función cost_function, que sirve como criterio para el optimizador clásico (Gradient Descent). Durante 100 iteraciones, el algoritmo ajusta los parámetros del circuito para minimizar la energía (valor esperado):

                for iteration in range(100):
                    params, energy = optimizer.step_and_cost(cost_function, params)

#### 4. Obtención de la Mejor Combinación
Tras la optimización, se calculan las probabilidades de cada estado base (combinación de bonos) con la función get_probabilities. Los resultados se interpretan como:

    ° Estados binarios: Cada qubit representa un bono (ej: 101 = incluir el bono 1 y 3, excluir el 2).

    ° Probabilidades: Indican la optimalidad de cada combinación.

Por ejemplo, si el estado 011 tiene una probabilidad del 90%, significa que la combinación que incluye los bonos 2 y 3 es cercana a la solución óptima.

#### Resultados y Conclusión
El programa imprime:

    ° La energía mínima encontrada (valor de la función de costo).
    ° Los parámetros óptimos del circuito.
    ° Las probabilidades de todas las combinaciones posibles.

Este enfoque demuestra cómo la computación cuántica híbrida (VQE) puede aplicarse a problemas financieros, aunque en este caso se usa un simulador debido a las limitaciones actuales de hardware. La metodología es escalable a problemas más complejos, como carteras con más activos o restricciones adicionales.


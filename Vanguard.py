# Este programa lo podemos seccionar en partes
# 1. Define el problema 
# 2. Conviertelo a física cuantica 
# 3. Entrena el circuito 
# 4. Obtenemos la mejor combinacion

import pennylane as qml
from pennylane import qaoa
from pennylane import numpy as np

# ----------------------------
# Configuración del problema, ingresamos los datos
# ----------------------------
# Definimos los mismos parámetros del problema original
betas = np.array([0.3, 0.5, 0.7])    # Contribución de cada activo a la duración
x_vals = np.array([1.0, 1.0, 1.0])   # Valores de los activos (simplificado)
target_duration = 1.0                # Duracion objetivo, queremos que la mezcla total sea exactamente 1.0.

# ----------------------------
# Construcción del Hamiltoniano QUBO
# ----------------------------
def build_qubo_hamiltonian(betas, x_vals, target):
                        # Se onstruye el Hamiltoniano QUBO para el problema de optimización
    Q = np.outer(betas * x_vals, betas * x_vals) # Calcula interacciones entre bonos
    c = -2 * target * betas * x_vals
    
                        # PennyLane requiere coeficientes y operadores Pauli
    coeffs = []         # Lista de coeficientes (pesos)
    pauli_terms = []    # Lista de operadores cuánticos (Z, ZZ)
    
                             # Términos lineales individuales (Z_i)
    for i in range(len(betas)):
        coeffs.append(Q[i,i]/4 + c[i]/2)    # Término de identidad
        pauli_terms.append(qml.Identity(i)) 
        
        coeffs.append(-Q[i,i]/2 - c[i]/2)   # Término Z
        pauli_terms.append(qml.PauliZ(i))   # Operador Z en el qubit i
    
                                            # Creamos los términos cuadráticos (Z_i Z_j)
    for i in range(len(betas)):
        for j in range(i+1, len(betas)):
            if Q[i,j] != 0:
                coeffs.append(Q[i,j]/4)
                pauli_terms.append(qml.PauliZ(i) @ qml.PauliZ(j)) # Operador ZZ
    
    return qml.Hamiltonian(coeffs, pauli_terms)                    # Retornamos la combinación lineal de términos

hamiltonian = build_qubo_hamiltonian(betas, x_vals, target_duration)

# ----------------------------
# Configuración del dispositivo cuántico
# ----------------------------
dev = qml.device("default.qubit", wires=len(betas))  # Usamos un simulador local

# ----------------------------
# Circuito cuántico (Ansatz)
# ----------------------------
def quantum_circuit(params, wires):
    """Ansatz de capas alternadas de rotaciones y entrelazamiento"""
    # Capa de rotaciones
    for i, wire in enumerate(wires):
        qml.RY(params[i], wires=wire)               # Rotación Y (ángulo = parámetro)

    for i in range(len(wires)-1):
        qml.CZ(wires=[wires[i], wires[i+1]])        # Entrelazamiento controlado-Z

    for i, wire in enumerate(wires):
        qml.RY(params[len(wires) + i], wires=wire) # Segunda capa de rotaciones

# ----------------------------
# Función de costo para VQE
# ----------------------------
@qml.qnode(dev)
def cost_function(params):
    """Evalúa el valor esperado del Hamiltoniano"""
    quantum_circuit(params, wires=range(len(betas)))
    return qml.expval(hamiltonian)                  # Valor esperado del Hamiltoniano

# ----------------------------
# Optimización clásica
# ----------------------------
optimizer = qml.GradientDescentOptimizer(stepsize=0.1)
params = np.random.uniform(0, 2*np.pi, size=2*len(betas))  # Parámetros iniciales aleatorios

print("Iniciando optimización con VQE...")
for iteration in range(100):
    params, energy = optimizer.step_and_cost(cost_function, params)
    
    if iteration % 10 == 0:
        print(f"Iteración {iteration}: Energía = {energy:.4f}")

# ----------------------------
# Se imprimen los Resultados
# ----------------------------
print("\nResultados finales:")
print(f"Energía mínima encontrada: {energy:.4f}")
print("Parámetros óptimos:", params)

# ----------------------------
# Interpretación de la solución
# ----------------------------
@qml.qnode(dev)
def get_probabilities(params):
    """Obtiene las probabilidades de cada estado base"""
    quantum_circuit(params, wires=range(len(betas)))
    return qml.probs(wires=range(len(betas)))

probs = get_probabilities(params)
print("\nProbabilidades de cada combinación de activos:")
for i, prob in enumerate(probs):
    binary_str = format(i, f'0{len(betas)}b')
    print(f"Combinación {binary_str}: {prob:.4%}")

# Interpretacion de los resultados
# Cada bit en binary_str representa un bono (ej: 011 = [A❌, B✅, C✅]).
# La probabilidad te dice cuán óptima es esa combinación. 
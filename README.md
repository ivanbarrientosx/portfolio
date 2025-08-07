# Quantum vs Classical Portfolio Optimization
# San Angel Digital
# Iván Barrientos Salas

Este notebook (`bq-vs-qaoa_v3.ipynb`) implementa y compara soluciones clásicas y cuánticas para un problema de **Optimización Binaria Cuadrática (BQP)** inspirado en asignación de portafolio.

## Objetivos

1. **Formulación matemática clásica** del problema con:
   - Variables binarias \( x_i \in \{0,1\} \)
   - Restricciones lineales de cardinalidad y opcionalmente por *bucket*
   - Objetivo cuadrático \(-\mu^T x + x^T (\gamma \Sigma) x\)

2. **Conversión a QUBO** (Task 2 del reto) mediante:
   - Penalización explícita de restricciones
   - `QuadraticProgramToQubo` de Qiskit Optimization

3. **Programa cuántico** usando QAOA con:
   - `SPSA` como optimizador clásico
   - Parámetros (`reps`, `maxiter`, `shots`) adaptados al tamaño del problema
   - Guardrails para escalabilidad

4. **Comparación con métodos clásicos**:
   - Solver exacto `NumPyMinimumEigensolver` (N ≤ 20)
   - Fuerza bruta (N ≤ 20)
   - Heurística random

5. **Escalamiento y métricas**:
   - Loop de escalamiento con N = 5, 10, 15 (y configurable)
   - Restricciones por *bucket* (uniformes o proporcionales)
   - Comparación “mismo tiempo” entre QAOA y heurística clásica
   - Gráficas de calidad y tiempo

## Estructura de bloques

- **Bloque 0:** Imports y utilidades (`objective_value`)
- **Bloque 1:** Carga de datos desde `data_assets_dictionary.xlsx` y construcción de μ, Σ
- **Bloque 2:** Formulación BQP clásica
- **Bloque 2.1:** Conversión explícita a QUBO
- **Bloque 2.2:** Restricciones por bucket (opcional)
- **Bloque 2.9:** Guardrails por tamaño (evita solver exacto si N > 20)
- **Bloque 3:** Baselines clásicos con guardrails
- **Bloque 4:** QAOA adaptativo
- **Bloque 5:** Resumen comparativo y visualización
- **Bloque 8:** Escalamiento con caps por bucket (proporcionales)
- **Bloque 9:** Comparación a mismo tiempo (QAOA vs heurística clásica)

## ⚙️ Uso

1. Colocar el archivo `data_assets_dictionary.xlsx` en la ruta correcta o ajustar `EXCEL_PATH` en Bloque 1.
2. Ajustar `N_SELECT` en Bloque 1:
   - 5 para demostraciones rápidas
   - 31 o 109 para replicar experimentos del ZIP
3. (Opcional) Activar o personalizar restricciones por bucket en Bloque 2.2.
4. Ejecutar los bloques en orden para:
   - Construir el problema
   - Resolver con métodos clásicos y cuánticos
   - Analizar escalamiento y comparativas a mismo tiempo

## Salidas

- **Resumen comparativo** de soluciones clásicas vs QAOA
- **Gráficas**:
  - Calidad de solución vs tamaño
  - Tiempo de cómputo vs tamaño
- **Tabla** con resultados por instancia (N, budget, f_numpy, f_qaoa, etc.)
- **Reporte por bucket**: capacidades, activos seleccionados, utilización

## Notas

- Con **N grande (>20)** el solver exacto se omite automáticamente y QAOA usa parámetros reducidos.
- Para N ≥ 64 se sugiere usar `AerSimulator(method='matrix_product_state')` o IBM Runtime.
- Las comparaciones “mismo tiempo” son útiles para mostrar la competitividad de QAOA frente a heurísticas clásicas bajo restricciones de tiempo.

## Requisitos

- `qiskit`
- `qiskit-aer` (opcional pero recomendado para shots realistas)
- `numpy`, `pandas`, `matplotlib`

---
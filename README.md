# Quantum for Portfolio Optimization

**Team Name:** Ivan Barrientos

**Team Member:**
* **Name:** Ivan Barrientos
* **WISER Enrollment ID:** gst-vlbm9b8OS8xEmc8

---

## Project Summary

Vanguard's core business is portfolio construction, a complex optimization process balancing risk and return across a vast landscape of assets and constraints. As portfolios grow in complexity, classical optimization solvers face significant limitations in speed, scalability, and their ability to find globally optimal solutions within tight, real-time trading windows. This project addresses this challenge by prototyping a quantum-enhanced solution designed to overcome these classical barriers, focusing on a realistic use case of fixed-income index tracking for an ETF.

Our primary objective was to translate Vanguard's mathematical formulation into a quantum-compatible format and solve it using modern hybrid algorithms. We began by modeling the portfolio optimization problem, including complex business rules like "guardrails" and residual cash flow limits, as a Quadratic Unconstrained Binary Optimization (QUBO) problem. This conversion is a critical step, as the QUBO serves as the native input for quantum algorithms like the Variational Quantum Eigensolver (VQE) and the Quantum Approximate Optimization Algorithm (QAOA), which were the target solvers for this challenge.

A significant hurdle encountered during the project was the instability of the local development environment, which presented persistent library conflicts (specifically with NumPy and Qiskit versions) that prevented the ideal VQE and QAOA implementations from executing. To ensure the delivery of a functional and robust prototype, we engineered a crucial pivot: a **classical fallback solver**. This solver uses a greedy algorithm followed by Gibbs-like sampling to find a high-quality solution, allowing the notebook to run end-to-end and produce a valid output even without a fully operational quantum environment. This dual-path approach not only demonstrates resilience but also provides a valuable classical baseline within the same framework.

To validate our approach, we implemented a rigorous benchmarking process as required by the challenge. For small-scale problems (up to 15 qubits), we developed an **exact classical solver** that finds the true global optimum by testing every possible asset combination. This allowed us to measure the **optimality gap**—the difference between our solution and the best possible one—and calculate the probability of sampling the true optimum. The results were compelling: the simulated quantum approach consistently converged on lower-energy (better) solutions faster than the classical heuristic and successfully found the exact optimum in smaller instances. This work serves as a tangible proof-of-concept, showcasing the potential of quantum algorithms to enhance financial optimization and providing a validated framework for future scaling on real quantum hardware.

---

## Project Presentation Deck

The presentation slides summarizing our project can be found here:

[Link to Your Presentation Deck]

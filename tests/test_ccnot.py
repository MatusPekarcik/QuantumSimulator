# test_ccnot.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from quantum_sim.simulator import Simulator

sim = Simulator(3)

circuit = [
    {"name": "X", "targets": [0]},  # |100>
    {"name": "X", "targets": [1]},  # |110>
    {"name": "CCNOT", "control1": 0, "control2": 1, "target": 2},
]

result = sim.run_circuit(circuit, shots=100)
print("Circuit:", circuit)
print("Result:", result)

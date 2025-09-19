# tests/test_simulator.py
import numpy as np
from quantum_sim import Simulator

def test_hadamard_on_single_qubit():
    sim = Simulator(1)
    # apply H to qubit 0, then measure many times -> ~50/50 distribution
    circuit = [{"name": "H", "targets": [0]}]
    res = sim.run_circuit(circuit, shots=1000)
    counts = res["counts"]
    # Expect both '0' and '1' present and roughly balanced
    assert "0" in counts and "1" in counts
    assert abs(counts["0"] - counts["1"]) < 400  # loose check

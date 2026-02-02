# tests/test_bell.py
import math
from quantum_sim import Simulator
from quantum_sim.gates import H

def test_bell_exact():
    sim = Simulator(2)
    sim.apply_single_qubit_gate(H, 0)
    sim.apply_cnot(control=0, target=1)
    probs = sim.probabilities()
    assert math.isclose(probs["00"], 0.5, abs_tol=1e-12)
    assert math.isclose(probs["11"], 0.5, abs_tol=1e-12)
    assert math.isclose(probs["01"], 0.0, abs_tol=1e-12)
    assert math.isclose(probs["10"], 0.0, abs_tol=1e-12)

def test_bell_marginals():
    sim = Simulator(2)
    sim.apply_single_qubit_gate(H, 0)
    sim.apply_cnot(control=0, target=1)
    m0 = sim.marginal_probability(0)
    m1 = sim.marginal_probability(1)
    assert math.isclose(m0["0"], 0.5, abs_tol=1e-12)
    assert math.isclose(m1["0"], 0.5, abs_tol=1e-12)

# run_2q.py
from quantum_sim import Simulator
from quantum_sim.gates import H

def main():
    sim = Simulator(2)

    # Create Bell state: H on qubit 0, then CNOT 0->1
    sim.apply_single_qubit_gate(H, 0)
    sim.apply_cnot(control=0, target=1)

    exact = sim.probabilities()
    print("Exact joint distribution:", exact)  # expect {'00': 0.5, '01': 0.0, '10': 0.0, '11': 0.5}

    m0 = sim.marginal_probability(0)
    m1 = sim.marginal_probability(1)
    print("Marginal qubit 0:", m0)
    print("Marginal qubit 1:", m1)

    shots = 10000
    res = sim.run_circuit([
        {"name": "H", "targets": [0]},
        {"name": "CNOT", "control": 0, "target": 1}
    ], shots=shots)
    counts = res["counts"]
    print(f"Sampled (shots={shots}) counts (small):",
          {k: counts[k] for k in sorted(counts) if k in ("00", "11")})
    p0_0 = sum(c for k, c in counts.items() if k[0] == "0") / shots
    p0_1 = sum(c for k, c in counts.items() if k[0] == "1") / shots
    print(f"Empirical marginal qubit0: p(0)={p0_0:.4f}, p(1)={p0_1:.4f}")

if __name__ == "__main__":
    main()

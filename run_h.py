# run_h.py
from quantum_sim import Simulator
from quantum_sim.gates import H

def main():
    sim = Simulator(1)

    # apply H gate to qubit 0 (leftmost)
    sim.apply_single_qubit_gate(H, 0)

    # Exact probabilities from statevector
    exact = sim.probabilities()
    marginal = sim.marginal_probability(0)
    print("Exact full distribution:", exact)
    print("Exact marginal (qubit 0):", marginal)

    # Empirical (sampled) probabilities using shots
    res = sim.run_circuit([{"name": "H", "targets": [0]}], shots=10000)
    counts = res["counts"]
    shots = res["shots"]
    p0 = counts.get("0", 0) / shots
    p1 = counts.get("1", 0) / shots
    print(f"Sampled (shots={shots}): p(0)={p0:.4f}, p(1)={p1:.4f}")
    print("Sampled counts (small):", {k: counts[k] for k in sorted(counts)[:10]})

if __name__ == "__main__":
    main()

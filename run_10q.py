# run_10q.py
from quantum_sim import Simulator
from quantum_sim.gates import H
import pprint

def main():
    n = 10
    sim = Simulator(n)

    # Example 1: put every qubit into H -> uniform superposition
    for q in range(n):
        sim.apply_single_qubit_gate(H, q)

    probs = sim.probabilities()
    expected = 1.0 / (2 ** n)
    # pick a single state (e.g., the first key) to show probability
    one_state = next(iter(probs))
    print(f"One state ({one_state}) probability = {probs[one_state]:.6e} (expected ~{expected:.6e})")

    # Sample some measurements
    shots = 5000
    res = sim.run_circuit([{"name":"H", "targets": list(range(n))}], shots=shots)
    counts = res["counts"]
    # print counts for a few states (sorted)
    first_keys = sorted(counts)[:10]
    few = {k: counts.get(k, 0) for k in first_keys}
    print("Sampled counts (first few keys):")
    pprint.pprint(few)

    # Example 2: create a small entangled block: H on qubit 0 then CNOT 0->1 (rest left in |0>)
    sim.reset()
    sim.apply_single_qubit_gate(H, 0)
    sim.apply_cnot(0, 1)
    probs2 = sim.probabilities()
    # all-zeroes bitstring of length n
    all_zeros = "0" * n
    print(f"\nExact prob of {all_zeros} (all zeros): {probs2.get(all_zeros, 0.0):.6f}")
    # print marginals for first two qubits
    print("Marginal q0:", sim.marginal_probability(0))
    print("Marginal q1:", sim.marginal_probability(1))

if __name__ == "__main__":
    main()

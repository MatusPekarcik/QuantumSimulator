import argparse
import time
import numpy as np

from quantum_sim.simulator import Simulator

def make_random_circuit(n, depth, seed=0):
    rng = np.random.default_rng(seed)
    ops = []
    oneq = ["H", "X", "Y", "Z", "S", "T"]
    twoq = ["CNOT", "CZ", "SWAP", "ISWAP"]

    for _ in range(depth):
        # 1Q layer
        for q in range(n):
            g = rng.choice(oneq)
            ops.append({"name": g, "targets": [int(q)]})

        # 2Q layer (pair neighbors)
        pairs = [(i, i+1) for i in range(0, n-1, 2)]
        rng.shuffle(pairs)
        for a, b in pairs:
            g2 = rng.choice(twoq)
            if g2 in ("CNOT", "CZ"):
                ops.append({"name": g2, "control": int(a), "target": int(b)})
            else:
                ops.append({"name": g2, "q1": int(a), "q2": int(b)})

    return ops

def run_once(n, depth, shots, noise_p, repeats, seed):
    circuit = make_random_circuit(n, depth, seed=seed)

    noise_model = None
    if noise_p is not None and noise_p > 0:
        noise_model = {
            "channels": [
                {"after": "each_gate", "type": "depolarizing", "p": float(noise_p)}
            ]
        }

    # warm-up
    sim = Simulator(n)
    sim.run_circuit(circuit, shots=min(10, shots), noise_model=noise_model)

    times = []
    for r in range(repeats):
        sim = Simulator(n)
        t0 = time.perf_counter()
        sim.run_circuit(circuit, shots=shots, noise_model=noise_model)
        t1 = time.perf_counter()
        times.append(t1 - t0)

    return {
        "n": n,
        "depth": depth,
        "shots": shots,
        "noise_p": noise_p or 0.0,
        "repeats": repeats,
        "mean_s": float(np.mean(times)),
        "std_s": float(np.std(times)),
        "min_s": float(np.min(times)),
        "max_s": float(np.max(times)),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--depth", type=int, default=10)
    ap.add_argument("--shots", type=int, default=1024)
    ap.add_argument("--noise_p", type=float, default=0.0)
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    res = run_once(args.n, args.depth, args.shots, args.noise_p, args.repeats, args.seed)
    print(res)

if __name__ == "__main__":
    main()
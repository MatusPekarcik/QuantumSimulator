# bench_aer.py
import argparse
import time
import numpy as np

try:
    import resource
except ImportError:
    resource = None

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

ONEQ = ["H", "X", "Y", "Z", "S", "T"]
TWOQ = ["CNOT", "CZ", "SWAP", "ISWAP"]

def rss_mb():
    if resource is None:
        return None
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if r > 10_000_000:
        return r / (1024 * 1024)
    return r / 1024.0

def make_random_circuit(n, depth, seed=0):
    rng = np.random.default_rng(seed)
    ops = []
    for _ in range(depth):
        for q in range(n):
            g = rng.choice(ONEQ)
            ops.append((g, q))
        pairs = [(i, i + 1) for i in range(0, n - 1, 2)]
        rng.shuffle(pairs)
        for a, b in pairs:
            g2 = rng.choice(TWOQ)
            ops.append((g2, a, b))
    return ops

def build_qiskit_circuit(n, ops):
    qc = QuantumCircuit(n, n)
    for item in ops:
        if len(item) == 2:
            g, q = item
            if g == "H": qc.h(q)
            elif g == "X": qc.x(q)
            elif g == "Y": qc.y(q)
            elif g == "Z": qc.z(q)
            elif g == "S": qc.s(q)
            elif g == "T": qc.t(q)
            else: raise ValueError(g)
        else:
            g, a, b = item
            if g == "CNOT": qc.cx(a, b)
            elif g == "CZ": qc.cz(a, b)
            elif g == "SWAP": qc.swap(a, b)
            elif g == "ISWAP": qc.iswap(a, b)
            else: raise ValueError(g)
    qc.measure(range(n), range(n))
    return qc

def build_noise_model_depol_each_gate(p: float):
    if p <= 0:
        return None

    nm = NoiseModel()
    err1 = depolarizing_error(p, 1)
    err2 = err1.tensor(err1)  # independent 1q depol on both qubits of 2q gates

    # 1q gates
    for g in ["h", "x", "y", "z", "s", "t"]:
        nm.add_all_qubit_quantum_error(err1, g)

    # 2q gates
    for g in ["cx", "cz", "swap", "iswap"]:
        nm.add_all_qubit_quantum_error(err2, g)

    return nm

def bench_one(n, depth, shots, noise_p, repeats, seed):
    ops = make_random_circuit(n, depth, seed=seed)
    qc = build_qiskit_circuit(n, ops)

    if noise_p > 0:
        method = "density_matrix"
        noise_model = build_noise_model_depol_each_gate(noise_p)
    else:
        method = "statevector"
        noise_model = None

    backend = AerSimulator(method=method, noise_model=noise_model)

    # transpile with no optimization to keep structure stable
    tqc = transpile(qc, backend=backend, optimization_level=0)

    # warm-up
    backend.run(tqc, shots=min(10, shots)).result()

    times = []
    rss_peaks = []

    for _ in range(repeats):
        rss0 = rss_mb()
        t0 = time.perf_counter()
        result = backend.run(tqc, shots=shots).result()
        _ = result.get_counts()
        t1 = time.perf_counter()
        rss1 = rss_mb()

        times.append(t1 - t0)
        if rss0 is not None and rss1 is not None:
            rss_peaks.append(max(rss0, rss1))
        elif rss1 is not None:
            rss_peaks.append(rss1)

    out = {
        "engine": "qiskit_aer",
        "method": method,
        "n": n,
        "depth": depth,
        "shots": shots,
        "noise_p": float(noise_p),
        "repeats": repeats,
        "mean_s": float(np.mean(times)),
        "std_s": float(np.std(times)),
        "min_s": float(np.min(times)),
        "max_s": float(np.max(times)),
    }
    if rss_peaks:
        out["rss_peak_mb"] = float(np.max(rss_peaks))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--depth", type=int, default=10)
    ap.add_argument("--shots", type=int, default=1024)
    ap.add_argument("--noise_p", type=float, default=0.0)
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    res = bench_one(args.n, args.depth, args.shots, args.noise_p, args.repeats, args.seed)
    print(res)

if __name__ == "__main__":
    main()
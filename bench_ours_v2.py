# bench_ours_v2.py
import argparse
import time
import numpy as np
import tracemalloc

try:
    import resource  # Unix (Linux/macOS)
except ImportError:
    resource = None  # Windows

from quantum_sim.simulator import Simulator

ONEQ = ["H", "X", "Y", "Z", "S", "T"]
TWOQ = ["CNOT", "CZ", "SWAP", "ISWAP"]


def format_time(seconds: float) -> str:
    """Pretty time format in seconds + milliseconds."""
    return f"{seconds:.6f} s  ({seconds * 1000:.3f} ms)"


def rss_mb():
    """Best-effort RSS in MB (works well on Linux/macOS; Windows returns None)."""
    if resource is None:
        return None
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # On Linux ru_maxrss is KB, on macOS it's bytes.
    if r > 10_000_000:  # likely bytes
        return r / (1024 * 1024)
    return r / 1024.0


def make_random_circuit(n, depth, seed=0):
    rng = np.random.default_rng(seed)
    ops = []
    for _ in range(depth):
        # 1Q layer
        for q in range(n):
            g = rng.choice(ONEQ)
            ops.append({"name": g, "targets": [int(q)]})

        # 2Q layer (pair neighbors)
        pairs = [(i, i + 1) for i in range(0, n - 1, 2)]
        rng.shuffle(pairs)
        for a, b in pairs:
            g2 = rng.choice(TWOQ)
            if g2 in ("CNOT", "CZ"):
                ops.append({"name": g2, "control": int(a), "target": int(b)})
            else:
                ops.append({"name": g2, "q1": int(a), "q2": int(b)})
    return ops


def build_noise_model(noise_p: float):
    if noise_p and noise_p > 0:
        return {"channels": [{"after": "each_gate", "type": "depolarizing", "p": float(noise_p)}]}
    return None


def run_ours_evolve_only(sim: Simulator, circuit, noise_model):
    """Copy of sim.run_circuit minus measure_all. No changes to simulator code."""
    from quantum_sim import gates

    use_noise = isinstance(noise_model, dict)
    if use_noise:
        sim.reset_density()
        channels = (noise_model.get("channels", []) or [])
    else:
        sim.reset()
        channels = []

    def apply_post_gate_noise(op, gate_name_upper: str):
        if not use_noise:
            return
        affected = sim._affected_qubits_from_op(op)
        gname = gate_name_upper.lower()

        for ch in channels:
            after = str(ch.get("after", "")).lower()
            ctype = str(ch.get("type", "")).lower()
            if ctype == "readout_error":
                continue
            if after == "each_gate" or after == gname:
                p = float(ch.get("p", 0.0))
                for q in affected:
                    sim.apply_kraus_channel_1q(ctype, p, q)

    for op in circuit:
        name = str(op.get("name", "")).upper()

        if name in ("H", "X", "Y", "Z", "S", "T"):
            mapping = {"H": gates.H, "X": gates.X, "Y": gates.Y, "Z": gates.Z, "S": gates.S, "T": gates.T}
            targets = op.get("targets")
            if not isinstance(targets, (list, tuple)) or len(targets) == 0:
                raise ValueError(f"{name} requires 'targets': [..]")
            for t in targets:
                sim.apply_single_qubit_gate_auto(mapping[name], int(t))
            apply_post_gate_noise(op, name)

        elif name == "CNOT":
            c = op.get("control")
            t = op.get("target")
            if c is None or t is None:
                raise ValueError("CNOT requires 'control' and 'target'")
            sim.apply_cnot(int(c), int(t))
            apply_post_gate_noise(op, name)

        elif name == "CZ":
            c = op.get("control")
            t = op.get("target")
            if c is None or t is None:
                raise ValueError("CZ requires 'control' and 'target'")
            sim.apply_two_qubit_gate_auto(gates.CZ_4x4, int(c), int(t))
            apply_post_gate_noise(op, name)

        elif name in ("SWAP", "ISWAP"):
            q1 = op.get("q1")
            q2 = op.get("q2")
            if q1 is None or q2 is None:
                raise ValueError(f"{name} requires 'q1' and 'q2'")
            G = gates.SWAP_4x4 if name == "SWAP" else gates.ISWAP_4x4
            sim.apply_two_qubit_gate_auto(G, int(q1), int(q2))
            apply_post_gate_noise(op, name)

        else:
            raise ValueError(f"Unsupported op in benchmark generator: {name}")


def bench_one(n, depth, shots, noise_p, repeats, seed, mode, use_tracemalloc, verbose_runs):
    circuit = make_random_circuit(n, depth, seed=seed)
    noise_model = build_noise_model(noise_p)

    # warm-up
    sim = Simulator(n)
    if mode == "evolve_only":
        run_ours_evolve_only(sim, circuit, noise_model)
    else:
        sim.run_circuit(circuit, shots=min(10, shots), noise_model=noise_model)

    times = []
    rss_peaks = []
    tm_peaks = []

    for r in range(repeats):
        if use_tracemalloc:
            tracemalloc.start()

        rss0 = rss_mb()
        sim = Simulator(n)

        t0 = time.perf_counter()
        if mode == "evolve_only":
            run_ours_evolve_only(sim, circuit, noise_model)
        else:
            sim.run_circuit(circuit, shots=shots, noise_model=noise_model)
        t1 = time.perf_counter()

        dt = t1 - t0
        times.append(dt)

        if verbose_runs:
            print(f"Run {r+1}/{repeats}: {format_time(dt)}")

        rss1 = rss_mb()
        if rss0 is not None and rss1 is not None:
            rss_peaks.append(max(rss0, rss1))
        elif rss1 is not None:
            rss_peaks.append(rss1)

        if use_tracemalloc:
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            tm_peaks.append(peak / (1024 * 1024))

    out = {
        "engine": "ours",
        "mode": mode,
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
    if tm_peaks:
        out["py_alloc_peak_mb"] = float(np.max(tm_peaks))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--depth", type=int, default=10)
    ap.add_argument("--shots", type=int, default=1024)
    ap.add_argument("--noise_p", type=float, default=0.0)
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--mode", choices=["evolve_only", "full"], default="full")
    ap.add_argument("--tracemalloc", action="store_true")
    ap.add_argument("--verbose_runs", action="store_true", help="Print time for each individual repeat run")
    args = ap.parse_args()

    global_start = time.perf_counter()

    res = bench_one(
        n=args.n,
        depth=args.depth,
        shots=args.shots,
        noise_p=args.noise_p,
        repeats=args.repeats,
        seed=args.seed,
        mode=args.mode,
        use_tracemalloc=args.tracemalloc,
        verbose_runs=args.verbose_runs,
    )

    global_end = time.perf_counter()
    total = global_end - global_start

    print("\n=== BENCHMARK RESULT (OURS) ===")
    print(f"n={res['n']} depth={res['depth']} shots={res['shots']} noise_p={res['noise_p']} mode={res['mode']}")
    print(f"Mean time: {format_time(res['mean_s'])}")
    print(f"Std  time: {format_time(res['std_s'])}")
    print(f"Min  time: {format_time(res['min_s'])}")
    print(f"Max  time: {format_time(res['max_s'])}")

    if "rss_peak_mb" in res:
        print(f"RSS peak : {res['rss_peak_mb']:.2f} MB")
    if "py_alloc_peak_mb" in res:
        print(f"Py alloc : {res['py_alloc_peak_mb']:.2f} MB (tracemalloc peak)")

    print("\n=== TOTAL BENCHMARK TIME ===")
    print(f"{format_time(total)}")

    # Also print raw dict for easy JSON-lines logging if you want
    print("\nRAW:", res)


if __name__ == "__main__":
    main()
# bench_accuracy_vs_aer.py
import argparse
import math
from typing import Any, Dict, List, Optional

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import DensityMatrix, Statevector, state_fidelity
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

from quantum_sim.simulator import Simulator
from quantum_sim import gates as our_gates


# ============================================================
# Circuit presets
# ============================================================

def preset_bell() -> Dict[str, Any]:
    return {
        "name": "bell",
        "n": 2,
        "ops": [
            {"name": "H", "targets": [0]},
            {"name": "CNOT", "control": 0, "target": 1},
        ],
    }


def preset_ghz() -> Dict[str, Any]:
    return {
        "name": "ghz",
        "n": 3,
        "ops": [
            {"name": "H", "targets": [0]},
            {"name": "CNOT", "control": 0, "target": 1},
            {"name": "CNOT", "control": 0, "target": 2},
        ],
    }


def preset_deutsch_constant_0() -> Dict[str, Any]:
    return {
        "name": "deutsch_constant_0",
        "n": 2,
        "ops": [
            {"name": "X", "targets": [1]},
            {"name": "H", "targets": [0]},
            {"name": "H", "targets": [1]},
            {"name": "H", "targets": [0]},
        ],
    }


def preset_deutsch_constant_1() -> Dict[str, Any]:
    return {
        "name": "deutsch_constant_1",
        "n": 2,
        "ops": [
            {"name": "X", "targets": [1]},
            {"name": "H", "targets": [0]},
            {"name": "H", "targets": [1]},
            {"name": "X", "targets": [1]},
            {"name": "H", "targets": [0]},
        ],
    }


def preset_deutsch_balanced_identity() -> Dict[str, Any]:
    return {
        "name": "deutsch_balanced_identity",
        "n": 2,
        "ops": [
            {"name": "X", "targets": [1]},
            {"name": "H", "targets": [0]},
            {"name": "H", "targets": [1]},
            {"name": "CNOT", "control": 0, "target": 1},
            {"name": "H", "targets": [0]},
        ],
    }


def preset_deutsch_balanced_not() -> Dict[str, Any]:
    return {
        "name": "deutsch_balanced_not",
        "n": 2,
        "ops": [
            {"name": "X", "targets": [1]},
            {"name": "H", "targets": [0]},
            {"name": "H", "targets": [1]},
            {"name": "CNOT", "control": 0, "target": 1},
            {"name": "X", "targets": [1]},
            {"name": "H", "targets": [0]},
        ],
    }


def preset_grover_2q_11() -> Dict[str, Any]:
    return {
        "name": "grover_2q_11",
        "n": 2,
        "ops": [
            {"name": "H", "targets": [0]},
            {"name": "H", "targets": [1]},
            {"name": "CZ", "control": 0, "target": 1},
            {"name": "H", "targets": [0]},
            {"name": "H", "targets": [1]},
            {"name": "X", "targets": [0]},
            {"name": "X", "targets": [1]},
            {"name": "CZ", "control": 0, "target": 1},
            {"name": "X", "targets": [0]},
            {"name": "X", "targets": [1]},
            {"name": "H", "targets": [0]},
            {"name": "H", "targets": [1]},
        ],
    }


PRESET_BUILDERS = {
    "bell": preset_bell,
    "ghz": preset_ghz,
    "deutsch_constant_0": preset_deutsch_constant_0,
    "deutsch_constant_1": preset_deutsch_constant_1,
    "deutsch_balanced_identity": preset_deutsch_balanced_identity,
    "deutsch_balanced_not": preset_deutsch_balanced_not,
    "grover_2q_11": preset_grover_2q_11,
}


# ============================================================
# Random circuit generator
# ============================================================

ONEQ = ["H", "X", "Y", "Z", "S", "T"]
TWOQ = ["CNOT", "CZ", "SWAP", "ISWAP"]


def make_random_circuit(n: int, depth: int, seed: int = 0) -> List[Dict[str, Any]]:
    rng = np.random.default_rng(seed)
    ops: List[Dict[str, Any]] = []

    for _ in range(depth):
        for q in range(n):
            g = str(rng.choice(ONEQ))
            ops.append({"name": g, "targets": [int(q)]})

        pairs = [(i, i + 1) for i in range(0, n - 1, 2)]
        rng.shuffle(pairs)
        for a, b in pairs:
            g2 = str(rng.choice(TWOQ))
            if g2 in ("CNOT", "CZ"):
                ops.append({"name": g2, "control": int(a), "target": int(b)})
            else:
                ops.append({"name": g2, "q1": int(a), "q2": int(b)})

    return ops


# ============================================================
# Qiskit helpers
# ============================================================

def build_qiskit_circuit(n: int, ops: List[Dict[str, Any]]) -> QuantumCircuit:
    qc = QuantumCircuit(n)

    for op in ops:
        name = str(op["name"]).upper()

        if name == "H":
            qc.h(op["targets"][0])
        elif name == "X":
            qc.x(op["targets"][0])
        elif name == "Y":
            qc.y(op["targets"][0])
        elif name == "Z":
            qc.z(op["targets"][0])
        elif name == "S":
            qc.s(op["targets"][0])
        elif name == "T":
            qc.t(op["targets"][0])

        elif name == "RX":
            qc.rx(float(op["theta"]), int(op["target"]))
        elif name == "RY":
            qc.ry(float(op["theta"]), int(op["target"]))
        elif name == "RZ":
            qc.rz(float(op["theta"]), int(op["target"]))
        elif name in ("PHASE", "P"):
            qc.p(float(op["phi"]), int(op["target"]))
        elif name == "U3":
            qc.u(float(op["theta"]), float(op["phi"]), float(op["lam"]), int(op["target"]))

        elif name == "CNOT":
            qc.cx(int(op["control"]), int(op["target"]))
        elif name == "CZ":
            qc.cz(int(op["control"]), int(op["target"]))
        elif name == "SWAP":
            qc.swap(int(op["q1"]), int(op["q2"]))
        elif name == "ISWAP":
            qc.iswap(int(op["q1"]), int(op["q2"]))

        elif name in ("CCNOT", "TOFFOLI"):
            qc.ccx(int(op["control1"]), int(op["control2"]), int(op["target"]))

        else:
            raise ValueError(f"Unsupported op for Qiskit conversion: {name}")

    return qc


def build_noise_model_depol_each_gate(p: float) -> Optional[NoiseModel]:
    if p <= 0:
        return None

    nm = NoiseModel()
    err1 = depolarizing_error(p, 1)
    err2 = err1.tensor(err1)

    for g in ["h", "x", "y", "z", "s", "t", "rx", "ry", "rz", "p", "u"]:
        nm.add_all_qubit_quantum_error(err1, g)

    for g in ["cx", "cz", "swap", "iswap", "ccx"]:
        nm.add_all_qubit_quantum_error(err2, g)

    return nm


def qiskit_reorder_permutation(n: int) -> List[int]:
    """
    Returns perm such that:
        our_state[i] = qiskit_state[perm[i]]
    because our basis strings are q0 q1 ... q_{n-1} (MSB-first)
    while Qiskit statevector indexing is little-endian.
    """
    perm = []
    for i in range(2**n):
        b = format(i, f"0{n}b")
        qiskit_idx = int(b[::-1], 2)
        perm.append(qiskit_idx)
    return perm


def reorder_qiskit_statevector_to_ours(qiskit_sv: np.ndarray, n: int) -> np.ndarray:
    perm = qiskit_reorder_permutation(n)
    return np.asarray(qiskit_sv, dtype=complex)[perm]


def reorder_qiskit_density_to_ours(qiskit_dm: np.ndarray, n: int) -> np.ndarray:
    perm = qiskit_reorder_permutation(n)
    qdm = np.asarray(qiskit_dm, dtype=complex)
    return qdm[np.ix_(perm, perm)]


# ============================================================
# Our simulator: evolution only
# ============================================================

def evolve_ours(n: int, circuit: List[Dict[str, Any]], noise_model: Optional[Dict[str, Any]]) -> Simulator:
    sim = Simulator(n)
    use_noise = isinstance(noise_model, dict)

    if use_noise:
        sim.reset_density()
        channels = (noise_model.get("channels", []) or [])
    else:
        sim.reset()
        channels = []

    def apply_post_gate_noise(op: Dict[str, Any], gate_name_upper: str):
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
            mapping = {
                "H": our_gates.H,
                "X": our_gates.X,
                "Y": our_gates.Y,
                "Z": our_gates.Z,
                "S": our_gates.S,
                "T": our_gates.T,
            }
            for t in op["targets"]:
                sim.apply_single_qubit_gate_auto(mapping[name], int(t))
            apply_post_gate_noise(op, name)

        elif name == "RX":
            sim.apply_single_qubit_gate_auto(our_gates.Rx(float(op["theta"])), int(op["target"]))
            apply_post_gate_noise(op, name)

        elif name == "RY":
            sim.apply_single_qubit_gate_auto(our_gates.Ry(float(op["theta"])), int(op["target"]))
            apply_post_gate_noise(op, name)

        elif name == "RZ":
            sim.apply_single_qubit_gate_auto(our_gates.Rz(float(op["theta"])), int(op["target"]))
            apply_post_gate_noise(op, name)

        elif name in ("PHASE", "P"):
            sim.apply_single_qubit_gate_auto(our_gates.Phase(float(op["phi"])), int(op["target"]))
            apply_post_gate_noise(op, name)

        elif name == "U3":
            sim.apply_single_qubit_gate_auto(
                our_gates.U3(float(op["theta"]), float(op["phi"]), float(op["lam"])),
                int(op["target"]),
            )
            apply_post_gate_noise(op, name)

        elif name == "CNOT":
            sim.apply_cnot(int(op["control"]), int(op["target"]))
            apply_post_gate_noise(op, name)

        elif name == "CZ":
            sim.apply_two_qubit_gate_auto(our_gates.CZ_4x4, int(op["control"]), int(op["target"]))
            apply_post_gate_noise(op, name)

        elif name == "SWAP":
            sim.apply_two_qubit_gate_auto(our_gates.SWAP_4x4, int(op["q1"]), int(op["q2"]))
            apply_post_gate_noise(op, name)

        elif name == "ISWAP":
            sim.apply_two_qubit_gate_auto(our_gates.ISWAP_4x4, int(op["q1"]), int(op["q2"]))
            apply_post_gate_noise(op, name)

        elif name in ("CCNOT", "TOFFOLI"):
            sim.apply_ccnot_auto(int(op["control1"]), int(op["control2"]), int(op["target"]))
            apply_post_gate_noise(op, name)

        else:
            raise ValueError(f"Unsupported op for our evolution benchmark: {name}")

    return sim


# ============================================================
# Metrics
# ============================================================

def probabilities_from_statevector(state: np.ndarray) -> np.ndarray:
    return np.abs(np.asarray(state, dtype=complex)) ** 2


def probabilities_from_density(rho: np.ndarray) -> np.ndarray:
    p = np.real(np.diag(np.asarray(rho, dtype=complex)))
    p = np.clip(p, 0.0, 1.0)
    s = p.sum()
    return p / s if s > 0 else p


def tvd(p: np.ndarray, q: np.ndarray) -> float:
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    return 0.5 * float(np.sum(np.abs(p - q)))


def max_abs_diff(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.max(np.abs(np.asarray(a) - np.asarray(b))))


# ============================================================
# Core comparison
# ============================================================

def compare_once(
    n: int,
    ops: List[Dict[str, Any]],
    label: str,
    noise_p: float = 0.0,
) -> Dict[str, Any]:
    if noise_p < 0:
        raise ValueError("noise_p must be >= 0")

    our_noise_model = None
    if noise_p > 0:
        our_noise_model = {
            "channels": [
                {"after": "each_gate", "type": "depolarizing", "p": float(noise_p)}
            ]
        }

    # ---------- ours ----------
    sim = evolve_ours(n, ops, our_noise_model)

    # ---------- qiskit aer ----------
    qc = build_qiskit_circuit(n, ops)

    if noise_p > 0:
        qc.save_density_matrix()
        aer = AerSimulator(method="density_matrix", noise_model=build_noise_model_depol_each_gate(noise_p))
    else:
        qc.save_statevector()
        aer = AerSimulator(method="statevector")

    tqc = transpile(qc, aer, optimization_level=0)
    result = aer.run(tqc).result()
    data = result.data(0)

    out: Dict[str, Any] = {
        "label": label,
        "n_qubits": n,
        "n_ops": len(ops),
        "noise_p": float(noise_p),
        "mode": "density_matrix" if noise_p > 0 else "statevector",
    }

    if noise_p > 0:
        our_rho = np.asarray(sim.rho, dtype=complex)
        aer_rho = reorder_qiskit_density_to_ours(np.asarray(data["density_matrix"], dtype=complex), n)

        our_probs = probabilities_from_density(our_rho)
        aer_probs = probabilities_from_density(aer_rho)

        out["fidelity"] = float(state_fidelity(DensityMatrix(our_rho), DensityMatrix(aer_rho)))
        out["frobenius_diff"] = float(np.linalg.norm(our_rho - aer_rho))
        out["max_abs_rho_diff"] = max_abs_diff(our_rho, aer_rho)
        out["prob_tvd"] = tvd(our_probs, aer_probs)
    else:
        our_sv = np.asarray(sim.state, dtype=complex)
        aer_sv = reorder_qiskit_statevector_to_ours(np.asarray(data["statevector"], dtype=complex), n)

        our_probs = probabilities_from_statevector(our_sv)
        aer_probs = probabilities_from_statevector(aer_sv)

        out["fidelity"] = float(state_fidelity(Statevector(our_sv), Statevector(aer_sv)))
        out["max_abs_amp_diff"] = max_abs_diff(our_sv, aer_sv)
        out["prob_tvd"] = tvd(our_probs, aer_probs)

    return out


# ============================================================
# CLI
# ============================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--preset",
        type=str,
        choices=list(PRESET_BUILDERS.keys()) + ["random"],
        required=True,
    )
    ap.add_argument("--n", type=int, default=2, help="Used only for preset=random")
    ap.add_argument("--depth", type=int, default=6, help="Used only for preset=random")
    ap.add_argument("--seed", type=int, default=0, help="Used only for preset=random")
    ap.add_argument("--noise_p", type=float, default=0.0)
    args = ap.parse_args()

    if args.preset == "random":
        ops = make_random_circuit(args.n, args.depth, seed=args.seed)
        label = f"random_n{args.n}_d{args.depth}_s{args.seed}"
        n = args.n
    else:
        built = PRESET_BUILDERS[args.preset]()
        ops = built["ops"]
        label = built["name"]
        n = built["n"]

    res = compare_once(n=n, ops=ops, label=label, noise_p=args.noise_p)

    print("\n=== ACCURACY COMPARISON: OURS vs QISKIT AER ===")
    for k, v in res.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
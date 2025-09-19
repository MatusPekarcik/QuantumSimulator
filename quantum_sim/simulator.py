import numpy as np
from functools import reduce
import json
from typing import Dict, Optional, List

def _kron_n(ops: List[np.ndarray]) -> np.ndarray:
    """Kronecker product of a list of matrices (left to right)."""
    return reduce(lambda a, b: np.kron(a, b), ops)

class Simulator:
    """
    Very small statevector simulator for N qubits.
    Qubit indexing: 0 is the leftmost (most significant) in tensor product.
    """

    def __init__(self, n_qubits: int):
        self.n = n_qubits
        self.dim = 2 ** n_qubits
        # initial state |0...0>
        self.state = np.zeros((self.dim,), dtype=complex)
        self.state[0] = 1.0

    def apply_single_qubit_gate(self, gate: np.ndarray, target: int):
        """
        Apply a 2x2 gate to a single qubit `target` (0..n-1).
        We build the full operator as I x ... x gate x ... x I and apply it.
        """
        if gate.shape != (2, 2):
            raise ValueError("Gate must be 2x2")
        if not (0 <= target < self.n):
            raise IndexError("target out of range")
        ops = []
        for q in range(self.n):
            ops.append(gate if q == target else np.eye(2, dtype=complex))
        full = _kron_n(ops)
        self.state = full @ self.state

    def measure_all(self, shots: int = 1024) -> Dict[str, int]:
        """
        Measure all qubits, return histogram of bitstrings.
        Bitstring format: e.g. '010' where index 0 is leftmost qubit.
        """
        probs = np.abs(self.state) ** 2
        outcomes = np.random.choice(self.dim, size=shots, p=probs)
        counts: Dict[str, int] = {}
        for idx in outcomes:
            b = format(idx, f"0{self.n}b")  # binary string of length n
            counts[b] = counts.get(b, 0) + 1
        return counts

    def run_circuit(self, circuit: List[Dict], shots: int = 1024) -> Dict:
        """
        circuit: list of operations, each op is {"name": "H", "targets": [0]}
        Supported ops: "H", "X" for now.
        """
        # reset to |0...0>
        self.state = np.zeros((self.dim,), dtype=complex)
        self.state[0] = 1.0

        for op in circuit:
            name = op.get("name", "").upper()
            targets = op.get("targets", [])
            if name == "H":
                from .gates import H as _H
                for t in targets:
                    self.apply_single_qubit_gate(_H, t)
            elif name == "X":
                from .gates import X as _X
                for t in targets:
                    self.apply_single_qubit_gate(_X, t)
            else:
                raise ValueError(f"Unsupported op: {name}")

        counts = self.measure_all(shots=shots)
        return {"counts": counts, "shots": shots}


    def probabilities(self) -> dict:
        """Return full distribution: bitstring -> probability (exact)."""
        probs = np.abs(self.state) ** 2
        return {format(i, f"0{self.n}b"): float(probs[i]) for i in range(self.dim)}

    def marginal_probability(self, target: int) -> dict:
        """
        Return marginal probability for specified qubit:
        {'0': p0, '1': p1}
        target: qubit index 0..n-1 where 0 is leftmost (most significant).
        """
        if not (0 <= target < self.n):
            raise IndexError("target out of range")
        probs = np.abs(self.state) ** 2
        p0 = 0.0
        # bit position inside integer: most-significant is n-1-target when indexing from LSB=0
        shift = self.n - 1 - target
        for idx, p in enumerate(probs):
            bit = (idx >> shift) & 1
            if bit == 0:
                p0 += p
        p1 = 1.0 - p0
        return {"0": float(p0), "1": float(p1)}

    
# --------- convenience loader ----------
    @classmethod
    def from_json(cls, json_str: str) -> "Simulator":
        data = json.loads(json_str)
        n = int(data["n_qubits"])
        return cls(n)

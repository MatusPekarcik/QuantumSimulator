# quantum_sim/circuit.py

import json
from typing import List, Dict, Any

from .simulator import Simulator


class Circuit:
    """
    High-level circuit builder and JSON-compatible representation.

    - Holds n_qubits and an ordered list of gate operations (dicts).
    - Provides fluent methods like h(), x(), cnot(), rz(), ccnot().
    - Can be serialized to/from JSON.
    - Can be executed via the Simulator.run_circuit() method.
    """

    def __init__(self, n_qubits: int):
        if n_qubits < 1:
            raise ValueError("Circuit must have at least one qubit")
        self.n_qubits = n_qubits
        self.operations: List[Dict[str, Any]] = []

    # ------------------------
    # Internal helpers
    # ------------------------
    def _check_qubit(self, q: int):
        if not (0 <= q < self.n_qubits):
            raise IndexError(f"Qubit index {q} out of range for {self.n_qubits} qubits")

    def _check_two_qubits(self, q1: int, q2: int):
        self._check_qubit(q1)
        self._check_qubit(q2)
        if q1 == q2:
            raise ValueError("q1 and q2 must be distinct")

    def _check_three_qubits(self, q1: int, q2: int, q3: int):
        self._check_qubit(q1)
        self._check_qubit(q2)
        self._check_qubit(q3)
        if len({q1, q2, q3}) < 3:
            raise ValueError("control1, control2, and target must be distinct qubits")

    # ------------------------
    # Single-qubit gates (fixed)
    # ------------------------
    def h(self, target: int):
        self._check_qubit(target)
        self.operations.append({"name": "H", "targets": [target]})
        return self

    def x(self, target: int):
        self._check_qubit(target)
        self.operations.append({"name": "X", "targets": [target]})
        return self

    def y(self, target: int):
        self._check_qubit(target)
        self.operations.append({"name": "Y", "targets": [target]})
        return self

    def z(self, target: int):
        self._check_qubit(target)
        self.operations.append({"name": "Z", "targets": [target]})
        return self

    def s(self, target: int):
        self._check_qubit(target)
        self.operations.append({"name": "S", "targets": [target]})
        return self

    def t(self, target: int):
        self._check_qubit(target)
        self.operations.append({"name": "T", "targets": [target]})
        return self

    # ------------------------
    # Parameterized 1-qubit gates
    # ------------------------
    def rx(self, target: int, theta: float):
        self._check_qubit(target)
        self.operations.append({"name": "RX", "target": target, "theta": float(theta)})
        return self

    def ry(self, target: int, theta: float):
        self._check_qubit(target)
        self.operations.append({"name": "RY", "target": target, "theta": float(theta)})
        return self

    def rz(self, target: int, theta: float):
        self._check_qubit(target)
        self.operations.append({"name": "RZ", "target": target, "theta": float(theta)})
        return self

    def phase(self, target: int, phi: float):
        """Phase gate P(phi) (same as 'PHASE' / 'P' in run_circuit)."""
        self._check_qubit(target)
        self.operations.append({"name": "PHASE", "target": target, "phi": float(phi)})
        return self

    def u3(self, target: int, theta: float, phi: float, lam: float):
        self._check_qubit(target)
        self.operations.append({
            "name": "U3",
            "target": target,
            "theta": float(theta),
            "phi": float(phi),
            "lam": float(lam),
        })
        return self

    # ------------------------
    # Two-qubit gates
    # ------------------------
    def cnot(self, control: int, target: int):
        self._check_two_qubits(control, target)
        self.operations.append({"name": "CNOT", "control": control, "target": target})
        return self

    def cz(self, control: int, target: int):
        self._check_two_qubits(control, target)
        self.operations.append({"name": "CZ", "control": control, "target": target})
        return self

    def swap(self, q1: int, q2: int):
        self._check_two_qubits(q1, q2)
        self.operations.append({"name": "SWAP", "q1": q1, "q2": q2})
        return self

    def iswap(self, q1: int, q2: int):
        self._check_two_qubits(q1, q2)
        self.operations.append({"name": "ISWAP", "q1": q1, "q2": q2})
        return self

    def custom_2q(self, matrix, q1: int, q2: int):
        """
        Custom 4x4 two-qubit unitary. Note: matrix must be JSON-serializable
        if you plan to call to_json() (e.g., convert to nested lists).
        """
        self._check_two_qubits(q1, q2)
        self.operations.append({"name": "CUSTOM_2Q", "matrix": matrix, "q1": q1, "q2": q2})
        return self

    # ------------------------
    # Three-qubit (Toffoli / CCNOT)
    # ------------------------
    def ccnot(self, control1: int, control2: int, target: int):
        self._check_three_qubits(control1, control2, target)
        self.operations.append({
            "name": "CCNOT",
            "control1": control1,
            "control2": control2,
            "target": target,
        })
        return self

    # alias
    def toffoli(self, control1: int, control2: int, target: int):
        return self.ccnot(control1, control2, target)

    # ------------------------
    # Introspection / debug
    # ------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Python-native representation (good for direct JSON use)."""
        return {
            "n_qubits": self.n_qubits,
            "gates": self.operations,
        }

    def to_json(self) -> str:
        """JSON string representation suitable for sending over network."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Circuit":
        n = int(data["n_qubits"])
        qc = cls(n)
        qc.operations = list(data.get("gates", []))
        return qc

    @classmethod
    def from_json(cls, json_str: str) -> "Circuit":
        data = json.loads(json_str)
        return cls.from_dict(data)

    # ------------------------
    # Simulation hook
    # ------------------------
    def run(self, shots: int = 1024) -> Dict[str, Any]:
        """
        Execute this circuit on a fresh Simulator instance.

        Returns the same dict as Simulator.run_circuit:
          {"counts": {...}, "shots": shots}
        """
        sim = Simulator(self.n_qubits)
        return sim.run_circuit(self.operations, shots=shots)

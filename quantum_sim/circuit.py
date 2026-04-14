# quantum_sim/circuit.py

import json
from typing import List, Dict, Any, Optional

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
        self.observables: List[Dict[str, Any]] = []
        self.witnesses: List[Dict[str, Any]] = []

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
        
    def expval(self, pauli: str, qubits: List[int]):
        """
        Request an expectation value for a Pauli-string observable.
        Example: qc.expval("ZZ", [0,1])
        """
        if len(pauli) != len(qubits):
            raise ValueError("pauli length must match number of qubits in observable")
        for q in qubits:
            self._check_qubit(q)
        if len(set(qubits)) != len(qubits):
            raise ValueError("observable qubits must be distinct")

        self.observables.append({"pauli": pauli.upper(), "qubits": list(qubits)})
        return self

    def add_linear_witness(self, name: str, terms: List[Dict[str, Any]], bound: float, violates_if: str = ">"):
        """
        Register a general linear entanglement witness:

            W = sum_k coef_k * <Pauli_k(qubits_k)>

        terms: list of dicts like:
            {"pauli": "XX", "qubits": [0,1], "coef": 1.0}

        bound: separable bound B
        violates_if: ">" or "<" meaning entanglement is certified if W > B (or W < B)
        """
        if violates_if not in (">", "<"):
            raise ValueError("violates_if must be '>' or '<'")

        if not isinstance(terms, list) or len(terms) == 0:
            raise ValueError("terms must be a non-empty list")

        cleaned_terms = []
        for t in terms:
            pauli = str(t.get("pauli", "")).upper()
            qubits = t.get("qubits")
            coef = t.get("coef", 1.0)

            if not pauli:
                raise ValueError("each term must have non-empty 'pauli'")
            if any(c not in "IXYZ" for c in pauli):
                raise ValueError("term pauli may contain only I, X, Y, Z")
            if not isinstance(qubits, list) or len(qubits) != len(pauli):
                raise ValueError("term 'qubits' must be a list with same length as 'pauli'")
            if len(set(qubits)) != len(qubits):
                raise ValueError("term qubits must be distinct")

            for q in qubits:
                self._check_qubit(int(q))

            cleaned_terms.append({
                "pauli": pauli,
                "qubits": [int(q) for q in qubits],
                "coef": float(coef),
            })

        self.witnesses.append({
            "type": "linear",
            "name": str(name),
            "terms": cleaned_terms,
            "bound": float(bound),
            "violates_if": violates_if,
        })
        return self


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
            "observables": self.observables,
            "witnesses": self.witnesses,
        }

    def to_json(self) -> str:
        """JSON string representation suitable for sending over network."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Circuit":
        n = int(data["n_qubits"])
        qc = cls(n)
        qc.operations = list(data.get("gates", []))
        qc.observables = list(data.get("observables", []))
        qc.witnesses = list(data.get("witnesses", []))
        return qc

    @classmethod
    def from_json(cls, json_str: str) -> "Circuit":
        data = json.loads(json_str)
        return cls.from_dict(data)

    # ------------------------
    # Simulation hook
    # ------------------------
    def run(self, shots: int = 1024, noise_model: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        sim = Simulator(self.n_qubits)

        result = sim.run_circuit(self.operations, shots=shots, noise_model=noise_model)

        probabilities = sim.probabilities()
        marginals = {
            str(q): sim.marginal_probability(q)
            for q in range(self.n_qubits)
        }

        expectations = {
            str(q): sim.expectation_values(q)
            for q in range(self.n_qubits)
        }

        # ------------------------
        # Pauli observables
        # ------------------------
        pauli_expectations = []
        for obs in self.observables:
            pauli = obs["pauli"]
            qubits = obs["qubits"]
            value = sim.expectation_pauli(pauli, qubits)
            pauli_expectations.append({
                "pauli": pauli,
                "qubits": qubits,
                "value": value
            })

        # ------------------------
        # Evaluate linear witnesses
        # ------------------------
        witness_results = []

        for w in self.witnesses:
            if w.get("type") != "linear":
                continue

            name = w.get("name", "unnamed_witness")
            bound = float(w.get("bound", 0.0))
            violates_if = w.get("violates_if", ">")
            terms = w.get("terms", [])

            value = 0.0
            term_details = []

            for term in terms:
                pauli = term["pauli"]
                qubits = term["qubits"]
                coef = float(term.get("coef", 1.0))

                expv = sim.expectation_pauli(pauli, qubits)
                value += coef * expv

                term_details.append({
                    "pauli": pauli,
                    "qubits": qubits,
                    "coef": coef,
                    "expval": float(expv),
                    "contribution": float(coef * expv),
                })

            entangled = (
                value > bound + 1e-9
                if violates_if == ">"
                else value < bound - 1e-9
            )

            witness_results.append({
                "type": "linear",
                "name": name,
                "value": float(value),
                "bound": float(bound),
                "violates_if": violates_if,
                "entangled": bool(entangled),
                "terms": term_details,
            })

        # ------------------------
        # Final quantum state
        # ------------------------
        if hasattr(sim, "rho"):
            state_type = "density_matrix"
            state = [
                [[float(c.real), float(c.imag)] for c in row]
                for row in sim.rho
            ]
        else:
            state_type = "statevector"
            state = [
                [float(c.real), float(c.imag)]
                for c in sim.state
            ]

        return {
            "shots": shots,
            "counts": result["counts"],
            "probabilities": probabilities,
            "marginals": marginals,
            "expectations": expectations,
            "pauli_expectations": pauli_expectations,
            "witnesses": witness_results,
            "state_type": state_type,
            "state": state,
        }

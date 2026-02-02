# quantum_sim/simulator.py
import numpy as np
from functools import reduce
import json
from typing import Dict, List, Sequence

def _kron_n(ops: List[np.ndarray]) -> np.ndarray:
    return reduce(lambda a, b: np.kron(a, b), ops)

class Simulator:
    """
    Statevector simulator optimized with tensor reshaping & contractions.
    Qubit indexing: 0 is the leftmost (most significant) bitstring position.
    """

    def __init__(self, n_qubits: int):
        if n_qubits < 1:
            raise ValueError("n_qubits must be >= 1")
        self.n = n_qubits
        self.dim = 2 ** n_qubits
        self.reset()

    def reset(self):
        """Reset to |0...0> state."""
        self.state = np.zeros((self.dim,), dtype=complex)
        self.state[0] = 1.0

    # -------------------------
    # Efficient single-qubit gate
    # -------------------------
    def apply_single_qubit_gate(self, gate: np.ndarray, target: int):
        """
        Apply 2x2 `gate` to `target` qubit (0..n-1) using tensor contraction.
        This avoids building the full 2^n x 2^n matrix.
        """
        if gate.shape != (2, 2):
            raise ValueError("Gate must be 2x2")
        if not (0 <= target < self.n):
            raise IndexError("target out of range")

        # reshape state to (2,2,...,2)
        tensor = self.state.reshape((2,) * self.n)

        # Use tensordot: contract gate's second axis with the target axis of tensor.
        # After tensordot the new array has outputs at front, so move them back.
        # tensordot result shape: (2,) + remaining axes (order depends on target)
        res = np.tensordot(gate, tensor, axes=([1], [target]))
        # move the gate's output axis (axis 0 of res) back into position `target`
        res = np.moveaxis(res, 0, target)
        # flatten back to statevector form
        self.state = res.reshape(self.dim)

    # -------------------------
    # General 2-qubit gate (4x4)
    # -------------------------
    def apply_two_qubit_gate(self, gate4: np.ndarray, q1: int, q2: int):
        """
        Apply a 4x4 two-qubit gate acting on qubits q1 and q2 (0..n-1).
        Gate is given in basis |00>,|01>,|10>,|11> where leftmost bit is most-significant.
        We use tensor contraction with gate4 reshaped into (2,2,2,2).
        """
        if gate4.shape != (4, 4):
            raise ValueError("gate4 must be 4x4")
        if not (0 <= q1 < self.n) or not (0 <= q2 < self.n):
            raise IndexError("qubit indices out of range")
        if q1 == q2:
            raise ValueError("q1 and q2 must be distinct")

        # ensure order for contraction: use axis_list in the order we pass to tensordot
        axis_list = [q1, q2]

        # reshape state tensor
        tensor = self.state.reshape((2,) * self.n)

        # reshape gate into (out_a, out_b, in_a, in_b) using row-major mapping
        U = gate4.reshape(2, 2, 2, 2)

        # contract input indices (in_a,in_b) with the two axes (q1,q2)
        res = np.tensordot(U, tensor, axes=([2, 3], axis_list))
        # res now has output axes (out_a,out_b) at front; move them back to q1,q2 positions
        res = np.moveaxis(res, [0, 1], axis_list)
        self.state = res.reshape(self.dim)

    # Convenience wrapper for CNOT using gates defined in gates.py
    def apply_cnot(self, control: int, target: int):
        from .gates import CNOT_4x4
        # CNOT uses apply_two_qubit_gate with control as first qubit index
        self.apply_two_qubit_gate(CNOT_4x4, control, target)
   
    # -------------------------
    # CONTROLLED-U gate
    # -------------------------
    # Apply a general controlled-U for any control, target
    def apply_controlled_u(self, gate: np.ndarray, control: int, target: int):
        """
        Apply a controlled-U where `gate` is a 2x2 single-qubit unitary.
        Control and target can be any distinct qubits in [0, n-1].

        The 4x4 controlled matrix is constructed with the control as the
        *first* (more significant) qubit and the target as the second.
        """
        if gate.shape != (2, 2):
            raise ValueError("Controlled-U expects a 2x2 single-qubit gate")
        if not (0 <= control < self.n) or not (0 <= target < self.n):
            raise IndexError("control/target out of range")
        if control == target:
            raise ValueError("control and target must be different")

        from .gates import controlled  # builds 4x4 controlled-U with left qubit as control

        U4 = controlled(gate)
        # order matters: first qubit index is control, second is target
        self.apply_two_qubit_gate(U4, control, target)
    
    
    # -------------------------
    # CCNOT gate
    # -------------------------
    def apply_ccnot(self, control1: int, control2: int, target: int):
        """
        Apply a CCNOT (Toffoli) gate with two controls and one target.

        - Flips the target qubit if AND(control 1 == 1, control 2 == 1)
        - Works for arbitrary qubit indices in [0, n-1].
        """
        if not (0 <= control1 < self.n) or not (0 <= control2 < self.n) or not (0 <= target < self.n):
            raise IndexError("control/target qubit index out of range")
        if len({control1, control2, target}) < 3:
            raise ValueError("control1, control2, and target must be all distinct")

        probs_dim = self.dim
        new_state = self.state.copy()

        # Map qubit indices to bit positions in the integer basis index
        shift_c1 = self.n - 1 - control1
        shift_c2 = self.n - 1 - control2
        shift_t  = self.n - 1 - target

        for i in range(probs_dim):
            # check both controls == 1 and target == 0
            if ((i >> shift_c1) & 1) == 1 and ((i >> shift_c2) & 1) == 1 and ((i >> shift_t) & 1) == 0:
                # flip target bit from 0 to 1
                j = i | (1 << shift_t)  # set target bit to 1
                # swap amplitudes between |...0_t...> and |...1_t...>
                new_state[i], new_state[j] = new_state[j], new_state[i]

        self.state = new_state

    # -------------------------
    # Measurement and circuits
    # -------------------------
    def measure_all(self, shots: int = 1024) -> Dict[str, int]:
        """Sample `shots` outcomes according to state probabilities and return counts."""
        probs = np.abs(self.state) ** 2
        # multinomial sampling of indices
        outcomes = np.random.choice(self.dim, size=shots, p=probs)
        counts: Dict[str, int] = {}
        for idx in outcomes:
            b = format(idx, f"0{self.n}b")
            counts[b] = counts.get(b, 0) + 1
        return counts

    def run_circuit(self, circuit: List[Dict], shots: int = 1024) -> Dict:
        
        """
            circuit: list of ops; ops supported (case-insensitive "name"):
          - {"name": "H", "targets":[i,...]}
          - {"name": "X", "targets":[...]}
          - {"name": "Y", "targets":[...]}
          - {"name": "Z", "targets":[...]}
          - {"name": "S", "targets":[...]}
          - {"name": "T", "targets":[...]}

          - {"name": "RX", "target": i, "theta": float}
          - {"name": "RY", "target": i, "theta": float}
          - {"name": "RZ", "target": i, "theta": float}
          - {"name": "PHASE", "target": i, "phi": float}   # alias: "P"
          - {"name": "U3", "target": i,
             "theta": float, "phi": float, "lam": float}

          - {"name": "CNOT", "control": a, "target": b}
          - {"name": "CZ",   "control": a, "target": b}
          - {"name": "SWAP", "q1": i, "q2": j}
          - {"name": "ISWAP","q1": i, "q2": j}

          - {"name": "CCNOT",  "control1": a, "control2": b, "target": c}
          - {"name": "TOFFOLI","control1": a, "control2": b, "target": c}

          - {"name": "CUSTOM_2Q", "matrix": <4x4 numpy-like>, "q1": i, "q2": j}
        """
        
        from . import gates  # import here to avoid circulars

        self.reset()

        for op in circuit:
            name = op.get("name", "").upper()

            # ----------------------------
            # Fixed single-qubit gates (no params)
            # ----------------------------
            if name in ("H", "X", "Y", "Z", "S", "T"):
                mapping = {
                    "H": gates.H,
                    "X": gates.X,
                    "Y": gates.Y,
                    "Z": gates.Z,
                    "S": gates.S,
                    "T": gates.T,
                }
                g = mapping[name]
                targets = op.get("targets", [])
                if not isinstance(targets, (list, tuple)) or not targets:
                    raise ValueError(f"{name} gate requires non-empty 'targets' list")
                for t in targets:
                    self.apply_single_qubit_gate(g, t)

            # ----------------------------
            # Parameterized single-qubit gates
            # ----------------------------
            elif name in ("RX", "RY", "RZ", "PHASE", "P", "U3"):
                target = op.get("target")
                if target is None:
                    raise ValueError(f"{name} gate requires 'target' field")

                if name == "RX":
                    theta = op.get("theta")
                    if theta is None:
                        raise ValueError("RX requires 'theta'")
                    g = gates.Rx(theta)
                elif name == "RY":
                    theta = op.get("theta")
                    if theta is None:
                        raise ValueError("RY requires 'theta'")
                    g = gates.Ry(theta)
                elif name == "RZ":
                    theta = op.get("theta")
                    if theta is None:
                        raise ValueError("RZ requires 'theta'")
                    g = gates.Rz(theta)
                elif name in ("PHASE", "P"):
                    phi = op.get("phi")
                    if phi is None:
                        raise ValueError("PHASE gate requires 'phi'")
                    g = gates.Phase(phi)
                elif name == "U3":
                    theta = op.get("theta")
                    phi = op.get("phi")
                    lam = op.get("lam")
                    if theta is None or phi is None or lam is None:
                        raise ValueError("U3 requires 'theta', 'phi', and 'lam'")
                    g = gates.U3(theta, phi, lam)
                else:
                    raise ValueError(f"Internal error: unhandled param gate {name}")

                self.apply_single_qubit_gate(g, target)

            # ----------------------------
            # CNOT
            # ----------------------------
            elif name == "CNOT":
                c = op.get("control")
                targ = op.get("target")
                if c is None or targ is None:
                    raise ValueError("CNOT requires 'control' and 'target'")
                self.apply_cnot(c, targ)

            # ----------------------------
            # CZ
            # ----------------------------
            elif name == "CZ":
                c = op.get("control")
                targ = op.get("target")
                if c is None or targ is None:
                    raise ValueError("CZ requires 'control' and 'target'")
                self.apply_two_qubit_gate(gates.CZ_4x4, c, targ)

            # ----------------------------
            # SWAP / ISWAP
            # ----------------------------
            elif name in ("SWAP", "ISWAP"):
                q1 = op.get("q1")
                q2 = op.get("q2")
                if q1 is None or q2 is None:
                    raise ValueError(f"{name} requires 'q1' and 'q2'")
                if name == "SWAP":
                    G = gates.SWAP_4x4
                else:
                    G = gates.ISWAP_4x4
                self.apply_two_qubit_gate(G, q1, q2)

            # ----------------------------
            # CCNOT / Toffoli
            # ----------------------------
            elif name in ("CCNOT", "TOFFOLI"):
                c1 = op.get("control1")
                c2 = op.get("control2")
                targ = op.get("target")
                if c1 is None or c2 is None or targ is None:
                    raise ValueError("CCNOT/TOFFOLI requires 'control1', 'control2', and 'target'")
                self.apply_ccnot(c1, c2, targ)

            # ----------------------------
            # Custom 2-qubit gate
            # ----------------------------
            elif name == "CUSTOM_2Q":
                mat = op.get("matrix")
                q1 = op.get("q1")
                q2 = op.get("q2")
                if mat is None or q1 is None or q2 is None:
                    raise ValueError("CUSTOM_2Q requires 'matrix', 'q1', and 'q2'")
                self.apply_two_qubit_gate(np.asarray(mat, dtype=complex), q1, q2)

            # ----------------------------
            # Unsupported
            # ----------------------------
            else:
                raise ValueError(f"Unsupported op: {name}")

        # Final sampling step
        counts = self.measure_all(shots=shots)
        return {"counts": counts, "shots": shots}


    # -------------------------
    # Probability helpers
    # -------------------------
    def probabilities(self) -> Dict[str, float]:
        """Return exact full joint distribution mapping bitstrings -> probabilities."""
        probs = np.abs(self.state) ** 2
        return {format(i, f"0{self.n}b"): float(probs[i]) for i in range(self.dim)}

    def marginal_probability(self, target: int) -> Dict[str, float]:
        """Accurate marginal: sums |amplitude|^2 over basis states where target bit is 0/1."""
        if not (0 <= target < self.n):
            raise IndexError("target out of range")
        probs = np.abs(self.state) ** 2
        # shift = n-1-target (maps bit position)
        shift = self.n - 1 - target
        p0 = 0.0
        for idx, p in enumerate(probs):
            if ((idx >> shift) & 1) == 0:
                p0 += p
        p1 = 1.0 - p0
        return {"0": float(p0), "1": float(p1)}

    @classmethod
    def from_json(cls, json_str: str) -> "Simulator":
        data = json.loads(json_str)
        n = int(data["n_qubits"])
        return cls(n)

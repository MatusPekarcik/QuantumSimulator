# quantum_sim/simulator.py
import json
from functools import reduce
from typing import Any, Dict, List, Optional

import numpy as np


def _kron_n(ops: List[np.ndarray]) -> np.ndarray:
    return reduce(lambda a, b: np.kron(a, b), ops)


class Simulator:
    """
    Quantum simulator supporting:
      - Pure (statevector) simulation (default)
      - Noisy simulation via density matrix + Kraus channels (when noise_model is provided)

    Conventions:
      - Qubit indexing: 0 is the leftmost (most significant) bit in bitstrings.
      - Basis ordering: |q0 q1 ... q_{n-1}> with q0 as MSB.
    """

    def __init__(self, n_qubits: int):
        if n_qubits < 1:
            raise ValueError("n_qubits must be >= 1")
        self.n = n_qubits
        self.dim = 2 ** n_qubits
        self.reset()

    # ============================================================
    # Reset / Mode
    # ============================================================
    def reset(self):
        """Reset to |0...0> statevector."""
        if hasattr(self, "rho"):
            delattr(self, "rho")
        self.state = np.zeros((self.dim,), dtype=complex)
        self.state[0] = 1.0

    def reset_density(self):
        """Reset to density matrix rho = |0...0><0...0|."""
        if hasattr(self, "state"):
            delattr(self, "state")
        rho = np.zeros((self.dim, self.dim), dtype=complex)
        rho[0, 0] = 1.0
        self.rho = rho

    def _is_density_mode(self) -> bool:
        return hasattr(self, "rho")

    # ============================================================
    # Helpers for noise application
    # ============================================================
    def _affected_qubits_from_op(self, op: Dict[str, Any]) -> List[int]:
        """Best-effort: which qubits this op touches (used to apply per-gate noise)."""
        name = str(op.get("name", "")).upper()
        qs: List[int] = []

        # fixed single-qubit uses "targets"
        targets = op.get("targets")
        if isinstance(targets, (list, tuple)):
            for t in targets:
                qs.append(int(t))

        # param single-qubit uses "target"
        if op.get("target") is not None:
            qs.append(int(op["target"]))

        # 2q control/target style
        if op.get("control") is not None:
            qs.append(int(op["control"]))
        if op.get("target") is not None and name in ("CNOT", "CZ"):
            qs.append(int(op["target"]))

        # 2q q1/q2 style
        if op.get("q1") is not None:
            qs.append(int(op["q1"]))
        if op.get("q2") is not None:
            qs.append(int(op["q2"]))

        # 3q
        if op.get("control1") is not None:
            qs.append(int(op["control1"]))
        if op.get("control2") is not None:
            qs.append(int(op["control2"]))
        if op.get("target") is not None and name in ("CCNOT", "TOFFOLI"):
            qs.append(int(op["target"]))

        # unique preserve order
        out: List[int] = []
        for q in qs:
            if q not in out:
                out.append(q)
        return out

    # ============================================================
    # Statevector gate application (existing)
    # ============================================================
    def apply_single_qubit_gate(self, gate: np.ndarray, target: int):
        """Apply 2x2 gate to target qubit using tensor contraction (statevector mode)."""
        gate = np.asarray(gate, dtype=complex)
        if gate.shape != (2, 2):
            raise ValueError("Gate must be 2x2")
        if not (0 <= target < self.n):
            raise IndexError("target out of range")
        if self._is_density_mode():
            raise RuntimeError("apply_single_qubit_gate called in density-matrix mode")

        tensor = self.state.reshape((2,) * self.n)
        res = np.tensordot(gate, tensor, axes=([1], [target]))
        res = np.moveaxis(res, 0, target)
        self.state = res.reshape(self.dim)

    def apply_two_qubit_gate(self, gate4: np.ndarray, q1: int, q2: int):
        """Apply 4x4 two-qubit gate on q1,q2 (statevector mode)."""
        gate4 = np.asarray(gate4, dtype=complex)
        if gate4.shape != (4, 4):
            raise ValueError("gate4 must be 4x4")
        if not (0 <= q1 < self.n) or not (0 <= q2 < self.n):
            raise IndexError("qubit indices out of range")
        if q1 == q2:
            raise ValueError("q1 and q2 must be distinct")
        if self._is_density_mode():
            raise RuntimeError("apply_two_qubit_gate called in density-matrix mode")

        axis_list = [q1, q2]
        tensor = self.state.reshape((2,) * self.n)
        U = gate4.reshape(2, 2, 2, 2)  # (out_a,out_b,in_a,in_b)
        res = np.tensordot(U, tensor, axes=([2, 3], axis_list))
        res = np.moveaxis(res, [0, 1], axis_list)
        self.state = res.reshape(self.dim)

    def apply_ccnot(self, control1: int, control2: int, target: int):
        """Apply CCNOT (Toffoli) in statevector mode (basis swap)."""
        if not (0 <= control1 < self.n) or not (0 <= control2 < self.n) or not (0 <= target < self.n):
            raise IndexError("control/target qubit index out of range")
        if len({control1, control2, target}) < 3:
            raise ValueError("control1, control2, and target must be all distinct")
        if self._is_density_mode():
            raise RuntimeError("apply_ccnot called in density-matrix mode")

        new_state = self.state.copy()

        shift_c1 = self.n - 1 - control1
        shift_c2 = self.n - 1 - control2
        shift_t = self.n - 1 - target

        for i in range(self.dim):
            if ((i >> shift_c1) & 1) == 1 and ((i >> shift_c2) & 1) == 1 and ((i >> shift_t) & 1) == 0:
                j = i | (1 << shift_t)
                new_state[i], new_state[j] = new_state[j], new_state[i]

        self.state = new_state

    # ============================================================
    # Density-matrix gate application (new)
    # ============================================================
    def apply_single_qubit_gate_density(self, gate: np.ndarray, target: int):
        """Apply 2x2 unitary to density matrix: rho <- U rho U†."""
        gate = np.asarray(gate, dtype=complex)
        if gate.shape != (2, 2):
            raise ValueError("Gate must be 2x2")
        if not (0 <= target < self.n):
            raise IndexError("target out of range")
        if not self._is_density_mode():
            raise RuntimeError("apply_single_qubit_gate_density called in statevector mode")

        rho_t = self.rho.reshape((2,) * self.n + (2,) * self.n)

        # Left multiply by U on row axis (ket)
        tmp = np.tensordot(gate, rho_t, axes=([1], [target]))
        tmp = np.moveaxis(tmp, 0, target)

        # Right multiply by U† on column axis (bra)
        tmp2 = np.tensordot(tmp, gate.conj(), axes=([target + self.n], [1]))
        tmp2 = np.moveaxis(tmp2, -1, target + self.n)

        self.rho = tmp2.reshape((self.dim, self.dim))

    def apply_two_qubit_gate_density(self, gate4: np.ndarray, q1: int, q2: int):
        """Apply 4x4 unitary to density matrix: rho <- U rho U† on qubits q1,q2."""
        gate4 = np.asarray(gate4, dtype=complex)
        if gate4.shape != (4, 4):
            raise ValueError("gate4 must be 4x4")
        if not (0 <= q1 < self.n) or not (0 <= q2 < self.n):
            raise IndexError("qubit indices out of range")
        if q1 == q2:
            raise ValueError("q1 and q2 must be distinct")
        if not self._is_density_mode():
            raise RuntimeError("apply_two_qubit_gate_density called in statevector mode")

        axes = [q1, q2]
        rho_t = self.rho.reshape((2,) * self.n + (2,) * self.n)
        U = gate4.reshape(2, 2, 2, 2)  # out1,out2,in1,in2

        # Left multiply
        tmp = np.tensordot(U, rho_t, axes=([2, 3], axes))
        tmp = np.moveaxis(tmp, [0, 1], axes)

        # Right multiply by U† (contract with U* on column axes)
        col_axes = [q1 + self.n, q2 + self.n]
        Uc = U.conj()
        tmp2 = np.tensordot(tmp, Uc, axes=(col_axes, [2, 3]))
        tmp2 = np.moveaxis(tmp2, [-2, -1], col_axes)

        self.rho = tmp2.reshape((self.dim, self.dim))

    def apply_ccnot_density(self, control1: int, control2: int, target: int):
        """
        Apply CCNOT in density-matrix mode.
        CCNOT is a permutation of computational basis states, so:
            rho' = P rho P†
        """
        if not (0 <= control1 < self.n) or not (0 <= control2 < self.n) or not (0 <= target < self.n):
            raise IndexError("control/target qubit index out of range")
        if len({control1, control2, target}) < 3:
            raise ValueError("control1, control2, and target must be all distinct")
        if not self._is_density_mode():
            raise RuntimeError("apply_ccnot_density called in statevector mode")

        shift_c1 = self.n - 1 - control1
        shift_c2 = self.n - 1 - control2
        shift_t = self.n - 1 - target

        # Build permutation old->new
        perm = np.arange(self.dim, dtype=int)
        for i in range(self.dim):
            if ((i >> shift_c1) & 1) == 1 and ((i >> shift_c2) & 1) == 1:
                perm[i] = i ^ (1 << shift_t)
            else:
                perm[i] = i

        # Need inverse mapping for rho' = P rho P†
        inv = np.argsort(perm)
        self.rho = self.rho[np.ix_(inv, inv)]

    # ============================================================
    # Convenience wrappers (mode-aware)
    # ============================================================
    def apply_cnot(self, control: int, target: int):
        from .gates import CNOT_4x4
        if self._is_density_mode():
            self.apply_two_qubit_gate_density(CNOT_4x4, control, target)
        else:
            self.apply_two_qubit_gate(CNOT_4x4, control, target)

    def apply_controlled_u(self, gate: np.ndarray, control: int, target: int):
        gate = np.asarray(gate, dtype=complex)
        if gate.shape != (2, 2):
            raise ValueError("Controlled-U expects a 2x2 single-qubit gate")
        if not (0 <= control < self.n) or not (0 <= target < self.n):
            raise IndexError("control/target out of range")
        if control == target:
            raise ValueError("control and target must be different")

        from .gates import controlled
        U4 = controlled(gate)
        if self._is_density_mode():
            self.apply_two_qubit_gate_density(U4, control, target)
        else:
            self.apply_two_qubit_gate(U4, control, target)

    def apply_single_qubit_gate_auto(self, gate: np.ndarray, target: int):
        if self._is_density_mode():
            self.apply_single_qubit_gate_density(gate, target)
        else:
            self.apply_single_qubit_gate(gate, target)

    def apply_two_qubit_gate_auto(self, gate4: np.ndarray, q1: int, q2: int):
        if self._is_density_mode():
            self.apply_two_qubit_gate_density(gate4, q1, q2)
        else:
            self.apply_two_qubit_gate(gate4, q1, q2)

    def apply_ccnot_auto(self, control1: int, control2: int, target: int):
        if self._is_density_mode():
            self.apply_ccnot_density(control1, control2, target)
        else:
            self.apply_ccnot(control1, control2, target)

    # ============================================================
    # Noise channels (Kraus) - 1 qubit channels + readout error
    # ============================================================
    def _kraus_1q(self, channel_type: str, p: float) -> List[np.ndarray]:
        """Return Kraus operators (2x2) for supported 1-qubit channels."""
        from . import gates
        ct = channel_type.lower()
        if not (0.0 <= p <= 1.0):
            raise ValueError("noise probability p must be in [0,1]")

        I = gates.I
        X = gates.X
        Y = gates.Y
        Z = gates.Z

        if ct == "bit_flip":
            return [np.sqrt(1 - p) * I, np.sqrt(p) * X]
        if ct == "phase_flip":
            return [np.sqrt(1 - p) * I, np.sqrt(p) * Z]
        if ct == "depolarizing":
            return [
                np.sqrt(1 - p) * I,
                np.sqrt(p / 3) * X,
                np.sqrt(p / 3) * Y,
                np.sqrt(p / 3) * Z,
            ]

        raise ValueError(f"Unsupported 1q channel type: {channel_type}")

    def apply_kraus_channel_1q(self, channel_type: str, p: float, target: int):
        """Apply a 1-qubit channel to density matrix rho via Kraus operators."""
        if not self._is_density_mode():
            raise RuntimeError("Noise channels require density-matrix mode (rho).")
        if not (0 <= target < self.n):
            raise IndexError("target out of range")

        kraus = self._kraus_1q(channel_type, p)

        rho_t = self.rho.reshape((2,) * self.n + (2,) * self.n)
        out = np.zeros_like(rho_t)

        for K in kraus:
            tmp = np.tensordot(K, rho_t, axes=([1], [target]))
            tmp = np.moveaxis(tmp, 0, target)

            tmp2 = np.tensordot(tmp, K.conj(), axes=([target + self.n], [1]))
            tmp2 = np.moveaxis(tmp2, -1, target + self.n)

            out += tmp2

        self.rho = out.reshape((self.dim, self.dim))

    # ============================================================
    # Measurement (mode-aware) + optional readout error
    # ============================================================
    def measure_all(self, shots: int = 1024, readout_error_p: float = 0.0) -> Dict[str, int]:
        """
        Sample outcomes and return counts.
        - In statevector mode: probs = |amp|^2
        - In density mode: probs = diag(rho)
        Optional symmetric readout bit-flip error: each measured qubit flips with prob readout_error_p.
        """
        if shots <= 0:
            raise ValueError("shots must be > 0")
        if not (0.0 <= readout_error_p <= 1.0):
            raise ValueError("readout_error_p must be in [0,1]")

        if self._is_density_mode():
            probs = np.real(np.diag(self.rho))
            # numerical safety
            probs = np.clip(probs, 0.0, 1.0)
            s = probs.sum()
            if s <= 0:
                raise RuntimeError("Invalid density matrix: probabilities sum to 0")
            probs = probs / s
        else:
            probs = np.abs(self.state) ** 2

        outcomes = np.random.choice(self.dim, size=shots, p=probs)

        # Apply symmetric readout flips after sampling
        if readout_error_p > 0:
            flips = (np.random.rand(shots, self.n) < readout_error_p)
            for s in range(shots):
                if flips[s].any():
                    idx = int(outcomes[s])
                    for q in range(self.n):
                        if flips[s, q]:
                            sh = self.n - 1 - q
                            idx ^= (1 << sh)
                    outcomes[s] = idx

        counts: Dict[str, int] = {}
        for idx in outcomes:
            b = format(int(idx), f"0{self.n}b")
            counts[b] = counts.get(b, 0) + 1
        return counts

    # ============================================================
    # Circuit execution (JSON-like ops) + optional noise_model
    # ============================================================
    def run_circuit(self, circuit: List[Dict], shots: int = 1024, noise_model: Optional[Dict[str, Any]] = None) -> Dict:
        """
        Run a circuit in either:
          - pure statevector mode (noise_model is None)
          - noisy density-matrix mode (noise_model provided)

        noise_model format (general):
          {
            "channels": [
              {"after": "each_gate", "type": "depolarizing", "p": 0.01},
              {"after": "H", "type": "bit_flip", "p": 0.005},          # after specific gate name
              {"after": "measurement", "type": "readout_error", "p": 0.02}
            ]
          }
        """
        from . import gates

        use_noise = isinstance(noise_model, dict)

        if use_noise:
            self.reset_density()
        else:
            self.reset()

        channels = (noise_model.get("channels", []) if use_noise else []) or []
        readout_p = 0.0
        if use_noise:
            for ch in channels:
                after = str(ch.get("after", "")).lower()
                ctype = str(ch.get("type", "")).lower()
                if after == "measurement" and ctype == "readout_error":
                    readout_p = float(ch.get("p", 0.0))

        def apply_post_gate_noise(op: Dict[str, Any], gate_name_upper: str):
            """Apply all matching post-gate channels to affected qubits (density mode only)."""
            if not use_noise:
                return
            affected = self._affected_qubits_from_op(op)
            gname = gate_name_upper.lower()

            for ch in channels:
                after = str(ch.get("after", "")).lower()
                ctype = str(ch.get("type", "")).lower()

                if ctype == "readout_error":
                    continue  # handled at measurement

                if after == "each_gate" or after == gname:
                    p = float(ch.get("p", 0.0))
                    for q in affected:
                        self.apply_kraus_channel_1q(ctype, p, q)

        for op in circuit:
            name = str(op.get("name", "")).upper()

            # Fixed single-qubit gates
            if name in ("H", "X", "Y", "Z", "S", "T"):
                mapping = {
                    "H": gates.H,
                    "X": gates.X,
                    "Y": gates.Y,
                    "Z": gates.Z,
                    "S": gates.S,
                    "T": gates.T,
                }
                targets = op.get("targets")
                if not isinstance(targets, (list, tuple)) or len(targets) == 0:
                    raise ValueError(f"{name} requires 'targets': [..]")
                for t in targets:
                    self.apply_single_qubit_gate_auto(mapping[name], int(t))

                apply_post_gate_noise(op, name)

            # Parameterized single-qubit gates
            elif name in ("RX", "RY", "RZ", "PHASE", "P", "U3"):
                target = op.get("target")
                if target is None:
                    raise ValueError(f"{name} requires 'target'")
                target = int(target)

                if name == "RX":
                    theta = op.get("theta")
                    if theta is None:
                        raise ValueError("RX requires 'theta'")
                    g = gates.Rx(float(theta))
                elif name == "RY":
                    theta = op.get("theta")
                    if theta is None:
                        raise ValueError("RY requires 'theta'")
                    g = gates.Ry(float(theta))
                elif name == "RZ":
                    theta = op.get("theta")
                    if theta is None:
                        raise ValueError("RZ requires 'theta'")
                    g = gates.Rz(float(theta))
                elif name in ("PHASE", "P"):
                    phi = op.get("phi")
                    if phi is None:
                        raise ValueError("PHASE requires 'phi'")
                    g = gates.Phase(float(phi))
                else:  # U3
                    theta = op.get("theta")
                    phi = op.get("phi")
                    lam = op.get("lam")
                    if theta is None or phi is None or lam is None:
                        raise ValueError("U3 requires 'theta', 'phi', 'lam'")
                    g = gates.U3(float(theta), float(phi), float(lam))

                self.apply_single_qubit_gate_auto(g, target)
                apply_post_gate_noise(op, name)

            # CNOT
            elif name == "CNOT":
                c = op.get("control")
                t = op.get("target")
                if c is None or t is None:
                    raise ValueError("CNOT requires 'control' and 'target'")
                self.apply_cnot(int(c), int(t))
                apply_post_gate_noise(op, name)

            # CZ
            elif name == "CZ":
                c = op.get("control")
                t = op.get("target")
                if c is None or t is None:
                    raise ValueError("CZ requires 'control' and 'target'")
                self.apply_two_qubit_gate_auto(gates.CZ_4x4, int(c), int(t))
                apply_post_gate_noise(op, name)

            # SWAP / ISWAP
            elif name in ("SWAP", "ISWAP"):
                q1 = op.get("q1")
                q2 = op.get("q2")
                if q1 is None or q2 is None:
                    raise ValueError(f"{name} requires 'q1' and 'q2'")
                G = gates.SWAP_4x4 if name == "SWAP" else gates.ISWAP_4x4
                self.apply_two_qubit_gate_auto(G, int(q1), int(q2))
                apply_post_gate_noise(op, name)

            # CCNOT / Toffoli
            elif name in ("CCNOT", "TOFFOLI"):
                c1 = op.get("control1")
                c2 = op.get("control2")
                t = op.get("target")
                if c1 is None or c2 is None or t is None:
                    raise ValueError("CCNOT/TOFFOLI requires 'control1', 'control2', 'target'")
                self.apply_ccnot_auto(int(c1), int(c2), int(t))
                apply_post_gate_noise(op, name)

            # Custom 2-qubit
            elif name == "CUSTOM_2Q":
                mat = op.get("matrix")
                q1 = op.get("q1")
                q2 = op.get("q2")
                if mat is None or q1 is None or q2 is None:
                    raise ValueError("CUSTOM_2Q requires 'matrix', 'q1', 'q2'")
                self.apply_two_qubit_gate_auto(np.asarray(mat, dtype=complex), int(q1), int(q2))
                apply_post_gate_noise(op, name)

            else:
                raise ValueError(f"Unsupported op: {name}")

        counts = self.measure_all(shots=shots, readout_error_p=readout_p)
        return {"counts": counts, "shots": shots}

    # ============================================================
    # Probabilities (mode-aware)
    # ============================================================
    def probabilities(self) -> Dict[str, float]:
        if self._is_density_mode():
            probs = np.real(np.diag(self.rho))
            probs = np.clip(probs, 0.0, 1.0)
            s = probs.sum()
            probs = probs / s if s > 0 else probs
        else:
            probs = np.abs(self.state) ** 2
        return {format(i, f"0{self.n}b"): float(probs[i]) for i in range(self.dim)}

    def marginal_probability(self, target: int) -> Dict[str, float]:
        if not (0 <= target < self.n):
            raise IndexError("target out of range")

        if self._is_density_mode():
            probs = np.real(np.diag(self.rho))
            probs = np.clip(probs, 0.0, 1.0)
            s = probs.sum()
            probs = probs / s if s > 0 else probs
        else:
            probs = np.abs(self.state) ** 2

        shift = self.n - 1 - target
        p0 = 0.0
        for idx, p in enumerate(probs):
            if ((idx >> shift) & 1) == 0:
                p0 += float(p)
        p1 = 1.0 - p0
        return {"0": float(p0), "1": float(p1)}

    # ============================================================
    # Expectation values (mode-aware)
    # ============================================================
    def expectation_values(self, target: int) -> Dict[str, float]:
        """
        Compute <X>, <Y>, <Z> for a single qubit.
        Works in both modes:
          - statevector mode uses your efficient implementation
          - density mode uses expectation_pauli("X"/"Y"/"Z", [target])
        """
        if not (0 <= target < self.n):
            raise IndexError("target out of range")

        if self._is_density_mode():
            return {
                "X": float(self.expectation_pauli("X", [target])),
                "Y": float(self.expectation_pauli("Y", [target])),
                "Z": float(self.expectation_pauli("Z", [target])),
            }

        # --- your original efficient statevector version ---
        shift = self.n - 1 - target
        ex = 0.0
        ey = 0.0
        ez = 0.0

        for i in range(self.dim):
            amp_i = self.state[i]
            p = abs(amp_i) ** 2

            bit = (i >> shift) & 1
            ez += (1 if bit == 0 else -1) * p

            j = i ^ (1 << shift)
            amp_j = self.state[j]

            ex += (amp_i.conjugate() * amp_j).real
            ey += ((-1j if bit == 0 else 1j) * amp_i.conjugate() * amp_j).real

        return {"X": float(ex), "Y": float(ey), "Z": float(ez)}

    def expectation_pauli(self, pauli: str, qubits: List[int]) -> float:
        """
        Compute expectation value of a Pauli-string observable.
        Works for:
          - statevector: <psi|P|psi>
          - density matrix: Tr(rho P)
        """
        if not isinstance(pauli, str) or len(pauli) == 0:
            raise ValueError("pauli must be a non-empty string")
        if len(pauli) != len(qubits):
            raise ValueError("len(pauli) must equal len(qubits)")
        if len(set(qubits)) != len(qubits):
            raise ValueError("qubits must be distinct")
        for q in qubits:
            if not (0 <= q < self.n):
                raise IndexError(f"qubit index out of range: {q}")

        pauli = pauli.upper()
        if any(ch not in {"I", "X", "Y", "Z"} for ch in pauli):
            raise ValueError("pauli string may contain only I, X, Y, Z")

        shifts = [self.n - 1 - q for q in qubits]

        # -------------------------
        # Density-matrix: Tr(rho P)
        # -------------------------
        if self._is_density_mode():
            exp_val = 0.0 + 0.0j
            for i in range(self.dim):
                j = i
                phase = 1.0 + 0.0j

                for ch, sh in zip(pauli, shifts):
                    bit = (i >> sh) & 1

                    if ch == "I":
                        continue
                    elif ch == "Z":
                        if bit == 1:
                            phase *= -1.0
                    elif ch == "X":
                        j ^= (1 << sh)
                    elif ch == "Y":
                        j ^= (1 << sh)
                        phase *= (1j if bit == 0 else -1j)

                exp_val += self.rho[i, j] * phase

            return float(exp_val.real)

        # -------------------------
        # Statevector: <psi|P|psi>
        # -------------------------
        exp_val = 0.0 + 0.0j
        for i in range(self.dim):
            amp_i = self.state[i]
            if amp_i == 0:
                continue

            j = i
            phase = 1.0 + 0.0j

            for ch, sh in zip(pauli, shifts):
                bit = (i >> sh) & 1

                if ch == "I":
                    continue
                elif ch == "Z":
                    if bit == 1:
                        phase *= -1.0
                elif ch == "X":
                    j ^= (1 << sh)
                elif ch == "Y":
                    j ^= (1 << sh)
                    phase *= (1j if bit == 0 else -1j)

            exp_val += np.conjugate(amp_i) * phase * self.state[j]

        return float(exp_val.real)

    # ============================================================
    # JSON helper
    # ============================================================
    @classmethod
    def from_json(cls, json_str: str) -> "Simulator":
        data = json.loads(json_str)
        n = int(data["n_qubits"])
        return cls(n)

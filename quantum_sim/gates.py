# quantum_sim/gates.py
"""
Common quantum gate matrices and helpers.

Conventions
- Qubit indexing / ordering: the simulator uses "leftmost is qubit 0" (most-significant).
- Two-qubit 4x4 matrices here assume basis order |00>, |01>, |10>, |11>
  where the first (left) bit is the MSB.
"""

from __future__ import annotations
import numpy as np
from functools import reduce

# --------------------
# Single-qubit gates
# --------------------
I = np.array([[1, 0], [0, 1]], dtype=complex)

X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)

S = np.array([[1, 0], [0, 1j]], dtype=complex)
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)

Sdg = S.conj().T
Tdg = T.conj().T

# --------------------
# Parameterized gates
# --------------------
def Rx(theta: float) -> np.ndarray:
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    return np.array([[c, -1j * s], [-1j * s, c]], dtype=complex)

def Ry(theta: float) -> np.ndarray:
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    return np.array([[c, -s], [s, c]], dtype=complex)

def Rz(theta: float) -> np.ndarray:
    return np.array(
        [[np.exp(-1j * theta / 2), 0], [0, np.exp(1j * theta / 2)]],
        dtype=complex
    )

def Phase(phi: float) -> np.ndarray:
    return np.array([[1, 0], [0, np.exp(1j * phi)]], dtype=complex)

def U3(theta: float, phi: float, lam: float) -> np.ndarray:
    ct = np.cos(theta / 2)
    st = np.sin(theta / 2)
    return np.array([
        [ct, -np.exp(1j * lam) * st],
        [np.exp(1j * phi) * st, np.exp(1j * (phi + lam)) * ct]
    ], dtype=complex)

# --------------------
# Two-qubit standard matrices (4x4)
# Basis ordering: |00>,|01>,|10>,|11> (MSB then LSB)
# --------------------
CNOT_4x4 = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
], dtype=complex)

CZ_4x4 = np.diag([1, 1, 1, -1]).astype(complex)

SWAP_4x4 = np.array([
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1]
], dtype=complex)

ISWAP_4x4 = np.array([
    [1, 0, 0, 0],
    [0, 0, 1j, 0],
    [0, 1j, 0, 0],
    [0, 0, 0, 1]
], dtype=complex)

# --------------------
# Helpers
# --------------------
def controlled(u: np.ndarray) -> np.ndarray:
    """
    Controlled-U with control as the LEFT qubit (MSB) and target as RIGHT (LSB).
    Basis: |00>,|01>,|10>,|11>
    """
    u = np.asarray(u, dtype=complex)
    if u.shape != (2, 2):
        raise ValueError("u must be 2x2")
    top = np.eye(2, dtype=complex)
    return np.block([
        [top, np.zeros((2, 2), dtype=complex)],
        [np.zeros((2, 2), dtype=complex), u]
    ])

def controlled_on_target_first(u: np.ndarray) -> np.ndarray:
    """
    Controlled-U with control as the RIGHT qubit (LSB) and target as LEFT (MSB).
    Basis: |00>,|01>,|10>,|11> where left bit is MSB, right bit is LSB.

    If LSB == 0: do nothing
    If LSB == 1: apply U to MSB
    
    u = np.asarray(u, dtype=complex)
    if u.shape != (2, 2):
        raise ValueError("u must be 2x2")

    top = np.eye(2, dtype=complex)   # control (LSB)=0 block
    bottom = u                       # control (LSB)=1 block

    return np.block([
        [top, np.zeros((2, 2), dtype=complex)],
        [np.zeros((2, 2), dtype=complex), bottom]
    ])
    """
    u = np.asarray(u, dtype=complex)
    if u.shape != (2, 2):
        raise ValueError("u must be 2x2")

    # Control is LSB: apply U on MSB iff LSB == 1.
    CU = np.eye(4, dtype=complex)
    CU[np.ix_([1, 3], [1, 3])] = u
    return CU

def expand_single_to_n(gate: np.ndarray, n_qubits: int, target: int) -> np.ndarray:
    if gate.shape != (2, 2):
        raise ValueError("gate must be 2x2")
    if not (0 <= target < n_qubits):
        raise IndexError("target out of range")
    parts = []
    for q in range(n_qubits):
        parts.append(gate if q == target else np.eye(2, dtype=complex))
    return reduce(lambda a, b: np.kron(a, b), parts)

__all__ = [
    "I", "X", "Y", "Z", "H", "S", "T", "Sdg", "Tdg",
    "Rx", "Ry", "Rz", "Phase", "U3",
    "CNOT_4x4", "CZ_4x4", "SWAP_4x4", "ISWAP_4x4",
    "controlled", "controlled_on_target_first", "expand_single_to_n"
]

# quantum_sim/gates.py
"""
Common quantum gate matrices and helpers.

Conventions
- Qubit indexing / ordering: the simulator uses "leftmost is qubit 0" (most-significant).
- Two-qubit 4x4 matrices here assume basis order |00>, |01>, |10>, |11>
  where the first (left) bit is the control when relevant.

Provided:
- Single-qubit constants: I, X, Y, Z, H, S, T
- Parameterized single-qubit gates: Rx, Ry, Rz, Phase (P), U3
- Two-qubit matrices: CNOT_4x4, CZ_4x4, SWAP_4x4, ISWAP_4x4
- Helper: controlled(u) -> 4x4 controlled-U (control = leftmost qubit)
"""

from __future__ import annotations
import numpy as np
from functools import reduce
from typing import Callable

# --------------------
# Single-qubit gates
# --------------------
I = np.array([[1, 0], [0, 1]], dtype=complex)

X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)

# Phase gates
S = np.array([[1, 0], [0, 1j]], dtype=complex)       # S = sqrt(Z)
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)  # T = fourth-root of Z

# Hermitian adjoints
Sdg = S.conj().T
Tdg = T.conj().T

# --------------------
# Parameterized gates
# --------------------
def Rx(theta: float) -> np.ndarray:
    """Rotation around X axis by angle theta (radians)."""
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    return np.array([[c, -1j * s], [-1j * s, c]], dtype=complex)

def Ry(theta: float) -> np.ndarray:
    """Rotation around Y axis by angle theta (radians)."""
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    return np.array([[c, -s], [s, c]], dtype=complex)

def Rz(theta: float) -> np.ndarray:
    """Rotation around Z axis by angle theta (radians)."""
    return np.array([[np.exp(-1j * theta / 2), 0], [0, np.exp(1j * theta / 2)]], dtype=complex)

def Phase(phi: float) -> np.ndarray:
    """Phase gate P(phi) = diag(1, exp(i*phi))."""
    return np.array([[1, 0], [0, np.exp(1j * phi)]], dtype=complex)

def U3(theta: float, phi: float, lam: float) -> np.ndarray:
    """
    U3 gate:
    U3(θ,φ,λ) = [[cos(θ/2), -exp(iλ) sin(θ/2)],
                 [exp(iφ) sin(θ/2), exp(i(φ+λ)) cos(θ/2)]]
    """
    ct = np.cos(theta / 2)
    st = np.sin(theta / 2)
    return np.array([
        [ct, -np.exp(1j * lam) * st],
        [np.exp(1j * phi) * st, np.exp(1j * (phi + lam)) * ct]
    ], dtype=complex)

# --------------------
# Two-qubit standard matrices (4x4)
# --------------------
# Ordering: |00>,|01>,|10>,|11>  (first/qubit0 is leftmost)
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

# iSWAP: swaps and adds i phase on off-diagonals
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
    Build a controlled-U (4x4) for a single-qubit 2x2 matrix u.
    Convention: control is the leftmost qubit (most-significant),
    so the resulting matrix in basis |00>,|01>,|10>,|11> is:
      [[1,0,0,0],
       [0,1,0,0],
       [0,0,u00,u01],
       [0,0,u10,u11]]
    """
    u = np.asarray(u, dtype=complex)
    if u.shape != (2, 2):
        raise ValueError("u must be 2x2")
    top = np.eye(2, dtype=complex)
    return np.block([
        [top, np.zeros((2, 2), dtype=complex)],
        [np.zeros((2, 2), dtype=complex), u]
    ])
"""
def controlled_on_target_first(u: np.ndarray) -> np.ndarray:
    """"""
    Alternative controlled-U where control is the *rightmost* qubit (less-significant).
    Basis still |00>,|01>,|10>,|11>. This constructs a block matrix
    diag(U, I) so it performs U when control bit (rightmost) == 1.
    """"""
    u = np.asarray(u, dtype=complex)
    if u.shape != (2, 2):
        raise ValueError("u must be 2x2")
    top = u
    bottom = np.eye(2, dtype=complex)
    return np.block([
        [top, np.zeros((2, 2), dtype=complex)],
        [np.zeros((2, 2), dtype=complex), bottom]
    ])
"""
def controlled_on_target_first(u: np.ndarray) -> np.ndarray:
    """
    Controlled-U where the CONTROL is the RIGHTMOST qubit (LSB),
    and the TARGET is the LEFTMOST qubit (MSB).

    Convention:
      Basis ordering = |q0 q1> = |MSB LSB> = |00>, |01>, |10>, |11>
    
    Behavior:
      - Apply U to the MSB when LSB == 1
      - Do nothing when LSB == 0
    
    Therefore block structure is:
        [ I   0 ]
        [ 0   U ]
    because the lower block corresponds to basis states |01> and |11>
    (LSB = 1).
    """
    u = np.asarray(u, dtype=complex)
    if u.shape != (2, 2):
        raise ValueError("u must be 2x2")

    # Identity block: applies when rightmost qubit == 0
    top = np.eye(2, dtype=complex)

    # U block: applies when rightmost qubit == 1
    bottom = u

    return np.block([
        [top,    np.zeros((2, 2), dtype=complex)],
        [np.zeros((2, 2), dtype=complex), bottom]
    ])

def expand_single_to_n(gate: np.ndarray, n_qubits: int, target: int) -> np.ndarray:
    """
    Return the full 2^n x 2^n operator that applies `gate` to `target` (0..n-1),
    using leftmost = index 0 convention.
    Warning: this constructs the full matrix (costly for large n).
    """
    if gate.shape != (2, 2):
        raise ValueError("gate must be 2x2")
    if not (0 <= target < n_qubits):
        raise IndexError("target out of range")
    parts = []
    for q in range(n_qubits):
        parts.append(gate if q == target else np.eye(2, dtype=complex))
    return reduce(lambda a, b: np.kron(a, b), parts)

# --------------------
# Exports
# --------------------
__all__ = [
    # single-qubit constants
    "I", "X", "Y", "Z", "H", "S", "T", "Sdg", "Tdg",
    # parameterized
    "Rx", "Ry", "Rz", "Phase", "U3",
    # two-qubit matrices
    "CNOT_4x4", "CZ_4x4", "SWAP_4x4", "ISWAP_4x4",
    # helpers
    "controlled", "controlled_on_target_first", "expand_single_to_n"
]

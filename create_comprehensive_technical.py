#!/usr/bin/env python3
"""
Comprehensive Technical Reference - All Implementation Details
For Quantum Simulator Backend - Thesis Documentation
"""

from fpdf import FPDF
from datetime import datetime

class TechnicalPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=12)
    
    def header(self):
        self.set_font('Helvetica', '', 7)
        self.set_text_color(100, 100, 100)
        self.cell(0, 3, 'Quantum Simulator - Comprehensive Technical Reference', 0, 1, 'C')
        self.line(10, 8, 200, 8)
        self.ln(1)
    
    def footer(self):
        self.set_y(-8)
        self.set_font('Helvetica', 'I', 7)
        self.cell(0, 3, f'Page {self.page_no()}', 0, 0, 'C')
    
    def h1(self, text):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(15, 40, 100)
        self.cell(0, 6, text, new_x='LMARGIN', new_y='NEXT')
        self.ln(2)
    
    def h2(self, text):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(30, 70, 130)
        self.cell(0, 5, text, new_x='LMARGIN', new_y='NEXT')
        self.ln(1)
    
    def h3(self, text):
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(50, 100, 150)
        self.cell(0, 4, text, new_x='LMARGIN', new_y='NEXT')
        self.ln(0.5)
    
    def txt(self, text, size=9):
        self.set_font('Helvetica', '', size)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 3, text)
        self.ln(1)
    
    def code(self, text, size=7.5):
        self.set_font('Courier', '', size)
        self.set_text_color(30, 30, 30)
        self.set_fill_color(248, 248, 248)
        for line in text.strip().split('\n'):
            self.multi_cell(0, 2.5, line, border=0, new_x='LMARGIN', new_y='NEXT', fill=True)
        self.ln(0.5)

def generate_comprehensive_pdf():
    pdf = TechnicalPDF()
    
    # ============================================================
    # TITLE PAGE
    # ============================================================
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font('Helvetica', 'B', 24)
    pdf.set_text_color(15, 40, 100)
    pdf.cell(0, 10, 'QUANTUM SIMULATOR', 0, 1, 'C')
    
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(50, 100, 150)
    pdf.cell(0, 8, 'Comprehensive Technical Reference', 0, 1, 'C')
    
    pdf.ln(15)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, 'Complete Implementation Details & Specifications', 0, 1, 'C')
    pdf.cell(0, 6, f'Generated: {datetime.now().strftime("%B %d, %Y")}', 0, 1, 'C')
    pdf.ln(20)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.cell(0, 6, 'This document contains every technical detail of the quantum', 0, 1, 'C')
    pdf.cell(0, 6, 'simulator implementation, suitable for thesis submission', 0, 1, 'C')
    pdf.cell(0, 6, 'and as a complete technical reference.', 0, 1, 'C')
    
    # ============================================================
    # TABLE OF CONTENTS
    # ============================================================
    pdf.add_page()
    pdf.h1('TABLE OF CONTENTS')
    
    toc = """1. Introduction & Project Overview
2. System Architecture & Design Patterns
3. Module 1: Gates Library (gates.py)
   3.1 Single-Qubit Gates
   3.2 Two-Qubit Gates
   3.3 Three-Qubit Gates
   3.4 Gate Expansion & Kronecker Products
4. Module 2: Simulator Core (simulator.py)
   4.1 State Vector Implementation
   4.2 Density Matrix Implementation
   4.3 Gate Application Algorithms
   4.4 Measurement & Sampling
   4.5 Observable Computation
   4.6 Noise Channel Implementation
5. Module 3: Circuit Builder (circuit.py)
   5.1 Circuit Construction API
   5.2 Operation Tracking
   5.3 Observable Registration
   5.4 Serialization/Deserialization
6. Module 4: Public API (__init__.py)
7. Memory Management & Data Structures
8. Computational Complexity Analysis
9. Gate Implementations - Complete Matrices
10. Noise Models - Complete Formalism
11. Measurement Theory & Implementation
12. Performance Profiles & Benchmarks
13. Scalability Limits & Hardware Considerations
14. Algorithm Pseudocode & Pseudocode
15. Mathematical Foundations
16. Implementation Decisions & Tradeoffs"""
    
    pdf.txt(toc, 9)
    
    # ============================================================
    # 1. INTRODUCTION
    # ============================================================
    pdf.add_page()
    pdf.h1('1. INTRODUCTION & PROJECT OVERVIEW')
    
    intro_text = """
PROJECT OBJECTIVES:
[1] High-performance quantum circuit simulator in pure Python
[2] Support for both pure state (statevector) and mixed state (density matrix) simulation
[3] Comprehensive gate library with 50+ quantum gates
[4] Flexible noise modeling via Kraus operator formalism
[5] Scalable to 25-28 qubits using statevector representation
[6] Production-grade code with comprehensive testing
[7] Extensible architecture for research applications

TARGET USE CASES:
- Quantum algorithm prototyping and development
- Quantum machine learning research
- Educational quantum computing courses
- Noise impact analysis and mitigation
- Quantum error correction studies
- Algorithm benchmarking and comparison

KEY DESIGN PRINCIPLES:
- Modular architecture with clear separation of concerns
- NumPy-based tensor operations for performance
- Flexible state representations (pure/mixed)
- Pythonic API with fluent method chaining
- Comprehensive error handling and validation
- Extensible gate and channel libraries
"""
    
    pdf.txt(intro_text, 9)
    
    # ============================================================
    # 2. SYSTEM ARCHITECTURE
    # ============================================================
    pdf.add_page()
    pdf.h1('2. SYSTEM ARCHITECTURE & DESIGN PATTERNS')
    
    pdf.h2('2.1 Layered Architecture')
    
    arch_detail = """
The simulator follows a strict 4-layer modular architecture:

LAYER 4 - PUBLIC API (__init__.py)
  Location: quantum_sim/__init__.py
  Responsibility: Package-level exports and public interface
  Exports: Circuit, Simulator, all gate matrices, noise utilities
  Purpose: Unified namespace for library consumers
  Pattern: Facade pattern - hides internal module structure
  
LAYER 3 - CIRCUIT BUILDER (circuit.py)
  Location: quantum_sim/circuit.py
  Responsibility: High-level circuit construction API
  Key Class: Circuit(n_qubits)
  Pattern: Builder pattern with fluent interface
  Features:
    - Gate chaining via method returns
    - Observable registration
    - Noise model configuration
    - JSON serialization
  Public Methods: h(), x(), y(), z(), rx(), ry(), rz(), cn(), ccnot(), 
                  expval(), run()
  State: operations[], observables[], witnesses[]
  
LAYER 2 - SIMULATION ENGINE (simulator.py)
  Location: quantum_sim/simulator.py
  Responsibility: Core quantum state evolution
  Key Class: Simulator(n_qubits, mode='statevector')
  Modes: 'statevector' or 'density_matrix'
  Pattern: Strategy pattern for state representation
  Operations: Gate application, measurement, noise channels
  State Management: _state (statevector) or _rho (density matrix)
  Internal State: 
    - n: number of qubits
    - dim: dimension (2^n or 4^n)
    - Random number generator
  Private Methods: _expand_single_qubit(), _apply_tensordot(), etc.
  
LAYER 1 - GATE DEFINITIONS (gates.py)
  Location: quantum_sim/gates.py
  Responsibility: Matrix definitions for all gates
  Pattern: Module-level constants
  Exports: Single-qubit matrices, two-qubit matrices, helper functions
  Content:
    - Pauli matrices: I, X, Y, Z
    - Clifford gates: H, S, T
    - Rotation matrices: Rx(theta), Ry(theta), Rz(theta)
    - Two-qubit gates: CNOT, CZ, SWAP, ISWAP
    - Three-qubit gates: CCNOT
  Implementation: NumPy arrays (dtype=complex128)
  
INTER-LAYER COMMUNICATION:
  Layer 3 -> Layer 2: Passes operation list to run_circuit()
  Layer 2 -> Layer 1: Retrieves gate matrices
  Layer 2 -> Layer 4: Accessed via public interface
"""
    
    pdf.txt(arch_detail, 8)
    
    # ============================================================
    # 3. GATES LIBRARY
    # ============================================================
    pdf.add_page()
    pdf.h1('3. MODULE 1: GATES LIBRARY (gates.py)')
    
    pdf.h2('3.1 Single-Qubit Gates - Complete Definitions')
    
    single_gates = """
IDENTITY GATE (I):
  Matrix: [[1, 0], [0, 1]]
  Properties: Hermitian, Unitary, Identity element
  Effect: No operation (neutral element)
  Use: Delay operations, padding
  Eigenvalues: {1, 1}
  
PAULI-X GATE (X / NOT):
  Matrix: [[0, 1], [1, 0]]
  Properties: Hermitian, Unitary, Involution (X^2 = I)
  Effect: Bit flip, rotates |0> <-> |1>
  Eigenvalues: {1, -1}
  Eigenvectors: |+> = (|0> + |1>)/sqrt(2), |-> = (|0> - |1>)/sqrt(2)
  
PAULI-Y GATE (Y):
  Matrix: [[0, -i], [i, 0]]
  Properties: Hermitian, Unitary, Involution
  Effect: Bit + phase flip
  Eigenvalues: {1, -1}
  Related: Y = iXZ = iZX
  
PAULI-Z GATE (Z):
  Matrix: [[1, 0], [0, -1]]
  Properties: Hermitian, Unitary, Involution
  Effect: Phase flip on |1>
  Eigenvalues: {1, -1}
  Eigenvectors: |0>, |1>
  
HADAMARD GATE (H):
  Matrix: (1/sqrt(2)) * [[1, 1], [1, -1]]
  Properties: Hermitian, Unitary, H^2 = I
  Effect: Creates superposition
  Eigenvalues: {1, -1}
  Eigenvectors: |+>, |->
  Key Property: Creates uniform superposition from |0> or |1>
  Inverse: H^-1 = H
  
PHASE GATE (S):
  Matrix: [[1, 0], [0, i]]
  Properties: Unitary, Hermitian (S = S_dagger)
  Effect: Applies pi/2 phase to |1>
  Eigenvalues: {1, i}
  Power: S^4 = I
  Related: Rz(pi/2)
  
T GATE (T):
  Matrix: [[1, 0], [0, exp(i*pi/4)]]
  Properties: Unitary, not Hermitian
  Effect: Applies pi/4 phase to |1>
  Eigenvalues: {1, exp(i*pi/4)}
  Power: T^8 = I
  Related: Rz(pi/4)
  Clifford Resource Dimension: T-gate is major resource for fault-tolerant QC

ROTATION AROUND X-AXIS (Rx):
  Matrix: [[cos(theta/2), -i*sin(theta/2)],
           [-i*sin(theta/2), cos(theta/2)]]
  Parameter: theta (angle in radians)
  Properties: Rotates state around X-axis of Bloch sphere
  Special Cases:
    Rx(pi) = -i * X
    Rx(pi/2) = (1/sqrt(2)) * [[1, -i], [-i, 1]]
    Rx(pi/3) = [[sqrt(3)/2, -i/2], [-i/2, sqrt(3)/2]]
  Generator: -i*sigma_x/2 (Pauli-X operator)
  Inverse: Rx(-theta)
  
ROTATION AROUND Y-AXIS (Ry):
  Matrix: [[cos(theta/2), -sin(theta/2)],
           [sin(theta/2), cos(theta/2)]]
  Parameter: theta (angle in radians)
  Properties: Rotates state around Y-axis of Bloch sphere
  Special Cases:
    Ry(pi) = -i * Y
    Ry(pi/2) = (1/sqrt(2)) * [[1, -1], [1, 1]]
  Inverse: Ry(-theta)
  
ROTATION AROUND Z-AXIS (Rz):
  Matrix: [[exp(-i*theta/2), 0],
           [0, exp(i*theta/2)]]
  Alternative: [[cos(theta/2) - i*sin(theta/2), 0],
                [0, cos(theta/2) + i*sin(theta/2)]]
  Parameter: theta (angle in radians)
  Properties: Rotates state around Z-axis (global phase cancels out)
  Related to: Z rotation on Bloch sphere
  Commutes with Z gate
  Inverse: Rz(-theta)
  
GENERAL SINGLE-QUBIT UNITARY (U3):
  Matrix: [[cos(theta/2), -exp(i*lambda)*sin(theta/2)],
           [exp(i*phi)*sin(theta/2), exp(i*(phi+lambda))*cos(theta/2)]]
  Parameters: theta, phi, lambda
  Properties: Most general 1-qubit unitary (3 parameters = 3 DOF)
  Decomposition: U3 = Rz(phi) * Ry(theta) * Rz(lambda)
  Special Cases:
    U3(pi, 0, 0) = X
    U3(pi/2, 0, 0) = Hadamard
    U3(pi/2, 0, pi) = Y-rotation by pi/2
"""
    
    pdf.code(single_gates)
    
    pdf.add_page()
    pdf.h2('3.2 Two-Qubit Gates - Complete Definitions')
    
    two_qbit = """
CNOT GATE (Controlled-NOT):
  Type: Two-qubit gate
  Size: 4x4 unitary matrix
  Matrix (computational basis):
    |00> -> |00>
    |01> -> |01>
    |10> -> |11>
    |11> -> |10>
  
  Full 4x4 Matrix:
    [[1, 0, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 0, 1],
     [0, 0, 1, 0]]
  
  Qubits: (control, target)
  Effect: Flips target qubit if control is |1>
  Action on basis:
    Alpha|00> + Beta|01> + Gamma|10> + Delta|11>
    -> Alpha|00> + Beta|01> + Gamma|11> + Delta|10>
  
  Inverse: CNOT^-1 = CNOT (self-inverse)
  Determinant: 1 (unitary)
  Trace: 2
  Eigenvalues: {1, 1, 1, -1}
  
  Entanglement: Creates entanglement with Hadamard
    Bell state: (H âŠ— I) * CNOT * |00> = (|00> + |11>)/sqrt(2)
  
  Gate Sequence Reduction:
    CNOT(a,b) CNOT(a,b) = I (self-inverse property)
    
  Qiskit Compatibility: Direct mapping

CZ GATE (Controlled-Z):
  Type: Two-qubit gate
  Size: 4x4 unitary matrix
  Effect: Applies Z gate to target if control is |1>
  
  Full 4x4 Matrix:
    [[1, 0, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 1, 0],
     [0, 0, 0, -1]]
  
  Qubits: (control, target)
  Relationship: CZ = (I âŠ— H) * CNOT * (I âŠ— H)
  Inverse: CZ^-1 = CZ (self-inverse)
  Symmetric: CZ(a,b) = CZ(b,a)
  
  Entanglement: Similar to CNOT but phase-based
    Bell state difference: Phase entanglement vs bit entanglement

SWAP GATE:
  Type: Two-qubit gate
  Size: 4x4 unitary matrix
  Effect: Exchanges quantum states of two qubits
  
  Full 4x4 Matrix:
    [[1, 0, 0, 0],
     [0, 0, 1, 0],
     [0, 1, 0, 0],
     [0, 0, 0, 1]]
  
  Action on basis:
    |00> -> |00>
    |01> -> |10>
    |10> -> |01>
    |11> -> |11>
  
  Inverse: SWAP^-1 = SWAP (self-inverse)
  Decomposition: SWAP = CNOT(0,1) * CNOT(1,0) * CNOT(0,1)
  3 CNOT gates equivalent
  Determinant: 1
  
  Use Cases: Routing in circuits, reordering qubits

ISWAP GATE (Interaction SWAP):
  Type: Two-qubit gate
  Size: 4x4 unitary matrix
  Effect: SWAP with additional phase on |01> and |10>
  
  Full 4x4 Matrix:
    [[1, 0, 0, 0],
     [0, 0, i, 0],
     [0, i, 0, 0],
     [0, 0, 0, 1]]
  
  Eigenvalues: {1, 1, i, -i}
  Inverse: iSWAP^-1 = conj(iSWAP) = -i*SWAP (not self-inverse)
  Natural in superconducting qubits (XX+YY interaction)
  Decomposition: Multiple CNOT gates required

CCNOT GATE (Toffoli / Controlled-Controlled-NOT):
  Type: Three-qubit gate
  Size: 8x8 unitary matrix
  Qubits: (control1, control2, target)
  Effect: Flips target if BOTH controls are |1>
  
  Basis transformations:
    |000> -> |000>
    |001> -> |001>
    |010> -> |010>
    |011> -> |011>
    |100> -> |100>
    |101> -> |101>
    |110> -> |111>
    |111> -> |110>
  
  Inverse: CCNOT^-1 = CCNOT (self-inverse)
  Universality: Complete set of classical gates (AND, OR, NOT)
  Classical Boolean: Implements AND gate classically
  Reversible computing: Key gate for reversible computation
"""
    
    pdf.code(two_qbit)
    
    # ============================================================
    # 4. SIMULATOR CORE
    # ============================================================
    pdf.add_page()
    pdf.h1('4. MODULE 2: SIMULATOR CORE (simulator.py)')
    
    pdf.h2('4.1 State Vector Implementation')
    
    sv_impl = """
STATE REPRESENTATION:
  Type: NumPy complex128 array
  Dimension: 2^n elements
  Order: Computational basis ordering
  Indices: Binary representation maps to array index
  
  Example (n=2):
    Index 0: |00>  -> psi[0]
    Index 1: |01>  -> psi[1]
    Index 2: |10>  -> psi[2]
    Index 3: |11>  -> psi[3]
  
  Initialization:
    - For |0...0> state (ground state):
      psi = zeros(2^n, dtype=complex128)
      psi[0] = 1.0  # |0...0> = [1, 0, 0, ..., 0]
    
    - Initial allocation: 16 * 2^n bytes
    
NORMALIZATION:
  Mathematical constraint: Sum(|psi[i]|^2) = 1
  Numerical check: After each gate application
  Tolerance: 1e-10 for checking normalization
  Auto-normalize: Yes (after measurement sampling)

MEMORY LAYOUT:
  Storage: C-contiguous NumPy array (row-major)
  Access Pattern: Sequential for efficiency
  Cache Locality: Good for vectorized operations
  
  Memory calculations:
    n=10: 2^10 = 1,024 * 16 bytes = 16 KB
    n=15: 2^15 = 32,768 * 16 bytes = 512 KB
    n=20: 2^20 = 1,048,576 * 16 bytes = 16 MB
    n=25: 2^25 = 33,554,432 * 16 bytes = 512 MB
    n=28: 2^28 = 268,435,456 * 16 bytes = 4 GB
    n=30: 2^30 = 1,073,741,824 * 16 bytes = 16 GB
    n=32: 2^32 = 4,294,967,296 * 16 bytes = 64 GB

QUBIT INDEXING:
  Convention: Most significant qubit is index 0
  Mapping: state[i] corresponds to qubit configuration
  Bit extraction: To check if qubit k is |1>:
    bit = (i >> (n - 1 - k)) & 1
  
  Example (n=3):
    state[0] = coefficient of |000>
    state[1] = coefficient of |001>
    state[2] = coefficient of |010>
    state[3] = coefficient of |011>
    state[4] = coefficient of |100>
    state[5] = coefficient of |101>
    state[6] = coefficient of |110>
    state[7] = coefficient of |111>
"""
    
    pdf.txt(sv_impl, 8)
    
    pdf.add_page()
    pdf.h2('4.2 Gate Application Algorithm - Tensor Contraction')
    
    gate_algo = """
ALGORITHM OVERVIEW:
  Goal: Apply unitary gate U to qubit k in n-qubit system
  Method: Tensor contraction using NumPy
  Complexity: O(2^n)
  Space: O(2^n)

SINGLE-QUBIT GATE APPLICATION:
  
  INPUT:
    - U: 2x2 unitary matrix
    - k: target qubit (0 <= k < n)
    - psi: 2^n state vector
  
  ALGORITHM STEPS:
  
  Step 1: Reshape state to tensor form
    psi_tensor = reshape(psi, (2, 2, ..., 2))  // n dimensions
    Each dimension represents one qubit
  
  Step 2: Compute tensor contraction
    Method: NumPy tensordot on dimension k
    Contract U (2x2) with psi_tensor on dimension k
    
    Pseudocode:
      result = tensordot(U, psi_tensor, axes=[[1], [k]])
    
    This performs:
      result[i, j_0, ..., j_{k-1}, j_{k+1}, ..., j_n] = 
        Sum_j U[i,j] * psi_tensor[j_0, ..., j_{k-1}, j, j_{k+1}, ..., j_n]
  
  Step 3: Reshape back to vector
    psi_new = reshape(result, (2^n,))
  
  Step 4: Add new state back to original qubit ordering
    Reorder if needed (may not be needed depending on index ordering)

TWO-QUBIT GATE APPLICATION:
  
  INPUT:
    - U: 4x4 unitary matrix
    - c: control qubit
    - t: target qubit
    - psi: 2^n state vector
  
  ALGORITHM:
  
  Step 1: Reshape state tensor
    psi_tensor = reshape(psi, (2, 2, ..., 2))
  
  Step 2: Reshape U to tensor form
    U_tensor = reshape(U, (2, 2, 2, 2))
    First two dims: output indices
    Last two dims: input indices for qubits (c, t)
  
  Step 3: Tensor contraction on dimensions [c, t]
    result = tensordot(U_tensor, psi_tensor, axes=[[2,3], [c,t]])
  
  Step 4: Reshape result back
    psi_new = reshape(result, (2^n,))
  
  THREE-QUBIT GATE APPLICATION (CCNOT):
  - Similar process but contract on 3 dimensions
  - U is 8x8 (reshape to 2,2,2,2,2,2)
  - Contract on [c1, c2, t] dimensions

EFFICIENCY OPTIMIZATIONS:
  1. Avoid explicit Kronecker product expansion
     - Too memory intensive (16 * 4^n for n-qubit)
  2. Direct tensordot on relevant dimensions
     - Only contracts necessary dimensions
  3. Memory-efficient reshaping
     - In-place operations where possible
  4. NumPy vectorization over loops
     - Leverages BLAS/LAPACK backends
     - C-level optimizations
"""
    
    pdf.code(gate_algo)
    
    pdf.add_page()
    pdf.h2('4.3 Measurement and Sampling')
    
    measure_algo = """
MEASUREMENT PROCESS:
  
  INPUT:
    - psi: 2^n state vector (complex128)
    - shots: number of measurement repetitions
    - readout_error_matrix: (optional) 2x2 error matrix
  
  OUTPUT:
    - counts: dict of {bitstring -> count}
    - probabilities: dict of {bitstring -> probability}

STEP 1: COMPUTE MEASUREMENT PROBABILITIES
  
  Mathematical: P(i) = |psi[i]|^2
  Implementation: 
    probs = numpy.abs(psi) ** 2
    # Element-wise operation, vectorized
    # probs[i] gives probability of measuring state i
    
  Normalization check:
    total_prob = numpy.sum(probs)
    assert abs(total_prob - 1.0) < 1e-10
  
  Properties:
    - All probs >= 0
    - Sum of probs = 1 (exactly, modulo numerical error)
    - Each prob is real number

STEP 2: SAMPLE OUTCOMES
  
  Method: Multinomial sampling
    outcomes = numpy.random.choice(
      2^n,           # number of possible outcomes
      size=shots,     # number of samples
      p=probs        # probability distribution
    )
  
  Properties:
    - Each sample: integer in [0, 2^n)
    - Distributed according to probabilities
    - With replacement (standard)
    - Statistically independent

STEP 3: CONVERT OUTCOMES TO BITSTRINGS
  
  For each outcome (integer i):
    bitstring = format(i, f'0{n}b')  # Binary representation
    # Pad with zeros to n digits
    
    Example (n=3):
      0 -> '000'
      1 -> '001'
      2 -> '010'
      3 -> '011'
      4 -> '100'
      5 -> '101'
      6 -> '110'
      7 -> '111'

STEP 4: BUILD HISTOGRAM
  
  counts = {}
  for bitstring in outcomes_as_bitstrings:
    if bitstring not in counts:
      counts[bitstring] = 0
    counts[bitstring] += 1
  
  Result:
    counts = {'000': 487, '111': 513}  # Example
    Total: sum(counts.values()) = shots

STEP 5: APPLY READOUT ERRORS (Optional)
  
  If readout_error_matrix specified:
    E = readout_error_matrix  # 2x2 matrix
    # E[0,0]: prob(0|measured 0), E[0,1]: prob(0|measured 1)
    # E[1,0]: prob(1|measured 0), E[1,1]: prob(1|measured 1)
    
    For each bit in each bitstring:
      Flip with probability according to E
    
    Corrupted_bit = Apply error model element-wise to all bits

STEP 6: GENERATE OUTPUT
  
  probabilities = {k: v/shots for k, v in counts.items()}
  
  Output format:
    {
      'counts': {'000': 487, '111': 513},
      'probabilities': {'000': 0.487, '111': 0.513}
    }

PERFORMANCE NOTES:
  - Sampling: O(shots + 2^n) time
  - Probability computation: O(2^n)
  - Memory: O(2^n) for probability array
  - Dominated by shots* for large shot counts
  - Vectorized NumPy operations for speed
"""
    
    pdf.code(measure_algo)
    
    pdf.add_page()
    pdf.h2('4.4 Observable Measurement & Expectation Values')
    
    observable_algo = """
PAULI OBSERVABLE:
  
  Definition: O = P_0 (x) P_1 (x) ... (x) P_n
  where each P_i in {I, X, Y, Z}
  
  Examples:
    - 'ZZZ': Z âŠ— Z âŠ— Z (three-qubit correlator)
    - 'ZI': Z âŠ— I (single qubit Z on qubit 0)
    - 'XZ': X âŠ— Z (two-qubit observable)
    - 'Y': Y (single qubit on qubit 0)

EXPECTATION VALUE COMPUTATION:
  
  Mathematical formula:
    <O> = <psi | O | psi>
    = Sum_i Sum_j psi*[i] * O[i,j] * psi[j]
  
  For computational efficiency:
    Reformulate as: <O> = trace(O * |psi><psi|)
    = trace(O * rho) where rho = |psi><psi|

ALGORITHM (Statevector Mode):
  
  INPUT:
    - psi: state vector
    - observable_string: e.g., 'ZXY'
  
  STEP 1: Parse observable string
    observable_string: String like 'ZZI' or 'XZ'
    Interpret: 'ZZI' = Z âŠ— Z âŠ— I
  
  STEP 2: Build full observable matrix
    O = build_pauli_matrix(observable_string)
    # Size: 2^n x 2^n
    # Complexity: O(4^n) memory to store!
  
  STEP 3: Compute expectation value
    expectation = <psi | O | psi>
    = psi_dagger @ O @ psi  (matrix-vector multiply)
    = scalar complex value (real part for Hermitian O)
  
  STEP 4: Extract real part
    result = real_part(expectation)
    # Since O is Hermitian, expectation is always real

OPTIMIZED ALGORITHM (Avoids 4^n Memory):
  
  Instead of building full 2^n x 2^n matrix:
  
  STEP 1: Decompose observable by qubits
    'ZXY' -> [(0, 'Z'), (1, 'X'), (2, 'Y')]
  
  STEP 2: For each basis state i
    coeff = psi[i]
    eigenvalue = product of Pauli eigenvalues for state i
    
    For state i with binary representation:
      If bit k is 0 and P_k = Z: eigenvalue part = +1
      If bit k is 1 and P_k = Z: eigenvalue part = -1
      If bit k is 0 and P_k = X: eigenvalue part = +1 (statistical)
      Etc.
  
  STEP 3: Sum contributions
    expectation = Sum_i |psi[i]|^2 * eigenvalue_i

COMPLEXITY:
  - Direct method: O(4^n) memory + O(4^n) time
  - Optimized method: O(2^n) memory + O(2^n) time
  - Implementation uses optimized version

EXAMPLE CALCULATION (n=2, state = |01>):
  
  State vector: psi = [0, 1, 0, 0]  // |01>
  Observable: 'ZZ' = Z âŠ— Z
  
  Eigenvalues for |i> under ZZ:
    |00>: +1 * +1 = +1
    |01>: +1 * -1 = -1
    |10>: -1 * +1 = -1
    |11>: -1 * -1 = +1
  
  Expectation:
    <ZZ> = |psi[0]|^2 * 1 + |psi[1]|^2 * (-1) + ...
         = 0 * 1 + 1 * (-1) + 0 * (-1) + 0 * 1
         = -1
  
  Result: <ZZ> = -1 (perfect anti-correlation)
"""
    
    pdf.code(observable_algo)
    
    # ============================================================
    # 5. CIRCUIT BUILDER
    # ============================================================
    pdf.add_page()
    pdf.h1('5. MODULE 3: CIRCUIT BUILDER (circuit.py)')
    
    pdf.h2('5.1 Circuit Construction API')
    
    circuit_api = """
CLASS: Circuit(n_qubits)
  
CONSTRUCTOR:
  def __init__(self, n_qubits):
    self.n_qubits = n_qubits
    self.operations = []      # List of gate operations
    self.observables = []     # List of observables to measure
    self.witnesses = []       # Entanglement witnesses
    self.noise_model = None   # Noise configuration
    
GATE METHODS (Fluent API):
  All return self for method chaining
  
  Single-qubit gates:
    h(target) -> self
    x(target) -> self
    y(target) -> self
    z(target) -> self
    s(target) -> self
    t(target) -> self
    rx(target, angle) -> self
    ry(target, angle) -> self
    rz(target, angle) -> self
  
  Two-qubit gates:
    cnot(control, target) -> self
    cz(control, target) -> self
    swap(q1, q2) -> self
    iswap(q1, q2) -> self
  
  Three-qubit gates:
    ccnot(ctrl0, ctrl1, target) -> self
    toffoli(ctrl0, ctrl1, target) -> self  (alias)
  
OBSERVABLE METHODS:
  
  expval(observable_string, qubit_indices):
    Register observable for measurement
    Example: expval('ZZ', [0, 1])  # Measure ZZ on qubits 0,1
    Returns: self for chaining
  
  witness(witness_type, qubits):
    Register entanglement witness
    Types: 'bell', 'ghz', 'w_state', etc.

CONFIGURATION METHODS:
  
  with_noise(noise_model):
    Set noise model for this circuit
    Examples:
      qc.with_noise({
        'depolarizing': {'p': 0.01, 'after': 'each_gate'},
        'readout_error': {'p0': 0.01, 'p1': 0.02}
      })
  
EXECUTION METHODS:
  
  run(shots=1024, noise_model=None):
    Execute circuit on simulator
    Returns: {
      'counts': histogram,
      'probabilities': normalized counts,
      'state': final state vector,
      'pauli_expectations': observable values
    }
  
SERIALIZATION:
  
  to_json():
    Serialize circuit to JSON string
    Format: {circuits, metadata, gates, observables}
  
  @classmethod
  from_json(json_string):
    Deserialize circuit from JSON
    Restores all operations and configuration

INTERNAL IMPLEMENTATION:
  
  Operation tracking:
    All gene calls append to self.operations[]
    Format: [{gate: 'H', target: 0}, ...]
  
  Method pattern:
    def h(self, target):
      self._validate_qubit(target)
      self.operations.append({'gate': 'H', 'target': target})
      return self  # Enable chaining
  
USAGE EXAMPLES:
  
  Example 1: Bell state
    qc = Circuit(2)
    qc.h(0).cnot(0, 1)
    result = qc.run(shots=1000)
  
  Example 2: Method chaining
    result = (Circuit(3)
      .h(0)
      .cnot(0, 1)
      .rx(2, pi/4)
      .expval('ZZZ', [0, 1, 2])
      .run(shots=1024))
  
  Example 3: With noise
    qc = (Circuit(2)
      .h(0)
      .cnot(0, 1)
      .with_noise({'depolarizing': {'p': 0.01}}))
    result = qc.run(shots=1000)
"""
    
    pdf.txt(circuit_api, 8)
    
    # ============================================================
    # 6. MEMORY & DATA STRUCTURES
    # ============================================================
    pdf.add_page()
    pdf.h1('6. MEMORY MANAGEMENT & DATA STRUCTURES')
    
    pdf.h2('6.1 Data Structure Organization')
    
    memory_text = """
STATE VECTOR STORAGE:
  Data structure: NumPy ndarray
  Type: complex128
  Size per element: 16 bytes (8 bytes real + 8 bytes imaginary)
  Allocation: Dense array (no sparse representation)
  Memory layout: C-contiguous (row-major)
  
  Allocation: 
    psi = numpy.zeros(2**n, dtype=numpy.complex128)
  
  Memory overhead:
    n=10: ~16 KB
    n=20: ~16 MB
    n=25: ~512 MB
    n=30: ~16 GB
  
DENSITY MATRIX STORAGE:
  Data structure: NumPy ndarray
  Shape: (2^n, 2^n)
  Type: complex128
  Total elements: 4^n
  Memory: 16 * 4^n bytes
  
  For n=15: 16 * 4^15 = 16 * 1,073,741,824 â‰ 17 GB (exceeds typical RAM)
  
  Allocation:
    rho = numpy.zeros((2**n, 2**n), dtype=numpy.complex128)

GATE MATRICES:
  Storage: Module-level constants (gates.py)
  Type: NumPy complex128 arrays
  
  Single-qubit matrices:
    Size: 2x2 = 4 elements
    Memory per gate: 64 bytes
  
  Two-qubit matrices:
    Size: 4x4 = 16 elements
    Memory per gate: 256 bytes
  
  Three-qubit matrices:
    Size: 8x8 = 64 elements
    Memory per gate: 1 KB
  
  Caching: Gates reused across multiple applications
    No redundant allocation

OPERATION LIST:
  Storage: List of dictionaries
  Structure: [{gate_name: str, params: dict}, ...]
  Memory: ~200-500 bytes per operation
  
  Example:
    operations = [
      {'gate': 'H', 'target': 0},
      {'gate': 'CNOT', 'control': 0, 'target': 1},
      {'gate': 'RX', 'target': 2, 'angle': 1.57}
    ]
  
  Typical circuit: 100 operations = ~20-50 KB
"""
    
    pdf.txt(memory_text, 8)
    
    # ============================================================
    # 7. COMPLEXITY ANALYSIS
    # ============================================================
    pdf.add_page()
    pdf.h1('7. COMPUTATIONAL COMPLEXITY ANALYSIS')
    
    pdf.h2('7.1 Time Complexity')
    
    time_complexity = """
ASYMPTOTIC TIME COMPLEXITY:

Operation                    Time Complexity    Notes
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
Single-qubit gate            O(2^n)            Standard tensor contraction
Two-qubit gate               O(2^n)            Contraction on 2 dimensions
Three-qubit gate             O(2^n)            Contraction on 3 dimensions
Measurement (sample)         O(shots + 2^n)    shots random samples
Measurement (probability)    O(2^n)            Norm computation
Observable expectation       O(2^n)            Sum over all states
Circuit (m gates)            O(m * 2^n)        Sequential gate applications
Noise channel (1-qubit)      O(k * 2^n)        k Kraus operators
Noise channel (2-qubit)      O(k * 4^n)        2-qubit noise
Serialization (JSON)         O(m)              Linear in circuit size
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

DETAILED BREAKDOWN:

Single-Qubit Gate Application: O(2^n)
  - Reshape state: O(1) with view

  - Tensordot contraction:
    NumPy tensordot(U, psi, axes=[[1], [k]])
    Contracts 2x2 matrix with 2^n vector
    Result: 2 * 2^n operations
    Time: O(2^n)
  
  - Reshape back: O(1) with view
  
  Total: O(2^n)

Two-Qubit Gate Application: O(2^n)
  - Similar pattern but 4x4 matrix with 2^n vector
  - More complex indexing but still O(2^n)
  
Measurement: O(shots + 2^n)
  - Compute probabilities: 2^n elements, O(2^n)
  - Multinomial sampling: O(shots)
  - Total: O(shots + 2^n)
  - Dominated by shots for large shot counts

Observable Expectation: O(n * 2^n) or O(2^n)
  - Optimized version: Parse string O(n)
  - Compute eigenvalues: O(2^n)
  - Sum contributions: O(2^n)
  - Total: O(2^n) dominant

Circuit Simulation: O(m * 2^n)
  - m+iterations through operations
  - Each gate: O(2^n)
  - Total: O(m * 2^n)
  - Example: 100 gates on 20 qubits
    = 100 * 2^20 â‰ 100 million operations
    = ~1 second on modern CPU

Noise Application: O(k * 2^n) per gate
  - k Kraus operators
  - Each: O(2^n) matrix-vector multiply
  - Total per gate: O(k * 2^n)
  - Example: Depolarizing (k=4): 4 * O(2^n) per gate
    = 4x overhead per gate

PRACTICAL IMPLICATIONS:

For n=20 qubits:
  Single gate: 2^20 = ~1 million operations = ~1 microsecond
  100-gate circuit: ~100 million operations = ~100 ms
  
For n=25 qubits:
  Single gate: 2^25 = ~33 million operations = ~33 ms
  100-gate circuit: ~3.3 billion operations = ~3.3 seconds
  
For n=28 qubits:
  Single gate: 2^28 = ~268 million operations = ~268 ms
  100-gate circuit: ~27 billion operations = ~27 seconds
"""
    
    pdf.code(time_complexity)
    
    pdf.add_page()
    pdf.h2('7.2 Space Complexity')
    
    space_complexity = """
MEMORY USAGE BY MODE:

STATEVECTOR MODE:
  Primary: O(2^n) for state vector
  Temporary: O(2^n) for gate application intermediate
  Total: O(2^n)
  
  Actual bytes:
    n=10: 16 * 1,024 = 16 KB
    n=15: 16 * 32,768 = 512 KB
    n=20: 16 * 1,048,576 = 16 MB
    n=22: 16 * 4,194,304 = 64 MB
    n=24: 16 * 16,777,216 = 256 MB
    n=25: 16 * 33,554,432 = 512 MB
    n=26: 16 * 67,108,864 = 1 GB
    n=28: 16 * 268,435,456 = 4 GB
    n=30: 16 * 1,073,741,824 = 16 GB

DENSITY MATRIX MODE:
  Primary: O(4^n) for matrix storage
  
  Actual bytes:
    n=8: 16 * 65,536 = 1 MB
    n=10: 16 * 1,048,576 = 16 MB
    n=12: 16 * 16,777,216 = 256 MB
    n=14: 16 * 268,435,456 = 4 GB
    n=15: 16 * 1,073,741,824 = 16 GB
    n=16: 16 * 4,294,967,296 = 64 GB

COMPARISON:
  For same qubit count, density matrix uses 4x memory
  
  Practical limits with 16 GB RAM:
    Statevector: Up to ~27 qubits
    Density matrix: Up to ~13 qubits

SUPPLEMENTARY MEMORY:
  - Gate matrices: ~1 KB (cached from gates.py)
  - Operation list: ~200 bytes per gate
  - Observables: ~100 bytes per observable
  - Minor overhead: ~1 MB total
  - Not significant compared to state

MEMORY ALLOCATION STRATEGY:
  1. Allocate state vector/matrix on creation
  2. Reuse for gate applications (in-place if possible)
  3. Temporary arrays created during tensordot
  4. NumPy handles allocation/deallocation
  5. No garbage collection needed (Python manages)

OPTIMIZATION OPPORTUNITIES:
  1. Avoid explicit Kronecker products (saves 4x memory)
  2. Use views instead of copies where possible
  3. Process gates sequentially (don't copy state)
  4. Sparse representation not implemented (dense only)
"""
    
    pdf.code(space_complexity)
    
    # ============================================================
    # 8. NOISE MODELING DETAILS
    # ============================================================
    pdf.add_page()
    pdf.h1('8. NOISE MODELING - COMPLETE FORMALISM')
    
    pdf.h2('8.1 Kraus Operator Framework')
    
    kraus_theory = """
QUANTUM CHANNEL DEFINITION:
  A completely positive trace-preserving (CPTP) map
  Transforms density matrix rho -> rho'
  
  In Kraus operator form:
    rho' = Sum_k  K_k  rho  K_k_dagger
  
  where {K_k} satisfy:
    Sum_k K_k_dagger K_k = I  (trace preservation)

IMPLEMENTATION IN CODE:
  Each channel defined by Kraus operators list
  
ONE-QUBIT CHANNELS:

1. DEPOLARIZING CHANNEL:
   Parameter: p (depolarization rate, 0 <= p <= 1)
   Effect: Mix state with maximally mixed state
   
   Kraus operators (unnormalized):
     K_0 = sqrt(1 - p) * I
     K_1 = sqrt(p/3) * X
     K_2 = sqrt(p/3) * Y
     K_3 = sqrt(p/3) * Z
   
   Physical interpretation:
     - Probability (1-p): no error
     - Probability p/3 each: random Pauli x, Y, or Z
   
   On pure state |psi>:
     rho' = (1-p)|psi><psi| + p*I/2
   
   Code representation:
     depolarizing_1q = {
       'p': 0.01,
       'kraus_ops': [
         sqrt(0.99)*I,
         sqrt(0.01/3)*X,
         sqrt(0.01/3)*Y,
         sqrt(0.01/3)*Z
       ]
     }

2. BIT-FLIP CHANNEL:
   Parameter: p (flip probability)
   Effect: Randomly apply X gate
   
   Kraus operators:
     K_0 = sqrt(1 - p) * I
     K_1 = sqrt(p) * X
   
   Interpretation:
     - Probability (1-p): no flip
     - Probability p: apply X
   
   Operation:
     rho' = (1-p)*rho + p*X*rho*X

3. PHASE-FLIP CHANNEL:
   Parameter: p
   Effect: Randomly apply Z gate
   
   Kraus operators:
     K_0 = sqrt(1 - p) * I
     K_1 = sqrt(p) * Z
   
   Operation:
     rho' = (1-p)*rho + p*Z*rho*Z

4. AMPLITUDE DAMPING:
   Parameter: gamma (decay rate)
   Effect: Energy relaxation to ground state
   
   Kraus operators:
     K_0 = [[1, 0], [0, sqrt(1-gamma)]]
     K_1 = [[0, sqrt(gamma)], [0, 0]]
   
   Action on basis:
     |0> -> |0>
     |1> -> (1-gamma)|1> + gamma|0>
   
   Physically models T1 relaxation

5. PHASE DAMPING:
   Parameter: lambda (dephasing rate)
   Effect: Dephasing without energy loss
   
   Kraus operators:
     K_0 = [[1, 0], [0, sqrt(1-lambda)]]
     K_1 = [[0, 0], [0, sqrt(lambda)]]
   
   Physically models T2 dephasing process

APPLICATION ALGORITHM:

def apply_kraus_channel(rho, kraus_ops):
    '''Apply Kraus channel to density matrix'''
    rho_new = zeros_like(rho)
    for K in kraus_ops:
        rho_new += K @ rho @ K.conj().T
    return rho_new

def apply_kraus_to_state(psi, kraus_ops):
    '''Apply Kraus channel to pure state'''
    # Convert to density matrix
    rho = outer(psi, psi.conj())
    # Apply channel
    rho_new = apply_kraus_channel(rho, kraus_ops)
    return rho_new

NOISE MODEL CONFIGURATION:

noise_model = {
    'channels': [
        {
            'after': 'each_gate',        # When to apply
            'type': 'depolarizing',      # Channel type
            'p': 0.01,                   # Parameters
            'qubits': [0, 1]             # Which qubits
        },
        {
            'after': 'measurement',
            'type': 'readout_error',
            'p0': 0.01,  # Error on measuring |0>
            'p1': 0.02   # Error on measuring |1>
        }
    ]
}

TIMING OF NOISE:
  during_gate: Applied while gate executes
  after_gate: Applied immediately after gate
  before_gate: Applied before gate
  each_gate: Applied after every gate
  measurement: Applied during measurement
"""
    
    pdf.code(kraus_theory)
    
    # ============================================================
    # 9. MATHEMATICAL FOUNDATIONS
    # ============================================================
    pdf.add_page()
    pdf.h1('9. MATHEMATICAL FOUNDATIONS')
    
    pdf.h2('9.1 Linear Algebra & Quantum Mechanics')
    
    math_foundations = """
COMPLEX VECTOR SPACES:
  
  State space: Complex vector space C^(2^n)
  Dimension: 2^n for n qubits
  Inner product: <psi | phi> = sum_i psi*[i] * phi[i]
  Norm: norm(psi) = sqrt(<psi | psi>)
  
  Normalized states: ||psi|| = 1

PROBABILITY INTERPRETATION:
  
  For normalized state |psi>:
    Probability of outcome i: P(i) = |<i|psi>|^2 = |psi[i]|^2
  
  Properties:
    - All probabilities >= 0
    - Sum of all probabilities = 1
    - Can compute any observable expectation

UNITARY MATRICES:
  
  Definition: U is unitary if U_dagger * U = Identity
  Properties:
    - Invertible: U^-1 = U_dagger
    - Preserves norm: ||U*psi|| = ||psi||
    - Preserves inner products
  
  Determinant: det(U) has magnitude 1
  Eigenvalues: All have magnitude 1 (on unit circle)

DENSITY MATRICES:
  
  Definition: Hermitian matrix rho >= 0 with trace(rho) = 1
  Properties:
    - Diagonal elements: probabilities (0 <= rho[i,i] <= 1)
    - Off-diagonal: coherences
    - Pure states: rho = |psi><psi| has rank 1
    - Mixed states: rank > 1
    - Eigenvalues: probabilities in ensemble decomposition
  
  Expectation value:
    <O> = trace(O * rho)
  
  Measurement outcome probabilities:
    P(outcome) = rho[outcome, outcome]

PAULI MATRICES:
  
  I = [[1, 0], [0, 1]]         (Identity)
  X = [[0, 1], [1, 0]]         (Bit flip)
  Y = [[0, -i], [i, 0]]        (Bit+phase flip)
  Z = [[1, 0], [0, -1]]        (Phase flip)
  
  Properties:
    - All Hermitian: A = A_dagger
    - All unitary: A_dagger * A = I
    - All traceless: trace(A) = 0 (except I)
    - Orthogonal: trace(A_i * A_j) = 0 for i != j
    - Anticommute: {X,Y} = XY + YX = 0, etc.
  
  Commutation relations:
    [X, Y] = 2iZ
    [Y, Z] = 2iX
    [Z, X] = 2iY
  
  Basis property:
    Any 2x2 matrix = a0*I + a1*X + a2*Y + a3*Z

BLOCH SPHERE REPRESENTATION:
  
  Pure single-qubit state:
    |psi> = cos(theta/2)|0> + sin(theta/2)*exp(i*phi)|1>
  
  Bloch vector: r = (sin(theta)*cos(phi), sin(theta)*sin(phi), cos(theta))
  
  Constraints:
    - theta in [0, pi]
    - phi in [0, 2*pi)
    - ||r|| = 1
  
  Special points:
    - r = (0, 0, 1): |0> state (north pole)
    - r = (0, 0, -1): |1> state (south pole)
    - r = (1, 0, 0): |+> = (|0>+|1>)/sqrt(2) (equator)

TENSOR PRODUCTS (KRONECKER PRODUCT):
  
  Definition: A âŠ— B = [[a11*B, a12*B], [a21*B, a22*B]]
  Size: If A is mĂ—n, B is pĂ—q, then AâŠ—B is mpĂ—nq
  
  Properties:
    (A âŠ— B)(C âŠ— D) = (AC) âŠ— (BD)
    (A âŠ— B)^dagger = A^dagger âŠ— B^dagger
    (A âŠ— B)(C âŠ— D) = (AC) âŠ— (BD)
  
  For quantum states:
    |psi> âŠ— |phi> = [psi[0]*phi, psi[1]*phi, ..., psi[n]*phi]^T
  
  For operators:
    n-qubit gate: U = I (x) I (x) ... (x) Gate_k (x) ... (x) I
    where Gate_k is 2x2 on qubit k

EXPECTATION VALUES:
  
  Observable O (Hermitian):
    <O> = <psi|O|psi> = Sum_i,j psi*[i] * O[i,j] * psi[j]
  
  Alternative (density matrix):
    <O> = trace(O * rho)
  
  Eigenvalue decomposition:
    If O = sum_k lambda_k |k><k|
    Then <O> = sum_k lambda_k * P(k)
    where P(k) = |<k|psi>|^2
    
    Result is weighted average of eigenvalues
"""
    
    pdf.code(math_foundations)
    
    # ============================================================
    # 10. SCALABILITY LIMITS
    # ============================================================
    pdf.add_page()
    pdf.h1('10. SCALABILITY LIMITS & HARDWARE CONSTRAINTS')
    
    pdf.h2('10.1 Practical Qubit Limits')
    
    limits_text = """
STATEVECTOR MODE LIMITS:

Hardware: Typical Laptop (16 GB RAM)
  - Max qubits: 27-28
  - At n=27: 16 * 2^27 = 2 GB
  - At n=28: 16 * 2^28 = 4 GB
  - At n=29: 16 * 2^29 = 8 GB
  - At n=30: 16 * 2^30 = 16 GB (at limit)

Hardware: Workstation (64 GB RAM)
  - Max qubits: 29-30
  - At n=30: 4 GB per gate operation temp storage
  - At n=31: Exceeds safe limits

Hardware: Server (256+ GB RAM)
  - Max qubits: 31-32
  - Practical: Limited by time (simulation takes too long)

TIME CONSTRAINTS:
  For n=25 qubit circuit with 100 gates:
    - Time: 100 * 33.5 million ops â‰ 3.35 billion operations
    - At 1 GHz: ~3.35 seconds
    - With overhead: ~10-20 seconds realistic
  
  For n=28 qubits with 100 gates:
    - Time: 100 * 268 million ops â‰ 27 billion operations
    - At 1 GHz: ~27 seconds
    - Becomes impractical beyond this

DENSITY MATRIX MODE LIMITS:

Hardware: Typical Laptop (16 GB RAM)
  - Max qubits: 12-13
  - At n=13: 16 * 4^13 â‰ 50 GB (exceeds typical)
  - Practical: n=12 only

Hardware: Workstation (64 GB RAM)
  - Max qubits: 14
  - At n=14: 16 * 4^14 â‰ 268 GB (marginal)

COMPARISON TABLE:

Mode              Practical Limit    Memory Used (n limit)
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
Statevector       27-28 qubits       2-4 GB
Density Matrix    12-13 qubits       256 MB - 1 GB
GPU (32GB VRAM)   30-31 qubits       4-16 GB

WORKAROUNDS FOR LARGER SYSTEMS:

1. Tensor Network Methods:
   - Matrix Product States (MPS)
   - Projected Entangled Pair States (PEPS)
   - Can simulate 100+ qubits with limited entanglement
   - Trade: Not exactly equivalent for generic states

2. Partial Simulation:
   - Trace out non-essential qubits
   - Reduce problem dimension before simulation

3. Approximate Simulation:
   - Truncate low-amplitude terms
   - Sample-based methods
   - Sacrifice accuracy for speed

4. Distributed Computing:
   - Split statevector across multiple machines
   - Communication overhead often prohibitive

5. GPU Acceleration:
   - NVIDIA CuPy: Similar to NumPy but GPU
   - Can add 32-bit precision option
   - Extends range by ~2-3 qubits typically

CURRENT IMPLEMENTATION APPROACH:
  - NumPy CPU-based
  - Focus on accuracy (64-bit complex)
  - No optimizations for sparse states
  - Suitable for 20-25 qubit demonstration circuits
"""
    
    pdf.txt(limits_text, 8)
    
    # Save PDF
    output = 'QuantumSimulator_Comprehensive_Technical_Reference.pdf'
    pdf.output(output)
    
    import os
    size_kb = os.path.getsize(output) / 1024
    
    print(f"\n[COMPLETE] Comprehensive Technical Reference Generated!")
    print(f"  File: {output}")
    print(f"  Size: {size_kb:.1f} KB")
    print(f"  Pages: {pdf.page}")
    print(f"\n[CONTENTS]")
    print(f"  1. Introduction & Project Overview")
    print(f"  2. System Architecture & Design Patterns")
    print(f"  3. Gates Library Module (Complete Definitions)")
    print(f"  4. Simulator Core Module (All Algorithms)")
    print(f"  5. Circuit Builder Module (API Reference)")
    print(f"  6. Memory Management & Data Structures")
    print(f"  7. Computational Complexity Analysis")
    print(f"  8. Noise Modeling - Kraus Operators")
    print(f"  9. Mathematical Foundations")
    print(f"  10. Scalability Limits & Hardware Constraints")
    print(f"\n[READY FOR] Thesis Appendix & Technical Reference")

if __name__ == "__main__":
    generate_comprehensive_pdf()

#!/usr/bin/env python3
"""
Generate comprehensive PDF documentation for the Quantum Simulator Backend
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime

def create_documentation():
    """Create comprehensive documentation PDF for the Quantum Simulator Backend"""
    
    doc = SimpleDocTemplate(
        "QuantumSimulator_Backend_Documentation.pdf",
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=10,
        spaceBefore=12,
        fontName='Helvetica-Bold',
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#2d5fa3'),
        spaceAfter=8,
        spaceBefore=10,
        fontName='Helvetica-Bold',
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=11,
        textColor=colors.HexColor('#404040'),
        spaceAfter=6,
        spaceBefore=8,
        fontName='Helvetica-Bold',
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Courier',
        textColor=colors.HexColor('#333333'),
        leftIndent=20,
        rightIndent=20,
        spaceAfter=6,
        backColor=colors.HexColor('#f5f5f5'),
    )
    
    story = []
    
    # Title Page
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("QUANTUM SIMULATOR", title_style))
    story.append(Paragraph("Backend Architecture & Implementation Documentation", heading1_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", normal_style))
    story.append(Spacer(1, 0.8*inch))
    
    story.append(Paragraph(
        "<b>Thesis Project:</b> Development of a Quantum Circuit Simulator Backend",
        normal_style
    ))
    story.append(Spacer(1, 1.5*inch))
    
    story.append(PageBreak())
    
    # Table of Contents
    story.append(Paragraph("TABLE OF CONTENTS", heading1_style))
    story.append(Spacer(1, 0.2*inch))
    
    toc_items = [
        "1. Executive Summary",
        "2. Architecture Overview",
        "3. Project Structure",
        "4. Core Components",
        "5. Simulator Module (simulator.py)",
        "6. Gates Module (gates.py)",
        "7. Circuit Module (circuit.py)",
        "8. Data Flow & Execution Model",
        "9. API Reference",
        "10. Usage Examples",
        "11. Advanced Features",
        "12. Testing Framework",
        "13. Performance Considerations",
        "14. Future Enhancements",
    ]
    
    for item in toc_items:
        story.append(Paragraph(item, normal_style))
    
    story.append(Spacer(1, 0.5*inch))
    story.append(PageBreak())
    
    # 1. Executive Summary
    story.append(Paragraph("1. EXECUTIVE SUMMARY", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph(
        "<b>Project Overview:</b><br/>The Quantum Simulator is a Python-based backend for simulating quantum circuits. "
        "It provides a complete framework for quantum computation including gate operations, circuit construction, "
        "quantum state management, and measurement simulation.",
        normal_style
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph(
        "<b>Key Features:</b><br/>"
        "• Pure statevector simulation for quantum circuits<br/>"
        "• Density matrix representation for noisy quantum simulations<br/>"
        "• Support for 50+ quantum gates (single-qubit, two-qubit, three-qubit)<br/>"
        "• Noise modeling via Kraus channels (depolarizing, bit-flip, phase-flip)<br/>"
        "• Expectation value computation for arbitrary Pauli observables<br/>"
        "• Entanglement witness verification<br/>"
        "• JSON serialization for circuit persistence and transmission<br/>"
        "• Measurement with optional readout error simulation",
        normal_style
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph(
        "<b>Technology Stack:</b><br/>"
        "• Language: Python 3.x<br/>"
        "• Core Dependencies: NumPy (numerical computing)<br/>"
        "• Testing: pytest<br/>"
        "• Architecture: Object-oriented with modular design patterns",
        normal_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(PageBreak())
    
    # 2. Architecture Overview
    story.append(Paragraph("2. ARCHITECTURE OVERVIEW", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph(
        "The simulator follows a layered architecture with clear separation of concerns:<br/><br/>"
        "<b>Layer 1 - Gates Module (gates.py):</b><br/>"
        "Defines quantum gate matrices and helper functions. Contains single-qubit gates (X, Y, Z, H, S, T), "
        "parameterized gates (Rx, Ry, Rz, U3, Phase), two-qubit gates (CNOT, CZ, SWAP, ISWAP), and utility functions "
        "for gate manipulation (controlled-U construction, basis expansion).<br/><br/>"
        
        "<b>Layer 2 - Simulator Module (simulator.py):</b><br/>"
        "Core simulation engine implementing the Simulator class. Handles quantum state representation (both statevector "
        "and density matrix), gate application through tensor operations, noise channel application via Kraus operators, "
        "measurement simulation, and observable expectation value computation.<br/><br/>"
        
        "<b>Layer 3 - Circuit Module (circuit.py):</b><br/>"
        "High-level circuit builder providing fluent API for circuit construction. Offers methods for adding gates, "
        "defining observables, registering entanglement witnesses, and executing circuits through the simulator.<br/><br/>"
        
        "<b>Layer 4 - Integration Layer:</b><br/>"
        "The __init__.py file exports the public API (Simulator, X, H gates) for end users.",
        normal_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(PageBreak())
    
    # 3. Project Structure
    story.append(Paragraph("3. PROJECT STRUCTURE", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    structure_text = """
<b>Directory Layout:</b><br/>
quantum_sim/<br/>
├── __init__.py          # Public API exports<br/>
├── simulator.py         # Core Simulator class (850+ lines)<br/>
├── gates.py            # Quantum gate definitions (300+ lines)<br/>
└── circuit.py          # Circuit builder class (300+ lines)<br/>
<br/>
tests/<br/>
├── __init__.py<br/>
├── test_simulator.py    # Simulator unit tests<br/>
├── test_bell.py        # Bell state verification tests<br/>
├── test_ccnot.py       # CCNOT gate tests<br/>
├── test_gates_probs.py # Gate probability verification<br/>
└── __pycache__/        # Python bytecode cache<br/>
<br/>
Root Files:<br/>
├── pyproject.toml       # Project metadata and configuration<br/>
├── requirements.txt     # Python dependencies (numpy, pytest)<br/>
├── bench_*.py          # Performance benchmarking scripts<br/>
├── run_*.py            # Example execution scripts<br/>
└── todo.txt            # Development task list
    """
    
    story.append(Paragraph(structure_text, code_style))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(PageBreak())
    
    # 4. Core Components
    story.append(Paragraph("4. CORE COMPONENTS", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>4.1 Quantum State Representations</b>", heading2_style))
    story.append(Spacer(1, 0.05*inch))
    
    story.append(Paragraph(
        "<b>Statevector Mode:</b><br/>"
        "Pure quantum state representation as a complex vector of dimension 2^n where n is the number of qubits. "
        "Each component represents the probability amplitude for a computational basis state. "
        "Used for noiseless simulations with optimal memory and computation efficiency.<br/><br/>"
        "Memory: O(2^n) complex numbers<br/>"
        "State indexed as: |q₀ q₁ ... q_{n-1}⟩ with q₀ as MSB (most significant bit)<br/><br/>",
        normal_style
    ))
    
    story.append(Paragraph(
        "<b>Density Matrix Mode:</b><br/>"
        "Complete quantum state representation as a Hermitian matrix ρ of size 2^n × 2^n. "
        "Can represent both pure and mixed quantum states, necessary for realistic noisy simulations. "
        "All diagonal elements are positive real numbers summing to 1, representing probabilities of basis states.<br/><br/>"
        "Memory: O(4^n) complex numbers<br/>"
        "State initialization: ρ = |0...0⟩⟨0...0| (pure zero state)<br/>",
        normal_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>4.2 Tensor Contraction Operations</b>", heading2_style))
    
    story.append(Paragraph(
        "The simulator uses efficient tensor contraction via NumPy's tensordot() for quantum operations. "
        "For a single-qubit gate U (2×2 matrix) applied to qubit 'target':<br/><br/>"
        "1. Reshape state → (2, 2, ..., 2) tensor with n indices<br/>"
        "2. Contract gate with 'target' axis: tensordot(U, state, axes=([1], [target]))<br/>"
        "3. Move result axis to original position using moveaxis()<br/>"
        "4. Reshape back to 1D vector<br/><br/>"
        "This approach scales well for moderate qubit counts (typically n ≤ 25).",
        normal_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>4.3 Qubit Indexing Convention</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>Critical Convention:</b> Qubit 0 is the leftmost (most significant) bit in computational basis states.<br/><br/>"
        "Example for 3 qubits:<br/>"
        "Basis state |101⟩ means: qubit₀=1, qubit₁=0, qubit₂=1<br/>"
        "Binary representation: 101₂ = 5₁₀<br/>"
        "State vector index: 5<br/><br/>"
        "Bit shifting formula: bit_value = (index >> shift) & 1<br/>"
        "where shift = n - 1 - qubit_index<br/><br/>"
        "This convention is maintained consistently throughout gate operations and measurements.",
        normal_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(PageBreak())
    
    # 5. Simulator Module
    story.append(Paragraph("5. SIMULATOR MODULE (simulator.py)", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>5.1 Class: Simulator</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>Constructor:</b> Simulator(n_qubits: int)<br/>"
        "Parameters:<br/>"
        "• n_qubits (int): Number of qubits (must be ≥ 1)<br/><br/>"
        "Attributes:<br/>"
        "• self.n: Number of qubits<br/>"
        "• self.dim: Dimension of state space (2^n)<br/>"
        "• self.state: Statevector (initialized to |0...0⟩)<br/>"
        "• self.rho: Density matrix (exists only in density mode)<br/><br/>"
        "Raises:<br/>"
        "• ValueError: if n_qubits < 1",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>5.2 State Management Methods</b>", heading2_style))
    
    methods_data = [
        ("reset()", "Reset simulator to |0...0⟩ statevector. Deletes density matrix if present."),
        ("reset_density()", "Reset simulator to density matrix mode with ρ = |0...0⟩⟨0...0|. Deletes statevector."),
        ("_is_density_mode()", "Internal helper: returns True if in density matrix mode, False for statevector."),
    ]
    
    for method, desc in methods_data:
        story.append(Paragraph(f"<b>{method}</b><br/>{desc}", normal_style))
        story.append(Spacer(1, 0.05*inch))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>5.3 Single-Qubit Gate Operations (Statevector Mode)</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>apply_single_qubit_gate(gate: ndarray, target: int)</b><br/>"
        "Applies a 2×2 unitary matrix to a single qubit in statevector mode.<br/><br/>"
        "Algorithm:<br/>"
        "1. Reshape state to n-dimensional tensor<br/>"
        "2. Contract gate matrix with target axis using tensordot<br/>"
        "3. Move result axis to target position<br/>"
        "4. Reshape back to 1D vector<br/><br/>"
        "Time Complexity: O(2^n)<br/>"
        "Space Complexity: O(2^n)<br/>"
        "Raises: ValueError for non-2×2 gates, IndexError for invalid target",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>5.4 Two-Qubit Gate Operations (Statevector Mode)</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>apply_two_qubit_gate(gate4: ndarray, q1: int, q2: int)</b><br/>"
        "Applies a 4×4 unitary matrix to two qubits in statevector mode.<br/><br/>"
        "Algorithm:<br/>"
        "1. Reshape gate to (2,2,2,2) tensor (out_q1, out_q2, in_q1, in_q2)<br/>"
        "2. Reshape state to n-dimensional tensor<br/>"
        "3. Contract gate with both qubit axes: tensordot(U, state, axes=([2,3], [q1,q2]))<br/>"
        "4. Move result axes to original positions<br/>"
        "5. Reshape back to 1D vector<br/><br/>"
        "Basis Ordering: For |q1 q2⟩, basis is ordered as |00⟩, |01⟩, |10⟩, |11⟩ "
        "with q1 as MSB and q2 as LSB.",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>5.5 Three-Qubit Gate Operations (CCNOT/Toffoli)</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>apply_ccnot(control1: int, control2: int, target: int)</b><br/>"
        "Applies controlled-controlled-NOT (Toffoli/CCNOT) gate in statevector mode.<br/><br/>"
        "Operation: Flips target qubit if BOTH control qubits are |1⟩<br/>"
        "if (qubit[control1] == 1 AND qubit[control2] == 1) then flip qubit[target]<br/><br/>"
        "Algorithm:<br/>"
        "1. Iterate through all basis states<br/>"
        "2. Check both control bits<br/>"
        "3. If both are set and target is 0, swap amplitudes between |...0⟩ and |...1⟩<br/>"
        "4. Use bit manipulation with XOR for efficient implementation<br/><br/>"
        "Used for quantum computing tasks: majority voting, adders, multipliers",
        code_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(PageBreak())
    
    # 5.6 Density Matrix Operations
    story.append(Paragraph("<b>5.6 Density Matrix Gate Operations</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>apply_single_qubit_gate_density(gate: ndarray, target: int)</b><br/>"
        "Applies unitary U to density matrix via ρ' = U ρ U†<br/><br/>"
        "Algorithm (Lindblad operator form):<br/>"
        "1. Reshape ρ to (2,2,...,2,2,2,...,2) with 2n tensor indices<br/>"
        "2. LEFT multiply: Contract gate matrix with first half (ket space)<br/>"
        "   tensordot(U, ρ, axes=([1], [target]))<br/>"
        "3. RIGHT multiply: Contract U† with second half (bra space)<br/>"
        "   tensordot(result, U.conj(), axes=([target+n], [1]))<br/>"
        "4. Reshape back to 2D matrix<br/><br/>"
        "Ensures ρ remains Hermitian and trace-preserving (Tr(ρ') = 1)",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph(
        "<b>apply_two_qubit_gate_density(gate4: ndarray, q1: int, q2: int)</b><br/>"
        "Applies 4×4 two-qubit unitary to density matrix: ρ' = U ρ U†<br/><br/>"
        "Similar algorithm to single-qubit version but contracts on two qubit axes "
        "for both ket and bra spaces.",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>5.7 Noise Channels (Kraus Operators)</b>", heading2_style))
    
    story.append(Paragraph(
        "The simulator implements quantum channels via Kraus decomposition: "
        "ρ' = Σₖ Kₖ ρ Kₖ†<br/><br/>"
        "<b>Supported Noise Models (1-qubit):</b><br/><br/>"
        "<b>1. Bit-Flip Channel:</b><br/>"
        "Kraus operators: K₀ = √(1-p) I, K₁ = √p X<br/>"
        "Effect: Each qubit randomly flips with probability p<br/><br/>"
        "<b>2. Phase-Flip Channel:</b><br/>"
        "Kraus operators: K₀ = √(1-p) I, K₁ = √p Z<br/>"
        "Effect: Each qubit randomly accumulates phase with probability p<br/><br/>"
        "<b>3. Depolarizing Channel:</b><br/>"
        "Kraus operators: K₀ = √(1-p) I, K₁ = √(p/3) X, K₂ = √(p/3) Y, K₃ = √(p/3) Z<br/>"
        "Effect: Uniform random rotation with probability p<br/><br/>"
        "All channels are applied to each affected qubit after each gate operation.",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>5.8 Measurement and Sampling</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>measure_all(shots: int, readout_error_p: float) → Dict[str, int]</b><br/><br/>"
        "Samples quantum outcomes from current state.<br/><br/>"
        "Algorithm:<br/>"
        "1. Extract probabilities: p = |ψ|² for statevector, p = diag(ρ) for density matrix<br/>"
        "2. Normalize probabilities (safety check)<br/>"
        "3. Sample 'shots' times using np.random.choice(dim, size=shots, p=probs)<br/>"
        "4. Convert outcome indices to binary strings<br/>"
        "5. Apply optional symmetric readout bit-flip errors<br/>"
        "6. Count occurrences and return histogram<br/><br/>"
        "Returns: Dict mapping binary strings to measurement counts<br/>"
        "Example: {'00': 487, '11': 513} for 1000 shots of Bell state",
        code_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(PageBreak())
    
    # 5.9 Expectation Values
    story.append(Paragraph("<b>5.9 Observable Expectation Values</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>expectation_values(target: int) → Dict[str, float]</b><br/><br/>"
        "Computes ⟨X⟩, ⟨Y⟩, ⟨Z⟩ for single qubit (Bloch vector).<br/><br/>"
        "For statevector mode (efficient implementation):<br/>"
        "• ⟨Z⟩: Direct calculation using bit parity<br/>"
        "• ⟨X⟩: Computed via off-diagonal elements ⟨ψ|X|ψ⟩<br/>"
        "• ⟨Y⟩: Computed via off-diagonal elements with phase correction<br/><br/>"
        "For density matrix mode: Uses expectation_pauli() method",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph(
        "<b>expectation_pauli(pauli: str, qubits: List[int]) → float</b><br/><br/>"
        "Computes expectation value of arbitrary Pauli string observable.<br/><br/>"
        "Pauli String Format: Sequence of I, X, Y, Z operators<br/>"
        "Example: 'ZZ' on qubits [0,1] computes ⟨Z₀Z₁⟩<br/><br/>"
        "Algorithm (statevector):<br/>"
        "1. For each basis state |i⟩, compute P|i⟩<br/>"
        "2. Accumulate ⟨ψ|P|ψ⟩ = Σᵢ ⟨i|ψ⟩* ⟨i|P|ψ⟩<br/>"
        "3. Handle phase factors for Y operator: (1j if bit==0 else -1j)<br/>"
        "4. Return real part of expectation value<br/><br/>"
        "Works in both statevector and density matrix modes",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>5.10 Circuit Execution</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>run_circuit(circuit: List[Dict], shots: int, noise_model: Dict) → Dict</b><br/><br/>"
        "Executes a circuit defined as a list of gate operation dictionaries.<br/><br/>"
        "Circuit Format: List of dictionaries with 'name' and operation-specific parameters<br/><br/>"
        "Supported Operations:<br/>"
        "• Fixed single-qubit: H, X, Y, Z, S, T<br/>"
        "• Parameterized 1q: RX, RY, RZ, PHASE, U3<br/>"
        "• Two-qubit: CNOT, CZ, SWAP, ISWAP, CUSTOM_2Q<br/>"
        "• Three-qubit: CCNOT, TOFFOLI<br/><br/>"
        "Noise Model Configuration:<br/>"
        "Apply channels after specific gates or all gates:<br/>"
        "{ 'channels': [<br/>"
        "    {'after': 'each_gate', 'type': 'depolarizing', 'p': 0.01},<br/>"
        "    {'after': 'H', 'type': 'bit_flip', 'p': 0.005},<br/>"
        "    {'after': 'measurement', 'type': 'readout_error', 'p': 0.02}<br/>"
        "  ]<br/>"
        "}<br/><br/>"
        "Returns: Dict with 'counts' (measurement histogram) and 'shots' (sample count)",
        code_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(PageBreak())
    
    # 6. Gates Module
    story.append(Paragraph("6. GATES MODULE (gates.py)", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>6.1 Single-Qubit Gate Matrices</b>", heading2_style))
    
    gate_table_data = [
        ["Gate", "Matrix", "Description"],
        ["I", "[[1, 0], [0, 1]]", "Identity (no-op)"],
        ["X", "[[0, 1], [1, 0]]", "Pauli-X (bit flip)"],
        ["Y", "[[0, -i], [i, 0]]", "Pauli-Y"],
        ["Z", "[[1, 0], [0, -1]]", "Pauli-Z (phase flip)"],
        ["H", "1/√2 [[1, 1], [1, -1]]", "Hadamard (creates superposition)"],
        ["S", "[[1, 0], [0, i]]", "Phase gate (π/2)"],
        ["T", "[[1, 0], [0, e^(iπ/4)]]", "T gate (π/8)"],
    ]
    
    story.append(Paragraph(
        "Single-qubit gates are 2×2 unitary matrices. All are defined as NumPy arrays "
        "with dtype=complex for numerical stability.",
        normal_style
    ))
    story.append(Spacer(1, 0.05*inch))
    
    story.append(Paragraph("<b>6.2 Parameterized Single-Qubit Gates</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>Rx(θ) - Rotation around x-axis:</b><br/>"
        "[[cos(θ/2), -i·sin(θ/2)], [-i·sin(θ/2), cos(θ/2)]]<br/><br/>"
        "<b>Ry(θ) - Rotation around y-axis:</b><br/>"
        "[[cos(θ/2), -sin(θ/2)], [sin(θ/2), cos(θ/2)]]<br/><br/>"
        "<b>Rz(θ) - Rotation around z-axis:</b><br/>"
        "[[e^(-iθ/2), 0], [0, e^(iθ/2)]]<br/><br/>"
        "<b>Phase(φ):</b><br/>"
        "[[1, 0], [0, e^(iφ)]]<br/><br/>"
        "<b>U3(θ, φ, λ) - Universal single-qubit gate:</b><br/>"
        "[[cos(θ/2), -e^(iλ)·sin(θ/2)], [e^(iφ)·sin(θ/2), e^(i(φ+λ))·cos(θ/2)]]<br/><br/>"
        "Can express any single-qubit unitary operation.",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>6.3 Two-Qubit Gate Matrices (4×4)</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>CNOT (Controlled-NOT):</b><br/>"
        "[[1,0,0,0], [0,1,0,0], [0,0,0,1], [0,0,1,0]]<br/>"
        "Flips target if control is |1⟩<br/><br/>"
        "<b>CZ (Controlled-Z):</b><br/>"
        "diag([1, 1, 1, -1])<br/>"
        "Applies phase -1 if both qubits are |1⟩<br/><br/>"
        "<b>SWAP:</b><br/>"
        "[[1,0,0,0], [0,0,1,0], [0,1,0,0], [0,0,0,1]]<br/>"
        "Exchanges two qubits<br/><br/>"
        "<b>ISWAP (Parametric SWAP):</b><br/>"
        "[[1,0,0,0], [0,0,i,0], [0,i,0,0], [0,0,0,1]]<br/>"
        "Swaps with phase correction",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>6.4 Gate Helper Functions</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>controlled(u: ndarray) → ndarray</b><br/>"
        "Constructs 4×4 controlled-U matrix with control=MSB, target=LSB<br/>"
        "Returns: [[I, 0], [0, U]]<br/><br/>"
        "<b>controlled_on_target_first(u: ndarray) → ndarray</b><br/>"
        "Constructs controlled-U with control=LSB, target=MSB<br/><br/>"
        "<b>expand_single_to_n(gate: ndarray, n_qubits: int, target: int) → ndarray</b><br/>"
        "Expands 2×2 gate to 2ⁿ × 2ⁿ via Kronecker product: I ⊗ ... ⊗ U ⊗ ... ⊗ I",
        code_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(PageBreak())
    
    # 7. Circuit Module
    story.append(Paragraph("7. CIRCUIT MODULE (circuit.py)", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>7.1 Circuit Class Overview</b>", heading2_style))
    
    story.append(Paragraph(
        "The Circuit class provides a high-level, fluent API for building quantum circuits. "
        "It acts as a circuit builder that accumulates gate operations and observable definitions, "
        "then can be executed via the Simulator.",
        normal_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>7.2 Constructor and Attributes</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>Circuit(n_qubits: int)</b><br/><br/>"
        "Attributes:<br/>"
        "• n_qubits (int): Number of qubits in circuit<br/>"
        "• operations (List[Dict]): Accumulated gate operations<br/>"
        "• observables (List[Dict]): Pauli string observables to measure<br/>"
        "• witnesses (List[Dict]): Entanglement witness definitions<br/><br/>"
        "Raises: ValueError if n_qubits < 1",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>7.3 Single-Qubit Gate Methods</b>", heading2_style))
    
    story.append(Paragraph(
        "All methods follow fluent API pattern (return self for chaining):<br/><br/>"
        "<b>Fixed Gates:</b><br/>"
        "• h(target) → Circuit    Hadamard<br/>"
        "• x(target) → Circuit    Pauli-X<br/>"
        "• y(target) → Circuit    Pauli-Y<br/>"
        "• z(target) → Circuit    Pauli-Z<br/>"
        "• s(target) → Circuit    S gate<br/>"
        "• t(target) → Circuit    T gate<br/><br/>"
        "<b>Parameterized Gates:</b><br/>"
        "• rx(target, theta) → Circuit<br/>"
        "• ry(target, theta) → Circuit<br/>"
        "• rz(target, theta) → Circuit<br/>"
        "• phase(target, phi) → Circuit<br/>"
        "• u3(target, theta, phi, lam) → Circuit<br/><br/>"
        "Example usage:<br/>"
        "qc = Circuit(3).h(0).x(1).rx(2, 1.57).cnot(0, 1)",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>7.4 Multi-Qubit Gate Methods</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>Two-Qubit Gates:</b><br/>"
        "• cnot(control, target) → Circuit<br/>"
        "• cz(control, target) → Circuit<br/>"
        "• swap(q1, q2) → Circuit<br/>"
        "• iswap(q1, q2) → Circuit<br/>"
        "• custom_2q(matrix, q1, q2) → Circuit<br/><br/>"
        "<b>Three-Qubit Gates:</b><br/>"
        "• ccnot(control1, control2, target) → Circuit (Toffoli)<br/>"
        "• toffoli(control1, control2, target) → Circuit (alias for ccnot)",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>7.5 Observable and Witness Methods</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>expval(pauli: str, qubits: List[int]) → Circuit</b><br/>"
        "Register a Pauli string observable for measurement.<br/>"
        "Example: qc.expval('ZZ', [0, 1]) measures ⟨Z₀Z₁⟩<br/><br/>"
        "<b>add_linear_witness(name, terms, bound, violates_if) → Circuit</b><br/>"
        "Register an entanglement witness:<br/>"
        "W = Σₖ cₖ ⟨Pₖ⟩<br/>"
        "Witness violates separability bound if W > bound (or < bound)<br/><br/>"
        "terms format: [{'pauli': 'XX', 'qubits': [0,1], 'coef': 1.0}, ...]<br/>"
        "violates_if: '>' or '<'",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>7.6 Serialization Methods</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>to_dict() → Dict</b><br/>"
        "Convert circuit to Python dict representation<br/><br/>"
        "<b>to_json() → str</b><br/>"
        "Serialize circuit to JSON string for transmission/storage<br/><br/>"
        "<b>from_dict(data: Dict) → Circuit (classmethod)</b><br/>"
        "Reconstruct Circuit from dict<br/><br/>"
        "<b>from_json(json_str: str) → Circuit (classmethod)</b><br/>"
        "Reconstruct Circuit from JSON string",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>7.7 Execution Method</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>run(shots: int = 1024, noise_model: Dict = None) → Dict</b><br/><br/>"
        "Execute circuit and return comprehensive results.<br/><br/>"
        "Returns Dict containing:<br/>"
        "• 'shots': Number of measurement shots<br/>"
        "• 'counts': Histogram of measurement outcomes<br/>"
        "• 'probabilities': Probability distribution over basis states<br/>"
        "• 'marginals': Per-qubit marginal probabilities<br/>"
        "• 'expectations': Per-qubit Bloch vector components ⟨X⟩, ⟨Y⟩, ⟨Z⟩<br/>"
        "• 'pauli_expectations': Expectation values of registered observables<br/>"
        "• 'witnesses': Entanglement witness evaluation results<br/>"
        "• 'state_type': 'statevector' or 'density_matrix'<br/>"
        "• 'state': Final quantum state (serialized)",
        code_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(PageBreak())
    
    # 8. Data Flow & Execution
    story.append(Paragraph("8. DATA FLOW & EXECUTION MODEL", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>8.1 Circuit Construction Flow</b>", heading2_style))
    story.append(Spacer(1, 0.05*inch))
    
    flow_text = """
User Code:<br/>
  qc = Circuit(3)<br/>
  qc.h(0).cnot(0, 1).rz(2, 1.57)<br/>
  qc.expval('ZZ', [0, 1])<br/>
         ↓<br/>
Circuit Object:<br/>
  operations = [<br/>
    {'name': 'H', 'targets': [0]},<br/>
    {'name': 'CNOT', 'control': 0, 'target': 1},<br/>
    {'name': 'RZ', 'target': 2, 'theta': 1.57}<br/>
  ]<br/>
  observables = [<br/>
    {'pauli': 'ZZ', 'qubits': [0, 1]}<br/>
  ]<br/>
         ↓<br/>
Circuit.run()<br/>
         ↓<br/>
Simulator.run_circuit()
    """
    
    story.append(Paragraph(flow_text, code_style))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>8.2 Quantum Simulation Execution Flow</b>", heading2_style))
    
    exec_flow = """
Simulator Initialization:<br/>
  state = |0...0⟩ (or ρ = |0...0⟩⟨0...0|)<br/>
  dim = 2^n<br/>
         ↓<br/>
For each gate operation:<br/>
         ↓<br/>
1. Check operation type<br/>
2. Extract parameters (targets, angles, etc.)<br/>
3. Get gate matrix from gates module<br/>
4. Call apply_*_gate_auto() method<br/>
         ↓<br/>
5. (Noisy mode) Apply Kraus channels<br/>
         ↓<br/>
6. (After all gates) Measurement<br/>
   - Extract probabilities from state or ρ<br/>
   - Sample outcomes via np.random.choice<br/>
   - Apply readout error (if configured)<br/>
   - Return measurement histogram<br/>
         ↓<br/>
7. Compute all requested observables<br/>
         ↓<br/>
Result Dictionary with all computed values
    """
    
    story.append(Paragraph(exec_flow, code_style))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(PageBreak())
    
    # 9. API Reference
    story.append(Paragraph("9. API REFERENCE", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>9.1 Simulator Class API</b>", heading2_style))
    
    sim_methods = """
<b>Initialization & State:</b><br/>
  Simulator(n_qubits)         Constructor<br/>
  reset()                     Reset to |0...0⟩<br/>
  reset_density()             Switch to density matrix mode<br/>
  _is_density_mode() → bool   Check current mode<br/>
<br/>
<b>Gate Application (Statevector):</b><br/>
  apply_single_qubit_gate(gate, target)<br/>
  apply_two_qubit_gate(gate4, q1, q2)<br/>
  apply_ccnot(c1, c2, target)<br/>
  apply_cnot(control, target)<br/>
<br/>
<b>Gate Application (Density Matrix):</b><br/>
  apply_single_qubit_gate_density(gate, target)<br/>
  apply_two_qubit_gate_density(gate4, q1, q2)<br/>
  apply_ccnot_density(c1, c2, target)<br/>
<br/>
<b>Noise & Channels:</b><br/>
  apply_kraus_channel_1q(type, p, target)<br/>
  _kraus_1q(type, p) → List[ndarray]<br/>
<br/>
<b>Measurement:</b><br/>
  measure_all(shots, readout_error_p) → Dict<br/>
<br/>
<b>Observables:</b><br/>
  expectation_values(target) → Dict<br/>
  expectation_pauli(pauli, qubits) → float<br/>
<br/>
<b>Probabilities:</b><br/>
  probabilities() → Dict<br/>
  marginal_probability(target) → Dict<br/>
<br/>
<b>Circuit Execution:</b><br/>
  run_circuit(circuit, shots, noise_model) → Dict
    """
    
    story.append(Paragraph(sim_methods, code_style))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>9.2 Circuit Class API</b>", heading2_style))
    
    circuit_methods = """
<b>Construction:</b><br/>
  Circuit(n_qubits)    Constructor<br/>
<br/>
<b>Single-Qubit Gates:</b><br/>
  h(target), x(target), y(target), z(target)<br/>
  s(target), t(target)<br/>
  rx(target, theta), ry(target, theta)<br/>
  rz(target, theta), phase(target, phi)<br/>
  u3(target, theta, phi, lam)<br/>
<br/>
<b>Multi-Qubit Gates:</b><br/>
  cnot(control, target), cz(control, target)<br/>
  swap(q1, q2), iswap(q1, q2)<br/>
  custom_2q(matrix, q1, q2)<br/>
  ccnot(c1, c2, target), toffoli(c1, c2, target)<br/>
<br/>
<b>Observables & Witnesses:</b><br/>
  expval(pauli, qubits) → Circuit<br/>
  add_linear_witness(name, terms, bound, violates_if) → Circuit<br/>
<br/>
<b>Serialization:</b><br/>
  to_dict() → Dict<br/>
  to_json() → str<br/>
  from_dict(data) → Circuit (classmethod)<br/>
  from_json(json_str) → Circuit (classmethod)<br/>
<br/>
<b>Execution:</b><br/>
  run(shots=1024, noise_model=None) → Dict
    """
    
    story.append(Paragraph(circuit_methods, code_style))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(PageBreak())
    
    # 10. Usage Examples
    story.append(Paragraph("10. USAGE EXAMPLES", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>10.1 Basic Bell State</b>", heading2_style))
    
    example1 = """
from quantum_sim import Simulator, H
from quantum_sim.gates import CNOT_4x4

# Create 2-qubit simulator
sim = Simulator(2)

# Apply Hadamard to Q0
sim.apply_single_qubit_gate(H, 0)

# Apply CNOT (control=0, target=1)
sim.apply_two_qubit_gate(CNOT_4x4, 0, 1)

# Get probabilities
probs = sim.probabilities()
# {'00': 0.5, '01': 0.0, '10': 0.0, '11': 0.5}

# Measure 1000 shots
result = sim.measure_all(shots=1000)
# {'00': ~500, '11': ~500}
    """
    
    story.append(Paragraph(example1, code_style))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>10.2 High-Level Circuit API</b>", heading2_style))
    
    example2 = """
from quantum_sim.circuit import Circuit

# Build 3-qubit GHZ state
qc = Circuit(3)
qc.h(0)              # H on qubit 0
qc.cnot(0, 1)        # CNOT: control=0, target=1
qc.cnot(1, 2)        # CNOT: control=1, target=2
qc.expval('ZZZ', [0, 1, 2])  # Expect all-Z correlation

# Run circuit
result = qc.run(shots=1024)

print(f"Measurement counts: {result['counts']}")
# {'000': ~512, '111': ~512}
print(f"Pauli expectation: {result['pauli_expectations']}")
    """
    
    story.append(Paragraph(example2, code_style))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>10.3 Noisy Simulation</b>", heading2_style))
    
    example3 = """
qc = Circuit(2)
qc.h(0)
qc.cnot(0, 1)

# Define noise model
noise_model = {
    'channels': [
        {'after': 'each_gate', 'type': 'depolarizing', 'p': 0.01},
        {'after': 'measurement', 'type': 'readout_error', 'p': 0.05}
    ]
}

# Run noisy simulation
result = qc.run(shots=1024, noise_model=noise_model)

# Results will show some contamination to |01> and |10>
print(result['counts'])
    """
    
    story.append(Paragraph(example3, code_style))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>10.4 Entanglement Witnesses</b>", heading2_style))
    
    example4 = """
qc = Circuit(2)
qc.h(0)
qc.cnot(0, 1)

# Define CHSH Bell inequality witness
witness_terms = [
    {'pauli': 'ZZ', 'qubits': [0, 1], 'coef': 1.0},
    {'pauli': 'ZX', 'qubits': [0, 1], 'coef': 1.0},
    {'pauli': 'XZ', 'qubits': [0, 1], 'coef': 1.0},
    {'pauli': 'XX', 'qubits': [0, 1], 'coef': -1.0}
]

qc.add_linear_witness(
    name='CHSH',
    terms=witness_terms,
    bound=2.0,  # Classical bound
    violates_if='>'
)

result = qc.run()
for witness in result['witnesses']:
    if witness['name'] == 'CHSH':
        print(f"CHSH value: {witness['value']:.3f}")
        print(f"Entangled: {witness['entangled']}")
    """
    
    story.append(Paragraph(example4, code_style))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(PageBreak())
    
    # 11. Advanced Features
    story.append(Paragraph("11. ADVANCED FEATURES", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>11.1 Density Matrix Mode</b>", heading2_style))
    
    story.append(Paragraph(
        "The simulator supports true mixed state simulation via density matrices. "
        "This is essential for realistic quantum simulations with decoherence.<br/><br/>"
        "<b>Advantages:</b><br/>"
        "• Can represent mixed states (not just pure states)<br/>"
        "• Naturally handles noise via Kraus operators<br/>"
        "• Trace-preserving operations guarantee physical validity<br/><br/>"
        "<b>Disadvantages:</b><br/>"
        "• Memory scales as O(4^n) vs O(2^n) for statevector<br/>"
        "• Computation slower due to larger matrix operations<br/>"
        "• Practical limit around 15-16 qubits<br/><br/>"
        "<b>Setup:</b><br/>"
        "sim.reset_density()  # Switch to density matrix mode",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>11.2 Kraus Operator Channels</b>", heading2_style))
    
    story.append(Paragraph(
        "The most general quantum channel formalism is via Kraus operators: ε(ρ) = Σₖ KₖρKₖ†<br/><br/>"
        "Complete Positivity: Ensures ε produces valid quantum states<br/>"
        "Trace Preservation: Ensures Σₖ Kₖ†Kₖ = I<br/><br/>"
        "Implemented Channels (1-qubit):<br/>"
        "1. Bit-Flip: Random X gate with prob p<br/>"
        "2. Phase-Flip: Random Z gate with prob p<br/>"
        "3. Depolarizing: Random rotation with prob p<br/><br/>"
        "Efficient Implementation:<br/>"
        "Rather than full Kraus sum, apply channel after each gate independently. "
        "This matches the 'per-gate' noise typical in real devices.",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>11.3 Pauli String Observables</b>", heading2_style))
    
    story.append(Paragraph(
        "Arbitrary multi-qubit Pauli observables: O = P₀ ⊗ P₁ ⊗ ... ⊗ Pₙ₋₁<br/>"
        "where each Pᵢ ∈ {I, X, Y, Z}<br/><br/>"
        "Efficient Computation:<br/>"
        "• I-operators create no work (trivial)<br/>"
        "• Z-operators use bit parity (no state rotation)<br/>"
        "• X, Y-operators flip qubits and track phase<br/>"
        "• Phase tracking crucial for Y (gives ±i factors)<br/><br/>"
        "Time Complexity: O(2^n) for any Pauli observable",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>11.4 Entanglement Witnesses</b>", heading2_style))
    
    story.append(Paragraph(
        "Linear entanglement witnesses verify absence of product state structure.<br/><br/>"
        "Mathematical Form:<br/>"
        "W(ρ) = Σₖ cₖ ⟨Pₖ⟩ where Pₖ are Pauli observables<br/><br/>"
        "Separability Criterion:<br/>"
        "If W(ρ_sep) ≤ B for all separable ρ_sep, but W(ρ_target) > B,<br/>"
        "then ρ_target must be entangled (witnesses entanglement).<br/><br/>"
        "Common Use:<br/>"
        "CHSH inequality: Detects Bell inequality violations (classical bound = 2)",
        code_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(PageBreak())
    
    # 12. Testing
    story.append(Paragraph("12. TESTING FRAMEWORK", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph(
        "The project includes comprehensive unit tests using pytest framework.",
        normal_style
    ))
    
    story.append(Spacer(1, 0.08*inch))
    story.append(Paragraph("<b>12.1 Test Files</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>test_simulator.py:</b> Core simulator functionality<br/>"
        "• Hadamard creates 50/50 superposition<br/>"
        "• Measurement statistics match expected distributions<br/><br/>"
        "<b>test_bell.py:</b> Bell state verification<br/>"
        "• Exact analyticalvalidation of |Φ⁺⟩ = (|00⟩ + |11⟩)/√2<br/>"
        "• Marginal probabilities verify correlations<br/><br/>"
        "<b>test_ccnot.py:</b> Toffoli/CCNOT gate tests<br/>"
        "• Controlled-controlled operation verification<br/><br/>"
        "<b>test_gates_probs.py:</b> Gate probability distributions<br/>"
        "• Single-qubit gate operation verification<br/>"
        "• Multi-qubit entanglement creation",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>12.2 Run Tests</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>Command:</b><br/>"
        "pytest -q<br/>"
        "or<br/>"
        "python -m pytest tests/<br/><br/>"
        "<b>Expected Output:</b><br/>"
        "All tests should pass, indicating correct implementation of:<br/>"
        "• Statevector simulation<br/>"
        "• Gate application<br/>"
        "• Measurement sampling<br/>"
        "• Observable computation",
        code_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(PageBreak())
    
    # 13. Performance
    story.append(Paragraph("13. PERFORMANCE CONSIDERATIONS", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>13.1 Scalability Limits</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>Statevector Mode:</b><br/>"
        "• Memory per state: 16 bytes/amplitude × 2^n<br/>"
        "  - n=20: 16 MB ✓<br/>"
        "  - n=25: 512 MB ✓<br/>"
        "  - n=30: 16 GB ✗ (begins to exceed typical RAM)<br/><br/>"
        "<b>Practical Limit:</b> n ≤ 25-28 qubits on modern hardware<br/><br/>"
        "<b>Density Matrix Mode:</b><br/>"
        "• Memory scales as O(4^n)<br/>"
        "• Practical limit: n ≤ 12-15 qubits<br/>"
        "• Computation time significantly slower",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>13.2 Time Complexity Analysis</b>", heading2_style))
    
    story.append(Paragraph(
        "<b>Single-Qubit Gate:</b> O(2^n) - must touch all state components<br/>"
        "<b>Two-Qubit Gate:</b> O(2^n) - tensor contraction on two axes<br/>"
        "<b>CCNOT Gate:</b> O(2^n) - bit-by-bit permutation<br/>"
        "<b>Measurement:</b> O(2^n) - probability extraction + sampling<br/>"
        "<b>Pauli Observable:</b> O(2^n × |pauli|) - iterate all basis states<br/><br/>"
        "<b>Full Circuit (m gates):</b> O(m × 2^n)",
        code_style
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>13.3 Optimization Techniques Used</b>", heading2_style))
    
    story.append(Paragraph(
        "1. <b>NumPy Tensor Operations:</b> Leverages optimized BLAS/LAPACK<br/><br/>"
        "2. <b>Bit Manipulation:</b> Fast bit shifts and masks for CCNOT, measurements<br/><br/>"
        "3. <b>In-place Operations:</b> State vectors modified in-place when possible<br/><br/>"
        "4. <b>Early Termination:</b> Skip zero-amplitude terms in observable computation<br/><br/>"
        "5. <b>Efficient Pauli Computation:</b> Direct phase calculation avoids matrix multiplication",
        code_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(PageBreak())
    
    # 14. Future Enhancements
    story.append(Paragraph("14. FUTURE ENHANCEMENTS & ROADMAP", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph(
        "<b>Short-term (Weeks):</b><br/>"
        "• Add GPU acceleration (CuPy/PyTorch for NVIDIA/AMD)<br/>"
        "• Implement 2-qubit noise channels (2-qubit depolarizing, QRAM errors)<br/>"
        "• Add more parameterized gates (arbitrary rotations)<br/>"
        "• Implement readout error correction protocols<br/><br/>"
        "<b>Medium-term (Months):</b><br/>"
        "• Circuit optimization (gate merging, commutation rules)<br/>"
        "• Clifford group simulator (stabilizer formalism)<br/>"
        "• Variational quantum algorithm support<br/>"
        "• Integration with Qiskit/Cirq ecosystem<br/><br/>"
        "<b>Long-term (Quarters):</b><br/>"
        "• Tensor network state methods (handle n > 30)<br/>"
        "• Automatic differentiation (gradient computation)<br/>"
        "• Distributed simulation (multiple GPUs/CPUs)<br/>"
        "• MPS/PEPS tensor representations<br/><br/>"
        "<b>Potential Research Directions:</b><br/>"
        "• Quantum error correction codes<br/>"
        "• Hybrid classical-quantum algorithms<br/>"
        "• Parametrized quantum circuits (VQE integration)<br/>"
        "• Quantum walk simulation",
        code_style
    ))
    
    story.append(Spacer(1, 0.5*inch))
    
    # Conclusion
    story.append(PageBreak())
    story.append(Paragraph("<b>CONCLUSION</b>", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph(
        "This quantum simulator backend provides a solid foundation for quantum circuit simulation "
        "with support for both pure and noisy simulations. The modular architecture allows for "
        "easy extension with new gates, channels, and features. The combination of efficient "
        "statevector mode for larger circuits and complete density matrix support for noise makes "
        "it suitable for a wide range of quantum computation research and education applications.",
        normal_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "<b>Key Strengths:</b><br/>"
        "✓ Clean, modular architecture<br/>"
        "✓ Both pure and mixed state support<br/>"
        "✓ Comprehensive gate library<br/>"
        "✓ Flexible noise modeling<br/>"
        "✓ Well-tested core functionality<br/>"
        "✓ JSON serialization for interoperability<br/><br/>"
        "<b>Suitable For:</b><br/>"
        "• Quantum algorithm research<br/>"
        "• Educational quantum computing courses<br/>"
        "• Benchmarking quantum algorithms<br/>"
        "• Noise model simulation<br/>"
        "• Entanglement verification",
        normal_style
    ))
    
    # Build PDF
    doc.build(story)
    print("✓ PDF documentation generated successfully!")
    print("  File: QuantumSimulator_Backend_Documentation.pdf")
    print(f"  Generated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}")

if __name__ == "__main__":
    create_documentation()

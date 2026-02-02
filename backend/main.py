# backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from quantum_sim.circuit import Circuit

app = FastAPI(
    title="Quantum Simulator API",
    description="Backend for executing quantum circuits built in React UI.",
    version="1.0.0"
)

# -------------------------------------------------------------
# Pydantic models (input validation)
# -------------------------------------------------------------

class GateOp(BaseModel):
    name: str
    targets: Optional[List[int]] = None
    target: Optional[int] = None
    control: Optional[int] = None
    control1: Optional[int] = None
    control2: Optional[int] = None
    theta: Optional[float] = None
    phi: Optional[float] = None
    lam: Optional[float] = None
    q1: Optional[int] = None
    q2: Optional[int] = None
    matrix: Optional[List[List[float]]] = None  # JSON-safe 4x4 list


class CircuitPayload(BaseModel):
    n_qubits: int
    gates: List[GateOp]
    shots: Optional[int] = 1024


# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------

@app.post("/simulate")
def simulate(payload: CircuitPayload):
    """
    Receives a circuit JSON from frontend.
    Builds a Circuit object.
    Runs the simulation using the Simulator engine.
    Returns probability results.
    """
    qc = Circuit(payload.n_qubits)

    # Load gates into Circuit object
    for op in payload.gates:
        name = op.name.upper()

        # SINGLE-QUBIT FIXED GATES
        if name in ("H", "X", "Y", "Z", "S", "T"):
            for t in op.targets:
                getattr(qc, name.lower())(t)

        # PARAMETERIZED GATES
        elif name == "RX":
            qc.rx(op.target, op.theta)
        elif name == "RY":
            qc.ry(op.target, op.theta)
        elif name == "RZ":
            qc.rz(op.target, op.theta)
        elif name in ("PHASE", "P"):
            qc.phase(op.target, op.phi)
        elif name == "U3":
            qc.u3(op.target, op.theta, op.phi, op.lam)

        # TWO-QUBIT GATES
        elif name == "CNOT":
            qc.cnot(op.control, op.target)
        elif name == "CZ":
            qc.cz(op.control, op.target)
        elif name == "SWAP":
            qc.swap(op.q1, op.q2)
        elif name == "ISWAP":
            qc.iswap(op.q1, op.q2)

        # THREE-QUBIT
        elif name in ("CCNOT", "TOFFOLI"):
            qc.ccnot(op.control1, op.control2, op.target)

        # CUSTOM
        elif name == "CUSTOM_2Q":
            qc.custom_2q(op.matrix, op.q1, op.q2)

        else:
            raise ValueError(f"Unsupported gate: {name}")

    # ----------------------------------------
    # Run simulation through Simulator engine
    # ----------------------------------------
    result = qc.run(shots=payload.shots)

    return {
        "n_qubits": payload.n_qubits,
        "shots": payload.shots,
        "counts": result["counts"]
    }


# -------------------------------------------------------------
# Optional: health check endpoint
# -------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Quantum Simulator Backend Running!"}

# backend/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, List, Optional

from quantum_sim.circuit import Circuit

app = FastAPI(
    title="Quantum Simulator API",
    description="Backend for executing quantum circuits built in React UI.",
    version="1.0.0"
)

# -----------------------------
# CORS (so React can call API)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev; later you can restrict to your React domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------
# Pydantic models
# -------------------------------------------------------------
class GateOp(BaseModel):
    name: str

    # fixed single-qubit
    targets: Optional[List[int]] = None

    # param single-qubit
    target: Optional[int] = None
    theta: Optional[float] = None
    phi: Optional[float] = None
    lam: Optional[float] = None

    # 2-qubit control/target style
    control: Optional[int] = None

    # 3-qubit Toffoli
    control1: Optional[int] = None
    control2: Optional[int] = None

    # 2-qubit q1/q2 style
    q1: Optional[int] = None
    q2: Optional[int] = None

    # custom matrix (JSON nested lists)
    matrix: Optional[Any] = None

class Observable(BaseModel):
    pauli: str
    qubits: List[int]

class WitnessTerm(BaseModel):
    pauli: str
    qubits: List[int]
    coef: float = 1.0

class LinearWitness(BaseModel):
    name: str
    terms: List[WitnessTerm]
    bound: float
    violates_if: str = ">"


class CircuitPayload(BaseModel):
    n_qubits: int
    gates: List[GateOp]
    observables: Optional[List[Observable]] = None
    witnesses: Optional[List[LinearWitness]] = None
    noise_model: Optional[Any] = None
    shots: Optional[int] = 1024


# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Quantum Simulator Backend Running!"}


@app.post("/simulate")
def simulate(payload: CircuitPayload):
    try:
        qc = Circuit(payload.n_qubits)

        for op in payload.gates:
            name = op.name.upper()

            # Fixed single-qubit
            if name in ("H", "X", "Y", "Z", "S", "T"):
                if not op.targets:
                    raise ValueError(f"{name} requires 'targets': [..]")
                for t in op.targets:
                    getattr(qc, name.lower())(t)

            # Param single-qubit
            elif name == "RX":
                if op.target is None or op.theta is None:
                    raise ValueError("RX requires 'target' and 'theta'")
                qc.rx(op.target, op.theta)

            elif name == "RY":
                if op.target is None or op.theta is None:
                    raise ValueError("RY requires 'target' and 'theta'")
                qc.ry(op.target, op.theta)

            elif name == "RZ":
                if op.target is None or op.theta is None:
                    raise ValueError("RZ requires 'target' and 'theta'")
                qc.rz(op.target, op.theta)

            elif name in ("PHASE", "P"):
                if op.target is None or op.phi is None:
                    raise ValueError("PHASE requires 'target' and 'phi'")
                qc.phase(op.target, op.phi)

            elif name == "U3":
                if op.target is None or op.theta is None or op.phi is None or op.lam is None:
                    raise ValueError("U3 requires 'target', 'theta', 'phi', 'lam'")
                qc.u3(op.target, op.theta, op.phi, op.lam)

            # Two-qubit
            elif name == "CNOT":
                if op.control is None or op.target is None:
                    raise ValueError("CNOT requires 'control' and 'target'")
                qc.cnot(op.control, op.target)

            elif name == "CZ":
                if op.control is None or op.target is None:
                    raise ValueError("CZ requires 'control' and 'target'")
                qc.cz(op.control, op.target)

            elif name == "SWAP":
                if op.q1 is None or op.q2 is None:
                    raise ValueError("SWAP requires 'q1' and 'q2'")
                qc.swap(op.q1, op.q2)

            elif name == "ISWAP":
                if op.q1 is None or op.q2 is None:
                    raise ValueError("ISWAP requires 'q1' and 'q2'")
                qc.iswap(op.q1, op.q2)

            # Three-qubit
            elif name in ("CCNOT", "TOFFOLI"):
                if op.control1 is None or op.control2 is None or op.target is None:
                    raise ValueError("CCNOT/TOFFOLI requires 'control1', 'control2', 'target'")
                qc.ccnot(op.control1, op.control2, op.target)

            # Custom 2-qubit
            elif name == "CUSTOM_2Q":
                if op.matrix is None or op.q1 is None or op.q2 is None:
                    raise ValueError("CUSTOM_2Q requires 'matrix', 'q1', 'q2'")
                qc.custom_2q(op.matrix, op.q1, op.q2)

            else:
                raise ValueError(f"Unsupported gate: {name}")
            

        if payload.observables:
            for obs in payload.observables:
                pauli = obs.pauli.upper()
                # Validate Pauli string early (API-level error message)
                if any(c not in "IXYZ" for c in pauli):
                    raise ValueError("Pauli string may contain only I, X, Y, Z")
                qc.expval(pauli, obs.qubits)  


        if payload.witnesses:
            for w in payload.witnesses:
                terms = [
                    {"pauli": t.pauli, "qubits": t.qubits, "coef": t.coef}
                    for t in w.terms
                ]
                qc.add_linear_witness(
                    name=w.name,
                    terms=terms,
                    bound=w.bound,
                    violates_if=w.violates_if
                )      


        result = qc.run(shots=payload.shots or 1024, noise_model=payload.noise_model)

        return {
            "n_qubits": payload.n_qubits,
            "shots": result["shots"],
            "counts": result["counts"],
            "probabilities": result["probabilities"],
            "marginals": result["marginals"],
            "expectations": result["expectations"],
            "pauli_expectations": result["pauli_expectations"],
            "witnesses": result["witnesses"],
            "state_type": result["state_type"],
            "state": result["state"],
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

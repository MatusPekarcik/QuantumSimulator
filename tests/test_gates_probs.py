# test_gates_probs.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from colorama import Fore, Style, init

# initialize colorama (important on Windows)
init(autoreset=True)

from quantum_sim.simulator import Simulator
from quantum_sim.gates import (
    I, X, Y, Z, H, S, T, Sdg, Tdg,
    Rx, Ry, Rz, Phase, U3,
    CNOT_4x4, CZ_4x4, SWAP_4x4, ISWAP_4x4,
)

# -----------------------------------------------------------
# Helpers
# -----------------------------------------------------------

def sampled_marginal_for_qubit(sim: Simulator, target: int, shots: int):
    counts = sim.measure_all(shots)
    total = sum(counts.values())

    c0 = 0
    c1 = 0
    for bitstring, c in counts.items():
        bit = bitstring[target]
        if bit == "0":
            c0 += c
        else:
            c1 += c

    return (c0 / total), (c1 / total), {"0": c0, "1": c1}


def header(title: str):
    print(
        "\n"
        + Fore.CYAN
        + Style.BRIGHT
        + "=" * 65
        + f"\n{title}\n"
        + "=" * 65
    )


# -----------------------------------------------------------
# Output formatting
# -----------------------------------------------------------

def print_1q(name: str, sim: Simulator, shots: int):
    header(f"1-QUBIT GATE: {Fore.YELLOW + Style.BRIGHT}{name}")

    # Exact
    full = sim.probabilities()
    marg = sim.marginal_probability(0)

    print(Fore.GREEN + "Exact full distribution:", full)
    print(Fore.GREEN + "Exact marginal (qubit 0):", marg)

    # Sampled
    p0, p1, raw = sampled_marginal_for_qubit(sim, target=0, shots=shots)

    print(
        Fore.MAGENTA
        + f"Sampled (shots={shots}): "
        + Fore.MAGENTA
        + f"p(0)={p0:.4f}, p(1)={p1:.4f}"
    )

    print(
        Fore.BLUE
        + f"Sampled counts (shots={shots}): {raw}"
    )


def print_2q(name: str, sim: Simulator, shots: int):
    header(f"2-QUBIT GATE: {Fore.YELLOW + Style.BRIGHT}{name}")

    full = sim.probabilities()
    marg0 = sim.marginal_probability(0)
    marg1 = sim.marginal_probability(1)

    print(Fore.GREEN + "Exact full distribution:", full)
    print(Fore.GREEN + "Exact marginal (qubit 0):", marg0)
    print(Fore.GREEN + "Exact marginal (qubit 1):", marg1)

    p0_q0, p1_q0, raw0 = sampled_marginal_for_qubit(sim, 0, shots)
    p0_q1, p1_q1, raw1 = sampled_marginal_for_qubit(sim, 1, shots)

    print(
        Fore.MAGENTA
        + f"Sampled (shots={shots}, qubit 0): "
        + f"p(0)={p0_q0:.4f}, p(1)={p1_q0:.4f}"
    )
    print(Fore.BLUE + f"Sampled counts (qubit 0): {raw0}")

    print(
        Fore.MAGENTA
        + f"Sampled (shots={shots}, qubit 1): "
        + f"p(0)={p0_q1:.4f}, p(1)={p1_q1:.4f}"
    )
    print(Fore.BLUE + f"Sampled counts (qubit 1): {raw1}")


# -----------------------------------------------------------
# Tests
# -----------------------------------------------------------

def test_1q(shots: int):
    gates = {
        "I": I,
        "X": X,
        "Y": Y,
        "Z": Z,
        "H": H,
        "S": S,
        "T": T,
        "Sdg": Sdg,
        "Tdg": Tdg,
        "Rx(pi/2)": Rx(np.pi / 2),
        "Ry(pi/2)": Ry(np.pi / 2),
        "Rz(pi/2)": Rz(np.pi / 2),
        "Phase(pi/3)": Phase(np.pi / 3),
        "U3(pi/2, pi/2, pi/2)": U3(np.pi / 2, np.pi / 2, np.pi / 2),
    }

    for name, gate in gates.items():
        sim = Simulator(1)
        sim.apply_single_qubit_gate(gate, 0)
        print_1q(name, sim, shots)


def test_2q(shots: int):
    gates = {
        "CNOT(0→1)": CNOT_4x4,
        "CZ(0,1)": CZ_4x4,
        "SWAP(0,1)": SWAP_4x4,
        "ISWAP(0,1)": ISWAP_4x4,
    }

    for name, g4 in gates.items():
        sim = Simulator(2)
        sim.state = np.zeros(4, dtype=complex)
        sim.state[2] = 1  # |10>

        sim.apply_two_qubit_gate(g4, 0, 1)
        print_2q(name, sim, shots)


# -----------------------------------------------------------
# Main
# -----------------------------------------------------------

if __name__ == "__main__":
    DEFAULT_SHOTS = 5000

    if len(sys.argv) > 1:
        try:
            shots = int(sys.argv[1])
        except ValueError:
            print("Usage: python test_gates_probs.py <shots>")
            sys.exit(1)
    else:
        shots = DEFAULT_SHOTS

    print(Fore.CYAN + f"\nRunning all gate tests with {Style.BRIGHT + Fore.MAGENTA}{shots}{Style.RESET_ALL + Fore.CYAN} shots.\n")

    test_1q(shots)
    test_2q(shots)

    print(Fore.CYAN + Style.BRIGHT + f"\nAll tests completed using {shots} shots.\n")

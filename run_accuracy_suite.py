# run_accuracy_suite.py
import csv
from pathlib import Path

from bench_accuracy_vs_aer import (
    PRESET_BUILDERS,
    compare_once,
    make_random_circuit,
)


def main():
    out_dir = Path("benchmark_results")
    out_dir.mkdir(exist_ok=True)

    out_csv = out_dir / "accuracy_vs_aer.csv"

    rows = []

    # -------------------------------------------------
    # Fixed educational / algorithmic presets
    # -------------------------------------------------
    preset_names = [
        "bell",
        "ghz",
        "deutsch_constant_0",
        "deutsch_constant_1",
        "deutsch_balanced_identity",
        "deutsch_balanced_not",
        "grover_2q_11",
    ]

    for preset_name in preset_names:
        built = PRESET_BUILDERS[preset_name]()
        row = compare_once(
            n=built["n"],
            ops=built["ops"],
            label=built["name"],
            noise_p=0.0,
        )
        rows.append(row)

    # -------------------------------------------------
    # Random noiseless circuits
    # -------------------------------------------------
    random_cases = [
        (2, 4, 0),
        (2, 8, 1),
        (3, 4, 2),
        (3, 8, 3),
        (4, 4, 4),
        (4, 8, 5),
        (5, 4, 6),
    ]

    for n, depth, seed in random_cases:
        ops = make_random_circuit(n=n, depth=depth, seed=seed)
        row = compare_once(
            n=n,
            ops=ops,
            label=f"random_n{n}_d{depth}_s{seed}",
            noise_p=0.0,
        )
        rows.append(row)

    # -------------------------------------------------
    # Optional noisy comparisons
    # -------------------------------------------------
    noisy_cases = [
        (2, 4, 11, 0.01),
        (2, 8, 12, 0.02),
        (3, 4, 13, 0.01),
        (3, 8, 14, 0.02),
    ]

    for n, depth, seed, noise_p in noisy_cases:
        ops = make_random_circuit(n=n, depth=depth, seed=seed)
        row = compare_once(
            n=n,
            ops=ops,
            label=f"random_noisy_n{n}_d{depth}_s{seed}_p{noise_p}",
            noise_p=noise_p,
        )
        rows.append(row)

    # -------------------------------------------------
    # Write CSV
    # -------------------------------------------------
    fieldnames = sorted({key for row in rows for key in row.keys()})

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} rows to: {out_csv}")


if __name__ == "__main__":
    main()
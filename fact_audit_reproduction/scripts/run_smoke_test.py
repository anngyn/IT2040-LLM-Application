#!/usr/bin/env python3
"""Run the 1-3 claim smoke test required by the assignment tracker."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    claim_set = ROOT / "data/claim_sets/claim_set_30.jsonl"
    if not claim_set.exists():
        subprocess.run(
            [sys.executable, "scripts/make_claim_set.py", "--size", "30"],
            cwd=ROOT,
            check=True,
        )
    subprocess.run(
        [
            sys.executable,
            "scripts/run_baseline.py",
            "--input-file",
            "data/claim_sets/claim_set_30.jsonl",
            "--output-jsonl",
            "outputs/smoke_test.jsonl",
            "--scores-csv",
            "outputs/smoke_test_scores.csv",
            "--limit",
            "3",
            "--provider",
            "mock",
        ],
        cwd=ROOT,
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

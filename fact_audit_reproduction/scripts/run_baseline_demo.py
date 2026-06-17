#!/usr/bin/env python3
"""Stable demo entry point with cached-output fallback."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run cached/live baseline demo.")
    parser.add_argument("--use-cache", action="store_true")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--provider", default="mock")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    claim_set = ROOT / "data/claim_sets/claim_set_30.jsonl"
    if not claim_set.exists():
        subprocess.run([sys.executable, "scripts/make_claim_set.py", "--size", "30"], cwd=ROOT, check=True)

    command = [
        sys.executable,
        "scripts/run_baseline.py",
        "--input-file",
        "data/claim_sets/claim_set_30.jsonl",
        "--output-jsonl",
        "outputs/cached_demo/baseline_demo_results.jsonl",
        "--scores-csv",
        "outputs/cached_demo/demo_scores.csv",
        "--limit",
        str(args.limit),
        "--provider",
        args.provider,
    ]
    if args.use_cache:
        command.append("--use-cache")
    subprocess.run(command, cwd=ROOT, check=True)
    print("Demo output: outputs/cached_demo/baseline_demo_results.jsonl")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build a small balanced claim set from the local normalized dataset."""

from __future__ import annotations

import argparse
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fact_audit_baseline.io_utils import read_jsonl, write_jsonl


DEFAULT_INPUT = Path("data/source/fact_checking_normalized.jsonl")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a deterministic mini claim set.")
    parser.add_argument("--input-file", default=str(DEFAULT_INPUT))
    parser.add_argument("--output-file", default="data/claim_sets/claim_set_30.jsonl")
    parser.add_argument("--size", type=int, default=30)
    parser.add_argument("--seed", type=int, default=2040)
    parser.add_argument("--binary-only", action="store_true", default=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = (ROOT / args.input_file).resolve()
    output_path = ROOT / args.output_file
    rows = read_jsonl(input_path)
    if args.binary_only:
        rows = [row for row in rows if row.get("ground_truth") in {"True", "False"}]

    buckets = defaultdict(list)
    for row in rows:
        key = (row.get("source_dataset", "unknown"), row.get("ground_truth", "Unknown"))
        buckets[key].append(row)

    rng = random.Random(args.seed)
    for bucket_rows in buckets.values():
        rng.shuffle(bucket_rows)

    selected = []
    while len(selected) < args.size and any(buckets.values()):
        for key in sorted(list(buckets)):
            if buckets[key] and len(selected) < args.size:
                selected.append(buckets[key].pop())

    write_jsonl(output_path, selected)
    print(f"Wrote {len(selected)} claims to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

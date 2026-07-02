#!/usr/bin/env python3
"""Compare baseline vs RAG results and generate a comparison report."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare baseline vs RAG results.")
    parser.add_argument(
        "--baseline",
        default="outputs/baseline_results.jsonl",
        help="Path to baseline results JSONL",
    )
    parser.add_argument(
        "--rag",
        default="outputs/rag_results.jsonl",
        help="Path to RAG results JSONL",
    )
    parser.add_argument(
        "--output-csv",
        default="outputs/comparison_report.csv",
        help="Output CSV path",
    )
    return parser.parse_args()


def resolve_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return ROOT / path


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def compute_metrics(results: List[Dict[str, Any]], score_key: str, verdict_key: str) -> Dict[str, float]:
    """Compute IMR, JFR, and Grade from a list of results."""
    if not results:
        return {"imr": 0.0, "jfr": 0.0, "grade": 0.0, "accuracy": 0.0, "count": 0}

    scores = [r.get(score_key, 5) for r in results]
    n = len(scores)

    low_score_count = sum(1 for s in scores if s <= 3)
    imr = low_score_count / n * 100

    correct_with_flaw = sum(
        1 for r in results
        if r.get("is_verdict_correct", False) and r.get("is_justification_flawed", False)
    )
    correct_count = sum(1 for r in results if r.get("is_verdict_correct", False))
    jfr = (correct_with_flaw / correct_count * 100) if correct_count > 0 else 0.0

    grade = sum(scores) / n
    accuracy = correct_count / n * 100

    return {
        "imr": round(imr, 2),
        "jfr": round(jfr, 2),
        "grade": round(grade, 2),
        "accuracy": round(accuracy, 2),
        "count": n,
    }


def main() -> int:
    args = parse_args()
    baseline_path = resolve_path(args.baseline)
    rag_path = resolve_path(args.rag)
    output_csv_path = resolve_path(args.output_csv)

    if not baseline_path.exists():
        print(f"[ERROR] Baseline file not found: {baseline_path}")
        return 1
    if not rag_path.exists():
        print(f"[ERROR] RAG file not found: {rag_path}")
        return 1

    baseline_rows = load_jsonl(baseline_path)
    rag_rows = load_jsonl(rag_path)

    baseline_by_id = {r.get("claim_id", r.get("id", "")): r for r in baseline_rows}
    rag_by_id = {r.get("claim_id", ""): r for r in rag_rows}

    common_ids = sorted(set(baseline_by_id.keys()) & set(rag_by_id.keys()))
    if not common_ids:
        print("[ERROR] No matching claim_ids between baseline and RAG results.")
        return 1

    baseline_matched = [baseline_by_id[cid] for cid in common_ids]
    rag_matched = [rag_by_id[cid] for cid in common_ids]

    baseline_metrics = compute_metrics(baseline_matched, "baseline_score", "baseline_verdict")
    rag_metrics = compute_metrics(rag_matched, "rag_score", "rag_verdict")

    test_modes = sorted(set(r.get("test_mode", "unknown") for r in rag_matched))
    mode_metrics = {}
    for mode in test_modes:
        b_mode = [r for r in baseline_matched if r.get("test_mode") == mode]
        r_mode = [r for r in rag_matched if r.get("test_mode") == mode]
        mode_metrics[mode] = {
            "baseline": compute_metrics(b_mode, "baseline_score", "baseline_verdict"),
            "rag": compute_metrics(r_mode, "rag_score", "rag_verdict"),
        }

    print("\n" + "=" * 70)
    print("FACT-AUDIT: Baseline vs RAG Comparison")
    print("=" * 70)
    print(f"\nMatched claims: {len(common_ids)}")
    print(f"\n{'Metric':<12} {'Baseline':>10} {'RAG':>10} {'Delta':>10}")
    print("-" * 44)
    for metric in ["accuracy", "grade", "imr", "jfr"]:
        b_val = baseline_metrics[metric]
        r_val = rag_metrics[metric]
        delta = r_val - b_val
        sign = "+" if delta > 0 else ""
        print(f"{metric.upper():<12} {b_val:>10.2f} {r_val:>10.2f} {sign}{delta:>9.2f}")

    print(f"\n{'Mode':<20} {'Metric':<8} {'Baseline':>10} {'RAG':>10} {'Delta':>10}")
    print("-" * 60)
    for mode in test_modes:
        for metric in ["accuracy", "grade"]:
            b_val = mode_metrics[mode]["baseline"][metric]
            r_val = mode_metrics[mode]["rag"][metric]
            delta = r_val - b_val
            sign = "+" if delta > 0 else ""
            print(f"{mode:<20} {metric.upper():<8} {b_val:>10.2f} {r_val:>10.2f} {sign}{delta:>9.2f}")

    output_csv_path.parent.mkdir(parents=True, exist_ok=True)
    csv_rows = []
    for cid in common_ids:
        b = baseline_by_id[cid]
        r = rag_by_id[cid]
        csv_rows.append({
            "claim_id": cid,
            "claim": r.get("claim", b.get("claim", "")),
            "test_mode": r.get("test_mode", ""),
            "gold_verdict": r.get("gold_verdict", b.get("gold_verdict", "")),
            "baseline_verdict": b.get("baseline_verdict", b.get("verdict", "")),
            "baseline_score": b.get("baseline_score", b.get("score", "")),
            "rag_verdict": r.get("rag_verdict", ""),
            "rag_score": r.get("rag_score", ""),
            "baseline_correct": b.get("is_verdict_correct", ""),
            "rag_correct": r.get("is_verdict_correct", ""),
            "evidence_count": len(r.get("retrieved_evidence", [])),
        })

    fields = list(csv_rows[0].keys()) if csv_rows else []
    with output_csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"\n[OUTPUT] Comparison CSV: {output_csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

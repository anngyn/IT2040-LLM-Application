#!/usr/bin/env python3
"""Run a lightweight FACT-AUDIT baseline over a JSONL claim set."""

from __future__ import annotations

import argparse
import time
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fact_audit_baseline.config import deep_get, load_env, load_simple_yaml
from fact_audit_baseline.evaluator import parse_model_response, score_response
from fact_audit_baseline.io_utils import read_jsonl, write_csv, write_jsonl
from fact_audit_baseline.llm_client import build_client
from fact_audit_baseline.prompting import build_fact_audit_prompt


CSV_FIELDS = [
    "claim_id",
    "claim",
    "verdict",
    "justification",
    "score",
    "latency",
    "cost",
    "source_dataset",
    "test_mode",
    "ground_truth",
    "gold_verdict",
    "baseline_verdict",
    "baseline_justification",
    "baseline_score",
    "is_verdict_correct",
    "is_justification_flawed",
    "latency_seconds",
    "cost_usd",
    "provider",
    "model",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run FACT-AUDIT baseline reproduction.")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--env-file", default=".env")
    parser.add_argument("--input-file")
    parser.add_argument("--output-jsonl")
    parser.add_argument("--scores-csv")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--provider")
    parser.add_argument("--model")
    parser.add_argument("--base-url")
    parser.add_argument("--temperature", type=float)
    parser.add_argument("--timeout-seconds", type=int)
    parser.add_argument("--model-path")
    parser.add_argument("--use-cache", action="store_true")
    return parser.parse_args()


def resolve_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return ROOT / path


def run_case(case: Dict[str, Any], client: Any) -> Dict[str, Any]:
    prompt = build_fact_audit_prompt(case)
    start = time.perf_counter()
    raw_response = client.generate(prompt, case)
    latency = time.perf_counter() - start
    parsed = parse_model_response(raw_response)
    score = score_response(case, parsed)
    latency_seconds = round(latency, 4)
    cost_usd = 0.0
    return {
        "claim_id": case["id"],
        "claim": case["source_claim"],
        "key_point": case["key_point"],
        "auxiliary_info": case.get("auxiliary_info", ""),
        "test_mode": case["test_mode"],
        "source_dataset": case.get("source_dataset", ""),
        "ground_truth": case["ground_truth"],
        "gold_verdict": score["gold_verdict"],
        "verdict": parsed["verdict"],
        "justification": parsed.get("justification", ""),
        "score": score["baseline_score"],
        "latency": latency_seconds,
        "cost": cost_usd,
        "baseline_verdict": parsed["verdict"],
        "baseline_justification": parsed.get("justification", ""),
        "baseline_score": score["baseline_score"],
        "is_verdict_correct": score["is_verdict_correct"],
        "is_justification_flawed": score["is_justification_flawed"],
        "evaluator_comment": score["evaluator_comment"],
        "latency_seconds": latency_seconds,
        "cost_usd": cost_usd,
        "provider": client.provider,
        "model": client.model,
        "raw_response": raw_response,
    }


def main() -> int:
    args = parse_args()
    load_env(resolve_path(args.env_file))
    config = load_simple_yaml(resolve_path(args.config))

    input_file = args.input_file or deep_get(config, "paths", "input_file", "data/claim_sets/claim_set_30.jsonl")
    output_jsonl = args.output_jsonl or deep_get(config, "paths", "baseline_results_jsonl", "outputs/baseline_results.jsonl")
    scores_csv = args.scores_csv or deep_get(config, "paths", "scores_csv", "outputs/scores.csv")
    limit = args.limit if args.limit is not None else deep_get(config, "run", "limit", None)

    output_jsonl_path = resolve_path(output_jsonl)
    scores_csv_path = resolve_path(scores_csv)
    if args.use_cache and output_jsonl_path.exists() and scores_csv_path.exists():
        print(f"Using cached outputs: {output_jsonl_path} and {scores_csv_path}")
        return 0

    provider = args.provider or deep_get(config, "llm", "provider", "mock")
    model = args.model or deep_get(config, "llm", "model", "mock-fact-audit-heuristic")
    client = build_client(
        provider=provider,
        model=model,
        base_url=args.base_url or deep_get(config, "llm", "base_url", None),
        temperature=args.temperature if args.temperature is not None else deep_get(config, "llm", "temperature", 0.0),
        timeout_seconds=args.timeout_seconds or deep_get(config, "llm", "timeout_seconds", 60),
        model_path=args.model_path or deep_get(config, "llm", "model_path", None),
    )

    rows = read_jsonl(resolve_path(input_file))
    if limit:
        rows = rows[: int(limit)]

    results: List[Dict[str, Any]] = [run_case(row, client) for row in rows]
    write_jsonl(output_jsonl_path, results)
    write_csv(scores_csv_path, results, CSV_FIELDS)

    correct = sum(1 for row in results if row["is_verdict_correct"])
    avg_score = sum(row["baseline_score"] for row in results) / len(results) if results else 0
    print(f"Wrote {len(results)} baseline rows to {output_jsonl_path}")
    print(f"Wrote score summary to {scores_csv_path}")
    print(f"Correct verdicts: {correct}/{len(results)} | avg_score={avg_score:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Run FACT-AUDIT RAG pipeline: retrieve Wikipedia evidence, then verify claims."""

from __future__ import annotations

import argparse
import json
import time
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fact_audit_baseline.config import deep_get, load_env, load_simple_yaml, resolve_model_name
from fact_audit_baseline.evaluator import parse_model_response, score_response
from fact_audit_baseline.io_utils import read_jsonl, write_jsonl
from fact_audit_baseline.llm_client import build_client
from fact_audit_baseline.retriever import retrieve_wikipedia


def build_rag_prompt(case: Dict[str, Any], evidence: List[Dict[str, str]]) -> str:
    """Build a RAG-enhanced fact-checking prompt with retrieved evidence."""
    evidence_lines = []
    for i, ev in enumerate(evidence, 1):
        source = ev.get("source", "Unknown")
        text = ev.get("text", "")
        evidence_lines.append(f"{i}. [Source: {source}]\n   {text}")

    evidence_block = "\n\n".join(evidence_lines) if evidence_lines else "(No evidence retrieved)"

    return f"""This is a FACT-AUDIT style fact-checking task with retrieved evidence.

Key Point:
{case.get("key_point", "Verify the factuality of the claim.")}

Source Claim:
{case.get("source_claim", "")}

Retrieved Evidence:
{evidence_block}

Instruction:
Use the retrieved evidence as the primary source for verification. Analyze whether
the evidence supports, refutes, or is insufficient to determine the claim's factuality.

Return one JSON object with exactly these keys:
- verdict: one of "Factual", "Non-Factual", or "Not Enough Information"
- justification: concise explanation grounded in the retrieved evidence
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run FACT-AUDIT RAG pipeline.")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--env-file", default=".env")
    parser.add_argument("--input-file")
    parser.add_argument("--output-jsonl")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--provider")
    parser.add_argument("--model")
    parser.add_argument("--base-url")
    parser.add_argument("--temperature", type=float)
    parser.add_argument("--timeout-seconds", type=int)
    parser.add_argument("--top-k", type=int, default=5, help="Number of Wikipedia articles to retrieve")
    parser.add_argument("--max-chars", type=int, default=1500, help="Max chars per article extract")
    parser.add_argument("--retrieval-delay", type=float, default=1.0, help="Delay between Wikipedia API calls")
    return parser.parse_args()


def resolve_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return ROOT / path


def run_rag_case(
    case: Dict[str, Any],
    client: Any,
    top_k: int,
    max_chars: int,
    retrieval_delay: float,
) -> Dict[str, Any]:
    """Run RAG pipeline for a single claim."""
    claim_text = case.get("source_claim", "")

    retrieval_start = time.perf_counter()
    evidence = retrieve_wikipedia(
        claim=claim_text,
        top_k=top_k,
        max_chars_per_article=max_chars,
        delay=retrieval_delay,
    )
    retrieval_time = time.perf_counter() - retrieval_start

    prompt = build_rag_prompt(case, evidence)

    llm_start = time.perf_counter()
    raw_response = client.generate(prompt, case)
    llm_time = time.perf_counter() - llm_start

    parsed = parse_model_response(raw_response)
    score = score_response(case, parsed)

    return {
        "claim_id": case["id"],
        "claim": claim_text,
        "test_mode": case.get("test_mode", "evidence"),
        "retrieved_evidence": evidence,
        "rag_verdict": parsed["verdict"],
        "rag_justification": parsed.get("justification", ""),
        "rag_score": score["baseline_score"],
        "baseline_result_ref": case["id"],
        "gold_verdict": score["gold_verdict"],
        "is_verdict_correct": score["is_verdict_correct"],
        "is_justification_flawed": score["is_justification_flawed"],
        "evaluator_comment": score["evaluator_comment"],
        "retrieval_latency_seconds": round(retrieval_time, 4),
        "llm_latency_seconds": round(llm_time, 4),
        "provider": client.provider,
        "model": client.model,
        "raw_response": raw_response,
    }


def main() -> int:
    args = parse_args()
    load_env(resolve_path(args.env_file))
    config = load_simple_yaml(resolve_path(args.config))

    input_file = args.input_file or deep_get(config, "paths", "input_file", "data/claim_sets/claim_set_30.jsonl")
    output_jsonl = args.output_jsonl or deep_get(config, "paths", "rag_results_jsonl", "outputs/rag_results.jsonl")
    limit = args.limit if args.limit is not None else deep_get(config, "run", "limit", None)

    provider = args.provider or deep_get(config, "llm", "provider", "mock")
    configured_model = deep_get(config, "llm", "model", "mock-fact-audit-heuristic")
    model = args.model or resolve_model_name(provider, configured_model)
    client = build_client(
        provider=provider,
        model=model,
        base_url=args.base_url or deep_get(config, "llm", "base_url", None),
        temperature=args.temperature if args.temperature is not None else deep_get(config, "llm", "temperature", 0.0),
        timeout_seconds=args.timeout_seconds or deep_get(config, "llm", "timeout_seconds", 60),
    )

    rows = read_jsonl(resolve_path(input_file))
    if limit:
        rows = rows[: int(limit)]

    print(f"[RAG] Running {len(rows)} claims | provider={provider} model={model} top_k={args.top_k}")

    results: List[Dict[str, Any]] = []
    for i, row in enumerate(rows, 1):
        print(f"  [{i}/{len(rows)}] {row['id']}: {row['source_claim'][:60]}...")
        result = run_rag_case(
            case=row,
            client=client,
            top_k=args.top_k,
            max_chars=args.max_chars,
            retrieval_delay=args.retrieval_delay,
        )
        results.append(result)

    output_path = resolve_path(output_jsonl)
    write_jsonl(output_path, results)

    correct = sum(1 for r in results if r["is_verdict_correct"])
    avg_score = sum(r["rag_score"] for r in results) / len(results) if results else 0
    print(f"\n[RAG] Wrote {len(results)} results to {output_path}")
    print(f"[RAG] Correct verdicts: {correct}/{len(results)} | avg_score={avg_score:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

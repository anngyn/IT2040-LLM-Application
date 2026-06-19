#!/usr/bin/env python3
"""Generate a small dynamic FACT-AUDIT-inspired claim set from taxonomy prompts."""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fact_audit_baseline.config import load_env, load_simple_yaml, resolve_model_name
from fact_audit_baseline.io_utils import write_jsonl
from fact_audit_baseline.llm_client import build_client


DEFAULT_TAXONOMY = Path("../external/FACT-AUDIT/data/fact_cat.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate dynamic FACT-AUDIT-style cases.")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--env-file", default=".env")
    parser.add_argument("--taxonomy-file", default=str(DEFAULT_TAXONOMY))
    parser.add_argument("--output-file", default="data/claim_sets/dynamic_claim_set_12.jsonl")
    parser.add_argument("--size", type=int, default=12)
    parser.add_argument("--provider")
    parser.add_argument("--model")
    parser.add_argument("--base-url")
    parser.add_argument("--temperature", type=float, default=0.3)
    parser.add_argument("--seed", type=int, default=2040)
    return parser.parse_args()


def resolve_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return ROOT / path


def load_taxonomy(path: Path) -> Dict[str, List[str]]:
    return json.loads(path.read_text(encoding="utf-8"))


def scenario_to_mode(group_name: str) -> str:
    if group_name == "complex_claim":
        return "evidence"
    if group_name == "fake_news":
        return "claim"
    return "wisdom_of_crowds"


def extract_json_object(text: str) -> Dict[str, Any]:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("Model output did not contain a JSON object.")
    return json.loads(match.group(0))


def build_generation_prompt(*, case_id: str, group_name: str, scenario_name: str, mode: str) -> str:
    return f"""You are generating one dynamic fact-checking test case inspired by FACT-AUDIT.

Scenario group: {group_name}
Scenario type: {scenario_name}
Test mode: {mode}
Case id: {case_id}

Generate exactly one JSON object with these fields:
- id
- key_point
- source_claim
- auxiliary_info
- test_mode
- ground_truth
- source_dataset
- scenario_object
- scenario_type

Rules:
- id must be "{case_id}"
- test_mode must be "{mode}"
- ground_truth must be one of: True, False, Unknown
- source_dataset must be "DYNAMIC_SYNTHETIC"
- scenario_object must be "{group_name}"
- scenario_type must be "{scenario_name}"
- source_claim must be realistic and check-worthy
- if test_mode is claim, auxiliary_info should be empty
- if test_mode is evidence, auxiliary_info should contain short evidence snippets
- if test_mode is wisdom_of_crowds, auxiliary_info should look like a short comment thread

Return JSON only.
"""


def main() -> int:
    args = parse_args()
    load_env(resolve_path(args.env_file))
    config = load_simple_yaml(resolve_path(args.config))
    provider = args.provider or config.get("llm", {}).get("provider", "mock")
    configured_model = config.get("llm", {}).get("model", "mock-fact-audit-heuristic")
    model = args.model or resolve_model_name(provider, configured_model)

    if provider == "mock":
        raise RuntimeError(
            "Dynamic claim generation requires gemini, openai, or transformers; mock is not suitable."
        )

    taxonomy = load_taxonomy(resolve_path(args.taxonomy_file))
    client = build_client(
        provider=provider,
        model=model,
        base_url=args.base_url or config.get("llm", {}).get("base_url"),
        temperature=args.temperature,
        timeout_seconds=config.get("llm", {}).get("timeout_seconds", 60),
        model_path=config.get("llm", {}).get("model_path"),
    )

    rng = random.Random(args.seed)
    scenarios: List[tuple[str, str]] = []
    for group_name, scenario_names in taxonomy.items():
        for scenario_name in scenario_names:
            scenarios.append((group_name, scenario_name))
    rng.shuffle(scenarios)

    rows: List[Dict[str, Any]] = []
    for idx, (group_name, scenario_name) in enumerate(scenarios[: args.size], start=1):
        case_id = f"dynamic_{idx:03d}"
        mode = scenario_to_mode(group_name)
        prompt = build_generation_prompt(
            case_id=case_id,
            group_name=group_name,
            scenario_name=scenario_name,
            mode=mode,
        )
        raw = client.generate(prompt, {})
        rows.append(extract_json_object(raw))

    output_path = resolve_path(args.output_file)
    write_jsonl(output_path, rows)
    print(f"Wrote {len(rows)} dynamic cases to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

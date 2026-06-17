"""Deterministic evaluator for baseline smoke tests and demos."""

from __future__ import annotations

import json
import re
from typing import Any, Dict


FACT_AUDIT_VERDICTS = {"Factual", "Non-Factual", "Not Enough Information"}


def gold_to_verdict(label: str) -> str:
    normalized = (label or "").strip().lower()
    if normalized in {"true", "supported", "factual"}:
        return "Factual"
    if normalized in {"false", "refuted", "non-factual", "non factual"}:
        return "Non-Factual"
    return "Not Enough Information"


def parse_model_response(text: str) -> Dict[str, str]:
    text = (text or "").strip()
    if not text:
        return {
            "verdict": "Not Enough Information",
            "justification": "The model returned an empty response.",
        }

    try:
        payload = json.loads(text)
        verdict = str(payload.get("verdict", "")).strip()
        justification = str(payload.get("justification", "")).strip()
        if verdict in FACT_AUDIT_VERDICTS:
            return {"verdict": verdict, "justification": justification}
    except json.JSONDecodeError:
        pass

    lowered = text.lower()
    if re.search(r"\bnon[- ]?factual\b|\bfalse\b|\brefuted\b", lowered):
        verdict = "Non-Factual"
    elif re.search(r"\bfactual\b|\btrue\b|\bsupported\b", lowered):
        verdict = "Factual"
    else:
        verdict = "Not Enough Information"
    return {"verdict": verdict, "justification": text}


def score_response(case: Dict[str, Any], parsed_response: Dict[str, str]) -> Dict[str, Any]:
    gold_verdict = gold_to_verdict(str(case.get("ground_truth", "")))
    predicted = parsed_response["verdict"]
    justification = parsed_response.get("justification", "").strip()
    is_correct = predicted == gold_verdict

    word_count = len(justification.split())
    generic_markers = {
        "not enough information to determine",
        "cannot be verified",
        "insufficient information",
    }
    justification_lower = justification.lower()
    has_generic_only = any(marker in justification_lower for marker in generic_markers) and word_count < 18
    is_justification_flawed = is_correct and (word_count < 10 or has_generic_only)

    if not is_correct:
        score = 2
        comment = f"Verdict mismatch: expected {gold_verdict}, got {predicted}."
    elif is_justification_flawed:
        score = 3
        comment = "Verdict is correct, but the justification is too thin for FACT-AUDIT scoring."
    else:
        score = 8
        if case.get("test_mode") == "evidence" and case.get("auxiliary_info"):
            score = 9
        comment = "Verdict matches the reference label and the justification is usable."

    return {
        "gold_verdict": gold_verdict,
        "is_verdict_correct": is_correct,
        "is_justification_flawed": is_justification_flawed,
        "baseline_score": score,
        "evaluator_comment": comment,
    }

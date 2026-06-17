"""Prompt templates adapted from the FACT-AUDIT fact verification stage."""

from __future__ import annotations

from typing import Any, Dict


def build_fact_audit_prompt(case: Dict[str, Any]) -> str:
    auxiliary = case.get("auxiliary_info") or ""
    mode = case.get("test_mode", "claim")

    mode_instruction = {
        "claim": "Use only the claim and your internal factual knowledge.",
        "evidence": "Use the auxiliary evidence as the primary source for verification.",
        "wisdom_of_crowds": "Extract useful signals from the conversation-style auxiliary information.",
    }.get(mode, "Verify the claim carefully.")

    return f"""This is a FACT-AUDIT style fact-checking task.

Key Point:
{case.get("key_point", "Verify the factuality of the claim.")}

Test Mode:
[{mode}]

Source Claim:
{case.get("source_claim", "")}

Auxiliary Information:
{auxiliary}

Instruction:
{mode_instruction}

Return one JSON object with exactly these keys:
- verdict: one of "Factual", "Non-Factual", or "Not Enough Information"
- justification: concise explanation grounded in the claim and auxiliary information
"""

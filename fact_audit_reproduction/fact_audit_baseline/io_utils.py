"""JSONL/CSV I/O helpers for the baseline reproduction."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


REQUIRED_INPUT_FIELDS = {
    "id",
    "key_point",
    "source_claim",
    "auxiliary_info",
    "test_mode",
    "ground_truth",
}


def read_jsonl(path: str | Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            missing = REQUIRED_INPUT_FIELDS.difference(row)
            if missing:
                raise ValueError(f"{path}:{line_no} missing fields: {sorted(missing)}")
            rows.append(row)
    return rows


def write_jsonl(path: str | Path, rows: Iterable[Dict[str, Any]]) -> int:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def write_csv(path: str | Path, rows: List[Dict[str, Any]], fields: List[str]) -> int:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})
    return len(rows)


def preview_rows(rows: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
    return rows[: max(0, limit)]

"""Small config helpers with no mandatory third-party dependency."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict


def _coerce_scalar(value: str) -> Any:
    value = value.strip().strip('"').strip("'")
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if lowered in {"null", "none"}:
        return None
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def load_env(path: str | Path | None) -> None:
    """Load KEY=VALUE lines into os.environ without overriding existing values."""
    if not path:
        return
    env_path = Path(path)
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def load_simple_yaml(path: str | Path | None) -> Dict[str, Dict[str, Any]]:
    """Parse the tiny subset of YAML used by config.yaml.

    Supported shape:

        section:
          key: value

    This keeps the demo runnable on a clean Python install.
    """
    if not path:
        return {}
    config_path = Path(path)
    if not config_path.exists():
        return {}

    parsed: Dict[str, Dict[str, Any]] = {}
    current_section: str | None = None
    for raw_line in config_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if not line.startswith(" ") and line.endswith(":"):
            current_section = line[:-1].strip()
            parsed.setdefault(current_section, {})
            continue
        if current_section and ":" in line:
            key, value = line.strip().split(":", 1)
            parsed[current_section][key.strip()] = _coerce_scalar(value)
    return parsed


def deep_get(config: Dict[str, Dict[str, Any]], section: str, key: str, default: Any) -> Any:
    return config.get(section, {}).get(key, default)

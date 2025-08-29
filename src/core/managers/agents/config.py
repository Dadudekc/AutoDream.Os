"""Configuration utilities for agent orchestrator."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def load_config(path: str | Path | None) -> Dict[str, Any]:
    """Load configuration from *path*.

    Returns an empty dictionary if the file does not exist or cannot be parsed.
    """
    if path is None:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    try:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

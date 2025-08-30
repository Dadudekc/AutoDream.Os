"""Shared utilities for performance profiling tools."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

# Default performance thresholds used across profiling tools
DEFAULT_THRESHOLDS: Dict[str, float] = {
    "critical_cpu": 95.0,
    "warning_cpu": 80.0,
    "critical_memory": 90.0,
    "warning_memory": 75.0,
    "critical_function_time": 5.0,
    "warning_function_time": 1.0,
}

def load_json_file(path: str) -> Any:
    """Load and parse JSON data from ``path``.

    Args:
        path: Path to the JSON file.

    Returns:
        Parsed data or an empty dictionary if loading fails.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:  # pragma: no cover - logging path
        logger.error("Error reading JSON file %s: %s", path, exc)
        return {}

def save_json_file(path: str, data: Any) -> bool:
    """Serialize ``data`` to ``path`` as JSON.

    Args:
        path: Destination file path.
        data: Data to serialize.

    Returns:
        ``True`` if the file was written successfully, ``False`` otherwise.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as exc:  # pragma: no cover - logging path
        logger.error("Error writing JSON file %s: %s", path, exc)
        return False

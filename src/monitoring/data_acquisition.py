"""Data loading utilities for health reports."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from ..constants import HEALTH_REPORTS_DIR


def load_health_reports(directory: Path | None = None) -> List[Dict[str, Any]]:
    """Load all health report JSON files.

    Args:
        directory: Optional override for the reports directory.

    Returns:
        List of report dictionaries loaded from JSON files.
    """
    reports_dir = directory or HEALTH_REPORTS_DIR
    reports: List[Dict[str, Any]] = []

    for path in sorted(reports_dir.glob("health_report_daily_summary_*.json")):
        try:
            with path.open("r", encoding="utf-8") as handle:
                reports.append(json.load(handle))
        except json.JSONDecodeError:
            continue
    return reports

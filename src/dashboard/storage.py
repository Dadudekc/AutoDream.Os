"""Storage helpers for dashboard data."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from ..constants import HEALTH_REPORTS_DIR


def load_reports(directory: Path | None = None) -> List[Dict[str, Any]]:
    """Load all health report JSON files."""
    reports_dir = directory or HEALTH_REPORTS_DIR
    reports: List[Dict[str, Any]] = []

    for path in sorted(reports_dir.glob("health_report_daily_summary_*.json")):
        try:
            with path.open("r", encoding="utf-8") as handle:
                reports.append(json.load(handle))
        except json.JSONDecodeError:
            continue
    return reports


def save_summary(
    summary: Dict[str, Any], *, directory: Path | None = None
) -> Path:
    """Persist aggregated dashboard summary to disk."""
    output_dir = directory or HEALTH_REPORTS_DIR
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "dashboard_summary.json"
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    return output_path


# Backwards compatibility
load_health_reports = load_reports


__all__ = ["load_reports", "save_summary", "load_health_reports"]

"""Reporting utilities for baseline measurements."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, List

from .data_handler import PerformanceBaseline


def export_baseline_data(
    baselines: List[PerformanceBaseline],
    baseline_config: Dict[str, Any],
    output_path: str,
    format: str = "json",
) -> bool:
    """Export baseline data to *output_path* in the specified *format*."""

    if format.lower() != "json":
        return False
    export_data = {
        "export_timestamp": datetime.now().isoformat(),
        "baseline_config": baseline_config,
        "baselines": [
            {
                "baseline_id": b.baseline_id,
                "name": b.name,
                "description": b.description,
                "baseline_type": b.baseline_type.value,
                "status": b.status.value,
                "version": b.version,
                "created_at": b.created_at.isoformat(),
                "updated_at": b.updated_at.isoformat(),
            }
            for b in baselines
        ],
    }
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(export_data, handle, indent=2)
    return True


def get_system_status(
    baselines: List[PerformanceBaseline], baseline_config: Dict[str, Any]
) -> Dict[str, Any]:
    """Return a summary of the current baseline system state."""

    return {
        "status": "active",
        "total_baselines": len(baselines),
        "baseline_types": {
            b.baseline_type.value: sum(
                1 for x in baselines if x.baseline_type == b.baseline_type
            )
            for b in baselines
        },
        "auto_calibration_enabled": baseline_config.get(
            "auto_calibration_enabled", False
        ),
    }


__all__ = ["export_baseline_data", "get_system_status"]

#!/usr/bin/env python3
"""
Performance Monitor Utilities
============================

Helper functions and utilities for performance monitoring.
Extracted to maintain V2 compliance (≤400 lines per file).

Author: Agent-6 (SSOT_MANAGER)
License: MIT
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)


def save_snapshot_to_file(snapshot: Dict[str, Any], output_dir: str = "logs/performance") -> Path:
    """Save performance snapshot to JSON file."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = snapshot.get("timestamp", "unknown")
    filename = f"performance_{timestamp.replace(':', '-')}.json"
    file_path = output_path / filename
    
    with open(file_path, 'w') as f:
        json.dump(snapshot, f, indent=2)
    
    logger.info(f"Performance snapshot saved: {file_path}")
    return file_path


def load_snapshots_from_dir(input_dir: str = "logs/performance") -> list:
    """Load all performance snapshots from directory."""
    input_path = Path(input_dir)
    if not input_path.exists():
        return []
    
    snapshots = []
    for file_path in input_path.glob("performance_*.json"):
        try:
            with open(file_path, 'r') as f:
                snapshot = json.load(f)
                snapshots.append(snapshot)
        except Exception as e:
            logger.warning(f"Error loading snapshot {file_path}: {e}")
    
    return snapshots


def calculate_average_metrics(snapshots: list) -> Dict[str, float]:
    """Calculate average metrics from snapshots."""
    if not snapshots:
        return {}
    
    total_cpu = sum(s.get("cpu_percent", 0) for s in snapshots)
    total_mem = sum(s.get("memory_mb", 0) for s in snapshots)
    total_response = sum(s.get("response_time_ms", 0) for s in snapshots)
    
    count = len(snapshots)
    return {
        "avg_cpu_percent": total_cpu / count,
        "avg_memory_mb": total_mem / count,
        "avg_response_time_ms": total_response / count,
        "snapshot_count": count
    }


def format_metrics_report(metrics: Dict[str, Any]) -> str:
    """Format metrics as human-readable report."""
    lines = []
    lines.append("=" * 60)
    lines.append("PERFORMANCE METRICS REPORT")
    lines.append("=" * 60)
    
    for key, value in metrics.items():
        if isinstance(value, float):
            lines.append(f"{key}: {value:.2f}")
        else:
            lines.append(f"{key}: {value}")
    
    lines.append("=" * 60)
    return "\n".join(lines)


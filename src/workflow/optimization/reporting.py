"""Reporting helpers for workflow optimization."""
from __future__ import annotations

from typing import Dict


def generate_report(analysis: Dict[str, float]) -> str:
    """Create a human readable report from analysis results."""

    lines = ["Workflow Optimization Report"]
    lines.append("-" * 30)
    for key, value in analysis.items():
        lines.append(f"{key}: {value}")
    return "\n".join(lines)

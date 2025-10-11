#!/usr/bin/env python3
"""
Compliance History Models
=========================

Data models for compliance tracking and trend analysis.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
Refactored from: compliance_history_tracker.py
License: MIT
"""

from dataclasses import dataclass


@dataclass
class ComplianceSnapshot:
    """Snapshot of compliance metrics at a point in time."""

    timestamp: str
    commit_hash: str | None
    total_files: int
    v2_compliance_rate: float
    complexity_compliance_rate: float
    critical_violations: int
    major_violations: int
    high_complexity: int
    medium_complexity: int
    overall_score: float


@dataclass
class TrendReport:
    """Trend analysis report."""

    snapshots: list[ComplianceSnapshot]
    trend_direction: str  # "improving", "stable", "degrading"
    compliance_change: float
    complexity_change: float
    score_change: float
    recommendations: list[str]

"""
Agent Metrics and Efficiency Scoring
===================================

Core metrics data model and scoring algorithms for agent efficiency.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Iterable, Dict, Any
from datetime import datetime, timedelta
import json
import math
import pathlib
import xml.etree.ElementTree as ET

# ---------- Public Datamodel ----------

@dataclass
class AgentSnapshot:
    """Agent performance snapshot for a time window."""
    agent_id: str
    # Raw metrics (per window)
    tasks_assigned: int
    tasks_completed: int
    tasks_on_time: int
    tasks_reworked: int               # count of reopens/rollbacks
    incidents: int                    # failing checks, prod issues, broken tests introduced
    prs_merged: int
    loc_touched: int                  # lines added+modified (rough proxy)
    wall_secs_active: float           # "active" time during window (sum of task spans)
    # Quality metrics
    unit_tests_failed: int
    unit_tests_total: int
    coverage_pct: float               # parsed from coverage.xml or CI
    # Optional signals
    complexity_avg: Optional[float] = None  # from radon or similar, lower is better
    review_findings: Optional[int] = 0      # PR comments marked must-fix
    # Window metadata
    window_start: Optional[datetime] = None
    window_end: Optional[datetime] = None

# ---------- Utilities ----------

def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    """Clamp value between bounds."""
    return max(lo, min(hi, x))

def safe_div(n: float, d: float) -> float:
    """Safe division with zero handling."""
    return 0.0 if d == 0 else n / d

# ---------- Parsers ----------

def parse_cobertura_coverage(coverage_xml_path: str) -> float:
    """
    Parse Cobertura/coverage.py XML and return coverage percentage (0..100).
    """
    p = pathlib.Path(coverage_xml_path)
    if not p.exists():
        return 0.0
    root = ET.parse(str(p)).getroot()
    # Try coverage.py schema
    rate = root.get("line-rate")
    if rate is not None:
        return float(rate) * 100.0
    # Try Cobertura schema
    lines_valid = root.get("lines-valid")
    lines_covered = root.get("lines-covered")
    if lines_valid and lines_covered:
        return safe_div(float(lines_covered), float(lines_valid)) * 100.0
    # Fallback scan
    covered = 0
    valid = 0
    for cls in root.iter("class"):
        for line in cls.iter("line"):
            hits = int(line.get("hits", "0"))
            valid += 1
            if hits > 0:
                covered += 1
    return safe_div(covered, valid) * 100.0 if valid else 0.0

# ---------- Scoring Model ----------

@dataclass
class Weights:
    """Configurable weights for efficiency scoring."""
    throughput: float = 0.25
    on_time: float = 0.15
    defect_rate_inv: float = 0.20
    rework_inv: float = 0.10
    test_pass: float = 0.10
    coverage: float = 0.10
    complexity_inv: float = 0.05
    review_findings_inv: float = 0.05

DEFAULT_WEIGHTS = Weights()

def efficiency_score(s: AgentSnapshot, w: Weights = DEFAULT_WEIGHTS) -> Dict[str, Any]:
    """
    Returns a normalized breakdown (0..1) and composite score (0..100).
    Interpretable, weight-tunable, and plug-and-play with the captain tracker.
    """

    # Normalize base rates
    throughput = safe_div(s.tasks_completed, max(1.0, s.wall_secs_active/3600.0))  # tasks/hour
    # Map throughput to [0..1] using soft cap (e.g., 2 tasks/hour saturates)
    throughput_norm = clamp(throughput / 2.0)

    on_time_rate = clamp(safe_div(s.tasks_on_time, max(1, s.tasks_completed)))
    defect_rate = safe_div(s.incidents, max(1, s.tasks_completed))  # lower better
    defect_rate_inv = clamp(1.0 - defect_rate)

    rework_rate = safe_div(s.tasks_reworked, max(1, s.tasks_completed))  # lower better
    rework_inv = clamp(1.0 - rework_rate)

    test_pass_rate = clamp(1.0 - safe_div(s.unit_tests_failed, max(1, s.unit_tests_total)))

    coverage_norm = clamp(s.coverage_pct / 100.0)

    if s.complexity_avg is None or s.complexity_avg <= 0:
        complexity_inv = 0.5  # neutral prior
    else:
        # Radon CC: <=5 good, 10 ok, 20 bad. Squash to [0..1] inverse.
        # Map 5->1.0, 10->0.6, 20->0.2, >=30->~0.0
        complexity_inv = clamp(1.2 - math.log10(max(1.0, s.complexity_avg)) * 0.8)

    findings = float(s.review_findings or 0)
    # 0 findings = 1.0, >=8 findings ~ 0.0; smooth decay
    review_findings_inv = clamp(1.0 / (1.0 + findings/2.0))

    # Weighted composite
    parts = dict(
        throughput=throughput_norm,
        on_time=on_time_rate,
        defect_rate_inv=defect_rate_inv,
        rework_inv=rework_inv,
        test_pass=test_pass_rate,
        coverage=coverage_norm,
        complexity_inv=complexity_inv,
        review_findings_inv=review_findings_inv,
    )

    weighted = (
        parts["throughput"] * w.throughput +
        parts["on_time"] * w.on_time +
        parts["defect_rate_inv"] * w.defect_rate_inv +
        parts["rework_inv"] * w.rework_inv +
        parts["test_pass"] * w.test_pass +
        parts["coverage"] * w.coverage +
        parts["complexity_inv"] * w.complexity_inv +
        parts["review_findings_inv"] * w.review_findings_inv
    )

    return {
        "breakdown": parts,
        "weights": w.__dict__,
        "composite_0_100": round(weighted * 100.0, 2),
        "raw": s.__dict__,
    }

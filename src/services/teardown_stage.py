"""Teardown stage utilities for test orchestration."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Dict

from .config import ENTERPRISE_STANDARDS


def calculate_metrics(results: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    """Aggregate suite results into enterprise metrics."""
    total_tests = sum(r["total_tests"] for r in results.values())
    total_failures = sum(r["failures"] for r in results.values())
    total_errors = sum(r["errors"] for r in results.values())
    success_rate = (
        (total_tests - total_failures - total_errors) / total_tests * 100
        if total_tests
        else 0.0
    )
    return {
        "total_tests": total_tests,
        "total_failures": total_failures,
        "total_errors": total_errors,
        "success_rate": success_rate,
        "services_tested": len([r for r in results.values() if r["total_tests"] > 0]),
    }


def generate_report(
    results: Dict[str, Dict[str, float]], metrics: Dict[str, float]
) -> Dict[str, object]:
    """Generate and save a comprehensive report."""
    report = {
        "timestamp": time.time(),
        "test_orchestrator": "Master V2 Test Orchestrator",
        "enterprise_metrics": metrics,
        "test_suite_results": results,
        "enterprise_standards": ENTERPRISE_STANDARDS,
    }
    report_file = Path("enterprise_v2_test_report.json")
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    return report

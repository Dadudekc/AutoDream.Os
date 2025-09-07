"""Execution stage utilities for test orchestration."""

from __future__ import annotations

from typing import Dict, Type
import unittest

from src.automation.common import execute_test_suite


def run_suite(
    suite_name: str, suite_class: Type[unittest.TestCase]
) -> Dict[str, float]:
    """Execute a single test suite and return summary metrics."""
    print(f"🚀 Running {suite_name.upper()} Test Suite...")
    summary = execute_test_suite(suite_class)
    success = summary["failures"] == 0 and summary["errors"] == 0
    if success:
        print(f"✅ {suite_name.upper()} Test Suite completed!")
    else:
        print(f"⚠️  {suite_name.upper()} Test Suite completed with issues")
    print(
        f"   Tests: {summary['total_tests']}, Success Rate: {summary['success_rate']:.1f}%"
    )
    summary["status"] = "passed" if success else "failed"
    summary["suite_name"] = suite_name
    return summary


def run_all_suites(
    test_suites: Dict[str, Type[unittest.TestCase]],
) -> Dict[str, Dict[str, float]]:
    """Execute all provided test suites."""
    results: Dict[str, Dict[str, float]] = {}
    for name, cls in test_suites.items():
        results[name] = run_suite(name, cls)
    return results

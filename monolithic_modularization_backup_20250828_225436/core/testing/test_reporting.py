"""Reporting helpers for test execution."""

from __future__ import annotations

from typing import Any, Dict, List

from .testing_utils import TestResult, TestStatus


def summarize_results(results: List[TestResult]) -> Dict[str, Any]:
    """Compute aggregate statistics for a collection of test results."""
    total = len(results)
    passed = sum(1 for r in results if r.status == TestStatus.PASSED)
    failed = sum(1 for r in results if r.status == TestStatus.FAILED)
    errors = sum(1 for r in results if r.status == TestStatus.ERROR)
    skipped = sum(1 for r in results if r.status == TestStatus.SKIPPED)
    success_rate = (passed / total * 100) if total else 0.0
    avg_time = sum(r.execution_time for r in results) / total if total else 0.0
    return {
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "skipped": skipped,
        "success_rate": success_rate,
        "avg_execution_time": avg_time,
    }


def print_execution_summary(results: List[TestResult]) -> None:
    """Print a human-readable execution summary."""
    stats = summarize_results(results)
    print("\n🚀 TEST EXECUTION SUMMARY")
    print("=" * 40)
    print(f"Total Tests: {stats['total_tests']}")
    print(f"✅ Passed: {stats['passed']}")
    print(f"❌ Failed: {stats['failed']}")
    print(f"💥 Errors: {stats['errors']}")
    print(f"⏭️  Skipped: {stats['skipped']}")
    print(f"📈 Success Rate: {stats['success_rate']:.1f}%")
    print(f"⏱️  Avg Execution Time: {stats['avg_execution_time']:.2f}s")

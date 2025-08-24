#!/usr/bin/env python3
"""Reporting utilities for authentication integration tests."""

import time
import json
import logging
from datetime import datetime


def generate_test_report(test_results: dict, logger: logging.Logger) -> dict:
    """Generate comprehensive test report."""
    logger.info("📊 Generating Test Report")
    logger.info("-" * 40)

    # Calculate success rate
    total_tests = test_results["tests_run"]
    passed_tests = test_results["tests_passed"]
    failed_tests = test_results["tests_failed"]
    error_tests = test_results.get("tests_error", 0)

    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    # Generate report
    report = {
        "report_id": f"auth_integration_report_{int(time.time())}",
        "timestamp": datetime.now().isoformat(),
        "test_summary": {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "error_tests": error_tests,
            "success_rate": f"{success_rate:.1f}%",
        },
        "test_results": test_results,
        "recommendations": [],
        "status": "PASS" if failed_tests == 0 and error_tests == 0 else "FAIL",
    }

    # Generate recommendations
    if failed_tests > 0:
        report["recommendations"].append(f"Investigate {failed_tests} failed tests")

    if error_tests > 0:
        report["recommendations"].append(f"Fix {error_tests} test errors")

    if success_rate < 90:
        report["recommendations"].append(
            "Overall success rate below 90% - review system"
        )

    if success_rate >= 95:
        report["recommendations"].append(
            "Excellent test results - system ready for production"
        )

    return report


def save_test_report(report: dict, logger: logging.Logger):
    """Save test report to file."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"auth_integration_report_{timestamp}.json"

        with open(filename, "w") as f:
            json.dump(report, f, indent=2, default=str)

        logger.info(f"✅ Test report saved to {filename}")

    except Exception as e:  # pragma: no cover - logging
        logger.error(f"❌ Failed to save test report: {e}")

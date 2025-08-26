"""Utilities for generating frontend test reports."""

import logging
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - for type hints only
    from .frontend_testing import TestSuite

logger = logging.getLogger(__name__)


def generate_summary_report(suites: Dict[str, "TestSuite"]) -> None:
    """Log a summary report for the given test suites."""
    total_tests = sum(s.total_tests for s in suites.values())
    total_passed = sum(s.passed_tests for s in suites.values())
    total_failed = sum(s.failed_tests for s in suites.values())
    total_skipped = sum(s.skipped_tests for s in suites.values())
    total_duration = sum(s.total_duration for s in suites.values())

    logger.info("=" * 60)
    logger.info("FRONTEND TESTING SUMMARY REPORT")
    logger.info("=" * 60)
    logger.info(f"Total Tests: {total_tests}")
    logger.info(f"Passed: {total_passed}")
    logger.info(f"Failed: {total_failed}")
    logger.info(f"Skipped: {total_skipped}")
    logger.info(f"Total Duration: {total_duration:.2f}s")
    logger.info("=" * 60)

    for suite_name, suite in suites.items():
        logger.info(f"{suite_name.upper()}: {suite.passed_tests}/{suite.total_tests} passed")

    logger.info("=" * 60)

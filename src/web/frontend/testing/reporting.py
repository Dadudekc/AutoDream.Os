"""Test report generation utilities for the frontend."""
import logging
from typing import Dict, Any


class TestReportGenerator:
    """Generate simple summary reports for test suites."""

    def __init__(self, logger: logging.Logger | None = None):
        self.logger = logger or logging.getLogger(__name__)

    def generate_summary(self, suites: Dict[str, Any]) -> None:
        """Log a summary of executed test suites."""
        total_tests = sum(s.total_tests for s in suites.values())
        total_passed = sum(s.passed_tests for s in suites.values())
        total_failed = sum(s.failed_tests for s in suites.values())
        total_skipped = sum(s.skipped_tests for s in suites.values())
        total_duration = sum(s.total_duration for s in suites.values())

        self.logger.info("=" * 60)
        self.logger.info("FRONTEND TESTING SUMMARY REPORT")
        self.logger.info("=" * 60)
        self.logger.info(f"Total Tests: {total_tests}")
        self.logger.info(f"Passed: {total_passed}")
        self.logger.info(f"Failed: {total_failed}")
        self.logger.info(f"Skipped: {total_skipped}")
        self.logger.info(f"Total Duration: {total_duration:.2f}s")
        self.logger.info("=" * 60)

        for suite_name, suite in suites.items():
            self.logger.info(
                f"{suite_name.upper()}: {suite.passed_tests}/{suite.total_tests} passed"
            )

        self.logger.info("=" * 60)

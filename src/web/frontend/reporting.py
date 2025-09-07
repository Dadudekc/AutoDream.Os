import logging
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - type hints only
    from .frontend_testing import TestSuite

logger = logging.getLogger(__name__)


def generate_summary_report(suites: Dict[str, "TestSuite"]) -> str:
    """Log a summary report for frontend test suites."""
    header = "FRONTEND TESTING SUMMARY REPORT"
    total = sum(s.total_tests for s in suites.values())
    passed = sum(s.passed_tests for s in suites.values())
    failed = sum(s.failed_tests for s in suites.values())
    skipped = sum(s.skipped_tests for s in suites.values())
    duration = sum(s.total_duration for s in suites.values())

    logger.info(header)
    logger.info("Total tests: %s", total)
    logger.info("Passed: %s", passed)
    logger.info("Failed: %s", failed)
    logger.info("Skipped: %s", skipped)
    logger.info("Total duration: %.2fs", duration)
    return header

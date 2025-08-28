"""Validation System Finalization.

This module coordinates the finalization process by delegating work to
aggregation, reporting and cleanup helpers. The goal is to keep the
finalization workflow simple and well structured.
"""

import logging
from datetime import datetime
from typing import Any, Dict

from .validation_manager import ValidationManager
from .finalization_aggregation import (
    check_system_health,
    run_integration_tests,
    optimize_performance,
    validate_framework,
)
from .finalization_reporting import generate_completion_report
from .finalization_cleanup import cleanup_resources

logger = logging.getLogger(__name__)


class ValidationSystemFinalizer:
    """Run the validation system finalization workflow."""

    def __init__(self) -> None:
        """Initialize the finalizer and start timer."""
        self.validation_manager = ValidationManager()
        self.finalization_results: Dict[str, Any] = {}
        self.start_time = datetime.now()
        logger.info("Validation System Finalizer initialized")

    def run_finalization_suite(self) -> Dict[str, Any]:
        """Execute all finalization phases and return aggregated results."""
        logger.info("Starting validation system finalization")
        try:
            self.finalization_results["system_health"] = check_system_health(
                self.validation_manager
            )
            self.finalization_results["integration_tests"] = run_integration_tests(
                self.validation_manager
            )
            self.finalization_results["performance_metrics"] = optimize_performance()
            self.finalization_results["framework_validation"] = validate_framework()

            end_time = datetime.now()
            duration = (end_time - self.start_time).total_seconds()
            self.finalization_results["completion_time"] = duration
            self.finalization_results["status"] = "COMPLETE"
            self.finalization_results["timestamp"] = end_time.isoformat()

            report_path = generate_completion_report(self.finalization_results)
            self.finalization_results["report_path"] = str(report_path)

            cleanup_resources(self.validation_manager)
            logger.info("Validation system finalization completed")
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Finalization failed: %s", exc)
            self.finalization_results["status"] = "FAILED"
            self.finalization_results["error"] = str(exc)
        return self.finalization_results


def main() -> None:  # pragma: no cover - convenience wrapper
    """Run the finalizer from the command line."""
    finalizer = ValidationSystemFinalizer()
    results = finalizer.run_finalization_suite()
    print(f"Status: {results.get('status')}")
    print(f"Report: {results.get('report_path')}")


if __name__ == "__main__":  # pragma: no cover - convenience wrapper
    main()

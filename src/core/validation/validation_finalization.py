#!/usr/bin/env python3
"""Validation System Finalization - TASK 4G COMPLETION.

This module orchestrates the validation system finalization by delegating work to
aggregation, reporting, and cleanup helpers. The goal is to provide a clear
separation of concerns while keeping the entrypoint minimal.
"""
import logging
from datetime import datetime
from typing import Any, Dict

from .finalization_aggregator import aggregate_finalization_data
from .finalization_cleanup import cleanup
from .finalization_constants import STATUS_COMPLETE, STATUS_FAILED
from .finalization_reporter import generate_completion_report
from .validation_manager import ValidationManager

logger = logging.getLogger(__name__)


class ValidationSystemFinalizer:
    """Coordinate validation system finalization steps."""

    def __init__(self) -> None:
        self.validation_manager = ValidationManager()
        self.start_time = datetime.now()
        self.results: Dict[str, Any] = {}

    def run_finalization_suite(self) -> Dict[str, Any]:
        """Run all finalization steps and return consolidated results."""
        try:
            logger.info("Starting validation system finalization")
            data = aggregate_finalization_data(self.validation_manager)
            self.results.update(data)
            report = generate_completion_report(data, self.start_time)
            self.results.update(report)
            self.results["status"] = STATUS_COMPLETE
            cleanup([])
            logger.info("Validation system finalization completed")
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Finalization failed: %s", exc)
            self.results = {"status": STATUS_FAILED, "error": str(exc)}
        finally:
            self.results["completion_time"] = (
                datetime.now() - self.start_time
            ).total_seconds()
        return self.results


def main() -> None:
    """Run the finalization process as a script."""
    finalizer = ValidationSystemFinalizer()
    results = finalizer.run_finalization_suite()
    print(f"Status: {results.get('status')}")


if __name__ == "__main__":
    main()

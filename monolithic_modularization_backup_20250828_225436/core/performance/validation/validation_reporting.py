"""Reporting utilities for performance validation."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import List

from .validation_constants import HISTORY_LIMIT, HISTORY_RETAIN
from .validation_types import ValidationResult, ValidationSummary


class ValidationReporter:
    """Record validation results and generate reports."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"{__name__}.ValidationReporter")
        self.validation_history: List[ValidationResult] = []

    def record_results(self, results: List[ValidationResult]) -> None:
        """Store validation results and trim history when necessary."""
        self.validation_history.extend(results)
        if len(self.validation_history) > HISTORY_LIMIT:
            self.validation_history = self.validation_history[-HISTORY_RETAIN:]

    def get_validation_summary(self) -> ValidationSummary:
        """Generate a summary of validation outcomes."""
        total_validations = len(self.validation_history)
        passed_validations = len([r for r in self.validation_history if r.passed])
        failed_validations = total_validations - passed_validations
        severity_counts = {}
        for result in self.validation_history:
            severity = result.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        return ValidationSummary(
            total_validations=total_validations,
            passed_validations=passed_validations,
            failed_validations=failed_validations,
            success_rate=round(passed_validations / max(total_validations, 1), 3),
            severity_distribution=severity_counts,
            last_validation=datetime.now().isoformat(),
        )

    def get_recent_validations(self, count: int = 100) -> List[ValidationResult]:
        """Return the most recent validation results."""
        return self.validation_history[-count:]

    def clear_validation_history(self) -> None:
        """Remove all stored validation results."""
        self.validation_history.clear()
        self.logger.info("✅ Validation history cleared")

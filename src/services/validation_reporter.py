"""Validation reporting module.

Summarises validation results into an easily consumable structure.
"""
from __future__ import annotations

from typing import Dict, List

from .validation_rules import ValidationResult


class ValidationReporter:
    """Aggregate validation results into summary statistics."""

    def summarize(self, results: List[ValidationResult]) -> Dict[str, int]:
        summary = {"passed": 0, "failed": 0}
        for result in results:
            if result.passed:
                summary["passed"] += 1
            else:
                summary["failed"] += 1
        return summary

"""Validation reporting module.

Summarises validation results into an easily consumable structure.
"""
from __future__ import annotations

from typing import Dict, List

from .validation_rules import ValidationResult
from .constants import SUMMARY_FAILED, SUMMARY_PASSED


class ValidationReporter:
    """Aggregate validation results into summary statistics."""

    def summarize(self, results: List[ValidationResult]) -> Dict[str, int]:
        summary = {SUMMARY_PASSED: 0, SUMMARY_FAILED: 0}
        for result in results:
            if result.passed:
                summary[SUMMARY_PASSED] += 1
            else:
                summary[SUMMARY_FAILED] += 1
        return summary

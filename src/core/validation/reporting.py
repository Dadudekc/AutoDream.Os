"""Reporting utilities for validation results."""

from __future__ import annotations

from typing import Any, Dict, List

from .models import ValidationResult, ValidationSeverity, ValidationStatus


class ValidationReporter:
    """Generate summaries and export detailed validation reports."""

    def __init__(self, executor: "ValidationExecutor") -> None:
        self.executor = executor

    # ------------------------------------------------------------------
    def get_validation_summary(self) -> Dict[str, Any]:
        """Produce a summary of all validation activity."""
        history = self.executor.history
        summary = {
            "total_validations": len(history),
            "passed": sum(1 for r in history if r.status == ValidationStatus.PASSED),
            "failed": sum(1 for r in history if r.status == ValidationStatus.FAILED),
            "warnings": sum(1 for r in history if r.status == ValidationStatus.WARNING),
            "critical": sum(1 for r in history if r.severity == ValidationSeverity.CRITICAL),
        }
        return summary

    # ------------------------------------------------------------------
    def export_validation_report(self) -> List[Dict[str, Any]]:
        """Return a serialisable representation of the validation history."""
        report: List[Dict[str, Any]] = []
        for result in self.executor.history:
            report.append(
                {
                    "rule_id": result.rule_id,
                    "rule_name": result.rule_name,
                    "status": result.status.value,
                    "severity": result.severity.value,
                    "message": result.message,
                    "details": result.details,
                    "timestamp": result.timestamp.isoformat(),
                    "field_path": result.field_path,
                    "actual_value": result.actual_value,
                    "expected_value": result.expected_value,
                }
            )
        return report

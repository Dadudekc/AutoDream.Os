"""Reporting utilities for onboarding validation."""

from typing import Dict, List

from .models import ValidationResult, ValidationSeverity, ValidationStatus


def generate_validation_report(results: List[ValidationResult]) -> Dict[str, int]:
    """Summarize validation results into a report."""
    return {
        "total": len(results),
        "passed": sum(1 for r in results if r.status == ValidationStatus.PASSED),
        "failed": sum(1 for r in results if r.status == ValidationStatus.FAILED),
        "warnings": sum(1 for r in results if r.severity == ValidationSeverity.WARNING),
        "errors": sum(1 for r in results if r.severity == ValidationSeverity.ERROR),
        "critical": sum(
            1 for r in results if r.severity == ValidationSeverity.CRITICAL
        ),
    }


__all__ = ["generate_validation_report"]

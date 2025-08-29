"""Reporting utilities for refactoring validation."""
import time
from typing import Dict, Any, List

from .validation_types import (
    ValidationResult,
    ValidationStatus,
    ValidationSeverity,
    ValidationReport,
)


def generate_validation_report(test_results: List[ValidationResult], validation_rules: Dict[str, Any], validation_id: str, execution_time: float) -> ValidationReport:
    """Generate comprehensive validation report."""
    total_tests = len(test_results)
    passed_tests = len([r for r in test_results if r.status == ValidationStatus.PASSED])
    failed_tests = len([r for r in test_results if r.status == ValidationStatus.FAILED])
    warning_tests = len([r for r in test_results if r.status == ValidationStatus.WARNING])
    skipped_tests = len([r for r in test_results if r.status == ValidationStatus.SKIPPED])

    summary = {
        "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
        "critical_issues": len([r for r in test_results if r.severity == ValidationSeverity.CRITICAL and r.status == ValidationStatus.FAILED]),
        "high_priority_issues": len([r for r in test_results if r.severity == ValidationSeverity.HIGH and r.status in [ValidationStatus.FAILED, ValidationStatus.WARNING]]),
        "validation_rules": {k: v["enabled"] for k, v in validation_rules.items()},
    }

    return ValidationReport(
        validation_id=validation_id,
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
        total_tests=total_tests,
        passed_tests=passed_tests,
        failed_tests=failed_tests,
        warning_tests=warning_tests,
        skipped_tests=skipped_tests,
        execution_time=execution_time,
        results=test_results.copy(),
        summary=summary,
    )

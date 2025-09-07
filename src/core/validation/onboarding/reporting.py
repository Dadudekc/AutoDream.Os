"""Reporting helpers for onboarding validation."""
from typing import Any

from ..base_validator import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)


def generate_success_result(validator: BaseValidator, total_checks: int) -> ValidationResult:
    """Create a success result when all checks pass."""
    return validator._create_result(
        rule_id="overall_onboarding_validation",
        rule_name="Overall Onboarding Validation",
        status=ValidationStatus.PASSED,
        severity=ValidationSeverity.INFO,
        message="Onboarding validation passed successfully",
        details={"total_checks": total_checks},
    )


def generate_error_result(validator: BaseValidator, error: Exception) -> ValidationResult:
    """Create a failure result when an exception occurs."""
    return validator._create_result(
        rule_id="onboarding_validation_error",
        rule_name="Onboarding Validation Error",
        status=ValidationStatus.FAILED,
        severity=ValidationSeverity.CRITICAL,
        message=f"Onboarding validation error: {str(error)}",
        details={"error_type": type(error).__name__},
    )

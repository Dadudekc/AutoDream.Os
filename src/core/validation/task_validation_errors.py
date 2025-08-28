"""Utility helpers for task validation error reporting."""

from .base_validator import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)


def create_error_result(validator: BaseValidator, error: Exception) -> ValidationResult:
    """Create a standardized error result for unexpected validation failures."""
    return validator._create_result(
        rule_id="task_validation_error",
        rule_name="Task Validation Error",
        status=ValidationStatus.FAILED,
        severity=ValidationSeverity.CRITICAL,
        message=f"Task validation error: {error}",
        details={"error_type": type(error).__name__},
    )

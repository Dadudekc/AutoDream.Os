"""
Code Validation Reporting - Unified Validation Framework

Provides helper class for generating final validation results and handling
errors during validation.
"""

from typing import List

from .base_validator import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)


class ValidationReporter:
    """Handles reporting of overall validation status and errors"""

    def __init__(self, validator: BaseValidator) -> None:
        self.validator = validator

    def finalize(self, results: List[ValidationResult]) -> None:
        """Append a success result if no errors are present"""
        if not any(r.severity == ValidationSeverity.ERROR for r in results):
            success_result = self.validator._create_result(
                rule_id="overall_code_validation",
                rule_name="Overall Code Validation",
                status=ValidationStatus.PASSED,
                severity=ValidationSeverity.INFO,
                message="Code validation passed successfully",
                details={"total_checks": len(results)},
            )
            results.append(success_result)

    def report_error(self, exc: Exception) -> ValidationResult:
        """Create a result for an unexpected error"""
        return self.validator._create_result(
            rule_id="code_validation_error",
            rule_name="Code Validation Error",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.CRITICAL,
            message=f"Code validation error: {str(exc)}",
            details={"error_type": type(exc).__name__},
        )

"""Structure rule evaluation logic."""

from typing import Any, Dict, List

from .base_validator import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)


class StructureRuleEvaluator:
    """Evaluates structural aspects of code data."""

    def __init__(self, validator: BaseValidator) -> None:
        self.validator = validator

    def validate(self, code_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate the structure and format of the provided code data."""
        results: List[ValidationResult] = []

        if not isinstance(code_data, dict):
            result = self.validator._create_result(
                rule_id="code_type",
                rule_name="Code Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Code data must be a dictionary",
                actual_value=type(code_data).__name__,
                expected_value="dict",
            )
            results.append(result)
            return results

        if len(code_data) == 0:
            result = self.validator._create_result(
                rule_id="code_empty",
                rule_name="Code Empty Check",
                status=ValidationStatus.WARNING,
                severity=ValidationSeverity.WARNING,
                message="Code data is empty",
                actual_value=code_data,
                expected_value="non-empty code data",
            )
            results.append(result)

        return results

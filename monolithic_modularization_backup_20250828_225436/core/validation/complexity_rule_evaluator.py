"""Complexity rule evaluation logic."""

from typing import Any, Dict, List

from .base_validator import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)


class ComplexityRuleEvaluator:
    """Validates code complexity metrics."""

    def __init__(self, validator: BaseValidator, code_standards: Dict[str, float]) -> None:
        self.validator = validator
        self.code_standards = code_standards

    def validate(self, complexity: Any) -> List[ValidationResult]:
        results: List[ValidationResult] = []

        if not isinstance(complexity, dict):
            result = self.validator._create_result(
                rule_id="complexity_type",
                rule_name="Complexity Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Code complexity must be a dictionary",
                field_path="complexity",
                actual_value=type(complexity).__name__,
                expected_value="dict",
            )
            results.append(result)
            return results

        if "cyclomatic_complexity" in complexity:
            cc = complexity["cyclomatic_complexity"]
            if isinstance(cc, (int, float)) and cc > 10:
                result = self.validator._create_result(
                    rule_id="cyclomatic_complexity_high",
                    rule_name="Cyclomatic Complexity High",
                    status=ValidationStatus.WARNING,
                    severity=ValidationSeverity.WARNING,
                    message=f"Cyclomatic complexity is high: {cc}",
                    field_path="complexity.cyclomatic_complexity",
                    actual_value=cc,
                    expected_value="<= 10",
                )
                results.append(result)

        if "nesting_depth" in complexity:
            depth = complexity["nesting_depth"]
            if (
                isinstance(depth, (int, float))
                and depth > self.code_standards["max_nesting_depth"]
            ):
                result = self.validator._create_result(
                    rule_id="nesting_depth_exceeded",
                    rule_name="Nesting Depth Exceeded",
                    status=ValidationStatus.WARNING,
                    severity=ValidationSeverity.WARNING,
                    message=(
                        f"Nesting depth exceeds threshold: {depth} >"
                        f" {self.code_standards['max_nesting_depth']}"
                    ),
                    field_path="complexity.nesting_depth",
                    actual_value=depth,
                    expected_value=f"<= {self.code_standards['max_nesting_depth']}",
                )
                results.append(result)

        return results

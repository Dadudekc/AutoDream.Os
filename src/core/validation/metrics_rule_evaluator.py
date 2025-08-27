"""Metrics rule evaluation logic."""

from typing import Any, Dict, List

from .base_validator import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)


class MetricsRuleEvaluator:
    """Evaluates code metrics against predefined thresholds."""

    def __init__(self, validator: BaseValidator, code_standards: Dict[str, float]) -> None:
        self.validator = validator
        self.code_standards = code_standards

    def validate(self, metrics: Any) -> List[ValidationResult]:
        results: List[ValidationResult] = []

        if not isinstance(metrics, dict):
            result = self.validator._create_result(
                rule_id="metrics_type",
                rule_name="Metrics Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Code metrics must be a dictionary",
                field_path="metrics",
                actual_value=type(metrics).__name__,
                expected_value="dict",
            )
            results.append(result)
            return results

        for metric_name, metric_value in metrics.items():
            if metric_name in self.code_standards:
                threshold = self.code_standards[metric_name]
                if isinstance(metric_value, (int, float)) and metric_value > threshold:
                    result = self.validator._create_result(
                        rule_id=f"{metric_name}_exceeded",
                        rule_name=f"{metric_name.title()} Exceeded",
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.WARNING,
                        message=(
                            f"Code metric '{metric_name}' exceeds threshold:"
                            f" {metric_value} > {threshold}"
                        ),
                        field_path=f"metrics.{metric_name}",
                        actual_value=metric_value,
                        expected_value=f"<= {threshold}",
                    )
                    results.append(result)

        return results

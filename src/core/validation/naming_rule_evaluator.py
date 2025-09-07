"""Naming rule evaluation logic."""

import re
from typing import Any, Dict, List

from .base_validator import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)


class NamingRuleEvaluator:
    """Validates naming convention configurations."""

    def __init__(self, validator: BaseValidator) -> None:
        self.validator = validator

    def validate(self, naming: Any) -> List[ValidationResult]:
        results: List[ValidationResult] = []

        if not isinstance(naming, dict):
            result = self.validator._create_result(
                rule_id="naming_type",
                rule_name="Naming Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Naming conventions must be a dictionary",
                field_path="naming",
                actual_value=type(naming).__name__,
                expected_value="dict",
            )
            results.append(result)
            return results

        if "patterns" in naming:
            patterns = naming["patterns"]
            if isinstance(patterns, dict):
                for pattern_name, pattern in patterns.items():
                    if isinstance(pattern, str):
                        try:
                            re.compile(pattern)
                        except re.error:
                            result = self.validator._create_result(
                                rule_id="naming_pattern_invalid",
                                rule_name="Naming Pattern Invalid",
                                status=ValidationStatus.FAILED,
                                severity=ValidationSeverity.ERROR,
                                message=(
                                    f"Invalid naming pattern '{pattern_name}': {pattern}"
                                ),
                                field_path=f"naming.patterns.{pattern_name}",
                                actual_value=pattern,
                                expected_value="valid regex pattern",
                            )
                            results.append(result)

        return results

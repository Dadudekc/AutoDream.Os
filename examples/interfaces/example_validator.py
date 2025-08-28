"""Example BaseValidator implementation."""

from typing import Any, List

from src.core.validation.base_validator import BaseValidator, ValidationResult


class AlwaysPassValidator(BaseValidator):
    """Validator that always passes for demonstration purposes."""

    def _setup_default_rules(self) -> None:  # pragma: no cover - example
        self.validation_rules.clear()

    def validate(self, data: Any, **kwargs) -> List[ValidationResult]:
        return [ValidationResult(rule_id="always_pass", passed=True, message="ok")]

"""Execution engine for running validations using registered validators."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from .rule_registry import RuleRegistry
from .models import ValidationResult, ValidationSeverity, ValidationStatus


class ValidationExecutor:
    """Run validation checks using validators stored in a registry."""

    def __init__(self, registry: RuleRegistry) -> None:
        self.registry = registry
        self.logger = logging.getLogger(f"{__name__}.ValidationExecutor")
        self.history: List[ValidationResult] = []

    # ------------------------------------------------------------------
    def validate_with_validator(self, name: str, data: Any, **kwargs) -> List[ValidationResult]:
        """Run a specific validator by name."""
        validator = self.registry.get(name)
        if not validator:
            result = ValidationResult(
                rule_id="validator_not_found",
                rule_name="Validator Not Found",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Validator '{name}' not found",
                details={"available_validators": self.registry.list()},
            )
            self.history.append(result)
            return [result]

        results = validator.validate(data, **kwargs)
        self.history.extend(results)
        if len(self.history) > 10000:
            self.history = self.history[-10000:]
        return results

    # ------------------------------------------------------------------
    def validate_all(self, data: Dict[str, Any], **kwargs) -> Dict[str, List[ValidationResult]]:
        """Run all registered validators and return their results."""
        results: Dict[str, List[ValidationResult]] = {}
        for name in self.registry.list():
            validator = self.registry.get(name)
            if not validator:
                continue
            validator_results = validator.validate(data, **kwargs)
            results[name] = validator_results
            self.history.extend(validator_results)
        if len(self.history) > 10000:
            self.history = self.history[-10000:]
        return results

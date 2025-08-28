"""Base Validator - Unified Validation Framework.

This module provides the abstract base class and common structures for all
validators in the unified validation system. Rule definitions are now loaded
from external YAML configuration files located in ``rules/``.
"""

import logging
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .models import (
    ValidationRule,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)


class BaseValidator(ABC):
    """Abstract base class for all validators in the unified framework"""

    def __init__(self, validator_name: str):
        """Initialize base validator"""
        self.validator_name = validator_name
        self.logger = logging.getLogger(f"{__name__}.{validator_name}")
        self.validation_rules: Dict[str, ValidationRule] = {}
        self.validation_history: List[ValidationResult] = []
        self._config: Dict[str, Any] = self._load_rules_from_file()

    def _load_rules_from_file(self) -> Dict[str, Any]:
        """Load validator rules from external YAML configuration."""
        try:
            base_name = re.sub(r"Validator$", "", self.validator_name)
            file_name = re.sub(r"(?<!^)(?=[A-Z])", "_", base_name).lower() + ".yaml"
            config_path = Path(__file__).resolve().parent / "rules" / file_name
            if not config_path.exists():
                return {}
            with config_path.open("r", encoding="utf-8") as f:
                data: Dict[str, Any] = yaml.safe_load(f) or {}
            for rule in data.get("rules", []):
                severity_str = rule.get("severity", "ERROR").upper()
                try:
                    severity = ValidationSeverity[severity_str]
                except KeyError:
                    severity = ValidationSeverity.ERROR
                self.add_validation_rule(
                    ValidationRule(
                        rule_id=rule["rule_id"],
                        rule_name=rule["rule_name"],
                        rule_type=rule.get("rule_type", base_name.lower()),
                        description=rule.get("description", ""),
                        severity=severity,
                    )
                )
            return data
        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to load rules: {e}")
            return {}

    @abstractmethod
    def validate(self, data: Any, **kwargs) -> List[ValidationResult]:
        """Main validation method.

        Subclasses must implement this method and return a list of
        :class:`ValidationResult` objects describing each validation check
        performed.

        Returns:
            List[ValidationResult]: Validation results generated for the
            provided data.
        """
        raise NotImplementedError("Subclasses must implement validate")

    def add_validation_rule(self, rule: ValidationRule) -> bool:
        """Add a new validation rule"""
        try:
            self.validation_rules[rule.rule_id] = rule
            self.logger.info(f"Validation rule added: {rule.rule_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add validation rule: {e}")
            return False

    def remove_validation_rule(self, rule_id: str) -> bool:
        """Remove a validation rule"""
        try:
            if rule_id in self.validation_rules:
                del self.validation_rules[rule_id]
                self.logger.info(f"Validation rule removed: {rule_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove validation rule: {e}")
            return False

    def get_validation_rules(self) -> Dict[str, ValidationRule]:
        """Get all validation rules"""
        return self.validation_rules.copy()

    def get_validation_history(self, limit: int = 100) -> List[ValidationResult]:
        """Get validation history with optional limit"""
        return (
            self.validation_history[-limit:]
            if limit > 0
            else self.validation_history.copy()
        )

    def clear_validation_history(self) -> None:
        """Clear validation history"""
        self.validation_history.clear()
        self.logger.info("Validation history cleared")

    def _create_result(
        self,
        rule_id: str,
        rule_name: str,
        status: ValidationStatus,
        severity: ValidationSeverity,
        message: str,
        **kwargs,
    ) -> ValidationResult:
        """Create a standardized validation result"""
        result = ValidationResult(
            rule_id=rule_id,
            rule_name=rule_name,
            status=status,
            severity=severity,
            message=message,
            **kwargs,
        )

        # Store in history
        self.validation_history.append(result)

        # Keep history manageable
        if len(self.validation_history) > 1000:
            self.validation_history = self.validation_history[-1000:]

        return result

    def _validate_required_fields(
        self, data: Dict[str, Any], required_fields: List[str]
    ) -> List[ValidationResult]:
        """Validate that required fields are present and non-empty"""
        results = []

        for field_name in required_fields:
            if field_name not in data or not data[field_name]:
                result = self._create_result(
                    rule_id=f"required_field_{field_name}",
                    rule_name=f"Required Field: {field_name}",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Required field '{field_name}' is missing or empty",
                    field_path=field_name,
                    actual_value=data.get(field_name),
                    expected_value="non-empty value",
                )
                results.append(result)

        return results

    def _validate_field_type(
        self,
        field_name: str,
        field_value: Any,
        expected_type: type,
        rule_id: str = None,
    ) -> Optional[ValidationResult]:
        """Validate field type"""
        if not isinstance(field_value, expected_type):
            return self._create_result(
                rule_id=rule_id or f"type_check_{field_name}",
                rule_name=f"Type Check: {field_name}",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Field '{field_name}' must be of type {expected_type.__name__}",
                field_path=field_name,
                actual_value=type(field_value).__name__,
                expected_value=expected_type.__name__,
            )
        return None

    def _validate_field_range(
        self,
        field_name: str,
        field_value: float,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        rule_id: str = None,
    ) -> Optional[ValidationResult]:
        """Validate numeric field range"""
        if min_value is not None and field_value < min_value:
            return self._create_result(
                rule_id=rule_id or f"range_check_{field_name}",
                rule_name=f"Range Check: {field_name}",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Field '{field_name}' must be >= {min_value}",
                field_path=field_name,
                actual_value=field_value,
                expected_value=f">= {min_value}",
            )

        if max_value is not None and field_value > max_value:
            return self._create_result(
                rule_id=rule_id or f"range_check_{field_name}",
                rule_name=f"Range Check: {field_name}",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Field '{field_name}' must be <= {max_value}",
                field_path=field_name,
                actual_value=field_value,
                expected_value=f"<= {max_value}",
            )

        return None

    def get_validation_summary(self) -> Dict[str, Any]:
        """Get validation summary statistics"""
        if not self.validation_history:
            return {
                "total_validations": 0,
                "passed": 0,
                "failed": 0,
                "warnings": 0,
                "success_rate": 0.0,
            }

        total = len(self.validation_history)
        passed = sum(
            1 for r in self.validation_history if r.status == ValidationStatus.PASSED
        )
        failed = sum(
            1 for r in self.validation_history if r.status == ValidationStatus.FAILED
        )
        warnings = sum(
            1 for r in self.validation_history if r.status == ValidationStatus.WARNING
        )

        return {
            "total_validations": total,
            "passed": passed,
            "failed": failed,
            "warnings": warnings,
            "success_rate": (passed / total) * 100 if total > 0 else 0.0,
        }

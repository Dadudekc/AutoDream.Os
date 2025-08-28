"""
Base Validator - Unified Validation Framework

This module provides the abstract base class and common structures for all validators
in the unified validation system. Follows V2 coding standards and SRP principles.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class ValidationSeverity(Enum):
    """Validation severity levels"""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidationStatus(Enum):
    """Validation result status"""

    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    PENDING = "pending"


@dataclass
class ValidationRule:
    """Configurable validation rule"""

    rule_id: str
    rule_name: str
    rule_type: str
    description: str
    severity: ValidationSeverity = ValidationSeverity.ERROR
    threshold: Optional[float] = None
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Standardized validation result"""

    rule_id: str
    rule_name: str
    status: ValidationStatus
    severity: ValidationSeverity
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    field_path: Optional[str] = None
    actual_value: Optional[Any] = None
    expected_value: Optional[Any] = None


class BaseValidator(ABC):
    """Abstract base class for all validators in the unified framework"""

    def __init__(self, validator_name: str):
        """Initialize base validator"""
        self.validator_name = validator_name
        self.logger = logging.getLogger(f"{__name__}.{validator_name}")
        self.validation_rules: Dict[str, ValidationRule] = {}
        self.validation_history: List[ValidationResult] = []
        self._setup_default_rules()

    @abstractmethod
    def _setup_default_rules(self) -> None:
        """Set up default validation rules for this validator type."""
        raise NotImplementedError(
            "_setup_default_rules must be implemented by subclasses"
        )

    @abstractmethod
    def validate(self, data: Any, **kwargs) -> List[ValidationResult]:
        """Validate the given data.

        Args:
            data (Any): Data to validate.
            **kwargs: Additional validation parameters.

        Returns:
            List[ValidationResult]: Collection of validation results.
        """
        raise NotImplementedError("validate must be implemented by subclasses")

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

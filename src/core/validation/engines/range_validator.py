#!/usr/bin/env python3
"""
Range Validator - Handles string length and numeric range validation.

Author: Agent-6 (Coordination & Communication Specialist)
Mission: V2 Compliance - Modular Architecture
Status: REFACTORED - Clean separation of concerns
"""

from typing import Any, Dict, Union

from ..models.validation_models import ValidationResult, ValidationType, ValidationSeverity
from .base_validator import BaseValidator


class RangeValidator(BaseValidator):
    """Validator for range-based validation (string length, numeric ranges)."""
    
    def validate(self, value: Any, **kwargs) -> ValidationResult:
        """Validate range-based constraints."""
        validation_type = kwargs.get('validation_type')
        
        if validation_type == ValidationType.STRING_LENGTH:
            min_length = kwargs.get('min_length', 0)
            max_length = kwargs.get('max_length', 1000)
            return self._validate_string_length(value, min_length, max_length)
        elif validation_type == ValidationType.NUMERIC_RANGE:
            min_value = kwargs.get('min_value', 0)
            max_value = kwargs.get('max_value', 999999)
            return self._validate_numeric_range(value, min_value, max_value)
        else:
            return ValidationResult(
                is_valid=False,
                errors=[f"Unsupported validation type: {validation_type}"],
                severity=ValidationSeverity.HIGH,
                validation_type=validation_type
            )
    
    def _validate_string_length(self, value: str, min_length: int, max_length: int) -> ValidationResult:
        """Validate string length constraints."""
        if not isinstance(value, str):
            return ValidationResult(
                is_valid=False,
                errors=["Value must be a string"],
                severity=ValidationSeverity.HIGH,
                validation_type=ValidationType.STRING_LENGTH
            )
        
        length = len(value)
        errors = []
        
        if length < min_length:
            errors.append(f"String too short: {length} < {min_length}")
        if length > max_length:
            errors.append(f"String too long: {length} > {max_length}")
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            severity=ValidationSeverity.MEDIUM,
            validation_type=ValidationType.STRING_LENGTH,
            details={"length": length, "min_length": min_length, "max_length": max_length}
        )
    
    def _validate_numeric_range(self, value: Union[int, float], min_value: float, max_value: float) -> ValidationResult:
        """Validate numeric range constraints."""
        if not isinstance(value, (int, float)):
            return ValidationResult(
                is_valid=False,
                errors=["Value must be numeric"],
                severity=ValidationSeverity.HIGH,
                validation_type=ValidationType.NUMERIC_RANGE
            )
        
        errors = []
        
        if value < min_value:
            errors.append(f"Value too small: {value} < {min_value}")
        if value > max_value:
            errors.append(f"Value too large: {value} > {max_value}")
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            severity=ValidationSeverity.MEDIUM,
            validation_type=ValidationType.NUMERIC_RANGE,
            details={"value": value, "min_value": min_value, "max_value": max_value}
        )
    
    def validate_string_length(self, value: str, min_length: int = 0, max_length: int = 1000) -> ValidationResult:
        """Validate string length - convenience method."""
        return self._validate_string_length(value, min_length, max_length)
    
    def validate_numeric_range(self, value: Union[int, float], min_value: float = 0, max_value: float = 999999) -> ValidationResult:
        """Validate numeric range - convenience method."""
        return self._validate_numeric_range(value, min_value, max_value)

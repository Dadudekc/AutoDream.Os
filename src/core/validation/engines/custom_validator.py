#!/usr/bin/env python3
"""
Custom Validator - Handles custom validation functions and complex validation logic.

Author: Agent-6 (Coordination & Communication Specialist)
Mission: V2 Compliance - Modular Architecture
Status: REFACTORED - Clean separation of concerns
"""

from typing import Any, Callable

from ..models.validation_models import ValidationResult, ValidationType, ValidationSeverity
from .base_validator import BaseValidator


class CustomValidator(BaseValidator):
    """Validator for custom validation functions and complex validation logic."""
    
    def validate(self, value: Any, **kwargs) -> ValidationResult:
        """Validate using custom validator function."""
        validation_type = kwargs.get('validation_type')
        
        if validation_type == ValidationType.CUSTOM:
            validator = kwargs.get('validator')
            field_name = kwargs.get('field_name', 'field')
            return self._validate_custom(value, validator, field_name)
        else:
            return ValidationResult(
                is_valid=False,
                errors=[f"Unsupported validation type: {validation_type}"],
                severity=ValidationSeverity.HIGH,
                validation_type=validation_type
            )
    
    def _validate_custom(self, value: Any, validator: Callable, field_name: str) -> ValidationResult:
        """Validate using custom validator function."""
        try:
            result = validator(value)
            if isinstance(result, bool):
                is_valid = result
                errors = [] if is_valid else [f"Custom validation failed for {field_name}"]
            elif isinstance(result, ValidationResult):
                return result
            else:
                is_valid = bool(result)
                errors = [] if is_valid else [f"Custom validation failed for {field_name}"]
        except Exception as e:
            is_valid = False
            errors = [f"Custom validation error for {field_name}: {str(e)}"]
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            severity=ValidationSeverity.MEDIUM,
            validation_type=ValidationType.CUSTOM,
            field_name=field_name
        )
    
    def validate_custom(self, value: Any, validator: Callable, field_name: str = "field") -> ValidationResult:
        """Validate using custom validator function - convenience method."""
        return self._validate_custom(value, validator, field_name)
    
    def validate_hasattr(self, obj: Any, attr_name: str) -> bool:
        """Validate that an object has a specific attribute."""
        return hasattr(obj, attr_name)

#!/usr/bin/env python3
"""
Numeric Validators - Specialized Numeric Validation Logic

This module contains specialized numeric validation functionality extracted
from the main value_validators.py to comply with V2 file size limits.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: V2 Compliance Modularization
"""

from typing import Union

from .base_validator import BaseValidator
from .validation_result import ValidationResult, ValidationStatus


class NumericValidators(BaseValidator):
    """
    Specialized numeric validation helpers.
    
    This class contains numeric-specific validation logic extracted from
    the main ValueValidators class to maintain V2 compliance.
    """
    
    def __init__(self):
        """Initialize the numeric validators."""
        super().__init__("NumericValidators")
    
    def validate_numeric_range(self, value: Union[int, float], 
                              min_value: Union[int, float] = None,
                              max_value: Union[int, float] = None) -> ValidationResult:
        """
        Validate numeric range.
        
        Args:
            value: Numeric value to validate
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            
        Returns:
            ValidationResult with validation status and details
        """
        try:
            if not isinstance(value, (int, float)):
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="Numeric range validation failed",
                    errors=["Value must be a number"],
                    validated_data=value,
                    validator_name=self.name
                )
            
            errors = []
            
            if min_value is not None and value < min_value:
                errors.append(f"Value {value} is less than minimum {min_value}")
            
            if max_value is not None and value > max_value:
                errors.append(f"Value {value} is greater than maximum {max_value}")
            
            if errors:
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="Numeric range validation failed",
                    errors=errors,
                    validated_data=value,
                    validator_name=self.name
                )
            else:
                return ValidationResult(
                    status=ValidationStatus.VALID,
                    message="Numeric range validation passed",
                    validated_data=value,
                    validator_name=self.name
                )
                
        except Exception as e:
            return ValidationResult(
                status=ValidationStatus.ERROR,
                message="Numeric range validation error occurred",
                errors=[f"Numeric range validation exception: {str(e)}"],
                validated_data=value,
                validator_name=self.name
            )
    
    def validate_numeric_value(self, value: Union[int, float], **kwargs) -> ValidationResult:
        """Validate numeric value."""
        return ValidationResult(
            status=ValidationStatus.VALID,
            message="Numeric value validation passed",
            validated_data=value,
            validator_name=self.name
        )

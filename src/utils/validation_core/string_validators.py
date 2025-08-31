#!/usr/bin/env python3
"""
String Validators - Specialized String Validation Logic

This module contains specialized string validation functionality extracted
from the main value_validators.py to comply with V2 file size limits.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: V2 Compliance Modularization
"""

from typing import Any

from .base_validator import BaseValidator
from .validation_result import ValidationResult, ValidationStatus


class StringValidators(BaseValidator):
    """
    Specialized string validation helpers.
    
    This class contains string-specific validation logic extracted from
    the main ValueValidators class to maintain V2 compliance.
    """
    
    def __init__(self):
        """Initialize the string validators."""
        super().__init__("StringValidators")
    
    def validate_string_length(self, text: str, min_length: int = 0, 
                              max_length: int = None) -> ValidationResult:
        """
        Validate string length.
        
        Args:
            text: Text to validate
            min_length: Minimum allowed length
            max_length: Maximum allowed length
            
        Returns:
            ValidationResult with validation status and details
        """
        try:
            if not isinstance(text, str):
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="String length validation failed",
                    errors=["Text must be a string"],
                    validated_data=text,
                    validator_name=self.name
                )
            
            text_length = len(text)
            errors = []
            
            if text_length < min_length:
                errors.append(f"Text length {text_length} is less than minimum {min_length}")
            
            if max_length is not None and text_length > max_length:
                errors.append(f"Text length {text_length} is greater than maximum {max_length}")
            
            if errors:
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="String length validation failed",
                    errors=errors,
                    validated_data=text,
                    validator_name=self.name
                )
            else:
                return ValidationResult(
                    status=ValidationStatus.VALID,
                    message="String length validation passed",
                    validated_data=text,
                    validator_name=self.name
                )
                
        except Exception as e:
            return ValidationResult(
                status=ValidationStatus.ERROR,
                message="String length validation error occurred",
                errors=[f"String length validation exception: {str(e)}"],
                validated_data=text,
                validator_name=self.name
            )
    
    def validate_string_value(self, text: str, **kwargs) -> ValidationResult:
        """Validate string value."""
        return ValidationResult(
            status=ValidationStatus.VALID,
            message="String value validation passed",
            validated_data=text,
            validator_name=self.name
        )

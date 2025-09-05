#!/usr/bin/env python3
"""
Format Validator - Handles email, URL, and regex pattern validation.

Author: Agent-6 (Coordination & Communication Specialist)
Mission: V2 Compliance - Modular Architecture
Status: REFACTORED - Clean separation of concerns
"""

import re
from typing import Any, Dict

from ..models.validation_models import ValidationResult, ValidationType, ValidationSeverity
from .base_validator import BaseValidator


class FormatValidator(BaseValidator):
    """Validator for format-based validation (email, URL, regex patterns)."""
    
    def __init__(self):
        """Initialize format validator with compiled patterns."""
        super().__init__()
        self._patterns = {
            "email": re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
            "url": re.compile(r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'),
            "phone": re.compile(r'^\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$'),
            "uuid": re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE),
            "alphanumeric": re.compile(r'^[a-zA-Z0-9]+$'),
            "numeric": re.compile(r'^[0-9]+$'),
            "alpha": re.compile(r'^[a-zA-Z]+$')
        }
    
    def validate(self, value: Any, **kwargs) -> ValidationResult:
        """Validate format-based patterns."""
        validation_type = kwargs.get('validation_type')
        
        if validation_type == ValidationType.EMAIL:
            return self._validate_email(value)
        elif validation_type == ValidationType.URL:
            return self._validate_url(value)
        elif validation_type == ValidationType.REGEX_PATTERN:
            pattern_name = kwargs.get('pattern_name', 'alphanumeric')
            return self._validate_regex_pattern(value, pattern_name)
        else:
            return ValidationResult(
                is_valid=False,
                errors=[f"Unsupported validation type: {validation_type}"],
                severity=ValidationSeverity.HIGH,
                validation_type=validation_type
            )
    
    def _validate_email(self, email: str) -> ValidationResult:
        """Validate email format."""
        if not email:
            return ValidationResult(
                is_valid=False,
                errors=["Email is required"],
                severity=ValidationSeverity.HIGH,
                validation_type=ValidationType.EMAIL
            )
        
        is_valid = bool(self._patterns["email"].match(email))
        errors = ["Invalid email format"] if not is_valid else []
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            severity=ValidationSeverity.MEDIUM,
            validation_type=ValidationType.EMAIL
        )
    
    def _validate_url(self, url: str) -> ValidationResult:
        """Validate URL format."""
        if not url:
            return ValidationResult(
                is_valid=False,
                errors=["URL is required"],
                severity=ValidationSeverity.HIGH,
                validation_type=ValidationType.URL
            )
        
        is_valid = bool(self._patterns["url"].match(url))
        errors = ["Invalid URL format"] if not is_valid else []
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            severity=ValidationSeverity.MEDIUM,
            validation_type=ValidationType.URL
        )
    
    def _validate_regex_pattern(self, value: str, pattern_name: str) -> ValidationResult:
        """Validate regex pattern."""
        if not isinstance(value, str):
            return ValidationResult(
                is_valid=False,
                errors=["Value must be a string"],
                severity=ValidationSeverity.HIGH,
                validation_type=ValidationType.REGEX_PATTERN
            )
        
        if pattern_name not in self._patterns:
            return ValidationResult(
                is_valid=False,
                errors=[f"Unknown pattern: {pattern_name}"],
                severity=ValidationSeverity.HIGH,
                validation_type=ValidationType.REGEX_PATTERN
            )
        
        is_valid = bool(self._patterns[pattern_name].match(value))
        errors = [f"Value does not match pattern: {pattern_name}"] if not is_valid else []
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            severity=ValidationSeverity.MEDIUM,
            validation_type=ValidationType.REGEX_PATTERN,
            details={"pattern_name": pattern_name}
        )
    
    def validate_email(self, email: str) -> ValidationResult:
        """Validate email format - convenience method."""
        return self._validate_email(email)
    
    def validate_url(self, url: str) -> ValidationResult:
        """Validate URL format - convenience method."""
        return self._validate_url(url)
    
    def validate_regex_pattern(self, value: str, pattern_name: str) -> ValidationResult:
        """Validate regex pattern - convenience method."""
        return self._validate_regex_pattern(value, pattern_name)

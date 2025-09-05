#!/usr/bin/env python3
"""
Validation Utilities - Helper functions and utilities for validation system.

Author: Agent-6 (Coordination & Communication Specialist)
Mission: V2 Compliance - Modular Architecture
Status: REFACTORED - Clean separation of concerns
"""

from typing import Any, Dict, List, Union, Callable

from ..models.validation_models import ValidationResult, ValidationType, ValidationSeverity
from ..validation_coordinator import ValidationCoordinator


# Global validation instance for backward compatibility
_validation_coordinator = None


def get_validation_coordinator() -> ValidationCoordinator:
    """Get global validation coordinator instance."""
    global _validation_coordinator
    if _validation_coordinator is None:
        _validation_coordinator = ValidationCoordinator()
    return _validation_coordinator


# Convenience functions for backward compatibility
def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> ValidationResult:
    """Validate required fields."""
    return get_validation_coordinator().validate_required_fields(data, required_fields)


def validate_data_types(data: Dict[str, Any], type_requirements: Dict[str, type]) -> ValidationResult:
    """Validate data types."""
    return get_validation_coordinator().validate_data_types(data, type_requirements)


def validate_email(email: str) -> ValidationResult:
    """Validate email format."""
    return get_validation_coordinator().validate_email(email)


def validate_url(url: str) -> ValidationResult:
    """Validate URL format."""
    return get_validation_coordinator().validate_url(url)


def validate_string_length(value: str, min_length: int = 0, max_length: int = 1000) -> ValidationResult:
    """Validate string length."""
    return get_validation_coordinator().validate_string_length(value, min_length, max_length)


def validate_numeric_range(value: Union[int, float], min_value: float = 0, max_value: float = 999999) -> ValidationResult:
    """Validate numeric range."""
    return get_validation_coordinator().validate_numeric_range(value, min_value, max_value)


def validate_regex_pattern(value: str, pattern_name: str) -> ValidationResult:
    """Validate regex pattern."""
    return get_validation_coordinator().validate_regex_pattern(value, pattern_name)


def validate_custom(value: Any, validator: Callable, field_name: str = "field") -> ValidationResult:
    """Validate using custom validator function."""
    return get_validation_coordinator().validate_custom(value, validator, field_name)

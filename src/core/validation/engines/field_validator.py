#!/usr/bin/env python3
"""
Field Validator - Handles required fields and data type validation.

Author: Agent-6 (Coordination & Communication Specialist)
Mission: V2 Compliance - Modular Architecture
Status: REFACTORED - Clean separation of concerns
"""

from typing import Any, Dict, List, Type

from ..models.validation_models import ValidationResult, ValidationType, ValidationSeverity
from .base_validator import BaseValidator


class FieldValidator(BaseValidator):
    """Validator for field requirements and data types."""
    
    def validate(self, value: Any, **kwargs) -> ValidationResult:
        """Validate field requirements and data types."""
        validation_type = kwargs.get('validation_type')
        
        if validation_type == ValidationType.REQUIRED_FIELDS:
            return self._validate_required(value, **kwargs)
        elif validation_type == ValidationType.DATA_TYPES:
            return self._validate_data_types(value, **kwargs)
        else:
            return ValidationResult(
                is_valid=False,
                errors=[f"Unsupported validation type: {validation_type}"],
                severity=ValidationSeverity.HIGH,
                validation_type=validation_type
            )
    
    def _validate_required(self, value: Any, **kwargs) -> ValidationResult:
        """Validate that a value is not None or empty."""
        is_valid = value is not None and value != "" and value != []
        errors = [] if is_valid else ["Value is required"]
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            severity=ValidationSeverity.HIGH,
            validation_type=ValidationType.REQUIRED_FIELDS
        )
    
    def _validate_data_types(self, value: Any, **kwargs) -> ValidationResult:
        """Validate data types."""
        expected_type = kwargs.get('expected_type', str)
        
        if not isinstance(value, expected_type):
            return ValidationResult(
                is_valid=False,
                errors=[f"Invalid type: expected {expected_type.__name__}, got {type(value).__name__}"],
                severity=ValidationSeverity.MEDIUM,
                validation_type=ValidationType.DATA_TYPES
            )
        
        return ValidationResult(
            is_valid=True,
            validation_type=ValidationType.DATA_TYPES
        )
    
    def validate_required_fields(self, data: Dict[str, Any], required_fields: List[str]) -> ValidationResult:
        """Validate required fields in a data dictionary."""
        missing_fields = []
        
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == "":
                missing_fields.append(field)
        
        is_valid = len(missing_fields) == 0
        errors = [f"Required field missing: {field}" for field in missing_fields] if missing_fields else []
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            severity=ValidationSeverity.HIGH,
            validation_type=ValidationType.REQUIRED_FIELDS,
            details={"missing_fields": missing_fields}
        )
    
    def validate_data_types(self, data: Dict[str, Any], type_requirements: Dict[str, Type]) -> ValidationResult:
        """Validate data types in a data dictionary."""
        invalid_fields = []
        
        for field, expected_type in type_requirements.items():
            if field in data and not isinstance(data[field], expected_type):
                invalid_fields.append(field)
        
        is_valid = len(invalid_fields) == 0
        errors = [f"Invalid type for field '{field}': expected {type_requirements[field].__name__}" 
                 for field in invalid_fields] if invalid_fields else []
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            severity=ValidationSeverity.MEDIUM,
            validation_type=ValidationType.DATA_TYPES,
            details={"invalid_fields": invalid_fields}
        )

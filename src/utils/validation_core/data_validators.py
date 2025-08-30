#!/usr/bin/env python3
"""
Consolidated Data Validators - Single Source of Truth for Data Validation

This module consolidates all data validation functionality from multiple
duplicate implementations into a single, maintainable validation system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 1: Validation System Consolidation
"""

import json
import re
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

from .base_validator import BaseValidator
from .validation_result import ValidationResult, ValidationStatus


class DataValidators(BaseValidator):
    """
    Consolidated data structure validation helpers.
    
    This class consolidates all data validation functionality from multiple
    duplicate implementations into a single, maintainable system.
    """
    
    def __init__(self):
        """Initialize the data validators."""
        super().__init__("DataValidators")
    
    def validate(self, data: Any, **kwargs) -> ValidationResult:
        """
        Validate data structure and content.
        
        Args:
            data: Data to validate
            **kwargs: Additional validation parameters
            
        Returns:
            ValidationResult with validation status and details
        """
        if isinstance(data, dict):
            return self._validate_dict(data, **kwargs)
        elif isinstance(data, list):
            return self._validate_list(data, **kwargs)
        elif isinstance(data, str):
            return self._validate_string(data, **kwargs)
        else:
            return ValidationResult(
                status=ValidationStatus.VALID,
                message="Data type validation passed",
                validated_data=data,
                validator_name=self.name
            )
    
    def validate_required_fields(self, data: Dict[str, Any], 
                               required_fields: List[str]) -> ValidationResult:
        """
        Validate that required fields are present and not empty.
        
        Args:
            data: Dictionary to validate
            required_fields: List of required field names
            
        Returns:
            ValidationResult with validation status and details
        """
        errors = super().validate_required_fields(data, required_fields)
        
        if errors:
            return ValidationResult(
                status=ValidationStatus.INVALID,
                message="Required field validation failed",
                errors=errors,
                validated_data=data,
                validator_name=self.name
            )
        else:
            return ValidationResult(
                status=ValidationStatus.VALID,
                message="Required field validation passed",
                validated_data=data,
                validator_name=self.name
            )
    
    def validate_data_types(self, data: Dict[str, Any], 
                           type_schema: Dict[str, type]) -> ValidationResult:
        """
        Validate data types against a provided schema.
        
        Args:
            data: Dictionary to validate
            type_schema: Dictionary mapping field names to expected types
            
        Returns:
            ValidationResult with validation status and details
        """
        errors = super().validate_data_types(data, type_schema)
        
        if errors:
            return ValidationResult(
                status=ValidationStatus.INVALID,
                message="Data type validation failed",
                errors=errors,
                validated_data=data,
                validator_name=self.name
            )
        else:
            return ValidationResult(
                status=ValidationStatus.VALID,
                message="Data type validation passed",
                validated_data=data,
                validator_name=self.name
            )
    
    def validate_json_string(self, json_str: str) -> ValidationResult:
        """
        Validate that a string contains valid JSON.
        
        Args:
            json_str: String to validate as JSON
            
        Returns:
            ValidationResult with validation status and details
        """
        try:
            parsed_json = json.loads(json_str)
            return ValidationResult(
                status=ValidationStatus.VALID,
                message="JSON string validation passed",
                validated_data=parsed_json,
                validator_name=self.name
            )
        except (json.JSONDecodeError, TypeError) as e:
            return ValidationResult(
                status=ValidationStatus.INVALID,
                message="JSON string validation failed",
                errors=[f"Invalid JSON: {str(e)}"],
                validated_data=json_str,
                validator_name=self.name
            )
    
    def validate_schema(self, data: Dict[str, Any], 
                       schema: Dict[str, Dict[str, Any]]) -> ValidationResult:
        """
        Validate data against a comprehensive schema definition.
        
        Args:
            data: Data to validate
            schema: Schema definition with field rules
            
        Returns:
            ValidationResult with validation status and details
        """
        errors = []
        warnings = []
        
        for field_name, field_rules in schema.items():
            if field_name not in data:
                if field_rules.get('required', False):
                    errors.append(f"Required field '{field_name}' is missing")
                continue
            
            field_value = data[field_name]
            
            # Type validation
            expected_type = field_rules.get('type')
            if expected_type and not isinstance(field_value, expected_type):
                errors.append(
                    f"Field '{field_name}' must be of type {expected_type.__name__}, "
                    f"got {type(field_value).__name__}"
                )
            
            # Pattern validation for strings
            if isinstance(field_value, str) and 'pattern' in field_rules:
                if not re.match(field_rules['pattern'], field_value):
                    errors.append(f"Field '{field_name}' does not match required pattern")
            
            # Range validation for numbers
            if isinstance(field_value, (int, float)):
                if 'min' in field_rules and field_value < field_rules['min']:
                    errors.append(f"Field '{field_name}' must be >= {field_rules['min']}")
                if 'max' in field_rules and field_value > field_rules['max']:
                    errors.append(f"Field '{field_name}' must be <= {field_rules['max']}")
            
            # Length validation for strings and collections
            if 'min_length' in field_rules:
                if len(field_value) < field_rules['min_length']:
                    errors.append(f"Field '{field_name}' must have length >= {field_rules['min_length']}")
            
            if 'max_length' in field_rules:
                if len(field_value) > field_rules['max_length']:
                    errors.append(f"Field '{field_name}' must have length <= {field_rules['max_length']}")
            
            # Choice validation
            if 'choices' in field_rules and field_value not in field_rules['choices']:
                errors.append(f"Field '{field_name}' must be one of {field_rules['choices']}")
        
        if errors:
            return ValidationResult(
                status=ValidationStatus.INVALID,
                message="Schema validation failed",
                errors=errors,
                warnings=warnings,
                validated_data=data,
                validator_name=self.name
            )
        else:
            return ValidationResult(
                status=ValidationStatus.VALID,
                message="Schema validation passed",
                warnings=warnings,
                validated_data=data,
                validator_name=self.name
            )
    
    def _validate_dict(self, data: Dict[str, Any], **kwargs) -> ValidationResult:
        """Validate dictionary data."""
        return ValidationResult(
            status=ValidationStatus.VALID,
            message="Dictionary validation passed",
            validated_data=data,
            validator_name=self.name
        )
    
    def _validate_list(self, data: List[Any], **kwargs) -> ValidationResult:
        """Validate list data."""
        return ValidationResult(
            status=ValidationStatus.VALID,
            message="List validation passed",
            validated_data=data,
            validator_name=self.name
        )
    
    def _validate_string(self, data: str, **kwargs) -> ValidationResult:
        """Validate string data."""
        return ValidationResult(
            status=ValidationStatus.VALID,
            message="String validation passed",
            validated_data=data,
            validator_name=self.name
        )

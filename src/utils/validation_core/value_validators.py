#!/usr/bin/env python3
"""
Consolidated Value Validators - Single Source of Truth for Value Validation

This module consolidates all value validation functionality from multiple
duplicate implementations into a single, maintainable validation system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: V2 Compliance Modularization
"""

from typing import Any, List, Optional, Union
from datetime import datetime, date

from .base_validator import BaseValidator
from .validation_result import ValidationResult, ValidationStatus
from .string_validators import StringValidators
from .numeric_validators import NumericValidators
from .collection_validators import CollectionValidators
from .date_validators import DateValidators


class ValueValidators(BaseValidator):
    """
    Consolidated value validation helpers.
    
    This class consolidates all value validation functionality from multiple
    duplicate implementations into a single, maintainable system.
    """
    
    def __init__(self):
        """Initialize the value validators."""
        super().__init__("ValueValidators")
        self.string_validators = StringValidators()
        self.numeric_validators = NumericValidators()
        self.collection_validators = CollectionValidators()
        self.date_validators = DateValidators()
    
    def validate(self, data: Any, **kwargs) -> ValidationResult:
        """
        Validate data values.
        
        Args:
            data: Data to validate
            **kwargs: Additional validation parameters
            
        Returns:
            ValidationResult with validation status and details
        """
        if isinstance(data, str):
            return self.string_validators.validate_string_value(data, **kwargs)
        elif isinstance(data, (int, float)):
            return self.numeric_validators.validate_numeric_value(data, **kwargs)
        elif isinstance(data, (list, tuple)):
            return self.collection_validators.validate_collection_value(data, **kwargs)
        else:
            return ValidationResult(
                status=ValidationStatus.VALID,
                message="Value validation passed for non-standard data type",
                validated_data=data,
                validator_name=self.name
            )
    
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
        return self.string_validators.validate_string_length(text, min_length, max_length)
    
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
        return self.numeric_validators.validate_numeric_range(value, min_value, max_value)
    
    def validate_choice(self, value: Any, choices: List[Any]) -> ValidationResult:
        """
        Validate choice from allowed options.
        
        Args:
            value: Value to validate
            choices: List of allowed choices
            
        Returns:
            ValidationResult with validation status and details
        """
        return self.collection_validators.validate_choice(value, choices)
    
    def validate_date_range(self, date_value: Union[datetime, date, str], 
                           min_date: Union[datetime, date, str] = None,
                           max_date: Union[datetime, date, str] = None) -> ValidationResult:
        """
        Validate date range.
        
        Args:
            date_value: Date to validate
            min_date: Minimum allowed date
            max_date: Maximum allowed date
            
        Returns:
            ValidationResult with validation status and details
        """
        return self.date_validators.validate_date_range(date_value, min_date, max_date)
    
    def validate_collection_size(self, collection: Union[list, tuple, set], 
                                min_size: int = 0, max_size: int = None) -> ValidationResult:
        """
        Validate collection size.
        
        Args:
            collection: Collection to validate
            min_size: Minimum allowed size
            max_size: Maximum allowed size
            
        Returns:
            ValidationResult with validation status and details
        """
        return self.collection_validators.validate_collection_size(collection, min_size, max_size)
    


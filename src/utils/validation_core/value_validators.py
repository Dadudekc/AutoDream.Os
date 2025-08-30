#!/usr/bin/env python3
"""
Consolidated Value Validators - Single Source of Truth for Value Validation

This module consolidates all value validation functionality from multiple
duplicate implementations into a single, maintainable validation system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 1: Validation System Consolidation
"""

from typing import Any, List, Optional, Union
from datetime import datetime, date

from .base_validator import BaseValidator
from .validation_result import ValidationResult, ValidationStatus


class ValueValidators(BaseValidator):
    """
    Consolidated value validation helpers.
    
    This class consolidates all value validation functionality from multiple
    duplicate implementations into a single, maintainable system.
    """
    
    def __init__(self):
        """Initialize the value validators."""
        super().__init__("ValueValidators")
    
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
            return self._validate_string_value(data, **kwargs)
        elif isinstance(data, (int, float)):
            return self._validate_numeric_value(data, **kwargs)
        elif isinstance(data, (list, tuple)):
            return self._validate_collection_value(data, **kwargs)
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
    
    def validate_choice(self, value: Any, choices: List[Any]) -> ValidationResult:
        """
        Validate choice from allowed options.
        
        Args:
            value: Value to validate
            choices: List of allowed choices
            
        Returns:
            ValidationResult with validation status and details
        """
        try:
            if not isinstance(choices, (list, tuple)):
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="Choice validation failed",
                    errors=["Choices must be a list or tuple"],
                    validated_data=value,
                    validator_name=self.name
                )
            
            if not choices:
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="Choice validation failed",
                    errors=["Choices list cannot be empty"],
                    validated_data=value,
                    validator_name=self.name
                )
            
            if value not in choices:
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="Choice validation failed",
                    errors=[f"Value '{value}' not in allowed choices: {choices}"],
                    validated_data=value,
                    validator_name=self.name
                )
            
            return ValidationResult(
                status=ValidationStatus.VALID,
                message="Choice validation passed",
                validated_data=value,
                validator_name=self.name
            )
            
        except Exception as e:
            return ValidationResult(
                status=ValidationStatus.ERROR,
                message="Choice validation error occurred",
                errors=[f"Choice validation exception: {str(e)}"],
                validated_data=value,
                validator_name=self.name
            )
    
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
        try:
            # Convert string dates to datetime objects if needed
            if isinstance(date_value, str):
                try:
                    date_value = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
                except ValueError:
                    return ValidationResult(
                        status=ValidationStatus.INVALID,
                        message="Date range validation failed",
                        errors=["Invalid date format. Use ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"],
                        validated_data=date_value,
                        validator_name=self.name
                    )
            
            if not isinstance(date_value, (datetime, date)):
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="Date range validation failed",
                    errors=["Date value must be a datetime, date, or ISO format string"],
                    validated_data=date_value,
                    validator_name=self.name
                )
            
            errors = []
            
            # Convert min_date if provided
            if min_date is not None:
                if isinstance(min_date, str):
                    try:
                        min_date = datetime.fromisoformat(min_date.replace('Z', '+00:00'))
                    except ValueError:
                        errors.append("Invalid minimum date format")
                if min_date and date_value < min_date:
                    errors.append(f"Date {date_value} is before minimum date {min_date}")
            
            # Convert max_date if provided
            if max_date is not None:
                if isinstance(max_date, str):
                    try:
                        max_date = datetime.fromisoformat(max_date.replace('Z', '+00:00'))
                    except ValueError:
                        errors.append("Invalid maximum date format")
                if max_date and date_value > max_date:
                    errors.append(f"Date {date_value} is after maximum date {max_date}")
            
            if errors:
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="Date range validation failed",
                    errors=errors,
                    validated_data=date_value,
                    validator_name=self.name
                )
            else:
                return ValidationResult(
                    status=ValidationStatus.VALID,
                    message="Date range validation passed",
                    validated_data=date_value,
                    validator_name=self.name
                )
                
        except Exception as e:
            return ValidationResult(
                status=ValidationStatus.ERROR,
                message="Date range validation error occurred",
                errors=[f"Date range validation exception: {str(e)}"],
                validated_data=date_value,
                validator_name=self.name
            )
    
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
        try:
            if not isinstance(collection, (list, tuple, set)):
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="Collection size validation failed",
                    errors=["Value must be a collection (list, tuple, or set)"],
                    validated_data=collection,
                    validator_name=self.name
                )
            
            collection_size = len(collection)
            errors = []
            
            if collection_size < min_size:
                errors.append(f"Collection size {collection_size} is less than minimum {min_size}")
            
            if max_size is not None and collection_size > max_size:
                errors.append(f"Collection size {collection_size} is greater than maximum {max_size}")
            
            if errors:
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="Collection size validation failed",
                    errors=errors,
                    validated_data=collection,
                    validator_name=self.name
                )
            else:
                return ValidationResult(
                    status=ValidationStatus.VALID,
                    message="Collection size validation passed",
                    validated_data=collection,
                    validator_name=self.name
                )
                
        except Exception as e:
            return ValidationResult(
                status=ValidationStatus.ERROR,
                message="Collection size validation error occurred",
                errors=[f"Collection size validation exception: {str(e)}"],
                validated_data=collection,
                validator_name=self.name
            )
    
    def _validate_string_value(self, text: str, **kwargs) -> ValidationResult:
        """Validate string value."""
        return ValidationResult(
            status=ValidationStatus.VALID,
            message="String value validation passed",
            validated_data=text,
            validator_name=self.name
        )
    
    def _validate_numeric_value(self, value: Union[int, float], **kwargs) -> ValidationResult:
        """Validate numeric value."""
        return ValidationResult(
            status=ValidationStatus.VALID,
            message="Numeric value validation passed",
            validated_data=value,
            validator_name=self.name
        )
    
    def _validate_collection_value(self, collection: Union[list, tuple, set], **kwargs) -> ValidationResult:
        """Validate collection value."""
        return ValidationResult(
            status=ValidationStatus.VALID,
            message="Collection value validation passed",
            validated_data=collection,
            validator_name=self.name
        )

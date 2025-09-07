#!/usr/bin/env python3
"""
Date Validators - Specialized Date Validation Logic

This module contains specialized date validation functionality extracted
from the main value_validators.py to comply with V2 file size limits.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: V2 Compliance Modularization
"""

from datetime import datetime, date
from typing import Union

from .base_validator import BaseValidator
from .validation_result import ValidationResult, ValidationStatus


class DateValidators(BaseValidator):
    """
    Specialized date validation helpers.
    
    This class contains date-specific validation logic extracted from
    the main ValueValidators class to maintain V2 compliance.
    """
    
    def __init__(self):
        """Initialize the date validators."""
        super().__init__("DateValidators")
    
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

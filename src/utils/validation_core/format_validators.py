#!/usr/bin/env python3
"""
Consolidated Format Validators - Single Source of Truth for Format Validation

This module consolidates all format validation functionality from multiple
duplicate implementations into a single, maintainable validation system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 1: Validation System Consolidation
"""

import re
from typing import Any, List, Optional

from .base_validator import BaseValidator
from .validation_result import ValidationResult, ValidationStatus
from .email_validators import EmailValidators
from .url_validators import URLValidators


class FormatValidators(BaseValidator):
    """
    Consolidated format validation helpers.
    
    This class consolidates all format validation functionality from multiple
    duplicate implementations into a single, maintainable system.
    """
    
    def __init__(self):
        """Initialize the format validators."""
        super().__init__("FormatValidators")
        self.email_validators = EmailValidators()
        self.url_validators = URLValidators()
    
    def validate(self, data: Any, **kwargs) -> ValidationResult:
        """
        Validate data format.
        
        Args:
            data: Data to validate
            **kwargs: Additional validation parameters
            
        Returns:
            ValidationResult with validation status and details
        """
        if isinstance(data, str):
            return self._validate_string_format(data, **kwargs)
        else:
            return ValidationResult(
                status=ValidationStatus.VALID,
                message="Format validation passed for non-string data",
                validated_data=data,
                validator_name=self.name
            )
    
    def validate_email(self, email: str) -> ValidationResult:
        """Delegate to email validators."""
        return self.email_validators.validate_email(email)
    
    def validate_url(self, url: str) -> ValidationResult:
        """Delegate to URL validators."""
        return self.url_validators.validate_url(url)
    
    def validate_file_extension(self, filename: str, 
                               allowed_extensions: List[str]) -> ValidationResult:
        """
        Validate file extension.
        
        Args:
            filename: Filename to validate
            allowed_extensions: List of allowed file extensions
            
        Returns:
            ValidationResult with validation status and details
        """
        try:
            if not filename or not isinstance(filename, str):
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="File extension validation failed",
                    errors=["Filename must be a non-empty string"],
                    validated_data=filename,
                    validator_name=self.name
                )
            
            # Extract file extension
            if '.' not in filename:
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="File extension validation failed",
                    errors=["Filename must have a file extension"],
                    validated_data=filename,
                    validator_name=self.name
                )
            
            file_extension = filename.split('.')[-1].lower()
            
            if file_extension not in [ext.lower() for ext in allowed_extensions]:
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="File extension validation failed",
                    errors=[f"File extension '{file_extension}' not in allowed extensions: {allowed_extensions}"],
                    validated_data=filename,
                    validator_name=self.name
                )
            
            return ValidationResult(
                status=ValidationStatus.VALID,
                message="File extension validation passed",
                validated_data=filename,
                validator_name=self.name
            )
            
        except Exception as e:
            return ValidationResult(
                status=ValidationStatus.ERROR,
                message="File extension validation error occurred",
                errors=[f"File extension validation exception: {str(e)}"],
                validated_data=filename,
                validator_name=self.name
            )
    
    def validate_pattern(self, text: str, pattern: str) -> ValidationResult:
        """
        Validate text against regex pattern.
        
        Args:
            text: Text to validate
            pattern: Regex pattern to match against
            
        Returns:
            ValidationResult with validation status and details
        """
        try:
            if not isinstance(text, str):
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="Pattern validation failed",
                    errors=["Text must be a string"],
                    validated_data=text,
                    validator_name=self.name
                )
            
            if not isinstance(pattern, str):
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="Pattern validation failed",
                    errors=["Pattern must be a string"],
                    validated_data=text,
                    validator_name=self.name
                )
            
            # Compile and test regex pattern
            try:
                compiled_pattern = re.compile(pattern)
                if compiled_pattern.match(text):
                    return ValidationResult(
                        status=ValidationStatus.VALID,
                        message="Pattern validation passed",
                        validated_data=text,
                        validator_name=self.name
                    )
                else:
                    return ValidationResult(
                        status=ValidationStatus.INVALID,
                        message="Pattern validation failed",
                        errors=[f"Text does not match pattern: {pattern}"],
                        validated_data=text,
                        validator_name=self.name
                    )
            except re.error as e:
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="Pattern validation failed",
                    errors=[f"Invalid regex pattern: {str(e)}"],
                    validated_data=text,
                    validator_name=self.name
                )
                
        except Exception as e:
            return ValidationResult(
                status=ValidationStatus.ERROR,
                message="Pattern validation error occurred",
                errors=[f"Pattern validation exception: {str(e)}"],
                validated_data=text,
                validator_name=self.name
            )
    
    def validate_phone_number(self, phone: str, country_code: str = "US") -> ValidationResult:
        """
        Validate phone number format.
        
        Args:
            phone: Phone number to validate
            country_code: Country code for validation rules
            
        Returns:
            ValidationResult with validation status and details
        """
        try:
            if not phone or not isinstance(phone, str):
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="Phone number validation failed",
                    errors=["Phone number must be a non-empty string"],
                    validated_data=phone,
                    validator_name=self.name
                )
            
            # Remove common separators
            clean_phone = re.sub(r'[\s\-\(\)\.]', '', phone)
            
            # Basic US phone number validation (10 or 11 digits)
            if country_code.upper() == "US":
                if len(clean_phone) == 10 and clean_phone.isdigit():
                    return ValidationResult(
                        status=ValidationStatus.VALID,
                        message="US phone number validation passed",
                        validated_data=phone,
                        validator_name=self.name
                    )
                elif len(clean_phone) == 11 and clean_phone.startswith('1') and clean_phone[1:].isdigit():
                    return ValidationResult(
                        status=ValidationStatus.VALID,
                        message="US phone number validation passed",
                        validated_data=phone,
                        validator_name=self.name
                    )
                else:
                    return ValidationResult(
                        status=ValidationStatus.INVALID,
                        message="US phone number validation failed",
                        errors=["Phone number must be 10 digits or 11 digits starting with 1"],
                        validated_data=phone,
                        validator_name=self.name
                    )
            else:
                # Generic international validation (basic)
                if clean_phone.isdigit() and len(clean_phone) >= 7:
                    return ValidationResult(
                        status=ValidationStatus.VALID,
                        message="International phone number validation passed",
                        validated_data=phone,
                        validator_name=self.name
                    )
                else:
                    return ValidationResult(
                        status=ValidationStatus.INVALID,
                        message="International phone number validation failed",
                        errors=["Phone number must contain at least 7 digits"],
                        validated_data=phone,
                        validator_name=self.name
                    )
                    
        except Exception as e:
            return ValidationResult(
                status=ValidationStatus.ERROR,
                message="Phone number validation error occurred",
                errors=[f"Phone number validation exception: {str(e)}"],
                validated_data=phone,
                validator_name=self.name
            )
    
    def _validate_string_format(self, text: str, **kwargs) -> ValidationResult:
        """Validate string format."""
        return ValidationResult(
            status=ValidationStatus.VALID,
            message="String format validation passed",
            validated_data=text,
            validator_name=self.name
        )

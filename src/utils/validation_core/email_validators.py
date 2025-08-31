#!/usr/bin/env python3
"""
Email Validators - Specialized Email Validation

This module provides specialized email validation functionality,
extracted from the main format validators to achieve V2 compliance.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: V2 Compliance - File size optimization
"""

import re
from typing import Any

from .base_validator import BaseValidator
from .validation_result import ValidationResult, ValidationStatus


class EmailValidators(BaseValidator):
    """
    Specialized email validation helpers.
    
    This class provides comprehensive email validation functionality
    while maintaining V2 compliance through focused responsibility.
    """
    
    def __init__(self):
        """Initialize the email validators."""
        super().__init__("EmailValidators")
    
    def validate_email(self, email: str) -> ValidationResult:
        """
        Validate email address format.
        
        Args:
            email: Email address to validate
            
        Returns:
            ValidationResult with validation status and details
        """
        try:
            # Basic email validation using regex
            if not email or not isinstance(email, str):
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="Email validation failed",
                    errors=["Email must be a non-empty string"],
                    validated_data=email,
                    validator_name=self.name
                )
            
            # Simple email regex pattern
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            
            if re.match(email_pattern, email):
                return ValidationResult(
                    status=ValidationStatus.VALID,
                    message="Email format validation passed",
                    validated_data=email,
                    validator_name=self.name
                )
            else:
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="Email format validation failed",
                    errors=["Invalid email format"],
                    validated_data=email,
                    validator_name=self.name
                )
                
        except Exception as e:
            return ValidationResult(
                status=ValidationStatus.ERROR,
                message="Email validation error occurred",
                errors=[f"Email validation exception: {str(e)}"],
                validated_data=email,
                validator_name=self.name
            )
    
    def validate_email_domain(self, email: str) -> ValidationResult:
        """
        Validate email domain specifically.
        
        Args:
            email: Email address to validate
            
        Returns:
            ValidationResult with validation status and details
        """
        try:
            if not email or not isinstance(email, str):
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="Email domain validation failed",
                    errors=["Email must be a non-empty string"],
                    validated_data=email,
                    validator_name=self.name
                )
            
            # Extract domain from email
            if '@' not in email:
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="Email domain validation failed",
                    errors=["Email must contain @ symbol"],
                    validated_data=email,
                    validator_name=self.name
                )
            
            domain = email.split('@')[1]
            
            # Basic domain validation
            if not domain or '.' not in domain:
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="Email domain validation failed",
                    errors=["Invalid domain format"],
                    validated_data=email,
                    validator_name=self.name
                )
            
            return ValidationResult(
                status=ValidationStatus.VALID,
                message="Email domain validation passed",
                validated_data=email,
                validator_name=self.name
            )
            
        except Exception as e:
            return ValidationResult(
                status=ValidationStatus.ERROR,
                message="Email domain validation error occurred",
                errors=[f"Email domain validation exception: {str(e)}"],
                validated_data=email,
                validator_name=self.name
            )

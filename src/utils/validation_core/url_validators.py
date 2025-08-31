#!/usr/bin/env python3
"""
URL Validators - Specialized URL Validation

This module provides specialized URL validation functionality,
extracted from the main format validators to achieve V2 compliance.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: V2 Compliance - File size optimization
"""

import re
import urllib.parse
from typing import Any

from .base_validator import BaseValidator
from .validation_result import ValidationResult, ValidationStatus


class URLValidators(BaseValidator):
    """
    Specialized URL validation helpers.
    
    This class provides comprehensive URL validation functionality
    while maintaining V2 compliance through focused responsibility.
    """
    
    def __init__(self):
        """Initialize the URL validators."""
        super().__init__("URLValidators")
    
    def validate_url(self, url: str) -> ValidationResult:
        """
        Validate URL format.
        
        Args:
            url: URL to validate
            
        Returns:
            ValidationResult with validation status and details
        """
        try:
            # Basic URL format validation
            if not url or not isinstance(url, str):
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="URL validation failed",
                    errors=["URL must be a non-empty string"],
                    validated_data=url,
                    validator_name=self.name
                )
            
            # Check for basic URL structure
            if not (url.startswith('http://') or url.startswith('https://') or 
                   url.startswith('ftp://') or url.startswith('file://')):
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="URL validation failed",
                    errors=["URL must start with http://, https://, ftp://, or file://"],
                    validated_data=url,
                    validator_name=self.name
                )
            
            # Parse URL to check structure
            parsed_url = urllib.parse.urlparse(url)
            if not parsed_url.netloc:
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="URL validation failed",
                    errors=["URL must have a valid domain/host"],
                    validated_data=url,
                    validator_name=self.name
                )
            
            return ValidationResult(
                status=ValidationStatus.VALID,
                message="URL format validation passed",
                validated_data=url,
                validator_name=self.name
            )
            
        except Exception as e:
            return ValidationResult(
                status=ValidationStatus.ERROR,
                message="URL validation error occurred",
                errors=[f"URL validation exception: {str(e)}"],
                validated_data=url,
                validator_name=self.name
            )
    
    def validate_url_scheme(self, url: str) -> ValidationResult:
        """
        Validate URL scheme specifically.
        
        Args:
            url: URL to validate
            
        Returns:
            ValidationResult with validation status and details
        """
        try:
            if not url or not isinstance(url, str):
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="URL scheme validation failed",
                    errors=["URL must be a non-empty string"],
                    validated_data=url,
                    validator_name=self.name
                )
            
            parsed_url = urllib.parse.urlparse(url)
            scheme = parsed_url.scheme
            
            if not scheme:
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="URL scheme validation failed",
                    errors=["URL must have a valid scheme"],
                    validated_data=url,
                    validator_name=self.name
                )
            
            # Validate common schemes
            valid_schemes = ['http', 'https', 'ftp', 'file']
            if scheme.lower() not in valid_schemes:
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    message="URL scheme validation failed",
                    errors=[f"Invalid scheme: {scheme}"],
                    validated_data=url,
                    validator_name=self.name
                )
            
            return ValidationResult(
                status=ValidationStatus.VALID,
                message="URL scheme validation passed",
                validated_data=url,
                validator_name=self.name
            )
            
        except Exception as e:
            return ValidationResult(
                status=ValidationStatus.ERROR,
                message="URL scheme validation error occurred",
                errors=[f"URL scheme validation exception: {str(e)}"],
                validated_data=url,
                validator_name=self.name
            )

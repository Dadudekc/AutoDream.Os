#!/usr/bin/env python3
"""
Unified Validation System - Single Source of Truth for All Validation

This module provides the main interface for the unified validation system,
consolidating all validation functionality from multiple duplicate implementations
into a single, maintainable validation system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 1: Validation System Consolidation
"""

import time
import psutil
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

from .base_validator import BaseValidator
from .data_validators import DataValidators
from .format_validators import FormatValidators
from .value_validators import ValueValidators
from .validation_result import ValidationResult, ValidationStatus


class UnifiedValidationSystem(BaseValidator):
    """
    Unified validation system for eliminating function duplication.
    
    This class consolidates all common validation logic into a single,
    maintainable location, eliminating the need for duplicate validation
    functions across the codebase.
    """
    
    def __init__(self):
        """Initialize the unified validation system."""
        super().__init__("UnifiedValidationSystem")
        
        # Initialize specialized validators
        self.data_validators = DataValidators()
        self.format_validators = FormatValidators()
        self.value_validators = ValueValidators()
        
        # Performance tracking
        self.total_validations = 0
        self.total_validation_time = 0.0
    
    def validate(self, data: Any, **kwargs) -> ValidationResult:
        """
        Main validation method that routes to appropriate validators.
        
        Args:
            data: Data to validate
            **kwargs: Additional validation parameters
            
        Returns:
            ValidationResult with validation status and details
        """
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024  # KB
        
        try:
            # Route to appropriate validator based on data type and context
            if isinstance(data, dict):
                result = self._validate_dict(data, **kwargs)
            elif isinstance(data, list):
                result = self._validate_list(data, **kwargs)
            elif isinstance(data, str):
                result = self._validate_string(data, **kwargs)
            else:
                result = ValidationResult(
                    status=ValidationStatus.VALID,
                    message="Data type validation passed",
                    validated_data=data,
                    validator_name=self.name
                )
            
            # Add performance metrics
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024  # KB
            
            result.validation_time_ms = (end_time - start_time) * 1000
            result.memory_usage_kb = end_memory - start_memory
            result.validator_name = self.name
            result.validator_version = "2.0.0"
            
            # Update performance tracking
            self.total_validations += 1
            self.total_validation_time += result.validation_time_ms
            
            # Log result
            self.log_validation_result(result)
            
            return result
            
        except Exception as e:
            # Handle validation errors gracefully
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024  # KB
            
            error_result = ValidationResult(
                status=ValidationStatus.ERROR,
                message=f"Validation error occurred: {str(e)}",
                errors=[f"Validation exception: {str(e)}"],
                validated_data=data,
                validator_name=self.name,
                validator_version="2.0.0",
                validation_time_ms=(end_time - start_time) * 1000,
                memory_usage_kb=end_memory - start_memory
            )
            
            self.log_validation_result(error_result)
            return error_result
    
    def validate_config(self, config: Dict[str, Any], 
                       required_fields: List[str] = None) -> ValidationResult:
        """
        Unified configuration validation function.
        
        Args:
            config: Configuration dictionary to validate
            required_fields: List of required field names
            
        Returns:
            ValidationResult with validation status and details
        """
        # Use data validators for configuration validation
        if required_fields:
            result = self.data_validators.validate_required_fields(config, required_fields)
            if not result.is_valid():
                return result
        
        # Additional configuration-specific validation
        errors = []
        warnings = []
        
        # Validate common configuration patterns
        if 'version' in config:
            if not isinstance(config['version'], str):
                errors.append("Version field must be a string")
        
        if 'enabled' in config:
            if not isinstance(config['enabled'], bool):
                errors.append("Enabled field must be a boolean")
        
        if 'timeout' in config:
            if not isinstance(config['timeout'], (int, float)) or config['timeout'] <= 0:
                errors.append("Timeout field must be a positive number")
        
        if errors:
            return ValidationResult(
                status=ValidationStatus.INVALID,
                message="Configuration validation failed",
                errors=errors,
                warnings=warnings,
                validated_data=config,
                validator_name=self.name
            )
        else:
            return ValidationResult(
                status=ValidationStatus.VALID,
                message="Configuration validation passed",
                warnings=warnings,
                validated_data=config,
                validator_name=self.name
            )
    
    def validate_email(self, email: str) -> ValidationResult:
        """
        Validate email address format.
        
        Args:
            email: Email address to validate
            
        Returns:
            ValidationResult with validation status and details
        """
        return self.format_validators.validate_email(email)
    
    def validate_url(self, url: str) -> ValidationResult:
        """
        Validate URL format.
        
        Args:
            url: URL to validate
            
        Returns:
            ValidationResult with validation status and details
        """
        return self.format_validators.validate_url(url)
    
    def validate_json_string(self, json_str: str) -> ValidationResult:
        """
        Validate JSON string format.
        
        Args:
            json_str: JSON string to validate
            
        Returns:
            ValidationResult with validation status and details
        """
        return self.data_validators.validate_json_string(json_str)
    
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
        return self.format_validators.validate_file_extension(filename, allowed_extensions)
    
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
        return self.value_validators.validate_string_length(text, min_length, max_length)
    
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
        return self.value_validators.validate_numeric_range(value, min_value, max_value)
    
    def validate_choice(self, value: Any, choices: List[Any]) -> ValidationResult:
        """
        Validate choice from allowed options.
        
        Args:
            value: Value to validate
            choices: List of allowed choices
            
        Returns:
            ValidationResult with validation status and details
        """
        return self.value_validators.validate_choice(value, choices)
    
    def validate_pattern(self, text: str, pattern: str) -> ValidationResult:
        """
        Validate text against regex pattern.
        
        Args:
            text: Text to validate
            pattern: Regex pattern to match against
            
        Returns:
            ValidationResult with validation status and details
        """
        return self.format_validators.validate_pattern(text, pattern)
    
    def _validate_dict(self, data: Dict[str, Any], **kwargs) -> ValidationResult:
        """Validate dictionary data."""
        return self.data_validators.validate(data, **kwargs)
    
    def _validate_list(self, data: List[Any], **kwargs) -> ValidationResult:
        """Validate list data."""
        return self.data_validators.validate(data, **kwargs)
    
    def _validate_string(self, data: str, **kwargs) -> ValidationResult:
        """Validate string data."""
        return self.data_validators.validate(data, **kwargs)
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics for the validation system.
        
        Returns:
            Dictionary with performance metrics
        """
        avg_time = (self.total_validation_time / self.total_validations 
                   if self.total_validations > 0 else 0)
        
        return {
            'total_validations': self.total_validations,
            'total_validation_time_ms': self.total_validation_time,
            'average_validation_time_ms': avg_time,
            'validator_name': self.name,
            'validator_version': "2.0.0"
        }
    
    def reset_performance_stats(self) -> None:
        """Reset performance statistics."""
        self.total_validations = 0
        self.total_validation_time = 0.0
        self.logger.info("Performance statistics reset")

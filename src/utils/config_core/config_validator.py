#!/usr/bin/env python3
"""
Config Validator - Configuration Validation Functionality

This module provides configuration validation functionality for the unified
configuration system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 2: Configuration System Consolidation
"""

from typing import Dict, Any, List, Optional
from validation_core import ValidationResult, ValidationStatus


class ConfigValidator:
    """
    Configuration validator for the unified configuration system.
    
    This class provides validation functionality for configuration data.
    """
    
    def __init__(self):
        """Initialize the configuration validator."""
        pass
    
    def validate_config(self, config: Dict[str, Any]) -> ValidationResult:
        """
        Validate configuration data.
        
        Args:
            config: Configuration dictionary to validate
            
        Returns:
            ValidationResult with validation status and details
        """
        errors = []
        warnings = []
        
        if not isinstance(config, dict):
            errors.append("Configuration must be a dictionary")
            return ValidationResult(
                status=ValidationStatus.INVALID,
                message="Configuration validation failed",
                errors=errors,
                warnings=warnings,
                validated_data=config
            )
        
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
        
        if 'log_level' in config:
            valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            if config['log_level'] not in valid_log_levels:
                errors.append(f"Log level must be one of: {valid_log_levels}")
        
        # Check for required sections
        required_sections = ['system', 'services']
        for section in required_sections:
            if section not in config:
                warnings.append(f"Recommended section '{section}' is missing")
        
        # Validate nested structures
        for key, value in config.items():
            if isinstance(value, dict):
                nested_result = self._validate_nested_config(value, f"{key}")
                if not nested_result.is_valid():
                    errors.extend([f"{key}.{error}" for error in nested_result.errors])
                warnings.extend([f"{key}.{warning}" for warning in nested_result.warnings])
        
        if errors:
            return ValidationResult(
                status=ValidationStatus.INVALID,
                message="Configuration validation failed",
                errors=errors,
                warnings=warnings,
                validated_data=config
            )
        else:
            return ValidationResult(
                status=ValidationStatus.VALID,
                message="Configuration validation passed",
                warnings=warnings,
                validated_data=config
            )
    
    def _validate_nested_config(self, config: Dict[str, Any], path: str) -> ValidationResult:
        """
        Validate nested configuration structure.
        
        Args:
            config: Nested configuration dictionary
            path: Path to current configuration level
            
        Returns:
            ValidationResult with validation status and details
        """
        errors = []
        warnings = []
        
        for key, value in config.items():
            # Validate key names
            if not isinstance(key, str):
                errors.append(f"Configuration key must be a string, got {type(key).__name__}")
                continue
            
            # Validate common field patterns
            if key.endswith('_enabled') and not isinstance(value, bool):
                warnings.append(f"Field '{key}' typically represents a boolean flag")
            
            if key.endswith('_timeout') and isinstance(value, (int, float)) and value <= 0:
                errors.append(f"Timeout field '{key}' must be positive")
            
            if key.endswith('_path') and isinstance(value, str) and not value.strip():
                warnings.append(f"Path field '{key}' is empty")
        
        if errors:
            return ValidationResult(
                status=ValidationStatus.INVALID,
                message=f"Nested configuration validation failed at {path}",
                errors=errors,
                warnings=warnings,
                validated_data=config
            )
        else:
            return ValidationResult(
                status=ValidationStatus.VALID,
                message=f"Nested configuration validation passed at {path}",
                warnings=warnings,
                validated_data=config
            )
    
    def validate_config_schema(self, config: Dict[str, Any], 
                              schema: Dict[str, Dict[str, Any]]) -> ValidationResult:
        """
        Validate configuration against a schema definition.
        
        Args:
            config: Configuration to validate
            schema: Schema definition with field rules
            
        Returns:
            ValidationResult with validation status and details
        """
        errors = []
        warnings = []
        
        for field_name, field_rules in schema.items():
            if field_name not in config:
                if field_rules.get('required', False):
                    errors.append(f"Required field '{field_name}' is missing")
                continue
            
            field_value = config[field_name]
            
            # Type validation
            expected_type = field_rules.get('type')
            if expected_type and not isinstance(field_value, expected_type):
                errors.append(
                    f"Field '{field_name}' must be of type {expected_type.__name__}, "
                    f"got {type(field_value).__name__}"
                )
            
            # Range validation for numbers
            if isinstance(field_value, (int, float)):
                if 'min' in field_rules and field_value < field_rules['min']:
                    errors.append(f"Field '{field_name}' must be >= {field_rules['min']}")
                if 'max' in field_rules and field_value > field_rules['max']:
                    errors.append(f"Field '{field_name}' must be <= {field_rules['max']}")
            
            # Choice validation
            if 'choices' in field_rules and field_value not in field_rules['choices']:
                errors.append(f"Field '{field_name}' must be one of {field_rules['choices']}")
        
        if errors:
            return ValidationResult(
                status=ValidationStatus.INVALID,
                message="Schema validation failed",
                errors=errors,
                warnings=warnings,
                validated_data=config
            )
        else:
            return ValidationResult(
                status=ValidationStatus.VALID,
                message="Schema validation passed",
                warnings=warnings,
                validated_data=config
            )

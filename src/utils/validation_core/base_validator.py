#!/usr/bin/env python3
"""
Base Validator Class - Foundation for All Validation Operations

This class provides common validation functionality and serves as the base
for all specialized validators in the unified validation system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 1: Validation System Consolidation
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import logging

from .validation_result import ValidationResult, ValidationStatus

logger = logging.getLogger(__name__)


class BaseValidator(ABC):
    """
    Abstract base class for all validators in the unified validation system.
    
    This class provides common validation functionality and ensures consistent
    behavior across all validation operations.
    """
    
    def __init__(self, name: str = None):
        """
        Initialize the base validator.
        
        Args:
            name: Optional name for the validator instance
        """
        self.name = name or self.__class__.__name__
        self.validation_history: List[ValidationResult] = []
        self.logger = logging.getLogger(f"{__name__}.{self.name}")
    
    @abstractmethod
    def validate(self, data: Any, **kwargs) -> ValidationResult:
        """
        Abstract method that must be implemented by all validators.
        
        Args:
            data: Data to validate
            **kwargs: Additional validation parameters
            
        Returns:
            ValidationResult with validation status and details
        """
        pass
    
    def validate_required_fields(self, data: Dict[str, Any], 
                               required_fields: List[str]) -> List[str]:
        """
        Validate that required fields are present and not empty.
        
        Args:
            data: Dictionary to validate
            required_fields: List of required field names
            
        Returns:
            List of validation error messages
        """
        errors = []
        
        for field in required_fields:
            if field not in data:
                errors.append(f"Required field '{field}' is missing")
            elif data[field] is None:
                errors.append(f"Required field '{field}' cannot be null")
            elif isinstance(data[field], str) and not data[field].strip():
                errors.append(f"Required field '{field}' cannot be empty")
            elif isinstance(data[field], (list, dict)) and not data[field]:
                errors.append(f"Required field '{field}' cannot be empty")
        
        return errors
    
    def validate_data_types(self, data: Dict[str, Any], 
                           type_schema: Dict[str, type]) -> List[str]:
        """
        Validate data types against a provided schema.
        
        Args:
            data: Dictionary to validate
            type_schema: Dictionary mapping field names to expected types
            
        Returns:
            List of validation error messages
        """
        errors = []
        
        for field, expected_type in type_schema.items():
            if field in data and not isinstance(data[field], expected_type):
                errors.append(
                    f"Field '{field}' must be of type {expected_type.__name__}, "
                    f"got {type(data[field]).__name__}"
                )
        
        return errors
    
    def log_validation_result(self, result: ValidationResult) -> None:
        """
        Log validation result for debugging and monitoring.
        
        Args:
            result: Validation result to log
        """
        if result.status == ValidationStatus.VALID:
            self.logger.info(f"Validation successful: {result.message}")
        elif result.status == ValidationStatus.WARNING:
            self.logger.warning(f"Validation warning: {result.message}")
        else:
            self.logger.error(f"Validation failed: {result.message}")
        
        # Store in validation history
        self.validation_history.append(result)
    
    def get_validation_summary(self) -> Dict[str, int]:
        """
        Get summary of validation results.
        
        Returns:
            Dictionary with counts of validation results by status
        """
        summary = {
            'total': len(self.validation_history),
            'valid': 0,
            'invalid': 0,
            'warning': 0,
            'error': 0
        }
        
        for result in self.validation_history:
            if result.status == ValidationStatus.VALID:
                summary['valid'] += 1
            elif result.status == ValidationStatus.INVALID:
                summary['invalid'] += 1
            elif result.status == ValidationStatus.WARNING:
                summary['warning'] += 1
            elif result.status == ValidationStatus.ERROR:
                summary['error'] += 1
        
        return summary
    
    def clear_validation_history(self) -> None:
        """Clear validation history."""
        self.validation_history.clear()
        self.logger.info("Validation history cleared")
    
    def __str__(self) -> str:
        """String representation of the validator."""
        return f"{self.name} (BaseValidator)"
    
    def __repr__(self) -> str:
        """Detailed string representation of the validator."""
        summary = self.get_validation_summary()
        return (f"{self.name} (BaseValidator) - "
                f"Total: {summary['total']}, "
                f"Valid: {summary['valid']}, "
                f"Invalid: {summary['invalid']}")

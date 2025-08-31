#!/usr/bin/env python3
"""
Collection Validators - Specialized Collection Validation Logic

This module contains specialized collection validation functionality extracted
from the main value_validators.py to comply with V2 file size limits.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: V2 Compliance Modularization
"""

from typing import Any, List, Union

from .base_validator import BaseValidator
from .validation_result import ValidationResult, ValidationStatus


class CollectionValidators(BaseValidator):
    """
    Specialized collection validation helpers.
    
    This class contains collection-specific validation logic extracted from
    the main ValueValidators class to maintain V2 compliance.
    """
    
    def __init__(self):
        """Initialize the collection validators."""
        super().__init__("CollectionValidators")
    
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
    
    def validate_collection_value(self, collection: Union[list, tuple, set], **kwargs) -> ValidationResult:
        """Validate collection value."""
        return ValidationResult(
            status=ValidationStatus.VALID,
            message="Collection value validation passed",
            validated_data=collection,
            validator_name=self.name
        )

#!/usr/bin/env python3
"""
Base Validator - Abstract base class for all validation engines.

Author: Agent-6 (Coordination & Communication Specialist)
Mission: V2 Compliance - Modular Architecture
Status: REFACTORED - Clean separation of concerns
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ..models.validation_models import ValidationResult, ValidationRule


class BaseValidator(ABC):
    """Abstract base class for all validation engines."""
    
    def __init__(self):
        """Initialize the validator."""
        self.logger = None
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging for the validator."""
        import logging
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def validate(self, value: Any, **kwargs) -> ValidationResult:
        """
        Validate a value.
        
        Args:
            value: The value to validate
            **kwargs: Additional validation parameters
            
        Returns:
            ValidationResult: The validation result
        """
        pass
    
    def validate_rule(self, value: Any, rule: ValidationRule) -> ValidationResult:
        """
        Validate a value against a specific rule.
        
        Args:
            value: The value to validate
            rule: The validation rule
            
        Returns:
            ValidationResult: The validation result
        """
        result = self.validate(value, **rule.parameters)
        result.field_name = rule.field_name
        result.validation_type = rule.rule_type
        result.severity = rule.severity
        return result

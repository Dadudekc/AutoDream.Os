"""
Unified Validation Framework - Agent Cellphone V2

This package provides a unified validation system with specialized validators
following Single Responsibility Principle and V2 coding standards.

Components:
- BaseValidator: Abstract base class for all validators
- ValidationResult: Standardized validation result structure
- ValidationRule: Configurable validation rules
- Specialized validators for different domains
"""

from .base_validator import BaseValidator, ValidationResult, ValidationRule, ValidationSeverity, ValidationStatus
from .contract_validator import ContractValidator
from .config_validator import ConfigValidator
from .workflow_validator import WorkflowValidator
from .message_validator import MessageValidator
from .quality_validator import QualityValidator
from .security_validator import SecurityValidator
from .storage_validator import StorageValidator
from .onboarding_validator import OnboardingValidator
from .task_validator import TaskValidator
from .code_validator import CodeValidator
from .validation_manager import ValidationManager

__all__ = [
    'BaseValidator',
    'ValidationResult',
    'ValidationRule',
    'ValidationSeverity',
    'ValidationStatus',
    'ContractValidator',
    'ConfigValidator',
    'WorkflowValidator',
    'MessageValidator',
    'QualityValidator',
    'SecurityValidator',
    'StorageValidator',
    'OnboardingValidator',
    'TaskValidator',
    'CodeValidator',
    'ValidationManager'
]

__version__ = "2.0.0"
__author__ = "Agent Cellphone V2 Team"
__description__ = "Unified validation framework following SRP principles"

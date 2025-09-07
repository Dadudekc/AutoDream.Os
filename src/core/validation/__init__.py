"""Public interface for the validation package."""

from .base_validator import (
    BaseValidator,
    ValidationRule,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)
from .security_validator import SecurityValidator

# Additional security modules from the refactored version
from .security_core import SecurityCore
from .security_authentication import SecurityAuthentication
from .security_authorization import SecurityAuthorization
from .security_encryption import SecurityEncryption
from .security_policy import SecurityPolicy
from .security_recommendations import SecurityRecommendations
from .security_validator_v2 import SecurityValidatorV2
from .rule_registry import RuleRegistry
from .executor import ValidationExecutor
from .reporting import ValidationReporter
from .validation_manager import ValidationManager


class WorkflowValidator:  # pragma: no cover - simple stub for tests
    """Placeholder WorkflowValidator used to satisfy legacy imports."""
    pass


__all__ = [
    "BaseValidator",
    "ValidationRule",
    "ValidationResult",
    "ValidationSeverity",
    "ValidationStatus",
    "SecurityValidator",
    "WorkflowValidator",
    # Additional security modules
    'SecurityCore',
    'SecurityAuthentication',
    'SecurityAuthorization',
    'SecurityEncryption',
    'SecurityPolicy',
    'SecurityRecommendations',
    'SecurityValidatorV2',
    'RuleRegistry',
    'ValidationExecutor',
    'ValidationReporter',
    'ValidationManager',
]

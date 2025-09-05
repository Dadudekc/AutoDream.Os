"""
Error Models Refactored - V2 Compliance Error Handling Data Models
=================================================================

Refactored data models and enums for error handling system with V2 compliance standards.

V2 COMPLIANCE: Type-safe error models with validation and configuration
DESIGN PATTERN: Builder pattern for error context creation
DEPENDENCY INJECTION: Configuration-driven error handling parameters

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - Error Models Refactored Optimized
"""

# Import all error handling components
from .error_models_enums import (
    ErrorSeverity, CircuitState, ErrorType, RetryStrategy
)
from .error_models_core import (
    ErrorContext, CircuitBreakerConfig, RetryConfig
)
from .error_models_metrics import (
    ErrorMetrics, ErrorReport, ErrorAlert
)

# Re-export all public components for backward compatibility
__all__ = [
    # Enums
    'ErrorSeverity', 'CircuitState', 'ErrorType', 'RetryStrategy',
    # Core Models
    'ErrorContext', 'CircuitBreakerConfig', 'RetryConfig',
    # Metrics Models
    'ErrorMetrics', 'ErrorReport', 'ErrorAlert'
]


def create_error_context(
    error_id: str,
    error_type: ErrorType,
    severity: ErrorSeverity,
    message: str,
    **kwargs
) -> ErrorContext:
    """Create error context with V2 compliance."""
    return ErrorContext(
        error_id=error_id,
        error_type=error_type,
        severity=severity,
        message=message,
        **kwargs
    )


def validate_error_configurations() -> bool:
    """Validate error configurations with V2 compliance."""
    try:
        # Validate circuit breaker config
        config = CircuitBreakerConfig(name="test")
        assert config.failure_threshold > 0
        assert config.recovery_timeout > 0
        assert config.success_threshold > 0
        
        # Validate retry config
        retry = RetryConfig()
        assert retry.max_attempts > 0
        assert retry.base_delay > 0
        assert retry.max_delay > 0
        assert retry.backoff_multiplier > 0
        
        return True
    except Exception:
        return False

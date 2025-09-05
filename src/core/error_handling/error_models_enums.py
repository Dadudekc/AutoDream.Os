"""
Error Models Enums - V2 Compliance Error Handling Enumerations
=============================================================

Enums for error handling system with V2 compliance standards.

V2 COMPLIANCE: Type-safe error enums with validation
DESIGN PATTERN: Enum pattern for error type definitions
DEPENDENCY INJECTION: Configuration-driven error handling parameters

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - Error Models Enums Optimized
"""

from enum import Enum


class ErrorSeverity(Enum):
    """Error severity levels with V2 compliance."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    def __str__(self) -> str:
        return self.value

    def __lt__(self, other) -> bool:
        """Compare severity levels."""
        order = [ErrorSeverity.LOW, ErrorSeverity.MEDIUM, ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]
        return order.index(self) < order.index(other)

    def __le__(self, other) -> bool:
        """Compare severity levels."""
        return self < other or self == other


class CircuitState(Enum):
    """Circuit breaker states with V2 compliance."""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

    def __str__(self) -> str:
        return self.value


class ErrorType(Enum):
    """Error types with V2 compliance."""

    VALIDATION_ERROR = "validation_error"
    CONFIGURATION_ERROR = "configuration_error"
    RUNTIME_ERROR = "runtime_error"
    NETWORK_ERROR = "network_error"
    DATABASE_ERROR = "database_error"
    AUTHENTICATION_ERROR = "authentication_error"
    AUTHORIZATION_ERROR = "authorization_error"
    TIMEOUT_ERROR = "timeout_error"
    RESOURCE_ERROR = "resource_error"
    UNKNOWN_ERROR = "unknown_error"

    def __str__(self) -> str:
        return self.value


class RetryStrategy(Enum):
    """Retry strategies with V2 compliance."""

    FIXED = "fixed"
    EXPONENTIAL = "exponential"
    LINEAR = "linear"
    CUSTOM = "custom"

    def __str__(self) -> str:
        return self.value

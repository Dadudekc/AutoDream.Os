#!/usr/bin/env python3
"""
Error Models - V2 Compliance Error Handling Data Models
======================================================

Data models and enums for error handling system with V2 compliance standards.

V2 COMPLIANCE: Type-safe error models with validation and configuration
DESIGN PATTERN: Builder pattern for error context creation
DEPENDENCY INJECTION: Configuration-driven error handling parameters

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - Error Models Optimized
"""

from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional, Type, List
# Configuration simplified - KISS compliance

# ================================
# ERROR SEVERITY LEVELS
# ================================

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

# ================================
# CIRCUIT BREAKER STATES
# ================================

class CircuitState(Enum):
    """Circuit breaker states with V2 compliance."""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Circuit is open, requests fail fast
    HALF_OPEN = "half_open"  # Testing if service is recovered

    def __str__(self) -> str:
        return self.value

# ================================
# ERROR CONTEXT MODEL
# ================================

@dataclass
class ErrorContext:
    """Context information for error handling with V2 compliance."""

    operation: str
    component: str
    timestamp: datetime
    severity: ErrorSeverity
    details: Optional[Dict[str, Any]] = None
    retry_count: int = 0
    max_retries: int = 3
    error_id: Optional[str] = None
    correlation_id: Optional[str] = None
    stack_trace: Optional[str] = None
    user_context: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.details is None:
            self.details = {}
        if self.user_context is None:
            self.user_context = {}
        if self.error_id is None:
            self.error_id = f"err_{self.timestamp.strftime('%Y%m%d_%H%M%S')}_{hash(self) % 10000:04d}"
        if self.correlation_id is None:
            self.correlation_id = f"corr_{hash((self.operation, self.component, self.timestamp)) % 1000000:06d}"

    def should_retry(self) -> bool:
        """Determine if error should be retried."""
        return self.retry_count < self.max_retries and self.severity < ErrorSeverity.CRITICAL

    def get_retry_delay(self, base_delay: float = 1.0, backoff_factor: float = 2.0) -> float:
        """Calculate retry delay with exponential backoff."""
        return min(base_delay * (backoff_factor ** self.retry_count), 300.0)  # Max 5 minutes

    def to_dict(self) -> Dict[str, Any]:
        """Convert error context to dictionary."""
        return {
            "error_id": self.error_id,
            "correlation_id": self.correlation_id,
            "operation": self.operation,
            "component": self.component,
            "timestamp": self.timestamp.isoformat(),
            "severity": self.severity.value,
            "details": self.details,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "stack_trace": self.stack_trace,
            "user_context": self.user_context
        }

# ================================
# CIRCUIT BREAKER CONFIGURATION
# ================================

@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker pattern with V2 compliance."""

    failure_threshold: int = 5
    recovery_timeout: int = 60
    expected_exception: Type[Exception] = Exception
    name: str = "default"
    success_threshold: int = 3
    timeout_seconds: float = 30.0
    monitoring_enabled: bool = True
    metrics_enabled: bool = True

    def __post_init__(self):
        """Validate configuration on initialization."""
        if self.failure_threshold <= 0:
            raise ValueError("failure_threshold must be positive")
        if self.recovery_timeout <= 0:
            raise ValueError("recovery_timeout must be positive")
        if self.success_threshold <= 0:
            raise ValueError("success_threshold must be positive")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")

# ================================
# RETRY CONFIGURATION
# ================================

@dataclass
class RetryConfig:
    """Configuration for retry mechanisms with V2 compliance."""

    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    backoff_factor: float = 2.0
    jitter: bool = True
    retryable_exceptions: Optional[List[Type[Exception]]] = None
    non_retryable_exceptions: Optional[List[Type[Exception]]] = None

    def __post_init__(self):
        """Validate configuration on initialization."""
        if self.max_attempts <= 0:
            raise ValueError("max_attempts must be positive")
        if self.base_delay <= 0:
            raise ValueError("base_delay must be positive")
        if self.max_delay <= 0:
            raise ValueError("max_delay must be positive")
        if self.backoff_factor <= 1:
            raise ValueError("backoff_factor must be greater than 1")

        if self.retryable_exceptions is None:
            self.retryable_exceptions = []
        if self.non_retryable_exceptions is None:
            self.non_retryable_exceptions = []

    def is_retryable_exception(self, exception: Exception) -> bool:
        """Determine if an exception should trigger a retry."""
        exception_type = type(exception)

        # Check non-retryable exceptions first
        for non_retryable in self.non_retryable_exceptions:
            if issubclass(exception_type, non_retryable):
                return False

        # Check retryable exceptions
        if self.retryable_exceptions:
            for retryable in self.retryable_exceptions:
                if issubclass(exception_type, retryable):
                    return True
            return False

        # Default: retry on common transient exceptions
        return isinstance(exception, (ConnectionError, TimeoutError, OSError))

# ================================
# ERROR METRICS MODEL
# ================================

@dataclass
class ErrorMetrics:
    """Metrics for error handling performance."""

    total_errors: int = 0
    errors_by_severity: Dict[str, int] = field(default_factory=dict)
    errors_by_component: Dict[str, int] = field(default_factory=dict)
    retry_attempts: int = 0
    successful_retries: int = 0
    circuit_breaker_trips: int = 0
    recovery_time_avg: float = 0.0

    def __post_init__(self):
        """Initialize default values."""
        if not self.errors_by_severity:
            for severity in ErrorSeverity:
                self.errors_by_severity[severity.value] = 0

    def record_error(self, context: ErrorContext):
        """Record an error in metrics."""
        self.total_errors += 1
        severity_key = context.severity.value
        self.errors_by_severity[severity_key] += 1
        self.errors_by_component[context.component] += 1

    def record_retry(self, successful: bool):
        """Record a retry attempt."""
        self.retry_attempts += 1
        if successful:
            self.successful_retries += 1

    def get_retry_success_rate(self) -> float:
        """Calculate retry success rate."""
        if self.retry_attempts == 0:
            return 0.0
        return self.successful_retries / self.retry_attempts

# ================================
# UTILITY FUNCTIONS
# ================================

def create_error_context(
    operation: str,
    component: str,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    details: Optional[Dict[str, Any]] = None,
    max_retries: int = 3
) -> ErrorContext:
    """Create a new error context with current timestamp."""
    return ErrorContext(
        operation=operation,
        component=component,
        timestamp=datetime.now(),
        severity=severity,
        details=details or {},
        max_retries=max_retries
    )

def validate_error_configurations() -> bool:
    """Validate error handling configurations."""
    config = get_unified_config()

    # Validate severity levels exist
    try:
        ErrorSeverity.LOW
        ErrorSeverity.MEDIUM
        ErrorSeverity.HIGH
        ErrorSeverity.CRITICAL
    except AttributeError:
        config.get_logger(__name__).error("ErrorSeverity enum is incomplete")
        return False

    # Validate circuit states exist
    try:
        CircuitState.CLOSED
        CircuitState.OPEN
        CircuitState.HALF_OPEN
    except AttributeError:
        config.get_logger(__name__).error("CircuitState enum is incomplete")
        return False

    return True

# ================================
# INITIALIZATION
# ================================

# Validate error configurations on import
if not validate_error_configurations():
    raise ValueError("Error configurations validation failed")

# ================================
# EXPORTS
# ================================

__all__ = [
    "ErrorSeverity",
    "CircuitState",
    "ErrorContext",
    "CircuitBreakerConfig",
    "RetryConfig",
    "ErrorMetrics",
    "create_error_context",
    "validate_error_configurations"
]

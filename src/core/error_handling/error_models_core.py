"""
Error Models Core - V2 Compliance Error Handling Core Models
============================================================

Core data models for error handling system with V2 compliance standards.

V2 COMPLIANCE: Type-safe error models with validation
DESIGN PATTERN: Dataclass pattern for error model definitions
DEPENDENCY INJECTION: Configuration-driven error handling parameters

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - Error Models Core Optimized
"""

from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Type, List
from .error_models_enums import ErrorSeverity, CircuitState, ErrorType, RetryStrategy


@dataclass
class ErrorContext:
    """Error context with V2 compliance."""
    error_id: str
    error_type: ErrorType
    severity: ErrorSeverity
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "unknown"
    stack_trace: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    context_data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization validation."""
        if not self.error_id:
            raise ValueError("error_id is required")
        if not self.message:
            raise ValueError("message is required")


@dataclass
class CircuitBreakerConfig:
    """Circuit breaker configuration with V2 compliance."""
    name: str
    failure_threshold: int = 5
    recovery_timeout: int = 60
    expected_exception: Type[Exception] = Exception
    success_threshold: int = 3
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization validation."""
        if not self.name:
            raise ValueError("name is required")
        if self.failure_threshold <= 0:
            raise ValueError("failure_threshold must be positive")
        if self.recovery_timeout <= 0:
            raise ValueError("recovery_timeout must be positive")
        if self.success_threshold <= 0:
            raise ValueError("success_threshold must be positive")


@dataclass
class RetryConfig:
    """Retry configuration with V2 compliance."""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL
    backoff_multiplier: float = 2.0
    jitter: bool = True
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization validation."""
        if self.max_attempts <= 0:
            raise ValueError("max_attempts must be positive")
        if self.base_delay <= 0:
            raise ValueError("base_delay must be positive")
        if self.max_delay <= 0:
            raise ValueError("max_delay must be positive")
        if self.backoff_multiplier <= 0:
            raise ValueError("backoff_multiplier must be positive")

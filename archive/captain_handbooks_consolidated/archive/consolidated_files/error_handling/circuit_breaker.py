"""
Circuit Breaker Module - V2 Compliance Refactored
================================================

Circuit breaker pattern implementation for error handling.
Refactored into modular architecture for V2 compliance.

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import logging
from collections.abc import Callable
from datetime import datetime
from typing import Any

# Import modular components
from .circuit_breaker.core import CircuitBreakerConfig, CircuitBreakerCore, CircuitState
from .circuit_breaker.executor import CircuitBreakerExecutor

logger = logging.getLogger(__name__)


class CircuitBreaker:
    """Circuit breaker implementation for fault tolerance - V2 compliant."""

    def __init__(self, config: CircuitBreakerConfig):
        """Initialize circuit breaker."""
        self.config = config
        self.core = CircuitBreakerCore(config)
        self.executor = CircuitBreakerExecutor(self.core)

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        return self.executor.call(func, *args, **kwargs)

    def call_with_fallback(self, func: Callable, fallback_func: Callable, *args, **kwargs) -> Any:
        """Execute function with fallback if circuit breaker is open."""
        return self.executor.call_with_fallback(func, fallback_func, *args, **kwargs)

    def call_with_retry(self, func: Callable, max_retries: int = 3, *args, **kwargs) -> Any:
        """Execute function with retry logic."""
        return self.executor.call_with_retry(func, max_retries, *args, **kwargs)

    def is_available(self) -> bool:
        """Check if circuit breaker is available for calls."""
        return self.executor.is_available()

    def get_retry_after(self) -> datetime | None:
        """Get the time when the circuit breaker will be available again."""
        return self.executor.get_retry_after()

    def get_status(self) -> dict:
        """Get current circuit breaker status."""
        return self.core.get_status()

    # Backward compatibility properties
    @property
    def state(self) -> CircuitState:
        """Get current circuit state."""
        return self.core.state

    @property
    def failure_count(self) -> int:
        """Get current failure count."""
        return self.core.failure_count

    @property
    def last_failure_time(self) -> datetime | None:
        """Get last failure time."""
        return self.core.last_failure_time

    @property
    def next_attempt_time(self) -> datetime | None:
        """Get next attempt time."""
        return self.core.next_attempt_time


# Global circuit breaker registry
_circuit_breakers = {}


def get_circuit_breaker(name: str, config: CircuitBreakerConfig = None) -> CircuitBreaker:
    """Get or create circuit breaker by name."""
    if name not in _circuit_breakers:
        if config is None:
            config = CircuitBreakerConfig(name)
        _circuit_breakers[name] = CircuitBreaker(config)

    return _circuit_breakers[name]


def list_circuit_breakers() -> dict:
    """List all circuit breakers and their status."""
    return {name: breaker.get_status() for name, breaker in _circuit_breakers.items()}


def reset_circuit_breaker(name: str) -> bool:
    """Reset circuit breaker by name."""
    if name in _circuit_breakers:
        breaker = _circuit_breakers[name]
        breaker.core.failure_count = 0
        breaker.core.state = CircuitState.CLOSED
        breaker.core.next_attempt_time = None
        return True
    return False

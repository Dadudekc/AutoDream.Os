#!/usr/bin/env python3
"""
Circuit Breaker Module - Agent Cellphone V2
==========================================

Circuit breaker pattern implementation for error handling.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import time
import logging
from typing import Callable, Any, Optional
from datetime import datetime, timedelta

from .error_models import CircuitState, CircuitBreakerConfig, ErrorContext, ErrorSeverity

logger = logging.getLogger(__name__)


class CircuitBreaker:
    """Circuit breaker implementation for fault tolerance."""

    def __init__(self, config: CircuitBreakerConfig):
        """Initialize circuit breaker."""
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.next_attempt_time: Optional[datetime] = None

    def _should_attempt_reset(self) -> bool:
        """Check if we should attempt to reset the circuit."""
        if self.state != CircuitState.OPEN:
            return False

        if self.next_attempt_time is None:
            return True

        return datetime.now() >= self.next_attempt_time

    def _record_success(self):
        """Record a successful operation."""
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            self.last_failure_time = None
            self.next_attempt_time = None
            logger.info(f"Circuit breaker '{self.config.name}' reset to CLOSED state")

    def _record_failure(self, exception: Exception):
        """Record a failed operation."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            self.next_attempt_time = datetime.now() + timedelta(seconds=self.config.recovery_timeout)
            logger.warning(f"Circuit breaker '{self.config.name}' moved to OPEN state after half-open failure")
        elif self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN
            self.next_attempt_time = datetime.now() + timedelta(seconds=self.config.recovery_timeout)
            logger.warning(f"Circuit breaker '{self.config.name}' opened after {self.failure_count} failures")

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            if not self._should_attempt_reset():
                raise CircuitBreakerOpenException(
                    f"Circuit breaker '{self.config.name}' is OPEN",
                    retry_after=self.next_attempt_time
                )

            self.state = CircuitState.HALF_OPEN
            logger.info(f"Circuit breaker '{self.config.name}' testing recovery (HALF_OPEN)")

        try:
            result = func(*args, **kwargs)
            self._record_success()
            return result

        except self.config.expected_exception as e:
            self._record_failure(e)
            raise

    def get_status(self) -> dict:
        """Get current circuit breaker status."""
        return {
            "name": self.config.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "failure_threshold": self.config.failure_threshold,
            "recovery_timeout": self.config.recovery_timeout,
            "last_failure_time": self.last_failure_time.isoformat() if self.last_failure_time else None,
            "next_attempt_time": self.next_attempt_time.isoformat() if self.next_attempt_time else None
        }


class CircuitBreakerOpenException(Exception):
    """Exception raised when circuit breaker is open."""

    def __init__(self, message: str, retry_after: Optional[datetime] = None):
        super().__init__(message)
        self.retry_after = retry_after

    def retry_in_seconds(self) -> Optional[float]:
        """Get seconds until retry is allowed."""
        if self.retry_after is None:
            return None
        return max(0, (self.retry_after - datetime.now()).total_seconds())


def circuit_breaker(config: CircuitBreakerConfig):
    """Decorator for applying circuit breaker pattern to functions."""
    breaker = CircuitBreaker(config)

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            return breaker.call(func, *args, **kwargs)
        return wrapper

    return decorator

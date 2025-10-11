"""
Circuit Breaker Module
======================

Circuit breaker pattern implementation extracted for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactor)
License: MIT
"""

import logging
from datetime import datetime, timedelta
from typing import Any

from .error_handling_core import CircuitBreakerConfig, CircuitBreakerError, CircuitState

logger = logging.getLogger(__name__)


class CircuitBreaker:
    """Circuit breaker pattern for preventing cascading failures."""

    def __init__(self, config: CircuitBreakerConfig):
        """Initialize circuit breaker."""
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.opened_at = None

    def call(self, func, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info(f"Circuit breaker entering half-open state for {self.config.name}")
            else:
                raise CircuitBreakerError(f"Circuit breaker is OPEN for {self.config.name}")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if not self.opened_at:
            return False
        return datetime.now() - self.opened_at >= timedelta(seconds=self.config.timeout)

    def _on_success(self):
        """Handle successful call."""
        if self.state == CircuitState.HALF_OPEN:
            logger.info(f"Circuit breaker reset to CLOSED for {self.config.name}")
            self.state = CircuitState.CLOSED
        self.failure_count = 0

    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN
            self.opened_at = datetime.now()
            logger.warning(
                f"Circuit breaker opened after {self.failure_count} failures for {self.config.name}"
            )

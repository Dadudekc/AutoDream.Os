#!/usr/bin/env python3
"""
Error Handling Configuration
=============================

Configuration classes for retry logic and circuit breakers.
Extracted from error_handling_core.py for V2 compliance.

Author: Agent-6 - Quality Gates & VSCode Specialist (V2 Refactor)
Original: Agent-3 - Infrastructure & DevOps Specialist (C-055-3)
License: MIT
"""

import random
from dataclasses import dataclass


@dataclass
class RetryConfig:
    """Unified retry configuration (consolidated from multiple sources)."""

    max_attempts: int = 3
    base_delay: float = 1.0
    backoff_factor: float = 2.0
    max_delay: float = 60.0
    jitter: bool = True
    exceptions: tuple = (Exception,)

    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt with exponential backoff and jitter."""
        delay = self.base_delay * (self.backoff_factor**attempt)

        # Apply maximum delay limit
        delay = min(delay, self.max_delay)

        # Apply jitter if enabled
        if self.jitter:
            jitter_range = delay * 0.1  # 10% jitter
            delay += random.uniform(-jitter_range, jitter_range)
            delay = max(0.1, delay)  # Minimum 100ms delay

        return delay


@dataclass
class CircuitBreakerConfig:
    """Circuit breaker configuration."""

    name: str
    failure_threshold: int = 5
    recovery_timeout: float = 60.0


class RecoverableErrors:
    """Recoverable error types."""

    TYPES = (ConnectionError, TimeoutError, OSError, FileNotFoundError, PermissionError)


class ErrorSeverityMapping:
    """Error severity mapping."""

    CRITICAL = (SystemError, MemoryError, KeyboardInterrupt)
    HIGH = (ValueError, TypeError, AttributeError, KeyError)
    MEDIUM = (FileNotFoundError, PermissionError, ConnectionError)
    # All others are LOW severity


__all__ = [
    "RetryConfig",
    "CircuitBreakerConfig",
    "RecoverableErrors",
    "ErrorSeverityMapping",
]

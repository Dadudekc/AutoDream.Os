#!/usr/bin/env python3
"""
Error Handling Exceptions
==========================

Custom exceptions for error handling system.
Extracted from error_handling_core.py for V2 compliance.

Author: Agent-6 - Quality Gates & VSCode Specialist (V2 Refactor)
Original: Agent-3 - Infrastructure & DevOps Specialist (C-055-3)
License: MIT
"""


class RetryException(Exception):
    """Exception raised to trigger retry mechanism."""

    pass


class CircuitBreakerError(Exception):
    """Exception raised when circuit breaker is OPEN."""

    pass


__all__ = [
    "RetryException",
    "CircuitBreakerError",
]

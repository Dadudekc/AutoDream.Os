#!/usr/bin/env python3
"""
Error Models Module - Agent Cellphone V2
=====================================

Data models and enums for error handling system.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from datetime import datetime
from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "CLOSED"      # Normal operation
    OPEN = "OPEN"          # Circuit is open, requests fail fast
    HALF_OPEN = "HALF_OPEN"  # Testing if service is recovered


@dataclass
class ErrorContext:
    """Context information for error handling."""
    operation: str
    component: str
    timestamp: datetime
    severity: ErrorSeverity
    details: Dict[str, Any] = None
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker pattern."""
    failure_threshold: int = 5
    recovery_timeout: int = 60
    expected_exception: Exception = Exception
    name: str = "default"


@dataclass
class RetryConfig:
    """Configuration for retry mechanisms."""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    backoff_factor: float = 2.0
    jitter: bool = True

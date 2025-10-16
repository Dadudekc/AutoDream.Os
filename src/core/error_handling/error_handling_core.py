#!/usr/bin/env python3
"""
Error Handling Core Models - V2 Compliant
==========================================

Consolidated data models, enums, and configurations for unified error handling.

Consolidates:
- error_handling_models.py (models, enums, response classes)
- Part of retry_mechanisms.py (RetryConfig)

DUP-006 Enhancement (Agent-8, 2025-10-17):
- Added ErrorSeverity → LogLevel mapping (coordination with DUP-007)
- Integrated with Agent-2's standardized_logging.py
- Unified error/logging format

Author: Agent-3 - Infrastructure & DevOps Specialist
Enhanced: Agent-8 - SSOT & System Integration Specialist (DUP-006)
Created: 2025-10-10 (C-055-3 Consolidation)
Enhanced: 2025-10-17 (DUP-006 Error/Logging Coordination)
Purpose: V2 compliant error handling core models (single source of truth)
"""

import random
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

# DUP-006/007 Coordination: Import Agent-2's standardized logging
try:
    from ..utilities.standardized_logging import LogLevel
    _LOGGING_AVAILABLE = True
except ImportError:
    _LOGGING_AVAILABLE = False

# ============================================================================
# ENUMS AND CONSTANTS
# ============================================================================


class ErrorSeverity(Enum):
    """Error severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error category types."""

    OPERATION = "operation"
    FILE = "file"
    NETWORK = "network"
    DATABASE = "database"
    VALIDATION = "validation"
    CONFIGURATION = "configuration"
    AGENT = "agent"
    COORDINATION = "coordination"


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


# ============================================================================
# ERROR CONTEXT AND RESPONSES
# ============================================================================


@dataclass
class ErrorContext:
    """Error context information."""

    operation: str
    timestamp: str
    error_type: str
    category: ErrorCategory
    severity: ErrorSeverity
    additional_data: dict[str, Any]


@dataclass
class StandardErrorResponse:
    """Standardized error response format."""

    success: bool = False
    error: str = ""
    error_type: str = ""
    operation: str = ""
    timestamp: str = ""
    context: dict[str, Any] = None

    def __post_init__(self):
        if self.context is None:
            self.context = {}
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "error": self.error,
            "error_type": self.error_type,
            "operation": self.operation,
            "timestamp": self.timestamp,
            "context": self.context,
        }


@dataclass
class FileErrorResponse(StandardErrorResponse):
    """File operation error response."""

    file_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        result["file_path"] = self.file_path
        return result


@dataclass
class NetworkErrorResponse(StandardErrorResponse):
    """Network operation error response."""

    url: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        result["url"] = self.url
        return result


@dataclass
class DatabaseErrorResponse(StandardErrorResponse):
    """Database operation error response."""

    table: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        result["table"] = self.table
        return result


@dataclass
class ValidationErrorResponse(StandardErrorResponse):
    """Validation error response."""

    validation_type: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        result["validation_type"] = self.validation_type
        return result


@dataclass
class ConfigurationErrorResponse(StandardErrorResponse):
    """Configuration error response."""

    config_key: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        result["config_key"] = self.config_key
        return result


@dataclass
class AgentErrorResponse(StandardErrorResponse):
    """Agent operation error response."""

    agent_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        result["agent_id"] = self.agent_id
        return result


@dataclass
class CoordinationErrorResponse(StandardErrorResponse):
    """Coordination error response."""

    coordination_type: str = ""
    participants: list[str] = None

    def __post_init__(self):
        super().__post_init__()
        if self.participants is None:
            self.participants = []

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        result["coordination_type"] = self.coordination_type
        result["participants"] = self.participants
        return result


# ============================================================================
# ERROR SUMMARY AND STATISTICS
# ============================================================================


@dataclass
class ErrorSummary:
    """Error summary statistics."""

    total_errors: int = 0
    error_types: dict[str, int] = None
    operations: dict[str, int] = None
    timestamp: str = ""

    def __post_init__(self):
        if self.error_types is None:
            self.error_types = {}
        if self.operations is None:
            self.operations = {}
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_errors": self.total_errors,
            "error_types": self.error_types,
            "operations": self.operations,
            "timestamp": self.timestamp,
        }


# ============================================================================
# CONFIGURATION CLASSES
# ============================================================================


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


# ============================================================================
# ERROR TYPE MAPPINGS
# ============================================================================


class RecoverableErrors:
    """Recoverable error types."""

    TYPES = (ConnectionError, TimeoutError, OSError, FileNotFoundError, PermissionError)


class ErrorSeverityMapping:
    """Error severity mapping."""

    CRITICAL = (SystemError, MemoryError, KeyboardInterrupt)
    HIGH = (ValueError, TypeError, AttributeError, KeyError)
    MEDIUM = (FileNotFoundError, PermissionError, ConnectionError)
    # All others are LOW severity


# ============================================================================
# DUP-006/007 COORDINATION: ErrorSeverity → LogLevel Mapping
# ============================================================================


def get_log_level_for_severity(severity: ErrorSeverity) -> int:
    """Map ErrorSeverity to LogLevel for coordinated error/logging.
    
    DUP-006/007 Coordination: Integrates error handling with Agent-2's standardized logging.
    
    Args:
        severity: Error severity level
        
    Returns:
        Logging level (int) compatible with logging module
    """
    if _LOGGING_AVAILABLE:
        mapping = {
            ErrorSeverity.CRITICAL: LogLevel.CRITICAL.value,
            ErrorSeverity.HIGH: LogLevel.ERROR.value,
            ErrorSeverity.MEDIUM: LogLevel.WARNING.value,
            ErrorSeverity.LOW: LogLevel.INFO.value,
        }
        return mapping.get(severity, LogLevel.ERROR.value)
    else:
        # Fallback to standard logging levels
        import logging
        mapping = {
            ErrorSeverity.CRITICAL: logging.CRITICAL,
            ErrorSeverity.HIGH: logging.ERROR,
            ErrorSeverity.MEDIUM: logging.WARNING,
            ErrorSeverity.LOW: logging.INFO,
        }
        return mapping.get(severity, logging.ERROR)


# ============================================================================
# EXCEPTIONS
# ============================================================================


class RetryException(Exception):
    """Exception raised to trigger retry mechanism."""

    pass


class CircuitBreakerError(Exception):
    """Exception raised when circuit breaker is OPEN."""

    pass


# ============================================================================
# DUP-006 ENHANCEMENT: Unified Exception Logging
# ============================================================================


def log_exception_with_severity(
    logger,
    severity: ErrorSeverity,
    exception: Exception,
    context: dict[str, Any] = None
) -> None:
    """Log exception with appropriate severity level.
    
    DUP-006/007 Coordination: Unified exception logging using Agent-2's standardized logging.
    
    Args:
        logger: Logger instance (from standardized_logging.get_logger)
        severity: Error severity level
        exception: Exception to log
        context: Additional context dictionary
    """
    log_level = get_log_level_for_severity(severity)
    context_str = f" | Context: {context}" if context else ""
    logger.log(log_level, f"Exception: {type(exception).__name__}: {exception}{context_str}", exc_info=True)

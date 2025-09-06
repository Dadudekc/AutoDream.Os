#!/usr/bin/env python3
"""
Error Handling Models - V2 Compliant
===================================

Data models and response formats for unified error handling.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
Created: 2025-01-27
Purpose: V2 compliant error handling data models
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


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


@dataclass
class ErrorContext:
    """Error context information."""

    operation: str
    timestamp: str
    error_type: str
    category: ErrorCategory
    severity: ErrorSeverity
    additional_data: Dict[str, Any]


@dataclass
class StandardErrorResponse:
    """Standardized error response format."""

    success: bool = False
    error: str = ""
    error_type: str = ""
    operation: str = ""
    timestamp: str = ""
    context: Dict[str, Any] = None

    def __post_init__(self):
        if self.context is None:
            self.context = {}
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
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

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        result["file_path"] = self.file_path
        return result


@dataclass
class NetworkErrorResponse(StandardErrorResponse):
    """Network operation error response."""

    url: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        result["url"] = self.url
        return result


@dataclass
class DatabaseErrorResponse(StandardErrorResponse):
    """Database operation error response."""

    table: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        result["table"] = self.table
        return result


@dataclass
class ValidationErrorResponse(StandardErrorResponse):
    """Validation error response."""

    validation_type: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        result["validation_type"] = self.validation_type
        return result


@dataclass
class ConfigurationErrorResponse(StandardErrorResponse):
    """Configuration error response."""

    config_key: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        result["config_key"] = self.config_key
        return result


@dataclass
class AgentErrorResponse(StandardErrorResponse):
    """Agent operation error response."""

    agent_id: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        result["agent_id"] = self.agent_id
        return result


@dataclass
class CoordinationErrorResponse(StandardErrorResponse):
    """Coordination error response."""

    coordination_type: str = ""
    participants: List[str] = None

    def __post_init__(self):
        super().__post_init__()
        if self.participants is None:
            self.participants = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        result["coordination_type"] = self.coordination_type
        result["participants"] = self.participants
        return result


@dataclass
class ErrorSummary:
    """Error summary statistics."""

    total_errors: int = 0
    error_types: Dict[str, int] = None
    operations: Dict[str, int] = None
    timestamp: str = ""

    def __post_init__(self):
        if self.error_types is None:
            self.error_types = {}
        if self.operations is None:
            self.operations = {}
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_errors": self.total_errors,
            "error_types": self.error_types,
            "operations": self.operations,
            "timestamp": self.timestamp,
        }


class RecoverableErrors:
    """Recoverable error types."""

    TYPES = (ConnectionError, TimeoutError, OSError, FileNotFoundError, PermissionError)


class ErrorSeverityMapping:
    """Error severity mapping."""

    CRITICAL = (SystemError, MemoryError, KeyboardInterrupt)
    HIGH = (ValueError, TypeError, AttributeError, KeyError)
    MEDIUM = (FileNotFoundError, PermissionError, ConnectionError)
    # All others are LOW severity


class RetryConfiguration:
    """Retry operation configuration."""

    def __init__(
        self,
        max_retries: int = 3,
        delay: float = 1.0,
        backoff_factor: float = 2.0,
        exceptions: tuple = (Exception,),
    ):
        self.max_retries = max_retries
        self.delay = delay
        self.backoff_factor = backoff_factor
        self.exceptions = exceptions

    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt."""
        return self.delay * (self.backoff_factor**attempt)

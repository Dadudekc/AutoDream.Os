#!/usr/bin/env python3
"""
Error Response Models
=====================

Error response classes for comprehensive error handling.
Extracted from error_handling_models.py for V2 compliance (class count limit).

Author: Agent-3 (Infrastructure & DevOps) - ROI Refactoring (500 pts, ROI 33.33)
License: MIT
"""

from dataclasses import dataclass
from typing import Any

from .error_models_enums import ErrorCategory, ErrorRecoverability, ErrorSeverity


@dataclass
class BaseErrorResponse:
    """Base error response with common fields."""

    error_type: str
    message: str
    severity: ErrorSeverity
    category: ErrorCategory
    recoverability: ErrorRecoverability
    timestamp: str
    context: dict[str, Any]
    suggested_recovery: str | None = None
    stacktrace: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "error_type": self.error_type,
            "message": self.message,
            "severity": self.severity.value,
            "category": self.category.value,
            "recoverability": self.recoverability.value,
            "timestamp": self.timestamp,
            "context": self.context,
            "suggested_recovery": self.suggested_recovery,
            "stacktrace": self.stacktrace,
        }


@dataclass
class RecoverableErrorResponse(BaseErrorResponse):
    """Error response for recoverable errors."""

    recovery_attempted: bool = False
    recovery_success: bool = False


@dataclass
class FileErrorResponse(RecoverableErrorResponse):
    """Error response for file operation errors."""

    filepath: str | None = None


@dataclass
class NetworkErrorResponse(RecoverableErrorResponse):
    """Error response for network/connection errors."""

    endpoint: str | None = None
    retry_count: int = 0


@dataclass
class DatabaseErrorResponse(RecoverableErrorResponse):
    """Error response for database operation errors."""

    query: str | None = None
    connection_info: dict | None = None
    transaction_id: str | None = None


@dataclass
class CriticalErrorResponse(BaseErrorResponse):
    """Error response for critical system errors."""

    requires_intervention: bool = True
    system_state: dict | None = None


@dataclass
class ValidationErrorResponse(CriticalErrorResponse):
    """Error response for validation failures."""

    validation_rules: list[str] | None = None


@dataclass
class ConfigurationErrorResponse(CriticalErrorResponse):
    """Error response for configuration errors."""

    config_key: str | None = None
    expected_type: str | None = None
    actual_value: Any | None = None


@dataclass
class AgentErrorResponse(RecoverableErrorResponse):
    """Error response for agent-specific errors."""

    agent_id: str | None = None


@dataclass
class CoordinationErrorResponse(RecoverableErrorResponse):
    """Error response for coordination/communication errors."""

    affected_agents: list[str] = None
    coordination_context: dict[str, Any] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.affected_agents is None:
            self.affected_agents = []
        if self.coordination_context is None:
            self.coordination_context = {}

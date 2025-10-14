#!/usr/bin/env python3
"""
Specialized Error Response Models
==================================

Domain-specific error response classes.
Extracted from error_handling_core.py for V2 compliance.

Author: Agent-6 - Quality Gates & VSCode Specialist (V2 Refactor)
Original: Agent-3 - Infrastructure & DevOps Specialist (C-055-3)
License: MIT
"""

from dataclasses import dataclass
from typing import Any

from .error_responses import StandardErrorResponse


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


@dataclass
class ErrorSummary:
    """Error summary statistics."""

    total_errors: int = 0
    error_types: dict[str, int] = None
    operations: dict[str, int] = None
    timestamp: str = ""

    def __post_init__(self):
        from datetime import datetime

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


__all__ = [
    "ValidationErrorResponse",
    "ConfigurationErrorResponse",
    "AgentErrorResponse",
    "CoordinationErrorResponse",
    "ErrorSummary",
]

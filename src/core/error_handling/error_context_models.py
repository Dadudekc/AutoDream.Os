#!/usr/bin/env python3
"""
Error Context Models
====================

Error context and summary models for error tracking and analysis.
Extracted from error_handling_models.py for V2 compliance.

Author: Agent-3 (Infrastructure & DevOps) - ROI Refactoring (500 pts, ROI 33.33)
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ErrorContext:
    """
    Error context information for debugging and recovery.

    Provides comprehensive context about error occurrence including:
    - Component and operation information
    - Execution environment details
    - Error metadata and timing
    """

    component: str
    operation: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)
    environment: dict[str, str] = field(default_factory=dict)
    stack_depth: int = 0
    execution_id: str | None = None

    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to context."""
        self.metadata[key] = value

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "component": self.component,
            "operation": self.operation,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "environment": self.environment,
            "stack_depth": self.stack_depth,
            "execution_id": self.execution_id,
        }


@dataclass
class ErrorSummary:
    """
    Error summary for reporting and analysis.

    Aggregates error information for monitoring and intelligence.
    """

    total_errors: int = 0
    by_severity: dict[str, int] = field(
        default_factory=lambda: {"critical": 0, "high": 0, "medium": 0, "low": 0}
    )
    by_category: dict[str, int] = field(
        default_factory=lambda: {
            "system": 0,
            "network": 0,
            "file": 0,
            "database": 0,
            "validation": 0,
            "configuration": 0,
        }
    )
    recoverable_count: int = 0
    critical_count: int = 0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def increment_severity(self, severity: str) -> None:
        """Increment count for a severity level."""
        severity_lower = severity.lower()
        if severity_lower in self.by_severity:
            self.by_severity[severity_lower] += 1
        self.total_errors += 1

    def increment_category(self, category: str) -> None:
        """Increment count for a category."""
        category_lower = category.lower()
        if category_lower in self.by_category:
            self.by_category[category_lower] += 1

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for reporting."""
        return {
            "total_errors": self.total_errors,
            "by_severity": self.by_severity,
            "by_category": self.by_category,
            "recoverable_count": self.recoverable_count,
            "critical_count": self.critical_count,
            "timestamp": self.timestamp,
        }

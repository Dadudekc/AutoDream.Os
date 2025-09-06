"""
Error Metrics - V2 Compliance Module
===================================

Error metrics functionality for error handling system.

V2 Compliance: < 300 lines, single responsibility, error metrics.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, Any, List

from ..error_models_enums import ErrorSeverity, ErrorType


@dataclass
class ErrorMetrics:
    """Error metrics with V2 compliance."""

    metrics_id: str
    time_period: str
    total_errors: int = 0
    errors_by_severity: Dict[str, int] = field(default_factory=dict)
    errors_by_type: Dict[str, int] = field(default_factory=dict)
    errors_by_source: Dict[str, int] = field(default_factory=dict)
    average_resolution_time: float = 0.0
    success_rate: float = 0.0
    circuit_breaker_trips: int = 0
    retry_attempts: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization validation."""
        if not self.metrics_id:
            raise ValueError("metrics_id is required")
        if not self.time_period:
            raise ValueError("time_period is required")

    def add_error(
        self, severity: ErrorSeverity, error_type: ErrorType, source: str
    ) -> None:
        """Add error to metrics."""
        self.total_errors += 1
        self.errors_by_severity[severity.value] = (
            self.errors_by_severity.get(severity.value, 0) + 1
        )
        self.errors_by_type[error_type.value] = (
            self.errors_by_type.get(error_type.value, 0) + 1
        )
        self.errors_by_source[source] = self.errors_by_source.get(source, 0) + 1

    def calculate_success_rate(self, total_operations: int) -> None:
        """Calculate success rate."""
        if total_operations > 0:
            self.success_rate = (
                total_operations - self.total_errors
            ) / total_operations
        else:
            self.success_rate = 0.0

    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary."""
        return {
            "metrics_id": self.metrics_id,
            "time_period": self.time_period,
            "total_errors": self.total_errors,
            "success_rate": self.success_rate,
            "average_resolution_time": self.average_resolution_time,
            "circuit_breaker_trips": self.circuit_breaker_trips,
            "retry_attempts": self.retry_attempts,
        }

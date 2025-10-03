"""
Error Tracker - V2 Compliant Main Interface
===========================================

Main interface for error tracking system.
V2 Compliance: ≤400 lines, single responsibility, KISS principle
"""

from dataclasses import dataclass
from typing import Any

from .error_tracker_core import ErrorTrackerCore
from .error_tracker_models import ErrorCategory, ErrorInfo, ErrorSeverity, ErrorSummary


@dataclass
class ErrorContext:
    """Error tracking context."""

    context: dict[str, Any] = None
    service_name: str = "unknown"
    user_id: str = None
    trace_id: str = None


class ErrorTracker:
    """Main error tracker interface."""

    def __init__(self, max_errors: int = 1000):
        """Initialize error tracker."""
        self.core = ErrorTrackerCore(max_errors)

    def track_error(self, error: Exception, ctx: ErrorContext = None) -> ErrorInfo:
        """Track an error."""
        if ctx is None:
            ctx = ErrorContext()
        return self.core.track_error(
            error, ctx.context, ctx.service_name, ctx.user_id, ctx.trace_id
        )

    def get_error_summary(self, hours: int = 24) -> ErrorSummary:
        """Get error summary for specified time period."""
        return self.core.get_error_summary(hours)

    def get_errors_by_severity(self, severity: ErrorSeverity) -> list[ErrorInfo]:
        """Get errors by severity level."""
        return self.core.get_errors_by_severity(severity)

    def get_errors_by_category(self, category: ErrorCategory) -> list[ErrorInfo]:
        """Get errors by category."""
        return self.core.get_errors_by_category(category)

    def get_errors_by_service(self, service_name: str) -> list[ErrorInfo]:
        """Get errors by service name."""
        return self.core.get_errors_by_service(service_name)

    def clear_errors(self):
        """Clear all tracked errors."""
        self.core.clear_errors()


# Global instance for backward compatibility
error_tracker = ErrorTracker()


def track_error(error: Exception, ctx: ErrorContext = None) -> ErrorInfo:
    """Track an error."""
    if ctx is None:
        ctx = ErrorContext()
    return error_tracker.track_error(error, ctx)


def get_error_summary(hours: int = 24) -> ErrorSummary:
    """Get error summary for specified time period."""
    return error_tracker.get_error_summary(hours)


def get_errors_by_severity(severity: ErrorSeverity) -> list[ErrorInfo]:
    """Get errors by severity level."""
    return error_tracker.get_errors_by_severity(severity)


def get_errors_by_category(category: ErrorCategory) -> list[ErrorInfo]:
    """Get errors by category."""
    return error_tracker.get_errors_by_category(category)


def get_errors_by_service(service_name: str) -> list[ErrorInfo]:
    """Get errors by service name."""
    return error_tracker.get_errors_by_service(service_name)


def clear_errors():
    """Clear all tracked errors."""
    error_tracker.clear_errors()

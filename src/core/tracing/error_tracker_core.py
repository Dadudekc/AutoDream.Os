"""
Error Tracker Core - V2 Compliant
==================================

Core error tracking functionality.
V2 Compliance: ≤400 lines, single responsibility, KISS principle
"""

import logging
import traceback
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Any

from .error_tracker_models import ErrorCategory, ErrorInfo, ErrorSeverity, ErrorSummary


class ErrorTrackerCore:
    """Core error tracking functionality."""

    def __init__(self, max_errors: int = 1000):
        """Initialize error tracker core."""
        self.max_errors = max_errors
        self.errors = deque(maxlen=max_errors)
        self.error_counts = defaultdict(int)
        self.severity_counts = defaultdict(int)
        self.category_counts = defaultdict(int)
        self.service_counts = defaultdict(int)
        self.logger = logging.getLogger(__name__)

    def track_error(
        self,
        error: Exception,
        context: dict[str, Any] = None,
        service_name: str = "unknown",
        user_id: str = None,
        trace_id: str = None,
    ) -> ErrorInfo:
        """Track an error."""
        error_info = ErrorInfo(
            error_id=self._generate_error_id(),
            error_type=type(error).__name__,
            error_message=str(error),
            severity=self._determine_severity(error),
            category=self._determine_category(error),
            stack_trace=traceback.format_exc(),
            context=context or {},
            user_id=user_id,
            timestamp=datetime.now(),
            service_name=service_name,
            trace_id=trace_id,
        )

        self._update_counts(error_info)
        self.errors.append(error_info)

        self.logger.error(f"Error tracked: {error_info.error_id} - {error_info.error_message}")
        return error_info

    def get_error_summary(self, hours: int = 24) -> ErrorSummary:
        """Get error summary for specified time period."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_errors = [e for e in self.errors if e.timestamp >= cutoff_time]

        errors_by_severity = defaultdict(int)
        errors_by_category = defaultdict(int)
        errors_by_service = defaultdict(int)

        for error in recent_errors:
            errors_by_severity[error.severity.value] += 1
            errors_by_category[error.category.value] += 1
            errors_by_service[error.service_name] += 1

        critical_errors = [e for e in recent_errors if e.severity == ErrorSeverity.CRITICAL]

        return ErrorSummary(
            total_errors=len(recent_errors),
            errors_by_severity=dict(errors_by_severity),
            errors_by_category=dict(errors_by_category),
            errors_by_service=dict(errors_by_service),
            recent_errors=recent_errors[-10:],  # Last 10 errors
            critical_errors=critical_errors,
        )

    def get_errors_by_severity(self, severity: ErrorSeverity) -> list[ErrorInfo]:
        """Get errors by severity level."""
        return [e for e in self.errors if e.severity == severity]

    def get_errors_by_category(self, category: ErrorCategory) -> list[ErrorInfo]:
        """Get errors by category."""
        return [e for e in self.errors if e.category == category]

    def get_errors_by_service(self, service_name: str) -> list[ErrorInfo]:
        """Get errors by service name."""
        return [e for e in self.errors if e.service_name == service_name]

    def clear_errors(self):
        """Clear all tracked errors."""
        self.errors.clear()
        self.error_counts.clear()
        self.severity_counts.clear()
        self.category_counts.clear()
        self.service_counts.clear()

    def _generate_error_id(self) -> str:
        """Generate unique error ID."""
        return f"err_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.errors)}"

    def _determine_severity(self, error: Exception) -> ErrorSeverity:
        """Determine error severity based on error type."""
        error_type = type(error).__name__.lower()

        if any(critical in error_type for critical in ["critical", "fatal", "panic"]):
            return ErrorSeverity.CRITICAL
        elif any(high in error_type for high in ["error", "exception", "failure"]):
            return ErrorSeverity.HIGH
        elif any(medium in error_type for medium in ["warning", "timeout", "retry"]):
            return ErrorSeverity.MEDIUM
        else:
            return ErrorSeverity.LOW

    def _determine_category(self, error: Exception) -> ErrorCategory:
        """Determine error category based on error type."""
        error_type = type(error).__name__.lower()

        if any(db in error_type for db in ["database", "sql", "connection"]):
            return ErrorCategory.DATABASE
        elif any(net in error_type for net in ["network", "http", "timeout"]):
            return ErrorCategory.NETWORK
        elif any(auth in error_type for auth in ["auth", "permission", "access"]):
            return ErrorCategory.AUTHENTICATION
        elif any(val in error_type for val in ["validation", "invalid", "format"]):
            return ErrorCategory.VALIDATION
        elif any(api in error_type for api in ["api", "external", "service"]):
            return ErrorCategory.EXTERNAL_API
        elif any(sys in error_type for sys in ["system", "os", "memory"]):
            return ErrorCategory.SYSTEM
        else:
            return ErrorCategory.UNKNOWN

    def _update_counts(self, error_info: ErrorInfo):
        """Update error counts."""
        self.error_counts[error_info.error_type] += 1
        self.severity_counts[error_info.severity.value] += 1
        self.category_counts[error_info.category.value] += 1
        self.service_counts[error_info.service_name] += 1

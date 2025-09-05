"""
Error Reporting Core - Agent Cellphone V2
=========================================

Core error reporting functionality for comprehensive error tracking.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict

logger = logging.getLogger(__name__)


class ErrorReport:
    """Represents a comprehensive error report."""

    def __init__(self, component: str, time_range: timedelta = timedelta(hours=24)):
        """Initialize error report."""
        self.component = component
        self.time_range = time_range
        self.start_time = datetime.now() - time_range
        self.errors: List[Any] = []  # ErrorContext type
        self.error_counts: Dict[str, int] = defaultdict(int)
        self.severity_counts: Dict[str, int] = defaultdict(int)

    def add_error(self, error: Any):
        """Add an error to the report."""
        if hasattr(error, 'timestamp') and error.timestamp >= self.start_time:
            self.errors.append(error)
            if hasattr(error, 'operation'):
                self.error_counts[error.operation] += 1
            if hasattr(error, 'severity'):
                self.severity_counts[str(error.severity)] += 1

    def get_summary(self) -> Dict[str, Any]:
        """Get error report summary."""
        return {
            "component": self.component,
            "time_range_hours": self.time_range.total_seconds() / 3600,
            "total_errors": len(self.errors),
            "unique_operations": len(self.error_counts),
            "severity_breakdown": dict(self.severity_counts),
            "most_common_operations": sorted(
                self.error_counts.items(), key=lambda x: x[1], reverse=True
            )[:5],
        }

    def get_detailed_report(self) -> Dict[str, Any]:
        """Get detailed error report."""
        return {
            "summary": self.get_summary(),
            "errors": [
                {
                    "error_id": getattr(error, 'error_id', 'unknown'),
                    "message": getattr(error, 'message', 'unknown'),
                    "severity": str(getattr(error, 'severity', 'unknown')),
                    "timestamp": getattr(error, 'timestamp', datetime.now()).isoformat(),
                    "source": getattr(error, 'source', 'unknown'),
                }
                for error in self.errors
            ],
        }

    def clear_errors(self):
        """Clear all errors from the report."""
        self.errors.clear()
        self.error_counts.clear()
        self.severity_counts.clear()
        logger.info(f"Cleared all errors for component: {self.component}")

    def get_error_count(self) -> int:
        """Get total error count."""
        return len(self.errors)

    def get_errors_by_severity(self, severity: str) -> List[Any]:
        """Get errors filtered by severity."""
        return [
            error for error in self.errors
            if hasattr(error, 'severity') and str(error.severity) == severity
        ]

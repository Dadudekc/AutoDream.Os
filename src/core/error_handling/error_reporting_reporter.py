"""
Error Reporting Reporter - Agent Cellphone V2
=============================================

Error reporter functionality for comprehensive error tracking.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import logging
from datetime import datetime, timedelta
from typing import Any

logger = logging.getLogger(__name__)


class ErrorReporter:
    """Centralized error reporting system."""

    def __init__(self):
        """Initialize error reporter."""
        self.reports: dict[str, Any] = {}  # ErrorReport type
        self.global_error_count = 0
        self.error_history: list[Any] = []  # ErrorContext type
        self.logger = logging.getLogger(__name__)

    def create_report(self, component: str, time_range: timedelta = timedelta(hours=24)) -> Any:
        """Create a new error report for a component."""
        from .error_reporting_core import ErrorReport

        report = ErrorReport(component, time_range)
        self.reports[component] = report
        self.logger.info(f"Created error report for component: {component}")
        return report

    def get_report(self, component: str) -> Any | None:
        """Get error report for a component."""
        return self.reports.get(component)

    def get_all_reports(self) -> dict[str, Any]:
        """Get all error reports."""
        return self.reports.copy()

    def add_error_to_report(self, component: str, error: Any):
        """Add error to specific component report."""
        if component in self.reports:
            self.reports[component].add_error(error)
        else:
            # Create report if it doesn't exist
            self.create_report(component).add_error(error)

        self.global_error_count += 1
        self.error_history.append(error)
        self.logger.debug(f"Added error to {component} report")

    def get_global_summary(self) -> dict[str, Any]:
        """Get global error summary across all components."""
        total_errors = sum(report.get_error_count() for report in self.reports.values())
        component_summaries = {
            component: report.get_summary() for component, report in self.reports.items()
        }

        return {
            "total_components": len(self.reports),
            "total_errors": total_errors,
            "global_error_count": self.global_error_count,
            "component_summaries": component_summaries,
            "timestamp": datetime.now().isoformat(),
        }

    def clear_all_reports(self):
        """Clear all error reports."""
        for report in self.reports.values():
            report.clear_errors()
        self.global_error_count = 0
        self.error_history.clear()
        self.logger.info("Cleared all error reports")

    def get_errors_by_component(self, component: str) -> list[Any]:
        """Get all errors for a specific component."""
        if component in self.reports:
            return self.reports[component].errors
        return []

    def get_error_statistics(self) -> dict[str, Any]:
        """Get comprehensive error statistics."""
        if not self.reports:
            return {"message": "No error reports available"}

        total_errors = sum(report.get_error_count() for report in self.reports.values())
        avg_errors_per_component = total_errors / len(self.reports) if self.reports else 0

        return {
            "total_components": len(self.reports),
            "total_errors": total_errors,
            "average_errors_per_component": avg_errors_per_component,
            "most_error_prone_component": (
                max(self.reports.items(), key=lambda x: x[1].get_error_count())[0]
                if self.reports
                else None
            ),
            "timestamp": datetime.now().isoformat(),
        }

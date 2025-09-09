"""
Error Reporting Utilities - Agent Cellphone V2
==============================================

Utility functions for error reporting and logging system.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import logging
from datetime import timedelta
from typing import Any

logger = logging.getLogger(__name__)

# Global error reporter instance
_error_reporter: Any | None = None


def get_error_reporter() -> Any:
    """Get global error reporter instance."""
    global _error_reporter
    if _error_reporter is None:
        from .error_reporting_reporter import ErrorReporter

        _error_reporter = ErrorReporter()
    return _error_reporter


def report_error(error: Any, component: str = "unknown"):
    """Report an error to the global error reporter."""
    try:
        reporter = get_error_reporter()
        reporter.add_error_to_report(component, error)
        logger.info(f"Reported error to {component}: {getattr(error, 'error_id', 'unknown')}")
    except Exception as e:
        logger.error(f"Failed to report error: {e}")


def get_error_report(component: str = None) -> dict[str, Any]:
    """Get error report for a component or global summary."""
    try:
        reporter = get_error_reporter()

        if component:
            report = reporter.get_report(component)
            if report:
                return report.get_detailed_report()
            else:
                return {"error": f"No report found for component: {component}"}
        else:
            return reporter.get_global_summary()
    except Exception as e:
        logger.error(f"Failed to get error report: {e}")
        return {"error": str(e)}


def clear_error_reports(component: str = None):
    """Clear error reports for a component or all components."""
    try:
        reporter = get_error_reporter()

        if component:
            if component in reporter.reports:
                reporter.reports[component].clear_errors()
                logger.info(f"Cleared error report for component: {component}")
            else:
                logger.warning(f"No report found for component: {component}")
        else:
            reporter.clear_all_reports()
            logger.info("Cleared all error reports")
    except Exception as e:
        logger.error(f"Failed to clear error reports: {e}")


def get_error_statistics() -> dict[str, Any]:
    """Get comprehensive error statistics."""
    try:
        reporter = get_error_reporter()
        return reporter.get_error_statistics()
    except Exception as e:
        logger.error(f"Failed to get error statistics: {e}")
        return {"error": str(e)}


def create_component_report(component: str, time_range: timedelta = timedelta(hours=24)) -> Any:
    """Create a new error report for a component."""
    try:
        reporter = get_error_reporter()
        return reporter.create_report(component, time_range)
    except Exception as e:
        logger.error(f"Failed to create component report: {e}")
        return None

"""
Error Reporting Refactored - Agent Cellphone V2
===============================================

Refactored error reporting and logging system for comprehensive error tracking.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

# Import all error reporting components
from .error_reporting_core import ErrorReport
from .error_reporting_reporter import ErrorReporter
from .error_reporting_utilities import (
    get_error_reporter, report_error, get_error_report,
    clear_error_reports, get_error_statistics, create_component_report
)

# Re-export all public components for backward compatibility
__all__ = [
    # Core Classes
    'ErrorReport', 'ErrorReporter',
    # Utility Functions
    'get_error_reporter', 'report_error', 'get_error_report',
    'clear_error_reports', 'get_error_statistics', 'create_component_report'
]

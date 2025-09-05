#!/usr/bin/env python3
"""
Error Reporting Module - Agent Cellphone V2 (V2 Refactored)
===========================================================

V2 Refactored error reporting and logging system for comprehensive error tracking.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

# V2 Refactored - Backward Compatibility Wrapper
from .error_reporting_refactored import *

# Maintain backward compatibility
__all__ = [
    # Core Classes
    'ErrorReport', 'ErrorReporter',
    # Utility Functions
    'get_error_reporter', 'report_error', 'get_error_report',
    'clear_error_reports', 'get_error_statistics', 'create_component_report'
]
"""
Error Models Metrics - V2 Compliance Refactored
==============================================

Metrics and analytics models for error handling system with V2 compliance standards.
Refactored into modular architecture for V2 compliance.

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, Any, List

from .error_models_enums import ErrorSeverity, ErrorType

# Import modular components
from .metrics.error_metrics import ErrorMetrics
from .metrics.error_reports import ErrorReport
from .metrics.error_alerts import ErrorAlert

# Re-export for backward compatibility
__all__ = [
    'ErrorMetrics',
    'ErrorReport', 
    'ErrorAlert',
    'ErrorSeverity',
    'ErrorType'
]

# Backward compatibility - create aliases
ErrorMetrics = ErrorMetrics
ErrorReport = ErrorReport
ErrorAlert = ErrorAlert
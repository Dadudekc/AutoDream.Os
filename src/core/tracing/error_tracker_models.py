"""
Error Tracker Models - V2 Compliant
====================================

Data models for error tracking system.
V2 Compliance: ≤400 lines, ≤5 classes, KISS principle
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ErrorSeverity(Enum):
    """Error severity levels."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories."""
    
    SYSTEM = "system"
    DATABASE = "database"
    NETWORK = "network"
    AUTHENTICATION = "authentication"
    VALIDATION = "validation"
    BUSINESS_LOGIC = "business_logic"
    EXTERNAL_API = "external_api"
    UNKNOWN = "unknown"


@dataclass
class ErrorInfo:
    """Error information structure."""
    
    error_id: str
    error_type: str
    error_message: str
    severity: ErrorSeverity
    category: ErrorCategory
    stack_trace: str
    context: Dict[str, Any]
    user_id: Optional[str]
    timestamp: datetime
    service_name: str
    trace_id: Optional[str]


@dataclass
class ErrorSummary:
    """Error summary structure."""
    
    total_errors: int
    errors_by_severity: Dict[str, int]
    errors_by_category: Dict[str, int]
    errors_by_service: Dict[str, int]
    recent_errors: List[ErrorInfo]
    critical_errors: List[ErrorInfo]


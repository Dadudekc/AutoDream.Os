"""
Error Models Metrics - V2 Compliance Error Handling Metrics
===========================================================

Metrics and analytics models for error handling system with V2 compliance standards.

V2 COMPLIANCE: Type-safe error metrics with validation
DESIGN PATTERN: Dataclass pattern for error metrics definitions
DEPENDENCY INJECTION: Configuration-driven error handling parameters

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - Error Models Metrics Optimized
"""

from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, Any, List
from .error_models_enums import ErrorSeverity, ErrorType


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


@dataclass
class ErrorReport:
    """Error report with V2 compliance."""
    report_id: str
    title: str
    summary: str
    error_count: int = 0
    severity_distribution: Dict[str, int] = field(default_factory=dict)
    type_distribution: Dict[str, int] = field(default_factory=dict)
    source_distribution: Dict[str, int] = field(default_factory=dict)
    resolution_times: List[float] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = "system"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization validation."""
        if not self.report_id:
            raise ValueError("report_id is required")
        if not self.title:
            raise ValueError("title is required")
        if not self.summary:
            raise ValueError("summary is required")


@dataclass
class ErrorAlert:
    """Error alert with V2 compliance."""
    alert_id: str
    error_id: str
    severity: ErrorSeverity
    message: str
    recipients: List[str] = field(default_factory=list)
    sent_at: Optional[datetime] = None
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization validation."""
        if not self.alert_id:
            raise ValueError("alert_id is required")
        if not self.error_id:
            raise ValueError("error_id is required")
        if not self.message:
            raise ValueError("message is required")

from __future__ import annotations

"""Shared data models for health reporting."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ReportType(Enum):
    """Types of health reports."""

    DAILY_SUMMARY = "daily_summary"
    WEEKLY_ANALYSIS = "weekly_analysis"
    MONTHLY_TREND = "monthly_trend"
    INCIDENT_REPORT = "incident_report"
    PERFORMANCE_REVIEW = "performance_review"
    CUSTOM_RANGE = "custom_range"


class ReportFormat(Enum):
    """Output formats for reports."""

    JSON = "json"
    CSV = "csv"
    HTML = "html"
    PDF = "pdf"
    MARKDOWN = "markdown"
    CONSOLE = "console"


@dataclass
class ReportConfig:
    """Configuration for report generation."""

    report_type: ReportType
    format: ReportFormat
    include_charts: bool = True
    include_metrics: bool = True
    include_alerts: bool = True
    include_recommendations: bool = True
    time_range: Optional[Dict[str, datetime]] = None
    agents: Optional[List[str]] = None
    custom_parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthReport:
    """Generated health report."""

    report_id: str
    report_type: ReportType
    format: ReportFormat
    generated_at: datetime
    time_range: Dict[str, datetime]
    summary: Dict[str, Any]
    metrics_data: Dict[str, Any]
    alerts_data: Dict[str, Any]
    charts: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

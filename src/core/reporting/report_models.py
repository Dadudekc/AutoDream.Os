"""Models and enums for the unified reporting framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ReportType(Enum):
    """Types of reports supported by the unified framework."""

    TESTING = "testing"
    PERFORMANCE = "performance"
    HEALTH = "health"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    QUALITY = "quality"
    ANALYTICS = "analytics"
    FINANCIAL = "financial"
    CUSTOM = "custom"


class ReportFormat(Enum):
    """Output formats for reports."""

    JSON = "json"
    TEXT = "text"
    HTML = "html"
    CSV = "csv"
    XML = "xml"
    PDF = "pdf"


class ReportPriority(Enum):
    """Report priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ReportConfig:
    """Configuration for report generation."""

    report_type: ReportType
    format: ReportFormat
    priority: ReportPriority = ReportPriority.MEDIUM
    include_charts: bool = False
    include_recommendations: bool = True
    max_history: int = 100
    output_directory: str = "reports"
    template_path: Optional[str] = None


@dataclass
class ReportMetadata:
    """Metadata for generated reports."""

    report_id: str
    timestamp: datetime
    report_type: ReportType
    format: ReportFormat
    priority: ReportPriority
    source_system: str
    version: str = "2.0.0"
    tags: List[str] = field(default_factory=list)


@dataclass
class UnifiedReport:
    """Unified report structure used by the framework."""

    metadata: ReportMetadata
    content: Dict[str, Any]
    summary: str
    recommendations: List[str] = field(default_factory=list)
    charts: List[Dict[str, Any]] = field(default_factory=list)
    raw_data: Optional[Dict[str, Any]] = None

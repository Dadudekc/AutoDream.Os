"""
Error Reports - V2 Compliance Module
===================================

Error reports functionality for error handling system.

V2 Compliance: < 300 lines, single responsibility, error reports.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ErrorReport:
    """Error report with V2 compliance."""

    report_id: str
    title: str
    summary: str
    error_count: int = 0
    severity_distribution: dict[str, int] = field(default_factory=dict)
    type_distribution: dict[str, int] = field(default_factory=dict)
    source_distribution: dict[str, int] = field(default_factory=dict)
    resolution_times: list[float] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = "system"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization validation."""
        if not self.report_id:
            raise ValueError("report_id is required")
        if not self.title:
            raise ValueError("title is required")
        if not self.summary:
            raise ValueError("summary is required")

    def add_error_data(
        self, severity: str, error_type: str, source: str, resolution_time: float = None
    ) -> None:
        """Add error data to report."""
        self.error_count += 1
        self.severity_distribution[severity] = self.severity_distribution.get(severity, 0) + 1
        self.type_distribution[error_type] = self.type_distribution.get(error_type, 0) + 1
        self.source_distribution[source] = self.source_distribution.get(source, 0) + 1

        if resolution_time is not None:
            self.resolution_times.append(resolution_time)

    def add_recommendation(self, recommendation: str) -> None:
        """Add recommendation to report."""
        if recommendation not in self.recommendations:
            self.recommendations.append(recommendation)

    def get_average_resolution_time(self) -> float:
        """Get average resolution time."""
        if self.resolution_times:
            return sum(self.resolution_times) / len(self.resolution_times)
        return 0.0

    def get_summary(self) -> dict[str, Any]:
        """Get report summary."""
        return {
            "report_id": self.report_id,
            "title": self.title,
            "error_count": self.error_count,
            "average_resolution_time": self.get_average_resolution_time(),
            "recommendations_count": len(self.recommendations),
            "created_at": self.created_at.isoformat(),
        }

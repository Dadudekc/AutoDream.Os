"""Data models for error report generation."""

from dataclasses import dataclass, asdict
from typing import Any, Dict, List
from datetime import datetime

@dataclass
class AnalyticsReport:
    """Structured analytics report object."""

    report_id: str
    timestamp: str
    time_range: str
    summary: Dict[str, Any]
    patterns: List[Dict[str, Any]]
    trends: List[Dict[str, Any]]
    correlations: List[Dict[str, Any]]
    recommendations: List[str]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Return dictionary representation of the report."""
        return asdict(self)

    @staticmethod
    def create(report_id: str, summary: Dict[str, Any], patterns: List[Dict[str, Any]],
               trends: List[Dict[str, Any]], correlations: List[Dict[str, Any]],
               recommendations: List[str], metadata: Dict[str, Any]) -> "AnalyticsReport":
        timestamp = datetime.now().isoformat()
        time_range = f"Last 24 hours (generated at {timestamp})"
        return AnalyticsReport(
            report_id=report_id,
            timestamp=timestamp,
            time_range=time_range,
            summary=summary,
            patterns=patterns,
            trends=trends,
            correlations=correlations,
            recommendations=recommendations,
            metadata=metadata,
        )

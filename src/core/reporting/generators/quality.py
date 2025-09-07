"""Quality report generator."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict

from ..report_models import ReportMetadata, ReportType, UnifiedReport
from .base import ReportGenerator


class QualityReportGenerator(ReportGenerator):
    """Generates quality reports."""

    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate a quality report."""
        metrics = data.get("quality_metrics", {})
        issues = data.get("issues", [])
        score = metrics.get("score", 0)

        content = {
            "quality_summary": {
                "issue_count": len(issues),
                "quality_score": score,
            },
            "quality_metrics": metrics,
            "issues": issues,
        }

        summary = f"Quality Report: score {score} with {len(issues)} issues"

        recommendations = []
        if score < 80:
            recommendations.append("Quality score below 80 - improvements recommended")

        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            report_type=ReportType.QUALITY,
            format=self.config.format,
            priority=self.config.priority,
            source_system="unified_quality_system",
        )

        return UnifiedReport(
            metadata=metadata,
            content=content,
            summary=summary,
            recommendations=recommendations,
        )

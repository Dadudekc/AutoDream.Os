"""Analytics report generator."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict

from ..report_models import ReportMetadata, ReportType, UnifiedReport
from .base import ReportGenerator


class AnalyticsReportGenerator(ReportGenerator):
    """Generates analytics reports."""

    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate an analytics report."""
        metrics = data.get("metrics", {})
        insights = data.get("insights", [])

        content = {
            "analytics_summary": metrics,
            "insights": insights,
        }

        summary = f"Analytics Report: {len(insights)} insights generated"

        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            report_type=ReportType.ANALYTICS,
            format=self.config.format,
            priority=self.config.priority,
            source_system="unified_analytics_system",
        )

        return UnifiedReport(metadata=metadata, content=content, summary=summary)

"""Custom report generator."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict

from ..report_models import ReportMetadata, ReportType, UnifiedReport
from .base import ReportGenerator


class CustomReportGenerator(ReportGenerator):
    """Generates custom reports."""

    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate a custom report."""
        content = data.get("content", data)
        summary = data.get("summary", "Custom report generated")

        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            report_type=ReportType.CUSTOM,
            format=self.config.format,
            priority=self.config.priority,
            source_system="unified_custom_system",
        )

        return UnifiedReport(metadata=metadata, content=content, summary=summary)

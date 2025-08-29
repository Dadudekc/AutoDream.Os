"""Handles persistence of formatted reports using configurable backends."""

from __future__ import annotations

import logging
from typing import Optional

from .report_data_collector import ReportDataCollector
from .report_models import ReportFormat, UnifiedReport
from .backends import FileReportBackend, ReportBackend


class ReportStorage:
    """Save formatted reports through a storage backend."""

    def __init__(
        self,
        collector: ReportDataCollector,
        backend: ReportBackend | None = None,
    ) -> None:
        self.collector = collector
        self.backend = backend or FileReportBackend()
        self.logger = logging.getLogger(f"{__name__}.ReportStorage")

    def save(
        self,
        report: UnifiedReport,
        formatted_content: str,
        format_type: ReportFormat,
        filename: Optional[str] = None,
    ) -> str:
        if not filename:
            timestamp = report.metadata.timestamp.strftime("%Y%m%d_%H%M%S")
            filename = (
                f"{report.metadata.report_type.value}_report_{timestamp}."
                f"{format_type.value}"
            )

        generator = self.collector.report_generators[report.metadata.report_type]
        output_path = generator.output_dir / filename
        saved_path = self.backend.save(output_path, formatted_content)
        self.logger.info(f"Report saved to: {saved_path}")
        return saved_path

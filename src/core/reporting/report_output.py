"""Handles persistence and output of generated reports."""

from __future__ import annotations

import logging
from typing import Optional

from .report_data_collector import ReportDataCollector
from .report_formatter import ReportFormatter
from .report_models import ReportFormat, UnifiedReport


class ReportOutput:
    """Handles report output operations like saving to disk."""

    def __init__(self, formatter: ReportFormatter, collector: ReportDataCollector) -> None:
        self.formatter = formatter
        self.collector = collector
        self.logger = logging.getLogger(f"{__name__}.ReportOutput")

    def save(
        self,
        report: UnifiedReport,
        format_type: Optional[ReportFormat] = None,
        filename: Optional[str] = None,
    ) -> str:
        if format_type is None:
            format_type = report.metadata.format

        if not filename:
            timestamp = report.metadata.timestamp.strftime("%Y%m%d_%H%M%S")
            filename = (
                f"{report.metadata.report_type.value}_report_{timestamp}."
                f"{format_type.value}"
            )

        generator = self.collector.report_generators[report.metadata.report_type]
        output_path = generator.output_dir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        formatted_content = self.formatter.format(report, format_type)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(formatted_content)

        self.logger.info(f"Report saved to: {output_path}")
        return str(output_path)

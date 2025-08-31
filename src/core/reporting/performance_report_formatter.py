"""
Report Formatter - V2 Modular Architecture
==========================================

Report formatting and output generation.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
from abc import ABC, abstractmethod
from typing import List

from .performance_report_types import PerformanceReport, ReportSection, ReportMetric, ReportFormat


class ReportFormatter(ABC):
    """Abstract base class for report formatters."""

    @abstractmethod
    def format_report(self, report: PerformanceReport) -> str:
        """Format a performance report.

        Args:
            report (PerformanceReport): Report data to format.

        Returns:
            str: Formatted report output.
        """
        raise NotImplementedError("format_report must be implemented by subclasses")

    @abstractmethod
    def format_section(self, section: ReportSection) -> str:
        """Format a report section.

        Args:
            section (ReportSection): Section to format.

        Returns:
            str: Formatted section output.
        """
        raise NotImplementedError("format_section must be implemented by subclasses")

    @abstractmethod
    def format_metric(self, metric: ReportMetric) -> str:
        """Format a report metric.

        Args:
            metric (ReportMetric): Metric to format.

        Returns:
            str: Formatted metric output.
        """
        raise NotImplementedError("format_metric must be implemented by subclasses")


class JSONFormatter(ReportFormatter):
    """JSON format formatter."""

    def format_report(self, report: PerformanceReport) -> str:
        """Format report as JSON."""
        return json.dumps(report.to_dict(), indent=2)

    def format_section(self, section: ReportSection) -> str:
        """Format section as JSON."""
        return json.dumps(section.to_dict(), indent=2)

    def format_metric(self, metric: ReportMetric) -> str:
        """Format metric as JSON."""
        return json.dumps(metric.to_dict(), indent=2)


class TextFormatter(ReportFormatter):
    """Plain text format formatter."""

    def format_report(self, report: PerformanceReport) -> str:
        """Format report as plain text."""
        lines = []
        lines.append(f"Performance Report: {report.title}")
        lines.append("=" * (len(report.title) + 20))
        lines.append(f"Report ID: {report.report_id}")
        lines.append(f"Generated: {report.timestamp}")
        lines.append(f"Status: {report.status.value}")
        lines.append("")
        lines.append(report.description)
        lines.append("")

        for section in report.sections:
            lines.append(self.format_section(section))
            lines.append("")

        return "\n".join(lines)

    def format_section(self, section: ReportSection) -> str:
        """Format section as plain text."""
        lines = []
        lines.append(f"## {section.title}")
        lines.append("-" * (len(section.title) + 3))
        lines.append(section.description)
        lines.append("")

        if section.metrics:
            lines.append("Metrics:")
            for metric in section.metrics:
                lines.append(f"  {metric.name}: {metric.value} {metric.unit}")
            lines.append("")

        if section.subsections:
            for subsection in section.subsections:
                lines.append(self.format_section(subsection))

        return "\n".join(lines)

    def format_metric(self, metric: ReportMetric) -> str:
        """Format metric as plain text."""
        return f"{metric.name}: {metric.value} {metric.unit}"


class HTMLFormatter(ReportFormatter):
    """HTML format formatter."""

    def format_report(self, report: PerformanceReport) -> str:
        """Format report as HTML."""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{report.title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .metric {{ margin: 10px 0; padding: 10px; background-color: #f9f9f9; }}
        .subsection {{ margin-left: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{report.title}</h1>
        <p><strong>Report ID:</strong> {report.report_id}</p>
        <p><strong>Generated:</strong> {report.timestamp}</p>
        <p><strong>Status:</strong> {report.status.value}</p>
        <p>{report.description}</p>
    </div>
"""

        for section in report.sections:
            html += self.format_section(section)

        html += """
</body>
</html>
"""
        return html

    def format_section(self, section: ReportSection) -> str:
        """Format section as HTML."""
        html = f"""
    <div class="section">
        <h2>{section.title}</h2>
        <p>{section.description}</p>
"""

        if section.metrics:
            html += "        <div class='metrics'>\n"
            for metric in section.metrics:
                html += self.format_metric(metric)
            html += "        </div>\n"

        if section.subsections:
            html += "        <div class='subsections'>\n"
            for subsection in section.subsections:
                html += self.format_section(subsection)
            html += "        </div>\n"

        html += "    </div>\n"
        return html

    def format_metric(self, metric: ReportMetric) -> str:
        """Format metric as HTML."""
        return f"""
            <div class="metric">
                <strong>{metric.name}:</strong> {metric.value} {metric.unit}
                <br><small>Type: {metric.metric_type.value} | Time: {metric.timestamp}</small>
            </div>"""


class CSVFormatter(ReportFormatter):
    """CSV format formatter."""

    def format_report(self, report: PerformanceReport) -> str:
        """Format report as CSV."""
        lines = []
        lines.append("Report ID,Title,Description,Timestamp,Status")
        lines.append(
            f"{report.report_id},{report.title},{report.description},{report.timestamp},{report.status.value}"
        )
        lines.append("")
        lines.append("Section,Subsection,Metric,Value,Unit,Type,Timestamp")

        for section in report.sections:
            lines.extend(self._format_section_csv(section))

        return "\n".join(lines)

    def _format_section_csv(
        self, section: ReportSection, parent_section: str = ""
    ) -> List[str]:
        """Format section as CSV rows."""
        lines = []
        current_section = (
            f"{parent_section}/{section.name}" if parent_section else section.name
        )

        for metric in section.metrics:
            lines.append(
                f"{current_section},,{metric.name},{metric.value},{metric.unit},{metric.metric_type.value},{metric.timestamp}"
            )

        for subsection in section.subsections:
            lines.extend(self._format_section_csv(subsection, current_section))

        return lines

    def format_section(self, section: ReportSection) -> str:
        """Format section as CSV (not implemented for CSV formatter)."""
        raise NotImplementedError(
            "CSV formatter does not support individual section formatting"
        )

    def format_metric(self, metric: ReportMetric) -> str:
        """Format metric as CSV (not implemented for CSV formatter)."""
        raise NotImplementedError(
            "CSV formatter does not support individual metric formatting"
        )


def get_formatter(format_type: ReportFormat) -> ReportFormatter:
    """Get formatter by format type."""
    formatters = {
        ReportFormat.JSON: JSONFormatter(),
        ReportFormat.TEXT: TextFormatter(),
        ReportFormat.HTML: HTMLFormatter(),
        ReportFormat.CSV: CSVFormatter(),
    }
    return formatters.get(format_type, JSONFormatter())

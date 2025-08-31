"""Example report formatter."""

from src.core.reporting.performance_report_formatter import (
    PerformanceReport,
    ReportFormatter,
    ReportMetric,
    ReportSection,
)


class SimpleFormatter(ReportFormatter):
    """Format reports as plain strings."""

    def format_report(self, report: PerformanceReport) -> str:
        return "report"

    def format_section(self, section: ReportSection) -> str:
        return "section"

    def format_metric(self, metric: ReportMetric) -> str:
        return "metric"

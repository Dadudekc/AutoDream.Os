"""Report output utilities."""

import json
from pathlib import Path
from typing import Any

from .config import (
    DEFAULT_REPORTS_DIR,
    HTML_TEMPLATE,
    MARKDOWN_TEMPLATE,
    ReportFormat,
)
from .models import AnalyticsReport


class ReportOutput:
    """Handle report export in multiple formats."""

    def __init__(self, output_dir: Path = DEFAULT_REPORTS_DIR):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)

    def output(self, report: AnalyticsReport, format_type: ReportFormat) -> Path:
        if format_type == ReportFormat.JSON:
            return self._output_json(report)
        if format_type == ReportFormat.MARKDOWN:
            return self._output_markdown(report)
        if format_type == ReportFormat.HTML:
            return self._output_html(report)
        if format_type == ReportFormat.CSV:
            return self._output_csv(report)
        return self._output_console(report)

    def _output_json(self, report: AnalyticsReport) -> Path:
        path = self.output_dir / f"{report.report_id}.json"
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(report.to_dict(), handle, indent=2, default=str)
        return path

    def _output_markdown(self, report: AnalyticsReport) -> Path:
        content = MARKDOWN_TEMPLATE.format(content=json.dumps(report.to_dict(), indent=2))
        path = self.output_dir / f"{report.report_id}.md"
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content)
        return path

    def _output_html(self, report: AnalyticsReport) -> Path:
        content = HTML_TEMPLATE.format(content=json.dumps(report.to_dict(), indent=2))
        path = self.output_dir / f"{report.report_id}.html"
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content)
        return path

    def _output_csv(self, report: AnalyticsReport) -> Path:
        # Simple CSV with summary values
        path = self.output_dir / f"{report.report_id}.csv"
        summary = report.summary
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(",".join(summary.keys()) + "\n")
            handle.write(",".join(str(v) for v in summary.values()) + "\n")
        return path

    def _output_console(self, report: AnalyticsReport) -> Path:
        print(json.dumps(report.to_dict(), indent=2))
        return self.output_dir / f"{report.report_id}.console"

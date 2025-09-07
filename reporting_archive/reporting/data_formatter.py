from typing import Any
import json

from .models import HealthReport, ReportFormat
from __future__ import annotations


"""Functions responsible for formatting :class:`HealthReport` objects."""



class ReportFormatter:
    """Convert :class:`HealthReport` objects into different representations."""

    def format(self, report: HealthReport, fmt: ReportFormat) -> str:
        if fmt == ReportFormat.JSON:
            return self._to_json(report)
        if fmt == ReportFormat.CSV:
            return self._to_csv(report)
        if fmt == ReportFormat.HTML:
            return self._to_html(report)
        if fmt == ReportFormat.MARKDOWN:
            return self._to_markdown(report)
        if fmt == ReportFormat.CONSOLE:
            return self._to_console(report)
        raise ValueError(f"Unsupported format: {fmt}")

    # ------------------------------------------------------------------
    def _to_json(self, report: HealthReport) -> str:
        report_dict: dict[str, Any] = {
            "report_id": report.report_id,
            "report_type": report.report_type.value,
            "format": report.format.value,
            "generated_at": report.generated_at.isoformat(),
            "time_range": {
                "start": report.time_range["start"].isoformat(),
                "end": report.time_range["end"].isoformat(),
            },
            "summary": report.summary,
            "metrics_data": report.metrics_data,
            "alerts_data": report.alerts_data,
            "charts": report.charts,
            "recommendations": report.recommendations,
            "metadata": report.metadata,
        }
        return json.dumps(report_dict, indent=2, ensure_ascii=False)

    def _to_csv(self, report: HealthReport) -> str:
        lines = ["SUMMARY"]
        for key, value in report.summary.items():
            lines.append(f"{key},{value}")
        lines.append("")
        lines.append("METRICS")
        for agent, data in report.metrics_data.items():
            lines.append(f"Agent: {agent}")
            for metric, mdata in data.get("metrics", {}).items():
                lines.append(f"  {metric},{mdata.get('value','')},{mdata.get('unit','')}")
        return "\n".join(lines)

    def _to_html(self, report: HealthReport) -> str:
        return (
            f"<html><body><h1>Health Report</h1><p>Type: {report.report_type.value}</p></body></html>"
        )

    def _to_markdown(self, report: HealthReport) -> str:
        return (
            f"# Health Report\n\nType: {report.report_type.value}\n"
        )

    def _to_console(self, report: HealthReport) -> str:
        return f"HEALTH REPORT: {report.report_type.value}\nTotal Agents: {report.summary.get('total_agents',0)}"

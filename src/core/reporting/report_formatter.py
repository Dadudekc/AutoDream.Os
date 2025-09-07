"""Report formatting utilities for the unified reporting framework."""

import html
import json

from .report_models import ReportFormat, UnifiedReport


class ReportFormatter:
    """Formats reports in various output formats"""

    def format(self, report: UnifiedReport, format_type: ReportFormat) -> str:
        """Dispatch formatting based on requested format type"""
        if format_type == ReportFormat.JSON:
            return self.format_as_json(report)
        if format_type == ReportFormat.TEXT:
            return self.format_as_text(report)
        if format_type == ReportFormat.HTML:
            return self.format_as_html(report)
        # Default to JSON for unsupported formats
        return self.format_as_json(report)

    @staticmethod
    def format_as_json(report: UnifiedReport) -> str:
        """Format report as JSON"""
        report_dict = {
            "metadata": {
                "report_id": report.metadata.report_id,
                "timestamp": report.metadata.timestamp.isoformat(),
                "report_type": report.metadata.report_type.value,
                "format": report.metadata.format.value,
                "priority": report.metadata.priority.value,
                "source_system": report.metadata.source_system,
                "version": report.metadata.version,
                "tags": report.metadata.tags,
            },
            "content": report.content,
            "summary": report.summary,
            "recommendations": report.recommendations,
            "charts": report.charts,
        }
        return json.dumps(report_dict, indent=2, default=str)

    @staticmethod
    def format_as_text(report: UnifiedReport) -> str:
        """Format report as human-readable text"""
        lines = []
        lines.append("=" * 80)
        lines.append(f"REPORT: {report.metadata.report_type.value.upper()}")
        lines.append("=" * 80)
        lines.append(f"Report ID: {report.metadata.report_id}")
        lines.append(f"Timestamp: {report.metadata.timestamp}")
        lines.append(f"Source: {report.metadata.source_system}")
        lines.append(f"Priority: {report.metadata.priority.value}")
        lines.append("")
        lines.append("SUMMARY:")
        lines.append("-" * 40)
        lines.append(report.summary)
        lines.append("")

        if report.recommendations:
            lines.append("RECOMMENDATIONS:")
            lines.append("-" * 40)
            for i, rec in enumerate(report.recommendations, 1):
                lines.append(f"{i}. {rec}")
            lines.append("")

        lines.append("DETAILS:")
        lines.append("-" * 40)
        lines.append(json.dumps(report.content, indent=2, default=str))

        return "\n".join(lines)

    @staticmethod
    def format_as_html(report: UnifiedReport) -> str:
        """Format report as HTML"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{report.metadata.report_type.value.title()} Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .summary {{ background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .recommendations {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .details {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; }}
                .priority-high {{ color: #dc3545; }}
                .priority-medium {{ color: #ffc107; }}
                .priority-low {{ color: #28a745; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{report.metadata.report_type.value.title()} Report</h1>
                <p><strong>Report ID:</strong> {report.metadata.report_id}</p>
                <p><strong>Timestamp:</strong> {report.metadata.timestamp}</p>
                <p><strong>Source:</strong> {report.metadata.source_system}</p>
                <p><strong>Priority:</strong> <span class="priority-{report.metadata.priority.value}">{report.metadata.priority.value.upper()}</span></p>
            </div>

            <div class="summary">
                <h2>Summary</h2>
                <p>{report.summary}</p>
            </div>
        """

        if report.recommendations:
            html_content += f"""
            <div class="recommendations">
                <h2>Recommendations</h2>
                <ul>
            """
            for rec in report.recommendations:
                html_content += f"<li>{html.escape(rec)}</li>"
            html_content += """
                </ul>
            </div>
            """

        html_content += f"""
            <div class="details">
                <h2>Details</h2>
                <pre>{json.dumps(report.content, indent=2, default=str)}</pre>
            </div>
        </body>
        </html>
        """

        return html_content

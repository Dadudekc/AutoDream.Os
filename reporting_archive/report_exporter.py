"""Export utilities for writing reports to disk."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from .archive_config import ENCODING, REPORTS_DIR


def _format_text_report(report: Dict[str, Any]) -> str:
    """Format report dictionary as a simple human-readable string."""
    lines = ["=" * 60]
    lines.append(f"SCANNER REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 60)

    if report.get("report_type") == "project_analysis":
        summary = report.get("summary", {})
        lines.append(f"Project: {report.get('project_name', 'Unknown')}")
        lines.append(f"Total Files: {summary.get('total_files', 0)}")
        lines.append(f"Total Lines: {summary.get('total_lines', 0)}")
        lines.append(f"Languages: {summary.get('languages_detected', 0)}")
    elif report.get("report_type") == "code_quality":
        lines.append(f"Quality Score: {report.get('quality_score', 0)}/100")
        lines.append("Recommendations:")
        for rec in report.get("recommendations", []):
            lines.append(f"  - {rec}")

    lines.append("=" * 60)
    return "\n".join(lines)


def export_report(
    report: Dict[str, Any],
    format_type: str = "json",
    filename: Optional[str] = None,
    output_dir: Path = REPORTS_DIR,
) -> Path:
    """Export a report to the specified directory and format."""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scanner_report_{timestamp}.{format_type}"

    file_path = output_dir / filename

    if format_type == "json":
        with open(file_path, "w", encoding=ENCODING) as f:
            json.dump(report, f, indent=2, default=str)
    elif format_type == "txt":
        with open(file_path, "w", encoding=ENCODING) as f:
            f.write(_format_text_report(report))
    else:
        raise ValueError(f"Unsupported format: {format_type}")

    return file_path

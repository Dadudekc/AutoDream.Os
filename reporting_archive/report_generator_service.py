from pathlib import Path
from typing import Any, Dict

from .archive_config import REPORTS_DIR
from .data_consolidator import (
from .file_importer import load_project_data
from .report_exporter import export_report
from __future__ import annotations
import time

"""Report Generator Service - Agent Cellphone V2
=============================================

Generates comprehensive reports from scanner analysis data.
Split into dedicated modules for file import, consolidation and export.
"""



    analyze_files,
    calculate_complexity_statistics,
    calculate_language_statistics,
    calculate_quality_metrics,
    generate_detailed_analysis,
    generate_recommendations,
    identify_priority_actions,
)


class ReportGeneratorService:
    """Generate project and code quality reports from analysis data."""

    def __init__(self, output_dir: Path | None = None) -> None:
        self.output_dir = output_dir or REPORTS_DIR
        self.output_dir.mkdir(exist_ok=True)

    # ------------------------------------------------------------------
    def generate_project_report(
        self, project_data: Dict[str, Any], include_details: bool = True
    ) -> Dict[str, Any]:
        """Generate a comprehensive project analysis report."""
        try:
            files = project_data.get("files", [])
            total_files = len(files)
            total_lines = sum(f.get("line_count", 0) for f in files)
            language_stats = calculate_language_statistics(files)
            complexity_stats = calculate_complexity_statistics(files)

            report = {
                "timestamp": time.time(),
                "report_type": "project_analysis",
                "project_name": project_data.get("project_name", "Unknown"),
                "summary": {
                    "total_files": total_files,
                    "total_lines": total_lines,
                    "languages_detected": len(language_stats.get("file_counts", {})),
                    "average_complexity": complexity_stats.get("average", 0.0),
                },
                "language_breakdown": language_stats,
                "complexity_analysis": complexity_stats,
                "file_analysis": analyze_files(files, include_details),
            }

            if include_details:
                report["detailed_analysis"] = generate_detailed_analysis(project_data)

            return report
        except Exception as exc:  # pragma: no cover - defensive
            return {"timestamp": time.time(), "error": str(exc), "status": "failed"}

    # ------------------------------------------------------------------
    def generate_code_quality_report(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a code quality assessment report."""
        try:
            quality_metrics = calculate_quality_metrics(analysis_data)
            recommendations = generate_recommendations(quality_metrics)
            report = {
                "timestamp": time.time(),
                "report_type": "code_quality",
                "quality_score": quality_metrics.get("overall_score", 0.0),
                "metrics": quality_metrics,
                "recommendations": recommendations,
                "priority_actions": identify_priority_actions(quality_metrics),
            }
            return report
        except Exception as exc:  # pragma: no cover - defensive
            return {"timestamp": time.time(), "error": str(exc), "status": "failed"}

    # ------------------------------------------------------------------
    def export_report(
        self, report: Dict[str, Any], format_type: str = "json", filename: str | None = None
    ) -> Path:
        """Export a report using the shared exporter module."""
        return export_report(report, format_type, filename, self.output_dir)

    # ------------------------------------------------------------------
    def load_analysis_from_file(self, file_path: Path) -> Dict[str, Any]:
        """Convenience helper to import analysis data from JSON."""
        return load_project_data(file_path)

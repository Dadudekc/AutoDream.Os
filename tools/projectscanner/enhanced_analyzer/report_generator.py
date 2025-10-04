"""
Enhanced Report Generator - V2 Compliant
========================================

Enhanced report generation for project analysis.
V2 Compliance: ≤200 lines, single responsibility, KISS principle.
"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class EnhancedReportGenerator:
    """Enhanced report generator with advanced analysis reporting."""

    def __init__(self, project_root: Path, analysis_data: dict[str, Any]):
        """Initialize enhanced report generator."""
        self.project_root = project_root
        self.analysis_data = analysis_data
        logger.debug("Enhanced Report Generator initialized")

    def generate_enhanced_reports(self) -> None:
        """Generate all enhanced analysis reports."""
        try:
            self._generate_summary_report()
            self._generate_language_report()
            self._generate_complexity_report()
            self._generate_v2_compliance_report()

            logger.info("✅ Enhanced reports generated successfully")
        except Exception as e:
            logger.error(f"Failed to generate enhanced reports: {e}")

    def _generate_summary_report(self) -> None:
        """Generate project summary report."""
        summary = {
            "project_name": "Agent Cellphone V2 Repository",
            "scan_timestamp": self._get_timestamp(),
            "total_files": len(self.analysis_data),
            "total_lines": sum(
                analysis.get("line_count", 0) for analysis in self.analysis_data.values()
            ),
            "languages": self._get_language_breakdown(),
            "v2_compliance": self._get_v2_compliance_summary(),
        }

        self._save_report("project_summary.json", summary)

    def _generate_language_report(self) -> None:
        """Generate language-specific analysis report."""
        language_stats = {}

        for file_path, analysis in self.analysis_data.items():
            lang = analysis.get("language", "Unknown")
            if lang not in language_stats:
                language_stats[lang] = {
                    "files": 0,
                    "total_lines": 0,
                    "total_functions": 0,
                    "total_classes": 0,
                    "average_complexity": 0,
                }

            stats = language_stats[lang]
            stats["files"] += 1
            stats["total_lines"] += analysis.get("line_count", 0)
            stats["total_functions"] += len(analysis.get("functions", []))
            stats["total_classes"] += len(analysis.get("classes", []))
            stats["average_complexity"] += analysis.get("complexity", 0)

        # Calculate averages
        for lang, stats in language_stats.items():
            if stats["files"] > 0:
                stats["average_complexity"] = stats["average_complexity"] / stats["files"]
                stats["average_lines_per_file"] = stats["total_lines"] / stats["files"]

        self._save_report("language_analysis.json", language_stats)

    def _generate_complexity_report(self) -> None:
        """Generate complexity analysis report."""
        complexity_data = {
            "total_complexity": 0,
            "average_complexity": 0,
            "max_complexity": 0,
            "high_complexity_files": [],
            "complexity_distribution": {"low": 0, "medium": 0, "high": 0, "critical": 0},
        }

        complexities = []
        for file_path, analysis in self.analysis_data.items():
            complexity = analysis.get("complexity", 0)
            complexities.append(complexity)
            complexity_data["total_complexity"] += complexity
            complexity_data["max_complexity"] = max(complexity_data["max_complexity"], complexity)

            # Categorize complexity
            if complexity <= 5:
                complexity_data["complexity_distribution"]["low"] += 1
            elif complexity <= 15:
                complexity_data["complexity_distribution"]["medium"] += 1
            elif complexity <= 30:
                complexity_data["complexity_distribution"]["high"] += 1
            else:
                complexity_data["complexity_distribution"]["critical"] += 1
                complexity_data["high_complexity_files"].append(
                    {
                        "file": file_path,
                        "complexity": complexity,
                        "line_count": analysis.get("line_count", 0),
                    }
                )

        if complexities:
            complexity_data["average_complexity"] = sum(complexities) / len(complexities)

        self._save_report("complexity_analysis.json", complexity_data)

    def _generate_v2_compliance_report(self) -> None:
        """Generate V2 compliance analysis report."""
        compliance_data = {
            "total_files": len(self.analysis_data),
            "compliant_files": 0,
            "violation_files": [],
            "compliance_rate": 0.0,
            "violation_types": {"line_limit": 0, "other": 0},
        }

        for file_path, analysis in self.analysis_data.items():
            is_compliant = analysis.get("v2_compliant", False)
            if is_compliant:
                compliance_data["compliant_files"] += 1
            else:
                violation_info = {
                    "file": file_path,
                    "line_count": analysis.get("line_count", 0),
                    "violations": [],
                }

                if analysis.get("line_count", 0) > 400:
                    violation_info["violations"].append("Exceeds 400 line limit")
                    compliance_data["violation_types"]["line_limit"] += 1
                else:
                    compliance_data["violation_types"]["other"] += 1

                compliance_data["violation_files"].append(violation_info)

        if compliance_data["total_files"] > 0:
            compliance_data["compliance_rate"] = (
                compliance_data["compliant_files"] / compliance_data["total_files"] * 100
            )

        self._save_report("v2_compliance.json", compliance_data)

    def _get_language_breakdown(self) -> dict[str, int]:
        """Get breakdown of files by language."""
        language_counts = {}
        for analysis in self.analysis_data.values():
            lang = analysis.get("language", "Unknown")
            language_counts[lang] = language_counts.get(lang, 0) + 1
        return language_counts

    def _get_v2_compliance_summary(self) -> dict[str, Any]:
        """Get V2 compliance summary."""
        compliant = sum(
            1 for analysis in self.analysis_data.values() if analysis.get("v2_compliant", False)
        )
        total = len(self.analysis_data)
        return {
            "compliant_files": compliant,
            "total_files": total,
            "compliance_rate": (compliant / total * 100) if total > 0 else 0,
        }

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime

        return datetime.now().isoformat()

    def _save_report(self, filename: str, data: dict[str, Any]) -> None:
        """Save report to file."""
        report_file = self.project_root / filename
        try:
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            logger.debug(f"Report saved: {report_file}")
        except Exception as e:
            logger.error(f"Failed to save report {filename}: {e}")

    def export_chatgpt_context(self) -> None:
        """Export project context for AI assistance."""
        context = {
            "project_name": "Agent Cellphone V2 Repository",
            "description": "V2_SWARM autonomous agent system with enhanced project scanning",
            "analysis_summary": self.analysis_data,
            "key_features": [
                "8 autonomous agents with coordinate-based communication",
                "Enhanced project scanning with V2 compliance",
                "Multi-language code analysis",
                "Advanced complexity metrics",
                "Comprehensive reporting system",
            ],
            "scan_timestamp": self._get_timestamp(),
        }

        context_file = self.project_root / "enhanced_chatgpt_context.json"
        try:
            with open(context_file, "w", encoding="utf-8") as f:
                json.dump(context, f, indent=2, default=str)
            logger.info(f"📄 Enhanced ChatGPT context exported to {context_file}")
        except Exception as e:
            logger.error(f"Failed to export ChatGPT context: {e}")

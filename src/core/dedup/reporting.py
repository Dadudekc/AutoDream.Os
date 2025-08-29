"""Reporting utilities for duplication analysis."""
from __future__ import annotations

import json
import logging
from typing import Any, Dict, List

from .models import DuplicationGroup


class ReportGenerator:
    """Generate and export duplication analysis reports."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"{__name__}.ReportGenerator")

    def build_report(
        self,
        duplication_groups: List[DuplicationGroup],
        consolidation_plan: Dict[str, Any],
    ) -> Dict[str, Any]:
        try:
            report = {
                "summary": {
                    "total_groups": len(duplication_groups),
                    "total_instances": sum(
                        len(g.instances) for g in duplication_groups
                    ),
                    "severity_distribution": self._get_severity_distribution(
                        duplication_groups
                    ),
                    "type_distribution": self._get_type_distribution(
                        duplication_groups
                    ),
                },
                "duplication_groups": [
                    {
                        "id": g.id,
                        "type": g.duplication_type.value,
                        "severity": g.consolidation_priority.value,
                        "instances": len(g.instances),
                        "suggestion": g.suggested_consolidation,
                        "effort": g.estimated_effort,
                        "instances_details": [
                            {
                                "id": i.id,
                                "similarity": i.similarity_score,
                                "lines": i.lines_count,
                                "locations": i.locations,
                            }
                            for i in g.instances
                        ],
                    }
                    for g in duplication_groups
                ],
                "consolidation_plan": consolidation_plan,
            }
            return report
        except Exception as exc:  # pragma: no cover - logging
            self.logger.error("Failed to build report: %s", exc)
            return {"error": str(exc)}

    def export_report(
        self, report: Dict[str, Any], output_path: str, format_type: str = "json"
    ) -> bool:
        try:
            if format_type == "json":
                with open(output_path, "w", encoding="utf-8") as file:
                    json.dump(report, file, indent=2, ensure_ascii=False)
            elif format_type == "txt":
                with open(output_path, "w", encoding="utf-8") as file:
                    file.write(self._format_text_report(report))
            elif format_type == "md":
                with open(output_path, "w", encoding="utf-8") as file:
                    file.write(self._format_markdown_report(report))
            else:
                raise ValueError(f"Unsupported format: {format_type}")
            self.logger.info("Report exported to: %s", output_path)
            return True
        except Exception as exc:  # pragma: no cover - logging
            self.logger.error("Failed to export report: %s", exc)
            return False

    def _get_severity_distribution(
        self, groups: List[DuplicationGroup]
    ) -> Dict[str, int]:
        distribution: Dict[str, int] = {}
        try:
            for group in groups:
                severity = group.consolidation_priority.value
                distribution[severity] = distribution.get(severity, 0) + 1
        except Exception:
            pass
        return distribution

    def _get_type_distribution(self, groups: List[DuplicationGroup]) -> Dict[str, int]:
        distribution: Dict[str, int] = {}
        try:
            for group in groups:
                dup_type = group.duplication_type.value
                distribution[dup_type] = distribution.get(dup_type, 0) + 1
        except Exception:
            pass
        return distribution

    def _format_text_report(self, report: Dict[str, Any]) -> str:
        try:
            lines: List[str] = []
            lines.append("=" * 80)
            lines.append("CODE DUPLICATION ANALYSIS REPORT")
            lines.append("=" * 80)
            lines.append("")
            summary = report.get("summary", {})
            lines.append(f"Total Duplication Groups: {summary.get('total_groups', 0)}")
            lines.append(
                f"Total Duplication Instances: {summary.get('total_instances', 0)}"
            )
            lines.append("")
            lines.append("DUPLICATION GROUPS:")
            lines.append("-" * 40)
            lines.append("")
            for group in report.get("duplication_groups", []):
                lines.append(f"Type: {group['type']}")
                lines.append(f"Severity: {group['severity']}")
                lines.append(f"Instances: {group['instances']}")
                lines.append(f"Suggestion: {group['suggestion']}")
                lines.append(f"Effort: {group['effort']}")
                lines.append("")
            return "\n".join(lines)
        except Exception:
            return "Error formatting report"

    def _format_markdown_report(self, report: Dict[str, Any]) -> str:
        try:
            lines: List[str] = []
            lines.append("# Code Duplication Analysis Report")
            lines.append("")
            summary = report.get("summary", {})
            lines.append("## Summary")
            lines.append("")
            lines.append(
                f"- **Total Duplication Groups:** {summary.get('total_groups', 0)}"
            )
            lines.append(
                f"- **Total Duplication Instances:** {summary.get('total_instances', 0)}"
            )
            lines.append("")
            lines.append("## Duplication Groups")
            lines.append("")
            for group in report.get("duplication_groups", []):
                lines.append(f"### {group['type'].replace('_', ' ').title()}")
                lines.append("")
                lines.append(f"- **Severity:** {group['severity']}")
                lines.append(f"- **Instances:** {group['instances']}")
                lines.append(f"- **Suggestion:** {group['suggestion']}")
                lines.append(f"- **Effort:** {group['effort']}")
                lines.append("")
            return "\n".join(lines)
        except Exception:
            return "# Error formatting report"

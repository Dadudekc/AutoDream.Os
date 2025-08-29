"""Remediation routines for addressing code duplication."""
from __future__ import annotations

import logging
from typing import Any, Dict, List

from .models import DuplicationGroup, DuplicationType


class ConsolidationEngine:
    """Engine for suggesting and automating code consolidation."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"{__name__}.ConsolidationEngine")

    def generate_consolidation_plan(
        self, duplication_groups: List[DuplicationGroup]
    ) -> Dict[str, Any]:
        """Generate a high level consolidation plan."""
        try:
            plan = {
                "total_duplications": sum(len(g.instances) for g in duplication_groups),
                "duplication_groups": len(duplication_groups),
                "estimated_effort": self._calculate_total_effort(duplication_groups),
                "priority_order": self._prioritize_consolidations(duplication_groups),
                "consolidation_steps": self._generate_consolidation_steps(
                    duplication_groups
                ),
                "expected_benefits": self._calculate_expected_benefits(
                    duplication_groups
                ),
                "risk_assessment": self._assess_consolidation_risks(duplication_groups),
            }
            return plan
        except Exception as exc:  # pragma: no cover - logging
            self.logger.error("Failed to generate consolidation plan: %s", exc)
            return {}

    def _calculate_total_effort(
        self, duplication_groups: List[DuplicationGroup]
    ) -> str:
        try:
            effort_scores = {"Low": 1, "Medium": 2, "High": 3}
            total_score = 0
            for group in duplication_groups:
                effort = group.estimated_effort
                if effort in effort_scores:
                    total_score += effort_scores[effort]
            if total_score <= 5:
                return "Low"
            if total_score <= 10:
                return "Medium"
            return "High"
        except Exception:
            return "Unknown"

    def _prioritize_consolidations(
        self, duplication_groups: List[DuplicationGroup]
    ) -> List[str]:
        try:
            sorted_groups = sorted(
                duplication_groups,
                key=lambda x: (x.consolidation_priority.value, x.total_duplication),
                reverse=True,
            )
            return [
                f"{group.duplication_type.value}: {group.suggested_consolidation}"
                for group in sorted_groups
            ]
        except Exception as exc:  # pragma: no cover - logging
            self.logger.error("Failed to prioritize consolidations: %s", exc)
            return []

    def _generate_consolidation_steps(
        self, duplication_groups: List[DuplicationGroup]
    ) -> List[Dict[str, Any]]:
        try:
            steps: List[Dict[str, Any]] = []
            for group in duplication_groups:
                steps.append(
                    {
                        "group_id": group.id,
                        "duplication_type": group.duplication_type.value,
                        "description": group.suggested_consolidation,
                        "effort": group.estimated_effort,
                        "priority": group.consolidation_priority.value,
                        "affected_files": self._get_affected_files(group),
                        "consolidation_approach": self._get_consolidation_approach(
                            group
                        ),
                    }
                )
            return steps
        except Exception as exc:  # pragma: no cover - logging
            self.logger.error("Failed to generate consolidation steps: %s", exc)
            return []

    def _get_affected_files(self, group: DuplicationGroup) -> List[str]:
        try:
            files = set()
            for instance in group.instances:
                for location in instance.locations:
                    if "file" in location:
                        files.add(str(location["file"]))
            return list(files)
        except Exception:
            return []

    def _get_consolidation_approach(self, group: DuplicationGroup) -> str:
        try:
            approaches = {
                DuplicationType.EXACT_MATCH: "Extract to constants or utility functions",
                DuplicationType.FUNCTION_DUPLICATE: "Create shared utility module",
                DuplicationType.CLASS_DUPLICATE: "Use inheritance or composition",
                DuplicationType.PATTERN_DUPLICATE: "Extract to decorators or base classes",
                DuplicationType.NEAR_DUPLICATE: "Refactor to share common code",
                DuplicationType.STRUCTURAL_DUPLICATE: "Create abstract base classes",
                DuplicationType.LOGIC_DUPLICATE: "Extract business logic to services",
            }
            return approaches.get(group.duplication_type, "Manual refactoring required")
        except Exception:
            return "Manual refactoring required"

    def _calculate_expected_benefits(
        self, duplication_groups: List[DuplicationGroup]
    ) -> Dict[str, Any]:
        try:
            total_duplications = sum(len(g.instances) for g in duplication_groups)
            total_lines = sum(
                sum(instance.lines_count for instance in g.instances)
                for g in duplication_groups
            )
            return {
                "code_reduction": f"{total_lines} lines",
                "maintenance_improvement": "High",
                "readability_improvement": "High",
                "bug_reduction": "Medium",
                "development_speed": "Improved",
            }
        except Exception:
            return {}

    def _assess_consolidation_risks(
        self, duplication_groups: List[DuplicationGroup]
    ) -> Dict[str, Any]:
        try:
            return {
                "breaking_changes": "Low",
                "testing_effort": "Medium",
                "integration_complexity": "Low",
                "rollback_difficulty": "Low",
                "overall_risk": "Low",
            }
        except Exception:
            return {}

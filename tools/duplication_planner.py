#!/usr/bin/env python3
"""
Duplication Consolidation Planner - V2 Compliant
=================================================

Generates consolidation plans from duplication analysis.
Extracted from duplication_analyzer.py for V2 compliance.

Author: Agent-3 - Infrastructure & DevOps Specialist (extracted)
"""

from typing import Any


class DuplicationPlanner:
    """Generates consolidation plans for duplications."""

    def generate_consolidation_plan(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """Generate detailed consolidation plan."""
        plan = {
            "safe_consolidations": [],
            "risky_consolidations": [],
            "manual_review_required": [],
            "estimated_effort": {},
            "risk_assessment": {},
        }

        # Process true duplicates (safest)
        for duplicate in analysis["true_duplicates"]:
            instances = duplicate["instances"]
            if len(instances) >= 2:
                consolidation = {
                    "type": "exact_duplicate",
                    "target_file": self._choose_target_file(instances),
                    "source_files": [inst["file"] for inst in instances],
                    "function_class": instances[0]["name"],
                    "risk_level": "LOW",
                    "effort": "SMALL",
                }
                plan["safe_consolidations"].append(consolidation)

        # Process similar functions (medium risk)
        for similar in analysis["similar_functions"]:
            instances = similar["instances"]
            if len(instances) >= 2:
                consolidation = {
                    "type": "similar_function",
                    "target_file": self._choose_target_file(instances),
                    "source_files": [inst["file"] for inst in instances],
                    "function_class": instances[0]["name"],
                    "similarity_score": similar["similarity_score"],
                    "risk_level": "MEDIUM",
                    "effort": "MEDIUM",
                }
                plan["risky_consolidations"].append(consolidation)

        # Process false duplicates (manual review)
        for false_dup in analysis["false_duplicates"]:
            instances = false_dup["instances"]
            if len(instances) >= 2:
                review_item = {
                    "type": "potential_false_duplicate",
                    "files": [inst["file"] for inst in instances],
                    "function_class": instances[0]["name"],
                    "domains": list(set(self._get_file_domain(inst["file"]) for inst in instances)),
                    "reason": "Different domains or purposes despite similar code",
                }
                plan["manual_review_required"].append(review_item)

        return plan

    def _choose_target_file(self, instances: list[dict]) -> str:
        """Choose the best target file for consolidation."""
        priority_order = ["core", "services", "utils", "web", "tests"]

        for domain in priority_order:
            for instance in instances:
                if domain in instance["file"]:
                    return instance["file"]

        return instances[0]["file"]

    def _get_file_domain(self, file_path: str) -> str:
        """Get the domain/module category of a file."""
        path_parts = file_path.split("/")
        if len(path_parts) >= 2:
            return path_parts[1]
        return "unknown"

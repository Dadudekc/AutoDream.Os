#!/usr/bin/env python3
"""
LOC Remediator - V2 Compliance Module
===================================

Focused module for providing remediation suggestions for LOC violations.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Test Type: LOC Remediation
"""

import json
from pathlib import Path
from typing import Any


class LOCRemediator:
    """Provides remediation suggestions for LOC violations."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.runtime_dir = project_root / "runtime"
        self.runtime_dir.mkdir(exist_ok=True)

    def generate_remediation_plan(self, violations: list[dict[str, Any]]) -> dict[str, Any]:
        """Generate remediation plan for violations."""
        plan = {
            "total_violations": len(violations),
            "file_violations": [],
            "class_violations": [],
            "function_violations": [],
            "recommendations": []
        }

        for violation_group in violations:
            for violation in violation_group.get("violations", []):
                violation_type = violation.get("type")
                
                if violation_type == "file_loc":
                    plan["file_violations"].append(violation)
                    plan["recommendations"].append(self._get_file_remediation(violation))
                
                elif violation_type == "class_loc":
                    plan["class_violations"].append(violation)
                    plan["recommendations"].append(self._get_class_remediation(violation))
                
                elif violation_type == "function_loc":
                    plan["function_violations"].append(violation)
                    plan["recommendations"].append(self._get_function_remediation(violation))

        return plan

    def _get_file_remediation(self, violation: dict[str, Any]) -> dict[str, Any]:
        """Get remediation suggestions for file LOC violations."""
        return {
            "type": "file_split",
            "file": violation["file"],
            "priority": "high",
            "description": f"Split large file ({violation['current']} lines) into smaller modules",
            "suggestions": [
                "Create core.py for main functionality",
                "Create utils.py for utility functions", 
                "Create models.py for data models",
                "Extract classes into separate modules"
            ],
            "estimated_effort": "medium"
        }

    def _get_class_remediation(self, violation: dict[str, Any]) -> dict[str, Any]:
        """Get remediation suggestions for class LOC violations."""
        return {
            "type": "class_refactor",
            "file": violation["file"],
            "class": violation["class"],
            "priority": "medium",
            "description": f"Refactor large class {violation['class']} ({violation['current']} lines)",
            "suggestions": [
                "Extract methods into utility classes",
                "Split into multiple smaller classes",
                "Use composition instead of inheritance",
                "Extract common functionality to base classes"
            ],
            "estimated_effort": "high"
        }

    def _get_function_remediation(self, violation: dict[str, Any]) -> dict[str, Any]:
        """Get remediation suggestions for function LOC violations."""
        return {
            "type": "function_split",
            "file": violation["file"],
            "function": violation["function"],
            "priority": "low",
            "description": f"Split large function {violation['function']} ({violation['current']} lines)",
            "suggestions": [
                "Extract helper functions",
                "Split into multiple smaller functions",
                "Use early returns to reduce nesting",
                "Extract complex logic into separate methods"
            ],
            "estimated_effort": "low"
        }

    def save_remediation_plan(self, plan: dict[str, Any]) -> Path:
        """Save remediation plan to file."""
        plan_path = self.runtime_dir / "v2_refactor_plan.json"
        
        with open(plan_path, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2)
        
        return plan_path

    def generate_human_readable_report(self, plan: dict[str, Any]) -> Path:
        """Generate human-readable remediation report."""
        report_path = self.runtime_dir / "refactor_suggestions.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("V2 LOC VIOLATION REMEDIATION PLAN\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Total Violations: {plan['total_violations']}\n")
            f.write(f"File Violations: {len(plan['file_violations'])}\n")
            f.write(f"Class Violations: {len(plan['class_violations'])}\n")
            f.write(f"Function Violations: {len(plan['function_violations'])}\n\n")
            
            f.write("RECOMMENDATIONS:\n")
            f.write("-" * 20 + "\n")
            
            for i, rec in enumerate(plan['recommendations'], 1):
                f.write(f"{i}. [{rec['priority'].upper()}] {rec['description']}\n")
                f.write(f"   File: {rec['file']}\n")
                f.write(f"   Effort: {rec['estimated_effort']}\n")
                f.write("   Suggestions:\n")
                for suggestion in rec['suggestions']:
                    f.write(f"     - {suggestion}\n")
                f.write("\n")
        
        return report_path

"""
V2 Compliance Refactoring Suggestions
====================================

Refactoring suggestions and planning for V2 compliance violations.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class RefactorPlanner:
    """Generates refactoring suggestions for V2 compliance violations."""
    
    def __init__(self):
        self.refactor_suggestions = []
    
    def generate_refactor_suggestions(self, results: dict[str, Any]) -> dict[str, Any]:
        """Generate refactoring suggestions based on analysis results."""
        refactor_plan = {
            "project_root": results["project_root"],
            "total_suggestions": 0,
            "suggestions_by_type": {},
            "file_suggestions": [],
            "priority_actions": []
        }
        
        for file_result in results["files"]:
            if not file_result["violations"]:
                continue
                
            file_suggestions = self._analyze_file_violations(file_result)
            if file_suggestions:
                refactor_plan["file_suggestions"].append(file_suggestions)
                refactor_plan["total_suggestions"] += len(file_suggestions["suggestions"])
        
        # Generate priority actions
        refactor_plan["priority_actions"] = self._generate_priority_actions(refactor_plan)
        
        return refactor_plan
    
    def _analyze_file_violations(self, file_result: dict[str, Any]) -> dict[str, Any] | None:
        """Analyze violations for a single file and generate suggestions."""
        suggestions = []
        file_path = file_result["file"]
        
        for violation in file_result["violations"]:
            suggestion = self._generate_violation_suggestion(violation, file_path)
            if suggestion:
                suggestions.append(suggestion)
        
        if not suggestions:
            return None
        
        return {
            "file": file_path,
            "lines": file_result["lines"],
            "violation_count": len(file_result["violations"]),
            "suggestions": suggestions
        }
    
    def _generate_violation_suggestion(self, violation: dict[str, Any], file_path: str) -> dict[str, Any] | None:
        """Generate suggestion for a specific violation."""
        violation_type = violation["type"]
        
        if violation_type == "file_loc":
            return {
                "type": "file_split",
                "priority": "high",
                "description": f"Split large file into smaller modules",
                "action": "Create separate modules for different concerns",
                "estimated_effort": "medium",
                "files_to_create": [
                    f"{file_path.replace('.py', '_core.py')}",
                    f"{file_path.replace('.py', '_utils.py')}",
                    f"{file_path.replace('.py', '_main.py')}"
                ]
            }
        
        elif violation_type == "class_loc":
            return {
                "type": "class_refactor",
                "priority": "high",
                "description": f"Refactor large class '{violation.get('class_name', 'Unknown')}'",
                "action": "Extract methods into separate utility classes",
                "estimated_effort": "medium",
                "suggested_approach": "Use composition and delegation pattern"
            }
        
        elif violation_type == "function_loc":
            return {
                "type": "function_split",
                "priority": "medium",
                "description": f"Split large function '{violation.get('function_name', 'Unknown')}'",
                "action": "Break into smaller, focused functions",
                "estimated_effort": "low",
                "suggested_approach": "Extract helper functions and use early returns"
            }
        
        elif violation_type == "print_statement":
            return {
                "type": "logging_migration",
                "priority": "low",
                "description": "Replace print statements with proper logging",
                "action": "Import logging and replace print() calls",
                "estimated_effort": "low",
                "suggested_approach": "Use logger.info(), logger.debug(), etc."
            }
        
        elif violation_type == "line_length":
            return {
                "type": "line_formatting",
                "priority": "low",
                "description": "Fix long lines",
                "action": "Break long lines using proper Python formatting",
                "estimated_effort": "low",
                "suggested_approach": "Use line continuation, string concatenation, or variable assignment"
            }
        
        return None
    
    def _generate_priority_actions(self, refactor_plan: dict[str, Any]) -> list[dict[str, Any]]:
        """Generate prioritized action list."""
        actions = []
        
        # Count suggestions by type
        type_counts = {}
        for file_suggestion in refactor_plan["file_suggestions"]:
            for suggestion in file_suggestion["suggestions"]:
                suggestion_type = suggestion["type"]
                type_counts[suggestion_type] = type_counts.get(suggestion_type, 0) + 1
        
        # Create priority actions
        for suggestion_type, count in type_counts.items():
            if suggestion_type in ["file_split", "class_refactor"]:
                priority = "high"
            elif suggestion_type in ["function_split"]:
                priority = "medium"
            else:
                priority = "low"
            
            actions.append({
                "type": suggestion_type,
                "count": count,
                "priority": priority,
                "description": f"Address {count} {suggestion_type} violations"
            })
        
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
# SECURITY: Key placeholder - replace with environment variable
        
        return actions


def generate_refactor_suggestions(results: dict[str, Any]) -> dict[str, Any]:
    """Generate refactoring suggestions for V2 compliance violations."""
    planner = RefactorPlanner()
    return planner.generate_refactor_suggestions(results)


def format_refactor_report(refactor_plan: dict[str, Any]) -> str:
    """Format refactor plan as human-readable report."""
    output = []
    output.append("=" * 80)
    output.append("V2 COMPLIANCE REFACTOR PLAN")
    output.append("=" * 80)
    output.append("")
    
    # Summary
    output.append("REFACTOR SUMMARY:")
    output.append(f"  Total suggestions: {refactor_plan['total_suggestions']}")
    output.append(f"  Files needing refactoring: {len(refactor_plan['file_suggestions'])}")
    output.append("")
    
    # Priority actions
    output.append("PRIORITY ACTIONS:")
    for action in refactor_plan["priority_actions"]:
        output.append(f"  [{action['priority'].upper()}] {action['description']}")
    output.append("")
    
    # File-specific suggestions
    output.append("FILE-SPECIFIC SUGGESTIONS:")
    for file_suggestion in refactor_plan["file_suggestions"]:
        output.append(f"  {file_suggestion['file']} ({file_suggestion['lines']} lines)")
        output.append(f"    Violations: {file_suggestion['violation_count']}")
        output.append(f"    Suggestions: {len(file_suggestion['suggestions'])}")
        
        for suggestion in file_suggestion["suggestions"]:
            output.append(f"      [{suggestion['priority'].upper()}] {suggestion['description']}")
            output.append(f"        Action: {suggestion['action']}")
            if "files_to_create" in suggestion:
                output.append(f"        Files to create: {', '.join(suggestion['files_to_create'])}")
        output.append("")
    
    return "\n".join(output)



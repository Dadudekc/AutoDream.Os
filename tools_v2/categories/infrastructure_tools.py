#!/usr/bin/env python3
"""
Infrastructure Tools - Agent Toolbelt V2
========================================

Infrastructure analysis and optimization tools for agents.
Created based on Agent-3 session learnings.

Author: Agent-3 (Infrastructure & DevOps) - Toolbelt Expansion
License: MIT
"""

import logging
from pathlib import Path
from typing import Any

from ..adapters.base_adapter import IToolAdapter

logger = logging.getLogger(__name__)


class OrchestratorScanTool(IToolAdapter):
    """Scan all orchestrators for violations and performance issues."""

    def get_name(self) -> str:
        return "orchestrator_scan"

    def get_description(self) -> str:
        return "Scan all orchestrator files for V2 violations and performance bottlenecks"

    def execute(self, **kwargs) -> dict[str, Any]:
        """Execute orchestrator scan."""
        try:
            violations = []
            all_orchestrators = []

            # Find all orchestrator files
            patterns = ["*orchestrat*.py"]
            for pattern in patterns:
                files = list(Path(".").rglob(pattern))
                for f in files:
                    if f.is_file():
                        try:
                            lines = len(open(f).readlines())
                            all_orchestrators.append((str(f), lines))

                            # Check for violations
                            if lines > 400:
                                violations.append(
                                    {
                                        "file": str(f),
                                        "lines": lines,
                                        "severity": "CRITICAL",
                                        "over_limit": lines - 400,
                                    }
                                )
                            elif lines > 300:
                                violations.append(
                                    {
                                        "file": str(f),
                                        "lines": lines,
                                        "severity": "HIGH",
                                        "over_limit": lines - 300,
                                    }
                                )
                            elif lines > 250:
                                violations.append(
                                    {
                                        "file": str(f),
                                        "lines": lines,
                                        "severity": "MEDIUM",
                                        "approaching_limit": 400 - lines,
                                    }
                                )
                        except:
                            pass

            # Sort by line count
            all_orchestrators.sort(key=lambda x: x[1], reverse=True)
            violations.sort(key=lambda x: x.get("lines", 0), reverse=True)

            return {
                "success": True,
                "total_orchestrators": len(all_orchestrators),
                "violations": violations,
                "violation_count": len(violations),
                "top_10_largest": [
                    {"file": f, "lines": lines} for f, lines in all_orchestrators[:10]
                ],
            }

        except Exception as e:
            logger.error(f"Orchestrator scan failed: {e}")
            return {"success": False, "error": str(e)}


class FileLineCounterTool(IToolAdapter):
    """Quick line count for files (V2 compliance checking)."""

    def get_name(self) -> str:
        return "file_lines"

    def get_description(self) -> str:
        return "Count lines in file(s) for V2 compliance verification"

    def execute(self, **kwargs) -> dict[str, Any]:
        """Execute line count."""
        try:
            files = kwargs.get("files", [])
            if isinstance(files, str):
                files = [files]

            results = []
            for filepath in files:
                try:
                    lines = len(open(filepath).readlines())
                    compliant = lines <= 400
                    results.append(
                        {
                            "file": filepath,
                            "lines": lines,
                            "v2_compliant": compliant,
                            "buffer": 400 - lines if compliant else None,
                            "over_by": lines - 400 if not compliant else None,
                        }
                    )
                except Exception as e:
                    results.append({"file": filepath, "error": str(e)})

            return {
                "success": True,
                "results": results,
                "total_files": len(results),
                "compliant_count": sum(1 for r in results if r.get("v2_compliant")),
            }

        except Exception as e:
            return {"success": False, "error": str(e)}


class ModuleExtractorPlannerTool(IToolAdapter):
    """Analyze file and suggest extraction opportunities."""

    def get_name(self) -> str:
        return "extract_planner"

    def get_description(self) -> str:
        return "Analyze file and suggest modular extraction plan"

    def execute(self, **kwargs) -> dict[str, Any]:
        """Execute extraction planning."""
        try:
            filepath = kwargs.get("file")
            if not filepath:
                return {"success": False, "error": "No file specified"}

            with open(filepath) as f:
                content = f.read()
                lines = content.splitlines()

            # Count classes and functions
            classes = [l.strip() for l in lines if l.strip().startswith("class ")]
            functions = [l.strip() for l in lines if "def " in l and not l.strip().startswith("#")]
            imports = [l.strip() for l in lines if l.strip().startswith(("import ", "from "))]

            # Suggest extractions
            suggestions = []

            if len(classes) > 5:
                suggestions.append(
                    {
                        "type": "class_extraction",
                        "reason": f"{len(classes)} classes (>5 limit)",
                        "recommendation": "Extract classes into logical groups",
                    }
                )

            if len(functions) > 30:
                suggestions.append(
                    {
                        "type": "function_extraction",
                        "reason": f"{len(functions)} functions (high count)",
                        "recommendation": "Group related functions into modules",
                    }
                )

            if len(lines) > 400:
                suggestions.append(
                    {
                        "type": "file_size",
                        "reason": f"{len(lines)} lines (>400 V2 limit)",
                        "recommendation": f"Extract {len(lines) - 400}+ lines",
                    }
                )

            return {
                "success": True,
                "file": filepath,
                "metrics": {
                    "lines": len(lines),
                    "classes": len(classes),
                    "functions": len(functions),
                    "imports": len(imports),
                },
                "class_list": classes[:20],  # First 20
                "function_list": functions[:20],
                "suggestions": suggestions,
                "needs_extraction": len(suggestions) > 0,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}


class ROICalculatorTool(IToolAdapter):
    """Calculate ROI for refactoring tasks."""

    def get_name(self) -> str:
        return "roi_calculator"

    def get_description(self) -> str:
        return "Calculate ROI for refactoring tasks (points/complexity)"

    def execute(self, **kwargs) -> dict[str, Any]:
        """Calculate ROI."""
        try:
            points = kwargs.get("points", 0)
            complexity = kwargs.get("complexity", 1)
            v2_impact = kwargs.get("v2_impact", 0)
            autonomy_impact = kwargs.get("autonomy_impact", 0)

            # ROI formula from Markov optimizer
            reward = points + (v2_impact * 100) + (autonomy_impact * 200)
            difficulty = max(complexity, 1)  # Avoid division by zero
            roi = reward / difficulty

            return {
                "success": True,
                "points": points,
                "complexity": complexity,
                "v2_impact": v2_impact,
                "autonomy_impact": autonomy_impact,
                "reward": reward,
                "difficulty": difficulty,
                "roi": round(roi, 2),
                "rating": (
                    "EXCELLENT"
                    if roi > 20
                    else "GOOD" if roi > 15 else "FAIR" if roi > 10 else "LOW"
                ),
            }

        except Exception as e:
            return {"success": False, "error": str(e)}


__all__ = [
    "OrchestratorScanTool",
    "FileLineCounterTool",
    "ModuleExtractorPlannerTool",
    "ROICalculatorTool",
]

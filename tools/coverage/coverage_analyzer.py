#!/usr/bin/env python3
"""
Coverage Analyzer - V2 Compliance Module
=======================================

Focused module for analyzing test coverage data and identifying gaps.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Test Type: Coverage Analysis
"""

import subprocess
import sys
from pathlib import Path
from typing import Any


class CoverageAnalyzer:
    """Analyzes test coverage and identifies gaps."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.tests_dir = project_root / "tests"

    def run_coverage_analysis(self, target: str = "all") -> dict[str, Any]:
        """Run coverage analysis for target."""
        coverage_cmd = [
            sys.executable,
            "-m",
            "pytest",
            "--cov-report=json",
            "--cov-report=term-missing",
            f"--cov={self._get_coverage_target(target)}",
        ]

        if target != "all":
            coverage_cmd.extend(["-k", target])

        coverage_cmd.append(str(self.tests_dir))

        try:
            result = subprocess.run(
                coverage_cmd, cwd=self.project_root, capture_output=True, text=True, timeout=300
            )

            return {
                "command": " ".join(coverage_cmd),
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {"error": "Coverage analysis timed out", "success": False}

    def _get_coverage_target(self, target: str) -> str:
        """Get coverage target based on analysis target."""
        targets = {
            "messaging": "src.integration.messaging_gateway,src.services.consolidated_messaging_service,src.core.orchestration.intent_subsystems.message_router",
            "consolidated": "src.services.consolidated_messaging_service,src.services.consolidated_vector_service,src.services.consolidated_coordination_service",
            "routing": "src.core.orchestration.intent_subsystems.message_router",
            "gateway": "src.integration.messaging_gateway",
            "all": "src",
        }
        return targets.get(target, "src")

    def analyze_coverage_gaps(self, coverage_data: dict[str, Any]) -> list[dict[str, Any]]:
        """Analyze coverage gaps from coverage data."""
        gaps = []

        if not coverage_data.get("success"):
            return [{"error": "Coverage analysis failed", "details": coverage_data}]

        # Parse coverage output for gaps
        stdout = coverage_data.get("stdout", "")
        lines = stdout.split("\n")

        for line in lines:
            if "TOTAL" in line and "%" in line:
                # Extract total coverage percentage
                parts = line.split()
                for part in parts:
                    if "%" in part:
                        try:
                            coverage_pct = float(part.replace("%", ""))
                            if coverage_pct < 80:  # Threshold for gaps
                                gaps.append(
                                    {
                                        "type": "overall_coverage",
                                        "current": coverage_pct,
                                        "target": 80.0,
                                        "gap": 80.0 - coverage_pct,
                                    }
                                )
                        except ValueError:
                            pass
                        break

        return gaps

    def get_coverage_summary(self, coverage_data: dict[str, Any]) -> dict[str, Any]:
        """Get coverage summary from analysis results."""
        if not coverage_data.get("success"):
            return {"error": "Coverage analysis failed"}

        stdout = coverage_data.get("stdout", "")

        # Extract summary information
        summary = {"success": True, "raw_output": stdout, "has_coverage_data": "TOTAL" in stdout}

        # Parse total coverage if available
        for line in stdout.split("\n"):
            if "TOTAL" in line and "%" in line:
                parts = line.split()
                for part in parts:
                    if "%" in part:
                        try:
                            summary["total_coverage"] = float(part.replace("%", ""))
                        except ValueError:
                            pass
                        break

        return summary

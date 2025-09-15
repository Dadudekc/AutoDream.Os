#!/usr/bin/env python3
"""
Audit Analyzer - V2 Compliance Module
==================================

Focused module for analyzing audit results and identifying cleanup opportunities.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Test Type: Audit Analysis
"""

from pathlib import Path
from typing import Any


class AuditAnalyzer:
    """Analyzes audit results and identifies cleanup opportunities."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.min_py_files = 50
        self.max_py_drop = 10

    def analyze_scan_results(self, scan_results: dict[str, Any]) -> dict[str, Any]:
        """Analyze scan results and identify cleanup opportunities."""
        analysis = {
            "cleanup_opportunities": [],
            "risk_assessment": {},
            "recommendations": [],
            "file_type_analysis": {},
            "duplicate_analysis": {},
            "temp_file_analysis": {},
        }

        # Analyze file types
        analysis["file_type_analysis"] = self._analyze_file_types(scan_results)

        # Analyze duplicates
        analysis["duplicate_analysis"] = self._analyze_duplicates(scan_results)

        # Analyze temp files
        analysis["temp_file_analysis"] = self._analyze_temp_files(scan_results)

        # Generate cleanup opportunities
        analysis["cleanup_opportunities"] = self._generate_cleanup_opportunities(analysis)

        # Risk assessment
        analysis["risk_assessment"] = self._assess_risks(scan_results, analysis)

        # Generate recommendations
        analysis["recommendations"] = self._generate_recommendations(analysis)

        return analysis

    def _analyze_file_types(self, scan_results: dict[str, Any]) -> dict[str, Any]:
        """Analyze file types and sizes."""
        file_counts = scan_results.get("file_counts", {})
        file_sizes = scan_results.get("file_sizes", {})

        analysis = {
            "total_types": len(file_counts),
            "largest_types": [],
            "smallest_types": [],
            "size_distribution": {},
        }

        # Sort by count
        sorted_by_count = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)
        analysis["largest_types"] = sorted_by_count[:5]
        analysis["smallest_types"] = sorted_by_count[-5:]

        # Size distribution
        total_size = scan_results.get("total_size", 0)
        for ext, size in file_sizes.items():
            if total_size > 0:
                analysis["size_distribution"][ext] = {
                    "size": size,
                    "percentage": (size / total_size) * 100,
                }

        return analysis

    def _analyze_duplicates(self, scan_results: dict[str, Any]) -> dict[str, Any]:
        """Analyze duplicate files."""
        duplicate_groups = scan_results.get("duplicate_groups", {})

        analysis = {
            "total_duplicate_groups": 0,
            "total_duplicate_files": 0,
            "largest_duplicate_groups": [],
            "potential_savings": 0,
        }

        duplicate_groups_with_multiple = {
            hash_val: files for hash_val, files in duplicate_groups.items() if len(files) > 1
        }

        analysis["total_duplicate_groups"] = len(duplicate_groups_with_multiple)

        for hash_val, files in duplicate_groups_with_multiple.items():
            analysis["total_duplicate_files"] += len(files)

            # Calculate potential savings (keep one, remove others)
            if len(files) > 1:
                try:
                    file_path = Path(files[0])
                    if file_path.exists():
                        file_size = file_path.stat().st_size
                        savings = file_size * (len(files) - 1)
                        analysis["potential_savings"] += savings
                except Exception:
                    pass

        # Sort by group size
        analysis["largest_duplicate_groups"] = sorted(
            duplicate_groups_with_multiple.items(), key=lambda x: len(x[1]), reverse=True
        )[:5]

        return analysis

    def _analyze_temp_files(self, scan_results: dict[str, Any]) -> dict[str, Any]:
        """Analyze temporary files."""
        temp_files = scan_results.get("temp_files", [])

        analysis = {
            "total_temp_files": len(temp_files),
            "temp_file_types": {},
            "temp_file_sizes": 0,
            "safe_to_delete": [],
        }

        for temp_file in temp_files:
            try:
                file_path = Path(temp_file)
                if file_path.exists():
                    file_size = file_path.stat().st_size
                    analysis["temp_file_sizes"] += file_size

                    # Categorize by type
                    ext = file_path.suffix.lower()
                    analysis["temp_file_types"][ext] = analysis["temp_file_types"].get(ext, 0) + 1

                    # Check if safe to delete
                    if self._is_safe_to_delete(file_path):
                        analysis["safe_to_delete"].append(temp_file)
            except Exception:
                pass

        return analysis

    def _is_safe_to_delete(self, file_path: Path) -> bool:
        """Check if file is safe to delete."""
        # Add safety checks here
        safe_patterns = [".tmp", ".temp", ".bak", ".backup", "~"]
        file_name = file_path.name.lower()

        return any(pattern in file_name for pattern in safe_patterns)

    def _generate_cleanup_opportunities(self, analysis: dict[str, Any]) -> list[dict[str, Any]]:
        """Generate cleanup opportunities."""
        opportunities = []

        # Duplicate file cleanup
        duplicate_analysis = analysis.get("duplicate_analysis", {})
        if duplicate_analysis.get("total_duplicate_groups", 0) > 0:
            opportunities.append(
                {
                    "type": "duplicate_files",
                    "priority": "high",
                    "description": f"Remove {duplicate_analysis['total_duplicate_files']} duplicate files",
                    "potential_savings": duplicate_analysis.get("potential_savings", 0),
                    "risk": "low",
                }
            )

        # Temp file cleanup
        temp_analysis = analysis.get("temp_file_analysis", {})
        if temp_analysis.get("total_temp_files", 0) > 0:
            opportunities.append(
                {
                    "type": "temp_files",
                    "priority": "medium",
                    "description": f"Remove {temp_analysis['total_temp_files']} temporary files",
                    "potential_savings": temp_analysis.get("temp_file_sizes", 0),
                    "risk": "low",
                }
            )

        return opportunities

    def _assess_risks(
        self, scan_results: dict[str, Any], analysis: dict[str, Any]
    ) -> dict[str, Any]:
        """Assess risks of cleanup operations."""
        risks = {
            "overall_risk": "low",
            "py_file_count": scan_results.get("file_counts", {}).get(".py", 0),
            "py_file_risk": "low",
            "cleanup_risks": [],
        }

        # Check Python file count
        py_count = risks["py_file_count"]
        if py_count < self.min_py_files:
            risks["py_file_risk"] = "high"
            risks["cleanup_risks"].append("Low Python file count - cleanup may be risky")
        elif py_count < self.min_py_files * 1.5:
            risks["py_file_risk"] = "medium"
            risks["cleanup_risks"].append("Python file count is low - proceed with caution")

        # Overall risk assessment
        if risks["py_file_risk"] == "high":
            risks["overall_risk"] = "high"
        elif risks["py_file_risk"] == "medium":
            risks["overall_risk"] = "medium"

        return risks

    def _generate_recommendations(self, analysis: dict[str, Any]) -> list[str]:
        """Generate cleanup recommendations."""
        recommendations = []

        risks = analysis.get("risk_assessment", {})
        opportunities = analysis.get("cleanup_opportunities", [])

        if risks.get("overall_risk") == "high":
            recommendations.append("High risk detected - use --force flag with caution")
        elif risks.get("overall_risk") == "medium":
            recommendations.append("Medium risk - review cleanup opportunities carefully")

        if opportunities:
            recommendations.append(f"Found {len(opportunities)} cleanup opportunities")

            for opp in opportunities:
                if opp.get("priority") == "high":
                    recommendations.append(f"High priority: {opp['description']}")

        if not opportunities:
            recommendations.append("No significant cleanup opportunities found")

        return recommendations

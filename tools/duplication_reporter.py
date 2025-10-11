#!/usr/bin/env python3
"""
Duplication Reporter - V2 Compliant
====================================

Generates reports from duplication analysis.
Extracted from duplication_analyzer.py for V2 compliance.

Author: Agent-3 - Infrastructure & DevOps Specialist (extracted)
"""

from typing import Any


class DuplicationReporter:
    """Generates reports from duplication analysis."""

    def generate_report(self, scan_results: dict[str, Any], analysis: dict[str, Any]) -> str:
        """Generate comprehensive duplication analysis report."""
        report = []
        report.append("# 🔍 DUPLICATION ANALYSIS REPORT")
        report.append(f"**Generated:** {__import__('datetime').datetime.now().isoformat()}")
        report.append("")

        # Summary
        summary = scan_results["summary"]
        report.append("## 📊 SCAN SUMMARY")
        report.append(f"- Total Python files: {summary['total_files']}")
        report.append(f"- Files processed: {summary['processed_files']}")
        report.append(f"- Function groups found: {summary['function_groups']}")
        report.append(f"- Class groups found: {summary['class_groups']}")
        report.append(f"- Potential duplicates: {summary['potential_duplicates']}")
        report.append("")

        # Detailed Analysis
        report.append("## 🔍 DETAILED ANALYSIS")
        report.append(f"- **True Duplicates:** {len(analysis['true_duplicates'])} (SAFE)")
        report.append(f"- **Similar Functions:** {len(analysis['similar_functions'])} (REVIEW)")
        report.append(f"- **False Duplicates:** {len(analysis['false_duplicates'])} (IGNORE)")
        report.append("")

        # Consolidation Plan
        plan = analysis["consolidation_plan"]
        report.append("## 🎯 CONSOLIDATION PLAN")
        report.append(f"- **Safe:** {len(plan['safe_consolidations'])}")
        report.append(f"- **Risky:** {len(plan['risky_consolidations'])}")
        report.append(f"- **Manual Review:** {len(plan['manual_review_required'])}")
        report.append("")

        # Safe Consolidations
        if plan["safe_consolidations"]:
            report.append("### ✅ SAFE CONSOLIDATIONS")
            for i, c in enumerate(plan["safe_consolidations"][:10], 1):
                report.append(f"{i}. **{c['function_class']}**")
                report.append(f"   - Target: `{c['target_file']}`")
                report.append(f"   - Sources: {len(c['source_files'])} files")
                report.append("")

        # Recommendations
        report.append("## 🎯 RECOMMENDATIONS")
        report.append("1. Start with Safe Consolidations")
        report.append("2. Review Risky Consolidations Carefully")
        report.append("3. Leave False Duplicates Alone")
        report.append("4. Test After Each Consolidation")

        return "\n".join(report)

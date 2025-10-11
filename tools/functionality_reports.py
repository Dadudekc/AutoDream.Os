#!/usr/bin/env python3
"""
Functionality Verification Reports
===================================

Generates verification reports and analysis.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
Refactored from: functionality_verification.py
License: MIT
"""

from typing import Any


class FunctionalityReports:
    """Generates verification reports."""

    @staticmethod
    def generate_report(
        comparison: dict[str, Any], test_results: dict[str, Any] | None = None
    ) -> str:
        """Generate comprehensive verification report."""
        lines = []
        lines.append("=" * 80)
        lines.append("FUNCTIONALITY VERIFICATION REPORT")
        lines.append("=" * 80)
        lines.append(f"Timestamp: {comparison.get('timestamp', 'N/A')}")
        lines.append(f"Baseline: {comparison.get('baseline_timestamp', 'N/A')}")
        lines.append("")

        # Risk Assessment
        risk = comparison.get("risk_assessment", "UNKNOWN")
        risk_icon = {"LOW": "✅", "MEDIUM": "⚠️", "HIGH": "🔴"}.get(risk, "❓")
        lines.append(f"RISK ASSESSMENT: {risk_icon} {risk}")
        lines.append("")

        # Files Changed
        if comparison.get("files_changed"):
            lines.append(f"FILES CHANGED: {len(comparison['files_changed'])}")
            for change in comparison["files_changed"][:10]:  # Show first 10
                lines.append(f"  {change}")
            if len(comparison["files_changed"]) > 10:
                lines.append(f"  ... and {len(comparison['files_changed']) - 10} more")
            lines.append("")

        # Functions Lost
        if comparison.get("functions_lost"):
            lines.append(f"⚠️ FUNCTIONS LOST: {len(comparison['functions_lost'])}")
            for func in comparison["functions_lost"][:10]:
                lines.append(f"  {func}")
            if len(comparison["functions_lost"]) > 10:
                lines.append(f"  ... and {len(comparison['functions_lost']) - 10} more")
            lines.append("")

        # New Functions
        if comparison.get("new_functions"):
            lines.append(f"✅ NEW FUNCTIONS: {len(comparison['new_functions'])}")
            for func in comparison["new_functions"][:5]:
                lines.append(f"  {func}")
            if len(comparison["new_functions"]) > 5:
                lines.append(f"  ... and {len(comparison['new_functions']) - 5} more")
            lines.append("")

        # Test Results
        if test_results:
            lines.append("AGENT-SPECIFIC TESTS:")
            lines.append(f"  Agent: {test_results.get('agent_id', 'N/A')}")
            lines.append(f"  Status: {test_results.get('functionality_status', 'UNKNOWN')}")
            lines.append(f"  Tests Run: {len(test_results.get('tests_run', []))}")
            lines.append(f"  Tests Passed: {len(test_results.get('tests_passed', []))}")
            lines.append(f"  Tests Failed: {len(test_results.get('tests_failed', []))}")
            lines.append("")

            if test_results.get("tests_failed"):
                lines.append("FAILED TESTS:")
                for failure in test_results["tests_failed"][:5]:
                    if isinstance(failure, dict):
                        lines.append(f"  - {failure.get('test', 'Unknown')}")
                        if "error" in failure:
                            lines.append(f"    Error: {failure['error']}")
                lines.append("")

        # Recommendations
        lines.append("RECOMMENDATIONS:")
        if comparison.get("functions_lost"):
            lines.append("  🔴 CRITICAL: Functions lost - review consolidation carefully")
        if risk == "HIGH":
            lines.append("  🔴 HIGH RISK: Manual verification strongly recommended")
        elif risk == "MEDIUM":
            lines.append("  ⚠️ MEDIUM RISK: Run comprehensive test suite")
        else:
            lines.append("  ✅ LOW RISK: Changes appear safe")

        lines.append("=" * 80)
        return "\n".join(lines)

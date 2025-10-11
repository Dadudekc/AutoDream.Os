"""
Complexity Analyzer Formatters - Report Formatting
==================================================
Formatting utilities for complexity analysis reports.
Extracted for V2 compliance.

Author: Agent-5 (extracted from Agent-6's complexity_analyzer.py)
License: MIT
"""

from pathlib import Path
from typing import List

try:
    from .complexity_analyzer_core import ComplexityReport, ComplexityViolation
except ImportError:
    from complexity_analyzer_core import ComplexityReport, ComplexityViolation


def format_report(report: ComplexityReport, verbose: bool = False) -> str:
    """Format complexity report as string."""
    lines = []
    lines.append("=" * 80)
    lines.append(f"COMPLEXITY ANALYSIS: {Path(report.file_path).name}")
    lines.append("=" * 80)
    lines.append(f"Total functions analyzed: {report.total_functions}")
    lines.append(f"Average cyclomatic complexity: {report.avg_cyclomatic:.1f}")
    lines.append(f"Average cognitive complexity: {report.avg_cognitive:.1f}")
    lines.append(f"Maximum nesting depth: {report.max_nesting}")
    lines.append("")
    if report.has_violations:
        lines.append(f"⚠️  COMPLEXITY VIOLATIONS: {len(report.violations)}")
        lines.append("")
        # Group by severity
        high = [v for v in report.violations if v.severity == "HIGH"]
        medium = [v for v in report.violations if v.severity == "MEDIUM"]
        low = [v for v in report.violations if v.severity == "LOW"]
        if high:
            lines.append(f"🔴 HIGH SEVERITY: {len(high)} violations")
            for v in high:
                lines.append(
                    f"  Line {v.line_number}: {v.entity_name} - {v.violation_type} = {v.current_value} (threshold: {v.threshold})"
                )
                if verbose:
                    lines.append(f"\n{v.suggestion}\n")
        if medium:
            lines.append(f"🟡 MEDIUM SEVERITY: {len(medium)} violations")
            for v in medium:
                lines.append(
                    f"  Line {v.line_number}: {v.entity_name} - {v.violation_type} = {v.current_value} (threshold: {v.threshold})"
                )
                if verbose:
                    lines.append(f"\n{v.suggestion}\n")
        if low:
            lines.append(f"🟢 LOW SEVERITY: {len(low)} violations")
            for v in low[:5]:  # Limit low severity display
                lines.append(
                    f"  Line {v.line_number}: {v.entity_name} - {v.violation_type} = {v.current_value} (threshold: {v.threshold})"
                )
            if len(low) > 5:
                lines.append(f"  ... and {len(low) - 5} more low severity violations")
    else:
        lines.append("✅ No complexity violations found!")
    lines.append("")
    lines.append("=" * 80)
    return "\n".join(lines)


def generate_summary_report(reports: List[ComplexityReport], limit: int = 20) -> str:
    """Generate summary report for multiple files."""
    lines = []
    lines.append("=" * 80)
    lines.append("COMPLEXITY ANALYSIS SUMMARY")
    lines.append("=" * 80)
    lines.append(f"Files analyzed: {len(reports)}")
    files_with_violations = [r for r in reports if r.has_violations]
    lines.append(f"Files with violations: {len(files_with_violations)}")
    if not files_with_violations:
        lines.append("\n✅ All files have acceptable complexity!")
        lines.append("=" * 80)
        return "\n".join(lines)
    # Calculate totals
    total_violations = sum(len(r.violations) for r in files_with_violations)
    high_violations = sum(
        len([v for v in r.violations if v.severity == "HIGH"]) for r in files_with_violations
    )
    medium_violations = sum(
        len([v for v in r.violations if v.severity == "MEDIUM"]) for r in files_with_violations
    )
    low_violations = sum(
        len([v for v in r.violations if v.severity == "LOW"]) for r in files_with_violations
    )
    lines.append(f"Total violations: {total_violations}")
    lines.append(f"  🔴 HIGH: {high_violations}")
    lines.append(f"  🟡 MEDIUM: {medium_violations}")
    lines.append(f"  🟢 LOW: {low_violations}")
    lines.append("")
    # Show worst offenders
    lines.append(f"TOP {min(limit, len(files_with_violations))} FILES BY VIOLATIONS:")
    lines.append("")
    sorted_reports = sorted(files_with_violations, key=lambda x: len(x.violations), reverse=True)
    for i, report in enumerate(sorted_reports[:limit], 1):
        lines.append(f"{i}. {Path(report.file_path).name} - {len(report.violations)} violations")
        lines.append(
            f"   Avg cyclomatic: {report.avg_cyclomatic:.1f} | Avg cognitive: {report.avg_cognitive:.1f} | Max nesting: {report.max_nesting}"
        )
    lines.append("")
    lines.append("=" * 80)
    return "\n".join(lines)


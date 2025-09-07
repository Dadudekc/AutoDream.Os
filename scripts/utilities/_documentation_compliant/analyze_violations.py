#!/usr/bin/env python3
"""V2 coding standards violation analyzer.

This module scans the repository for files that exceed the V2 line-count
thresholds and optionally emits a human readable report. It returns a typed
dictionary with the raw data so other tooling can consume the results.
"""

from datetime import date
from pathlib import Path
from typing import List, Optional, Tuple, TypedDict

CRITICAL_THRESHOLD = 1000
MAJOR_THRESHOLD = 500
MODERATE_THRESHOLD = 300
MAX_DISPLAY = 10


class ViolationStats(TypedDict):
    """Structured results from :func:`analyze_violations`.

    Attributes:
        total_files: Number of ``.py`` files inspected.
        violations: List of ``(path, line_count)`` tuples for all violations.
        critical: Subset of ``violations`` with more than ``CRITICAL_THRESHOLD`` lines.
        major: Subset of ``violations`` between ``MAJOR_THRESHOLD`` and ``CRITICAL_THRESHOLD`` - 1 lines.
        moderate: Subset of ``violations`` between ``MODERATE_THRESHOLD`` + 1 and ``MAJOR_THRESHOLD`` - 1 lines.
        generated_on: ISO formatted date of when the analysis was run.
    """

    total_files: int
    violations: List[Tuple[str, int]]
    critical: List[Tuple[str, int]]
    major: List[Tuple[str, int]]
    moderate: List[Tuple[str, int]]
    generated_on: str


def analyze_violations(
        """
        analyze_violations
        
        Purpose: Automated function documentation
        """
    root: Path = Path("."),
    report: bool = True,
    report_path: Optional[Path] = None,
) -> ViolationStats:
    """Analyze Python files for V2 coding standards violations.

    Args:
        root: Directory to scan.
        report: If ``True`` the report is printed to stdout.
        report_path: Optional path to write the report to disk.

    Returns:
        A :class:`ViolationStats` dictionary containing totals and categorized
        violation lists.
    """

    violations: List[Tuple[str, int]] = []
    total_files = 0

    for file_path in root.rglob("*.py"):
        total_files += 1
        try:
            line_count = len(file_path.read_text(encoding="utf-8").splitlines())
            if line_count > MODERATE_THRESHOLD:
                violations.append((str(file_path), line_count))
        except Exception as exc:  # pragma: no cover - best effort logging
            if report:
                print(f"Error reading {file_path}: {exc}")

    violations.sort(key=lambda x: x[1], reverse=True)
    critical = [v for v in violations if v[1] >= CRITICAL_THRESHOLD]
    major = [
        v
        for v in violations
        if MAJOR_THRESHOLD <= v[1] < CRITICAL_THRESHOLD
    ]
    moderate = [
        v
        for v in violations
        if MODERATE_THRESHOLD < v[1] < MAJOR_THRESHOLD
    ]

    lines_out: List[str] = []
    lines_out.append("🚨 V2 CODING STANDARDS VIOLATIONS DETECTED")
    lines_out.append("=" * 60)

    def _append_section(header: str, items: List[Tuple[str, int]]) -> None:
        """
        _append_section
        
        Purpose: Automated function documentation
        """
        lines_out.append(f"\n{header}: {len(items)} files")
        for file_path, count in items[:MAX_DISPLAY]:
            lines_out.append(f"  {count:>4} lines: {file_path}")
        if len(items) > MAX_DISPLAY:
            lines_out.append(f"  ... and {len(items) - MAX_DISPLAY} more files")

    if critical:
        _append_section(
            f"🔴 CRITICAL VIOLATIONS ({CRITICAL_THRESHOLD}+ lines)", critical
        )

    if major:
        _append_section(
            f"⚠️  MAJOR VIOLATIONS ({MAJOR_THRESHOLD}-{CRITICAL_THRESHOLD - 1} lines)",
            major,
        )

    if moderate:
        _append_section(
            f"🟡 MODERATE VIOLATIONS ({MODERATE_THRESHOLD + 1}-{MAJOR_THRESHOLD - 1} lines)",
            moderate,
        )

    lines_out.append("\n📊 SUMMARY:")
    lines_out.append(f"  Total violations: {len(violations)} files")
    lines_out.append(
        f"  Critical ({CRITICAL_THRESHOLD}+): {len(critical)} files"
    )
    lines_out.append(
        f"  Major ({MAJOR_THRESHOLD}-{CRITICAL_THRESHOLD - 1}): {len(major)} files"
    )
    lines_out.append(
        f"  Moderate ({MODERATE_THRESHOLD + 1}-{MAJOR_THRESHOLD - 1}): {len(moderate)} files"
    )

    report_text = "\n".join(lines_out)
    if report:
        print(report_text)
    if report_path:
        report_path.write_text(report_text + "\n", encoding="utf-8")

    return {
        "total_files": total_files,
        "violations": violations,
        "critical": critical,
        "major": major,
        "moderate": moderate,
        "generated_on": date.today().isoformat(),
    }


if __name__ == "__main__":
    analyze_violations()


#!/usr/bin/env python3
"""
V2 Coding Standards Violation Analyzer
Agent-2 Emergency Response Tool
"""

import os
from datetime import date
from typing import Dict, List, Tuple


def analyze_violations(root: str = ".", report: bool = True) -> Dict[str, object]:
    """Analyze Python files for V2 coding standards violations.

    Args:
        root: Directory to scan.
        report: If True, prints a human-readable report.

    Returns:
        Dictionary containing total files, lists of violations and their
        severities.
    """

    violations: List[Tuple[str, int]] = []
    total_files = 0

    for dirpath, _, files in os.walk(root):
        for file in files:
            if file.endswith(".py"):
                total_files += 1
                file_path = os.path.join(dirpath, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = len(f.readlines())
                    if lines > 300:
                        violations.append((file_path, lines))
                except Exception as exc:  # pragma: no cover - best effort logging
                    if report:
                        print(f"Error reading {file_path}: {exc}")

    violations.sort(key=lambda x: x[1], reverse=True)
    critical = [v for v in violations if v[1] >= 1000]
    major = [v for v in violations if 500 <= v[1] < 1000]
    moderate = [v for v in violations if 300 < v[1] < 500]

    if report:
        print("🚨 V2 CODING STANDARDS VIOLATIONS DETECTED")
        print("=" * 60)

        if critical:
            print(f"\n🔴 CRITICAL VIOLATIONS (1000+ lines): {len(critical)} files")
            for file_path, lines in critical:
                print(f"  {lines:>4} lines: {file_path}")

        if major:
            print(f"\n⚠️  MAJOR VIOLATIONS (500-999 lines): {len(major)} files")
            for file_path, lines in major[:10]:
                print(f"  {lines:>4} lines: {file_path}")
            if len(major) > 10:
                print(f"  ... and {len(major) - 10} more files")

        if moderate:
            print(f"\n🟡 MODERATE VIOLATIONS (300-499 lines): {len(moderate)} files")
            for file_path, lines in moderate[:10]:
                print(f"  {lines:>4} lines: {file_path}")
            if len(moderate) > 10:
                print(f"  ... and {len(moderate) - 10} more files")

        print("\n📊 SUMMARY:")
        print(f"  Total violations: {len(violations)} files")
        print(f"  Critical (1000+): {len(critical)} files")
        print(f"  Major (500-999): {len(major)} files")
        print(f"  Moderate (300-499): {len(moderate)} files")

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

#!/usr/bin/env python3
"""
V2 Compliance Batch Checker
============================

Quickly check multiple files for V2 compliance (400 line limit).
Faster than running full project scanner.

Author: Agent-8 (Operations & Support Specialist)
Created: 2025-10-13
"""

import sys
from pathlib import Path


def check_file_compliance(file_path: Path, limit: int = 400) -> dict[str, any]:
    """Check single file for V2 compliance."""
    try:
        lines = file_path.read_text(encoding="utf-8").split("\n")
        line_count = len(lines)

        compliant = line_count <= limit
        status = "✅ COMPLIANT" if compliant else "❌ VIOLATION"

        return {
            "file": str(file_path),
            "lines": line_count,
            "limit": limit,
            "compliant": compliant,
            "status": status,
            "over_by": max(0, line_count - limit),
        }

    except Exception as e:
        return {
            "file": str(file_path),
            "lines": 0,
            "limit": limit,
            "compliant": False,
            "status": f"❌ ERROR: {e}",
            "over_by": 0,
        }


def batch_check(file_paths: list[Path], limit: int = 400) -> dict[str, any]:
    """Check multiple files for compliance."""
    results = []
    compliant_count = 0
    violation_count = 0

    for file_path in file_paths:
        result = check_file_compliance(file_path, limit)
        results.append(result)

        if result["compliant"]:
            compliant_count += 1
        else:
            violation_count += 1

    return {
        "results": results,
        "total_files": len(results),
        "compliant": compliant_count,
        "violations": violation_count,
        "compliance_rate": (compliant_count / len(results) * 100) if results else 0,
    }


def print_report(batch_results: dict[str, any]):
    """Print compliance report."""
    print("\n" + "=" * 80)
    print("📊 V2 COMPLIANCE BATCH CHECK")
    print("=" * 80)

    print(f"\n📁 Files Checked: {batch_results['total_files']}")
    print(f"✅ Compliant: {batch_results['compliant']}")
    print(f"❌ Violations: {batch_results['violations']}")
    print(f"📈 Compliance Rate: {batch_results['compliance_rate']:.1f}%")

    # Show violations first
    if batch_results["violations"] > 0:
        print(f"\n❌ VIOLATIONS ({batch_results['violations']}):")
        print("-" * 80)

        for result in batch_results["results"]:
            if not result["compliant"]:
                print(f"\n  {result['file']}")
                print(f"  Lines: {result['lines']} (over by {result['over_by']})")
                print(f"  Status: {result['status']}")

    # Show compliant files
    if batch_results["compliant"] > 0:
        print(f"\n✅ COMPLIANT FILES ({batch_results['compliant']}):")
        print("-" * 80)

        for result in batch_results["results"]:
            if result["compliant"]:
                print(f"  {result['file']:60s} {result['lines']:4d} lines")

    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python v2_compliance_batch_checker.py <file_or_directory> [file_or_directory...]"
        )
        print("\nExamples:")
        print("  python v2_compliance_batch_checker.py src/utils/*.py")
        print("  python v2_compliance_batch_checker.py src/core/")
        print("  python v2_compliance_batch_checker.py file1.py file2.py file3.py")
        sys.exit(1)

    # Collect all files to check
    files_to_check = []

    for arg in sys.argv[1:]:
        path = Path(arg)

        if path.is_file():
            files_to_check.append(path)
        elif path.is_dir():
            # Add all Python files in directory
            files_to_check.extend(path.rglob("*.py"))
        else:
            # Try as glob pattern
            for match in Path.cwd().glob(arg):
                if match.is_file():
                    files_to_check.append(match)

    if not files_to_check:
        print("❌ No files found to check!")
        sys.exit(1)

    # Run batch check
    results = batch_check(files_to_check)
    print_report(results)

    # Exit code based on violations
    sys.exit(0 if results["violations"] == 0 else 1)

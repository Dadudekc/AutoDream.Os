#!/usr/bin/env python3
"""
Coverage Threshold Validator
=============================

Validates test coverage meets thresholds.
Reads Jest/pytest coverage output and checks against targets.

Author: Agent-8 (Operations & Support Specialist)
Created: 2025-10-13
"""

import json
import sys
from pathlib import Path


def parse_jest_coverage_summary(coverage_dir: Path) -> dict[str, float]:
    """Parse Jest coverage-summary.json file."""
    summary_file = coverage_dir / "coverage-summary.json"

    if not summary_file.exists():
        print(f"❌ Coverage summary not found: {summary_file}")
        print("   Run: npm run test:coverage")
        return {}

    try:
        data = json.loads(summary_file.read_text())

        # Get total coverage
        total = data.get("total", {})

        return {
            "statements": total.get("statements", {}).get("pct", 0),
            "branches": total.get("branches", {}).get("pct", 0),
            "functions": total.get("functions", {}).get("pct", 0),
            "lines": total.get("lines", {}).get("pct", 0),
        }

    except Exception as e:
        print(f"❌ Error parsing coverage: {e}")
        return {}


def validate_coverage(coverage: dict[str, float], thresholds: dict[str, float]) -> bool:
    """Validate coverage meets thresholds."""

    print("\n" + "=" * 80)
    print("📊 COVERAGE THRESHOLD VALIDATION")
    print("=" * 80)

    if not coverage:
        print("\n❌ No coverage data available!")
        print("=" * 80 + "\n")
        return False

    print(f"\n{'Metric':<15} {'Actual':>8} {'Target':>8} {'Diff':>8} {'Status':>10}")
    print("-" * 80)

    all_passed = True

    for metric in ["statements", "branches", "functions", "lines"]:
        actual = coverage.get(metric, 0)
        target = thresholds.get(metric, 85)
        diff = actual - target

        passed = actual >= target
        status = "✅ PASS" if passed else "❌ FAIL"

        if not passed:
            all_passed = False

        print(f"{metric.capitalize():<15} {actual:7.2f}% {target:7.2f}% {diff:+7.2f}% {status:>10}")

    print("-" * 80)

    if all_passed:
        print("\n✅ ALL THRESHOLDS MET!")
        print("🏆 Coverage targets achieved!")
    else:
        print("\n❌ SOME THRESHOLDS NOT MET!")
        print("⚠️  Add more tests to reach targets")

    print("=" * 80 + "\n")

    return all_passed


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python coverage_validator.py <coverage_directory> [threshold]")
        print("\nExamples:")
        print("  python coverage_validator.py extensions/repository-navigator/coverage")
        print("  python coverage_validator.py coverage/ 90")
        sys.exit(1)

    coverage_dir = Path(sys.argv[1])
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 85.0

    if not coverage_dir.exists():
        print(f"❌ Coverage directory not found: {coverage_dir}")
        print("   Run tests with coverage first!")
        sys.exit(1)

    # Parse coverage
    coverage = parse_jest_coverage_summary(coverage_dir)

    # Set thresholds (same for all metrics)
    thresholds = {
        "statements": threshold,
        "branches": threshold,
        "functions": threshold,
        "lines": threshold,
    }

    # Validate
    passed = validate_coverage(coverage, thresholds)

    sys.exit(0 if passed else 1)

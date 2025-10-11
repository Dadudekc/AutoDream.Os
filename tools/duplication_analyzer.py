#!/usr/bin/env python3
"""
Duplication Analysis Tool - V2 Compliant
=========================================

Advanced duplication detection system for safe consolidation.
Refactored into modular architecture for V2 compliance.

Author: Agent-3 - Infrastructure & DevOps Specialist (V2 refactor)
Original: Agent-1 (Integration & Core Systems Specialist)

Usage:
    python tools/duplication_analyzer.py --scan
    python tools/duplication_analyzer.py --comprehensive
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.duplication_analysis import DuplicationAnalysis
from tools.duplication_reporter import DuplicationReporter
from tools.duplication_scanner import DuplicationScanner


class DuplicationAnalyzer:
    """Main orchestrator for duplication analysis."""

    def __init__(self):
        """Initialize analyzer with modular components."""
        self.project_root = project_root
        self.scanner = DuplicationScanner(project_root)
        self.analyzer = DuplicationAnalysis()
        self.reporter = DuplicationReporter()

    def scan_codebase(self):
        """Scan codebase for duplications."""
        return self.scanner.scan_codebase()

    def analyze_duplicates(self, scan_results):
        """Analyze duplication patterns."""
        return self.analyzer.analyze_duplicates(scan_results)

    def generate_report(self, scan_results, analysis):
        """Generate analysis report."""
        return self.reporter.generate_report(scan_results, analysis)


def main():
    """Main CLI function."""
    import argparse

    parser = argparse.ArgumentParser(description="Duplication Analysis Tool")
    parser.add_argument("--scan", action="store_true", help="Scan codebase")
    parser.add_argument("--comprehensive", action="store_true", help="Full analysis")

    args = parser.parse_args()

    analyzer = DuplicationAnalyzer()

    if args.scan:
        results = analyzer.scan_codebase()
        print(f"✅ Scan: {results['summary']['potential_duplicates']} potential duplicates")

    elif args.comprehensive:
        print("🔍 Running comprehensive analysis...")
        scan_results = analyzer.scan_codebase()
        analysis = analyzer.analyze_duplicates(scan_results)
        report = analyzer.generate_report(scan_results, analysis)

        # Save report
        report_file = project_root / "duplication_analysis_report.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"✅ Complete. Report: {report_file}")
        plan = analysis["consolidation_plan"]
        print(f"   Safe: {len(plan['safe_consolidations'])}")
        print(f"   Risky: {len(plan['risky_consolidations'])}")

    else:
        print("Usage: python tools/duplication_analyzer.py --scan | --comprehensive")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Audit Cleanup Tool - V2 Compliance Wrapper
=========================================

V2 compliant wrapper for the modular audit cleanup system.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Usage: python tools/audit_cleanup.py --scan
"""

import argparse
import sys
from pathlib import Path

# Add tools directory to path for imports
tools_dir = Path(__file__).parent
sys.path.insert(0, str(tools_dir))

from audit.audit_analyzer import AuditAnalyzer
from audit.audit_reporter import AuditReporter
from audit.audit_scanner import AuditScanner


def main():
    """Main entry point for audit cleanup tool."""
    parser = argparse.ArgumentParser(description="Audit Cleanup Tool")
    parser.add_argument(
        "--scan", action="store_true", help="Scan working tree for cleanup opportunities"
    )
    parser.add_argument("--analyze", action="store_true", help="Analyze scan results")
    parser.add_argument("--report", action="store_true", help="Generate comprehensive report")
    parser.add_argument("--force", action="store_true", help="Force cleanup even with high risk")

    args = parser.parse_args()

    project_root = Path(".")
    scanner = AuditScanner(project_root)
    analyzer = AuditAnalyzer(project_root)
    reporter = AuditReporter(project_root)

    if args.scan or args.analyze or args.report:
        print("🔍 Scanning working tree for cleanup opportunities...")

        # Scan working tree
        scan_results = scanner.scan_working_tree()

        # Compare with git if available
        git_comparison = scanner.compare_with_git(scan_results)
        scan_results["git_comparison"] = git_comparison

        # Analyze results
        analysis = analyzer.analyze_scan_results(scan_results)

        # Generate report
        report = reporter.generate_audit_report(scan_results, analysis)

        # Save reports
        json_path = reporter.save_json_report(report)
        md_path = reporter.save_markdown_report(report)

        print(f"📄 JSON report saved to: {json_path}")
        print(f"📄 Markdown report saved to: {md_path}")

        # Print summary
        reporter.print_audit_summary(report)

        # Exit with appropriate code
        risk_assessment = analysis.get("risk_assessment", {})
        overall_risk = risk_assessment.get("overall_risk", "low")

        if overall_risk == "high" and not args.force:
            print("\n⚠️  High risk detected! Use --force flag to proceed.")
            exit(1)
        else:
            print("\n✅ Audit cleanup analysis completed successfully!")
            exit(0)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

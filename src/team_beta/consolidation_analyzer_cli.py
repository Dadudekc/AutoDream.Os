#!/usr/bin/env python3
"""
Consolidation Analyzer CLI
=========================
Command-line interface for system consolidation analyzer
V2 Compliant: ≤400 lines, focused CLI operations
"""

import argparse
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.team_beta.consolidation_analyzer_core import (
    ConsolidationStatus,
    DuplicationSeverity,
    SystemConsolidationAnalyzerCore,
)


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="System Consolidation Analyzer CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze system duplications")
    analyze_parser.add_argument("--output", help="Output file for analysis results")

    # Plan command
    plan_parser = subparsers.add_parser("plan", help="Create consolidation plan")
    plan_parser.add_argument("--output", help="Output file for consolidation plan")

    # Status command
    status_parser = subparsers.add_parser("status", help="Show consolidation status")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update duplication status")
    update_parser.add_argument("name", help="Duplication name")
    update_parser.add_argument(
        "status", choices=[s.value for s in ConsolidationStatus], help="New status"
    )

    # Export command
    export_parser = subparsers.add_parser("export", help="Export full analysis")
    export_parser.add_argument("filepath", help="Output file path")

    # List command
    list_parser = subparsers.add_parser("list", help="List duplications")
    list_parser.add_argument(
        "--severity", choices=[s.value for s in DuplicationSeverity], help="Filter by severity"
    )
    list_parser.add_argument(
        "--status", choices=[s.value for s in ConsolidationStatus], help="Filter by status"
    )

    return parser


def handle_analyze(args, analyzer: SystemConsolidationAnalyzerCore) -> None:
    """Handle analyze command"""
    analysis = analyzer.manage_consolidation_operations("analyze")

    print("📊 Consolidation Analysis Results:")
    print(f"   Total duplications: {analysis['total_duplications']}")
    print(f"   SSOT violations: {analysis['ssot_violations']}")
    print(f"   V2 compliance issues: {analysis['v2_compliance_issues']}")
    print(f"   Maintenance complexity: {analysis['maintenance_complexity_score']:.1f}%")

    print("\n📈 Severity Breakdown:")
    for severity, count in analysis["duplications_by_severity"].items():
        print(f"   {severity.title()}: {count}")

    print("\n🎯 Priority Order:")
    for i, item in enumerate(analysis["consolidation_priority_order"], 1):
        print(f"   {i}. {item['name']} ({item['severity']}) - {item['file_count']} files")

    print(f"\n⚠️ Overall Risk Level: {analysis['risk_assessment']['overall_risk_level'].title()}")

    if args.output:
        with open(args.output, "w") as f:
            import json

            json.dump(analysis, f, indent=2)
        print(f"\n✅ Analysis saved to {args.output}")


def handle_plan(args, analyzer: SystemConsolidationAnalyzerCore) -> None:
    """Handle plan command"""
    plan = analyzer.manage_consolidation_operations("create_plan")

    consolidation_plan = plan["consolidation_plan"]

    print("🎯 Consolidation Plan:")
    print(f"   Estimated duration: {consolidation_plan['estimated_duration_days']} days")
    print(f"   Required agents: {', '.join(consolidation_plan['required_agents'])}")

    print("\n📋 Phases:")
    for phase in consolidation_plan["phases"]:
        print(f"   Phase {phase['phase']}: {phase['name']} ({phase['duration_days']} days)")
        print(f"     Responsible: {', '.join(phase['responsible_agents'])}")
        print(f"     Tasks: {len(phase['tasks'])} tasks")

    print("\n📊 Success Metrics:")
    for metric, value in consolidation_plan["success_metrics"].items():
        print(f"   {metric.replace('_', ' ').title()}: {value}")

    print("\n🛡️ Risk Mitigation:")
    for strategy, description in consolidation_plan["risk_mitigation"].items():
        print(f"   {strategy.replace('_', ' ').title()}: {description}")

    if args.output:
        with open(args.output, "w") as f:
            import json

            json.dump(plan, f, indent=2)
        print(f"\n✅ Plan saved to {args.output}")


def handle_status(args, analyzer: SystemConsolidationAnalyzerCore) -> None:
    """Handle status command"""
    progress = analyzer.manage_consolidation_operations("get_progress")

    print("📈 Consolidation Progress:")
    print(f"   Total duplications: {progress['total_duplications']}")
    print(f"   Completed: {progress['completed']}")
    print(f"   In progress: {progress['in_progress']}")
    print(f"   Pending: {progress['pending']}")
    print(f"   Completion: {progress['completion_percentage']:.1f}%")
    print(f"   Current phase: {progress['current_phase']}")


def handle_update(args, analyzer: SystemConsolidationAnalyzerCore) -> None:
    """Handle update command"""
    status = ConsolidationStatus(args.status)

    analyzer.manage_consolidation_operations("update_status", name=args.name, status=status)

    print(f"✅ Updated {args.name} status to {status.value}")


def handle_export(args, analyzer: SystemConsolidationAnalyzerCore) -> None:
    """Handle export command"""
    success = analyzer.manage_consolidation_operations("export", filepath=args.filepath)

    if success:
        print(f"✅ Full analysis exported to {args.filepath}")
    else:
        print("❌ Failed to export analysis")
        sys.exit(1)


def handle_list(args, analyzer: SystemConsolidationAnalyzerCore) -> None:
    """Handle list command"""
    duplications = analyzer.duplications

    # Filter by severity if specified
    if args.severity:
        severity = DuplicationSeverity(args.severity)
        duplications = [d for d in duplications if d.severity == severity]

    # Filter by status if specified
    if args.status:
        status = ConsolidationStatus(args.status)
        duplications = [d for d in duplications if d.status == status]

    if not duplications:
        print("No duplications found matching your criteria.")
        return

    print(f"Found {len(duplications)} duplications:")
    for dup in duplications:
        print(f"  🔍 {dup.name}")
        print(f"     Description: {dup.description}")
        print(f"     Severity: {dup.severity.value}")
        print(f"     Status: {dup.status.value}")
        print(f"     Files: {len(dup.files)} files")
        print(f"     Impact: {dup.impact}")
        print(f"     Plan: {dup.consolidation_plan}")
        if dup.dependencies:
            print(f"     Dependencies: {', '.join(dup.dependencies)}")
        if dup.risks:
            print(f"     Risks: {', '.join(dup.risks)}")
        print()


def main():
    """Main CLI function"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Initialize analyzer
    analyzer = SystemConsolidationAnalyzerCore()

    # Handle commands
    if args.command == "analyze":
        handle_analyze(args, analyzer)
    elif args.command == "plan":
        handle_plan(args, analyzer)
    elif args.command == "status":
        handle_status(args, analyzer)
    elif args.command == "update":
        handle_update(args, analyzer)
    elif args.command == "export":
        handle_export(args, analyzer)
    elif args.command == "list":
        handle_list(args, analyzer)


if __name__ == "__main__":
    main()

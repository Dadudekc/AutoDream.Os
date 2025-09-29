#!/usr/bin/env python3
"""
Project Update CLI - V2 Compliant
=================================

Command-line interface for project update messaging system.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import argparse
import json
import logging
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.messaging.project_update_system import ProjectUpdateSystem
from src.services.messaging.service import MessagingService

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Build command line argument parser."""
    parser = argparse.ArgumentParser(description="Project Update Messaging System CLI")

    parser.add_argument(
        "--dry-run", action="store_true", help="Dry run mode - don't actually send messages"
    )

    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    subparsers = parser.add_subparsers(dest="cmd", help="Available commands")

    # Project update command
    update_parser = subparsers.add_parser("update", help="Send project update")
    update_parser.add_argument("--type", required=True, help="Update type")
    update_parser.add_argument("--title", required=True, help="Update title")
    update_parser.add_argument("--description", required=True, help="Update description")
    update_parser.add_argument("--agents", help="Comma-separated list of agents (default: all)")
    update_parser.add_argument("--priority", default="NORMAL", help="Message priority")
    update_parser.add_argument("--metadata", help="JSON metadata")

    # Milestone command
    milestone_parser = subparsers.add_parser("milestone", help="Send milestone notification")
    milestone_parser.add_argument("--name", required=True, help="Milestone name")
    milestone_parser.add_argument("--description", required=True, help="Milestone description")
    milestone_parser.add_argument(
        "--completion", type=int, required=True, help="Completion percentage"
    )
    milestone_parser.add_argument("--next-steps", help="Comma-separated next steps")

    # System status command
    status_parser = subparsers.add_parser("system-status", help="Send system status update")
    status_parser.add_argument("--system", required=True, help="System name")
    status_parser.add_argument("--status", required=True, help="System status")
    status_parser.add_argument("--details", required=True, help="Status details")
    status_parser.add_argument("--metrics", help="JSON health metrics")

    # V2 compliance command
    compliance_parser = subparsers.add_parser("v2-compliance", help="Send V2 compliance update")
    compliance_parser.add_argument("--status", required=True, help="Compliance status")
    compliance_parser.add_argument("--files-checked", type=int, required=True, help="Files checked")
    compliance_parser.add_argument("--violations", type=int, required=True, help="Violations found")
    compliance_parser.add_argument("--details", required=True, help="Compliance details")

    # Documentation cleanup command
    cleanup_parser = subparsers.add_parser("doc-cleanup", help="Send documentation cleanup update")
    cleanup_parser.add_argument("--files-removed", type=int, required=True, help="Files removed")
    cleanup_parser.add_argument("--files-kept", type=int, required=True, help="Files kept")
    cleanup_parser.add_argument("--summary", required=True, help="Cleanup summary")

    # Feature announcement command
    feature_parser = subparsers.add_parser("feature", help="Send feature announcement")
    feature_parser.add_argument("--name", required=True, help="Feature name")
    feature_parser.add_argument("--description", required=True, help="Feature description")
    feature_parser.add_argument("--agents", help="Comma-separated list of agents")
    feature_parser.add_argument("--usage", help="Usage instructions")

    # History command
    history_parser = subparsers.add_parser("history", help="View update history")
    history_parser.add_argument("--limit", type=int, default=10, help="Number of updates to show")
    history_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Statistics command
    subparsers.add_parser("stats", help="View update statistics")

    return parser


def parse_agents(agents_str: str | None) -> list[str] | None:
    """Parse comma-separated agent list."""
    if not agents_str:
        return None
    return [agent.strip() for agent in agents_str.split(",")]


def parse_metadata(metadata_str: str | None) -> dict | None:
    """Parse JSON metadata."""
    if not metadata_str:
        return None
    try:
        return json.loads(metadata_str)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON metadata: {e}")
        return None


def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    if not args.cmd:
        parser.print_help()
        return 1

    try:
        # Initialize services
        messaging_service = MessagingService(dry_run=args.dry_run)
        update_system = ProjectUpdateSystem(messaging_service)

        if args.cmd == "update":
            agents = parse_agents(args.agents)
            metadata = parse_metadata(args.metadata)

            results = update_system.send_project_update(
                update_type=args.type,
                title=args.title,
                description=args.description,
                affected_agents=agents,
                priority=args.priority,
                metadata=metadata,
            )

            print(f"Project update sent to {len(results)} agents")
            for agent, success in results.items():
                status = "✅" if success else "❌"
                print(f"  {status} {agent}")

        elif args.cmd == "milestone":
            next_steps = None
            if args.next_steps:
                next_steps = [step.strip() for step in args.next_steps.split(",")]

            results = update_system.send_milestone_notification(
                milestone=args.name,
                description=args.description,
                completion_percentage=args.completion,
                next_steps=next_steps,
            )

            print(f"Milestone notification sent to {len(results)} agents")
            for agent, success in results.items():
                status = "✅" if success else "❌"
                print(f"  {status} {agent}")

        elif args.cmd == "system-status":
            metrics = parse_metadata(args.metrics)

            results = update_system.send_system_status_update(
                system_name=args.system,
                status=args.status,
                details=args.details,
                health_metrics=metrics,
            )

            print(f"System status update sent to {len(results)} agents")
            for agent, success in results.items():
                status = "✅" if success else "❌"
                print(f"  {status} {agent}")

        elif args.cmd == "v2-compliance":
            results = update_system.send_v2_compliance_update(
                compliance_status=args.status,
                files_checked=args.files_checked,
                violations_found=args.violations,
                details=args.details,
            )

            print(f"V2 compliance update sent to {len(results)} agents")
            for agent, success in results.items():
                status = "✅" if success else "❌"
                print(f"  {status} {agent}")

        elif args.cmd == "doc-cleanup":
            results = update_system.send_documentation_cleanup_update(
                files_removed=args.files_removed,
                files_kept=args.files_kept,
                cleanup_summary=args.summary,
            )

            print(f"Documentation cleanup update sent to {len(results)} agents")
            for agent, success in results.items():
                status = "✅" if success else "❌"
                print(f"  {status} {agent}")

        elif args.cmd == "feature":
            agents = parse_agents(args.agents)

            results = update_system.send_feature_announcement(
                feature_name=args.name,
                description=args.description,
                affected_agents=agents,
                usage_instructions=args.usage,
            )

            print(f"Feature announcement sent to {len(results)} agents")
            for agent, success in results.items():
                status = "✅" if success else "❌"
                print(f"  {status} {agent}")

        elif args.cmd == "history":
            history = update_system.get_update_history(limit=args.limit)

            if args.json:
                print(json.dumps(history, indent=2))
            else:
                if not history:
                    print("No update history found.")
                else:
                    print(f"Recent Updates (last {len(history)}):")
                    print("=" * 50)
                    for record in history:
                        timestamp = record.get("timestamp", "Unknown")
                        update_type = record.get("update_type", "Unknown")
                        title = record.get("title", "Unknown")
                        success_count = record.get("success_count", 0)
                        total_count = record.get("total_count", 0)

                        print(f"📅 {timestamp}")
                        print(f"📝 {title} ({update_type})")
                        print(f"📊 {success_count}/{total_count} agents notified")
                        print("-" * 30)

        elif args.cmd == "stats":
            stats = update_system.get_update_statistics()

            if "error" in stats:
                print(f"Error: {stats['error']}")
                return 1

            print("Project Update Statistics:")
            print("=" * 30)
            print(f"Total Updates: {stats.get('total_updates', 0)}")
            print(f"Total Deliveries: {stats.get('total_deliveries', 0)}")
            print(f"Successful Deliveries: {stats.get('successful_deliveries', 0)}")
            print(f"Success Rate: {stats.get('success_rate', 0)}%")

            update_types = stats.get("update_types", {})
            if update_types:
                print("\nUpdate Types:")
                for update_type, count in update_types.items():
                    print(f"  • {update_type}: {count}")

        return 0

    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Captain Hard Onboarding CLI
===========================

Command-line interface for Captain to execute hard onboarding operations
with full task database integration and reporting.

V2 Compliance: ≤400 lines, focused CLI tool
Author: Agent-4 (Captain) - Strategic Oversight & Emergency Intervention
"""

import argparse
import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from integrations.hard_onboarding_bridge import (
    captain_hard_onboard,
    ensure_db,
    get_onboarding_status,
)
from tools.cursor_task_database_integration import CursorTaskIntegrationManager


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Captain Hard Onboarding CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run test (no actual clicks)
  python tools/captain_onboard_cli.py --agent Agent-6 --dry-run

  # Real onboarding execution
  python tools/captain_onboard_cli.py --agent Agent-6

  # Onboarding with full report
  python tools/captain_onboard_cli.py --agent Agent-6 --report

  # Check current status
  python tools/captain_onboard_cli.py --agent Agent-6 --status
        """,
    )

    parser.add_argument("--agent", required=True, help="Agent ID to onboard (e.g., Agent-6)")

    parser.add_argument(
        "--dry-run", action="store_true", help="Simulate onboarding without actual PyAutoGUI clicks"
    )

    parser.add_argument(
        "--report",
        action="store_true",
        help="Print execution orders and integration report after onboarding",
    )

    parser.add_argument(
        "--status", action="store_true", help="Check current onboarding status for agent"
    )

    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    try:
        # Ensure database is initialized
        if args.verbose:
            print("🔧 Initializing database...")
        ensure_db()

        if args.status:
            # Status check mode
            if args.verbose:
                print(f"📊 Checking status for {args.agent}...")

            status = get_onboarding_status(args.agent)
            print(json.dumps(status, indent=2))

            return 0 if not status.get("error") else 1

        # Execute hard onboarding
        if args.verbose:
            mode = "DRY RUN" if args.dry_run else "LIVE"
            print(f"🎯 Executing {mode} hard onboarding for {args.agent}...")

        summary = captain_hard_onboard(args.agent, dry_run=args.dry_run)

        # Print main result
        print(json.dumps(summary, indent=2))

        # Print additional report if requested
        if args.report:
            if args.verbose:
                print("\n📋 Generating Captain execution orders...")

            manager = CursorTaskIntegrationManager()
            execution_orders = manager.generate_captain_execution_orders()
            integration_report = manager.export_integration_report()

            print("\n" + "=" * 60)
            print("CAPTAIN EXECUTION ORDERS")
            print("=" * 60)
            print(json.dumps(execution_orders, indent=2))

            print("\n" + "=" * 60)
            print("INTEGRATION SYSTEM REPORT")
            print("=" * 60)
            print(json.dumps(integration_report, indent=2))

        # Return success/failure code
        return 0 if summary["success"] else 1

    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        return 130

    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())


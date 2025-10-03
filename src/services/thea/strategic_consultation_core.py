#!/usr/bin/env python3
"""
Strategic Consultation Core - Main CLI Interface
================================================

Core command-line interface for strategic consultation with Commander Thea.
Provides structured context delivery and consultation management.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
Refactored By: Agent-6 (Quality Assurance Specialist)
Original: strategic_consultation_cli.py (473 lines) - Core module
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.thea.strategic_consultation_templates import STRATEGIC_TEMPLATES, ProjectContextManager
from src.services.thea.thea_autonomous_system import send_thea_message_autonomous


def consult_command(args):
    """Handle consultation command."""
    context_manager = ProjectContextManager()

    if args.template:
        # Use pre-defined template
        if args.template not in STRATEGIC_TEMPLATES:
            print(f"❌ Invalid template: {args.template}")
            print(f"Available templates: {', '.join(STRATEGIC_TEMPLATES.keys())}")
            return 1

        question = STRATEGIC_TEMPLATES[args.template]
        print(f"📋 Using template: {args.template}")
        print(f"📝 Question: {question}")
    else:
        # Use custom question
        question = args.question
        print(f"📝 Custom question: {question}")

    # Create consultation message
    context_level = args.context_level or "standard"
    message = context_manager.create_strategic_consultation(question, context_level)

    if not message:
        print("❌ Failed to create consultation message")
        return 1

    print("📤 Sending consultation to Commander Thea...")
    print(f"📊 Context level: {context_level}")
    print(f"📏 Message length: {len(message)} characters")

    # Send to Thea
    try:
        response = send_thea_message_autonomous(message)
        if response:
            print("✅ Consultation sent successfully")
            print(f"📥 Response received: {len(response)} characters")
            return 0
        else:
            print("⚠️ No response received from Commander Thea")
            return 1
    except Exception as e:
        print(f"❌ Error sending consultation: {e}")
        return 1


def status_report_command(args):
    """Handle status report command."""
    context_manager = ProjectContextManager()

    print("📊 Generating status report for Commander Thea...")

    # Create status report
    status_report = context_manager.create_status_report()

    if not status_report:
        print("❌ Failed to create status report")
        return 1

    print("📤 Sending status report to Commander Thea...")
    print(f"📏 Report length: {len(status_report)} characters")

    # Send to Thea
    try:
        response = send_thea_message_autonomous(status_report)
        if response:
            print("✅ Status report sent successfully")
            print(f"📥 Response received: {len(response)} characters")
            return 0
        else:
            print("⚠️ No response received from Commander Thea")
            return 1
    except Exception as e:
        print(f"❌ Error sending status report: {e}")
        return 1


def emergency_command(args):
    """Handle emergency consultation command."""
    context_manager = ProjectContextManager()

    print(f"🚨 Emergency consultation: {args.issue}")

    # Create emergency consultation
    emergency_message = context_manager.create_emergency_consultation(args.issue)

    if not emergency_message:
        print("❌ Failed to create emergency consultation")
        return 1

    print("📤 Sending emergency consultation to Commander Thea...")
    print(f"📏 Message length: {len(emergency_message)} characters")

    # Send to Thea
    try:
        response = send_thea_message_autonomous(emergency_message)
        if response:
            print("✅ Emergency consultation sent successfully")
            print(f"📥 Response received: {len(response)} characters")
            return 0
        else:
            print("⚠️ No response received from Commander Thea")
            return 1
    except Exception as e:
        print(f"❌ Error sending emergency consultation: {e}")
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Strategic Consultation CLI - Commander Thea Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/services/thea/strategic_consultation_cli.py consult --question "What should be our next priority?"
  python src/services/thea/strategic_consultation_cli.py consult --template priority_guidance
  python src/services/thea/strategic_consultation_cli.py status-report
  python src/services/thea/strategic_consultation_cli.py emergency --issue "System degradation detected"
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Consult command
    consult_parser = subparsers.add_parser(
        "consult", help="Strategic consultation with Commander Thea"
    )
    consult_parser.add_argument("--question", help="Custom consultation question")
    consult_parser.add_argument("--template", help="Pre-defined consultation template")
    consult_parser.add_argument(
        "--context-level",
        choices=["minimal", "standard", "comprehensive"],
        help="Context detail level",
    )

    # Status report command
    status_parser = subparsers.add_parser(
        "status-report", help="Send status report to Commander Thea"
    )

    # Emergency command
    emergency_parser = subparsers.add_parser(
        "emergency", help="Emergency consultation with Commander Thea"
    )
    emergency_parser.add_argument("--issue", required=True, help="Emergency issue description")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == "consult":
            return consult_command(args)
        elif args.command == "status-report":
            return status_report_command(args)
        elif args.command == "emergency":
            return emergency_command(args)
        else:
            print(f"❌ Unknown command: {args.command}")
            return 1
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

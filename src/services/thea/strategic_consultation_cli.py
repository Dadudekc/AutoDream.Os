#!/usr/bin/env python3
"""
Strategic Consultation CLI - Unified Interface
==============================================

Unified command-line interface for strategic consultation with Commander Thea.
Integrates core functionality with templates and utilities.

V2 Compliance: ≤400 lines - REFACTORED FROM 473 LINES
Refactored By: Agent-6 (Quality Assurance Specialist)
Split into: core.py, templates.py, utils.py
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.thea.strategic_consultation_core import (
    consult_command,
    emergency_command,
    status_report_command,
)
from src.services.thea.strategic_consultation_templates import STRATEGIC_TEMPLATES, ProjectContextManager


def create_argument_parser():
    """Create argument parser with all commands."""
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

    # Help command
    help_parser = subparsers.add_parser("help", help="Show available templates and usage")
    help_parser.set_defaults(
        func=lambda args: print_template_help()
    )

    return parser


def print_template_help():
    """Print available templates and usage."""
    print("📋 Available Strategic Consultation Templates:")
    print("=" * 50)
    
    for template_name, template in STRATEGIC_TEMPLATES.items():
        print(f"• {template_name}: {template.question}")
    
    print("\n💡 Usage Examples:")
    print("  python strategic_consultation_cli.py consult --template priority_guidance")
    print("  python strategic_consultation_cli.py consult --template quality_improvement")
    print("  python strategic_consultation_cli.py consult --template crisis_management")


def handle_command(args):
    """Handle command execution."""
    try:
        if args.command == "consult":
            return consult_command(args)
        elif args.command == "status-report":
            return status_report_command(args)
        elif args.command == "emergency":
            return emergency_command(args)
        elif args.command == "help":
            args.func(args)
            return 0
        else:
            print(f"❌ Unknown command: {args.command}")
            return 1
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


def main():
    """Main CLI entry point."""
    parser = create_argument_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    return handle_command(args)


if __name__ == "__main__":
    sys.exit(main())

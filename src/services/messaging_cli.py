#!/usr/bin/env python3
"""
Consolidated Messaging CLI - Command Line Interface
==================================================

Command line interface for consolidated messaging service.
Handles argument parsing, CLI operations, and main execution.

V2 Compliance: ≤400 lines, focused CLI interface module
Author: Agent-6 (Quality Assurance Specialist)
"""

import argparse
import json
import logging
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.append(str(project_root))

logger = logging.getLogger(__name__)


class ConsolidatedMessagingCLI:
    """
    Command line interface for consolidated messaging service.

    Handles argument parsing, CLI operations, and main execution.
    """

    def __init__(self):
        """Initialize CLI interface."""
        self.logger = logging.getLogger(f"{__name__}.ConsolidatedMessagingCLI")

    def build_parser(self) -> argparse.ArgumentParser:
        """Build argument parser for CLI commands."""
        parser = argparse.ArgumentParser(
            description="Consolidated Messaging Service CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python consolidated_messaging_service_main.py send --agent Agent-4 --message "Hello"
  python consolidated_messaging_service_main.py broadcast --message "System update"
  python consolidated_messaging_service_main.py status
  python consolidated_messaging_service_main.py protocol-check
  python consolidated_messaging_service_main.py cue --agents Agent-4 Agent-5 --message "Task"
  python consolidated_messaging_service_main.py hard-onboard --agent Agent-6
  python consolidated_messaging_service_main.py stall --agent Agent-7
  python consolidated_messaging_service_main.py unstall --agent Agent-7
            """,
        )

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Send message command
        send_parser = subparsers.add_parser("send", help="Send message to specific agent")
        send_parser.add_argument("--agent", required=True, help="Target agent ID")
        send_parser.add_argument("--message", required=True, help="Message content")
        send_parser.add_argument("--from-agent", default="Agent-4", help="Sender agent ID")
        send_parser.add_argument(
            "--priority",
            default="NORMAL",
            choices=["NORMAL", "HIGH", "URGENT"],
            help="Message priority",
        )

        # Broadcast message command
        broadcast_parser = subparsers.add_parser(
            "broadcast", help="Broadcast message to all agents"
        )
        broadcast_parser.add_argument("--message", required=True, help="Message content")
        broadcast_parser.add_argument("--from-agent", default="Agent-4", help="Sender agent ID")
        broadcast_parser.add_argument(
            "--priority",
            default="NORMAL",
            choices=["NORMAL", "HIGH", "URGENT"],
            help="Message priority",
        )

        # Status command
        status_parser = subparsers.add_parser("status", help="Show messaging service status")

        # Protocol check command
        protocol_parser = subparsers.add_parser("protocol-check", help="Check protocol compliance")

        # Cued messaging command
        cue_parser = subparsers.add_parser("cue", help="Send cued message to multiple agents")
        cue_parser.add_argument("--agents", required=True, nargs="+", help="Target agent IDs")
        cue_parser.add_argument("--message", required=True, help="Message content")
        cue_parser.add_argument("--cue", required=True, help="Cue identifier")
        cue_parser.add_argument("--from-agent", default="Agent-4", help="Sender agent ID")

        # Hard onboard command
        onboard_parser = subparsers.add_parser("hard-onboard", help="Hard onboard specific agent")
        onboard_parser.add_argument("--agent", help="Agent ID to onboard (default: all agents)")

        # Stall command
        stall_parser = subparsers.add_parser("stall", help="Stall specific agent")
        stall_parser.add_argument("--agent", required=True, help="Agent ID to stall")

        # Unstall command
        unstall_parser = subparsers.add_parser("unstall", help="Unstall specific agent")
        unstall_parser.add_argument("--agent", required=True, help="Agent ID to unstall")

        return parser

    def main(self) -> int:
        """Main CLI execution function."""
        try:
            parser = self.build_parser()
            args = parser.parse_args()

            if not args.command:
                parser.print_help()
                return 1

            # Initialize messaging service
            from src.services.messaging_service_main import ConsolidatedMessagingService

            service = ConsolidatedMessagingService()

            # Execute command
            if args.command == "send":
                success = service.send_message(
                    args.agent, args.message, args.from_agent, args.priority
                )
                print("✅ Message sent successfully" if success else "❌ Failed to send message")
                return 0 if success else 1

            elif args.command == "broadcast":
                success = service.broadcast_message(args.message, args.from_agent, args.priority)
                print(
                    "✅ Broadcast sent successfully" if success else "❌ Failed to broadcast message"
                )
                return 0 if success else 1

            elif args.command == "status":
                status = service.get_status()
                print(json.dumps(status, indent=2))
                return 0

            elif args.command == "protocol-check":
                violations = service.check_protocol_compliance()
                if violations:
                    print(f"❌ Found {len(violations)} protocol violations:")
                    for violation in violations:
                        print(f"  - {violation}")
                    return 1
                else:
                    print("✅ All protocols compliant")
                    return 0

            elif args.command == "cue":
                success = service.send_cued_message(
                    args.agents, args.message, args.cue, args.from_agent
                )
                print(
                    "✅ Cued message sent successfully"
                    if success
                    else "❌ Failed to send cued message"
                )
                return 0 if success else 1

            elif args.command == "hard-onboard":
                if args.agent:
                    success = service.hard_onboard_agent(args.agent)
                    print(
                        f"✅ Agent {args.agent} onboarded successfully"
                        if success
                        else f"❌ Failed to onboard agent {args.agent}"
                    )
                else:
                    success = service.hard_onboard_all_agents()
                    print(
                        "✅ All agents onboarded successfully"
                        if success
                        else "❌ Failed to onboard all agents"
                    )
                return 0 if success else 1

            elif args.command == "stall":
                success = service.stall_agent(args.agent)
                print(
                    f"✅ Agent {args.agent} stalled successfully"
                    if success
                    else f"❌ Failed to stall agent {args.agent}"
                )
                return 0 if success else 1

            elif args.command == "unstall":
                success = service.unstall_agent(args.agent)
                print(
                    f"✅ Agent {args.agent} unstalled successfully"
                    if success
                    else f"❌ Failed to unstall agent {args.agent}"
                )
                return 0 if success else 1

            else:
                print(f"❌ Unknown command: {args.command}")
                return 1

        except KeyboardInterrupt:
            print("\n⚠️ Operation cancelled by user")
            return 1
        except Exception as e:
            self.logger.error(f"CLI execution error: {e}")
            print(f"❌ Error: {e}")
            return 1


if __name__ == "__main__":
    cli = ConsolidatedMessagingCLI()
    sys.exit(cli.main())


__all__ = ["ConsolidatedMessagingCLI"]

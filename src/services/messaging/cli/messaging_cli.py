#!/usr/bin/env python3
"""
Messaging CLI Interface - V2 Compliant Module
===========================================

Command-line interface for unified messaging system.
V2 COMPLIANT: Focused CLI interface under 300 lines.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import argparse
import logging
from typing import List, Optional

try:
    from ..models.messaging_models import UnifiedMessage
    from ..models.messaging_enums import UnifiedMessagePriority, UnifiedMessageType
except ImportError:
    # Fallback for direct execution
    from models.messaging_models import UnifiedMessage
    from models.messaging_enums import UnifiedMessagePriority, UnifiedMessageType

logger = logging.getLogger(__name__)


class MessagingCLI:
    """Command-line interface for messaging system."""

    def __init__(self, messaging_service):
        self.messaging_service = messaging_service

    def create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser for CLI interface."""
        parser = argparse.ArgumentParser(
            description="Unified Messaging CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python -m messaging.cli send --message "Hello" --recipient Agent-1
  python -m messaging.cli broadcast --message "System update" --priority high
  python -m messaging.cli history --agent Agent-1
            """
        )

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Send message command
        send_parser = subparsers.add_parser("send", help="Send message to agent")
        send_parser.add_argument("--message", "-m", required=True, help="Message content")
        send_parser.add_argument("--recipient", "-r", required=True, help="Recipient agent")
        send_parser.add_argument("--priority", "-p", choices=["low", "normal", "high", "urgent"],
                                default="normal", help="Message priority")
        send_parser.add_argument("--type", "-t", choices=["direct", "broadcast", "system"],
                                default="direct", help="Message type")
        send_parser.add_argument("--sender", "-s", default="CLI", help="Sender identifier")

        # Broadcast command
        broadcast_parser = subparsers.add_parser("broadcast", help="Broadcast message to all agents")
        broadcast_parser.add_argument("--message", "-m", required=True, help="Message content")
        broadcast_parser.add_argument("--priority", "-p", choices=["low", "normal", "high", "urgent"],
                                     default="normal", help="Message priority")
        broadcast_parser.add_argument("--sender", "-s", default="CLI", help="Sender identifier")

        # History command
        history_parser = subparsers.add_parser("history", help="Show message history")
        history_parser.add_argument("--agent", "-a", help="Agent to show history for")
        history_parser.add_argument("--limit", "-l", type=int, default=10, help="Number of messages to show")

        # Status command
        status_parser = subparsers.add_parser("status", help="Show system status")

        # List agents command
        list_parser = subparsers.add_parser("list", help="List available agents")

        # Start onboarding command
        start_parser = subparsers.add_parser("start", help="Start agent onboarding sequence")
        start_parser.add_argument("--dry-run", action="store_true",
                                help="Run in dry-run mode (no actual clicking/pasting)")
        start_parser.add_argument("--agent", "-a", help="Specific agent to onboard (default: all agents)")

        return parser

    def run_cli_interface(self, args: Optional[List[str]] = None) -> int:
        """Run the CLI interface."""
        parser = self.create_parser()

        if args is None:
            parsed_args = parser.parse_args()
        else:
            parsed_args = parser.parse_args(args)

        try:
            if parsed_args.command == "send":
                return self._handle_send_message(parsed_args)
            elif parsed_args.command == "broadcast":
                return self._handle_broadcast_message(parsed_args)
            elif parsed_args.command == "history":
                return self._handle_show_history(parsed_args)
            elif parsed_args.command == "status":
                return self._handle_show_status()
            elif parsed_args.command == "list":
                return self._handle_list_agents()
            elif parsed_args.command == "start":
                return self._handle_start_onboarding(parsed_args)
            else:
                parser.print_help()
                return 0

        except Exception as e:
            logger.error(f"CLI error: {e}")
            print(f"Error: {e}")
            return 1

    def _handle_send_message(self, args) -> int:
        """Handle sending a message."""
        try:
            # Create message
            message = UnifiedMessage(
                content=args.message,
                recipient=args.recipient,
                sender=args.sender,
                message_type=UnifiedMessageType(args.type.upper()),
                priority=UnifiedMessagePriority(args.priority.upper())
            )

            # Send message
            success = self.messaging_service.send_message(message)

            if success:
                print(f"✅ Message sent successfully to {args.recipient}")
                return 0
            else:
                print(f"❌ Failed to send message to {args.recipient}")
                return 1

        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return 1

    def _handle_broadcast_message(self, args) -> int:
        """Handle broadcasting a message."""
        try:
            # Send broadcast message
            results = self.messaging_service.broadcast_message(
                content=args.message,
                sender=args.sender
            )

            successful = sum(1 for success in results.values() if success)
            total = len(results)

            if successful > 0:
                print(f"✅ Broadcast sent to {successful}/{total} agents")
                return 0
            else:
                print(f"❌ Failed to send broadcast to any agents")
                return 1

        except Exception as e:
            print(f"❌ Error broadcasting message: {e}")
            return 1

    def _handle_show_history(self, args) -> int:
        """Handle showing message history."""
        try:
            messages = self.messaging_service.show_message_history(args.agent)
            if messages:
                print(f"Message history for {args.agent}:")
                for msg in messages[-args.limit:]:
                    print(f"  [{msg.timestamp}] {msg.sender}: {msg.content}")
            else:
                print(f"No message history found for {args.agent}")
            return 0
        except Exception as e:
            print(f"❌ Error showing history: {e}")
            return 1

    def _handle_show_status(self) -> int:
        """Handle showing system status."""
        try:
            status = self.messaging_service.get_system_status()
            print("Messaging System Status:")
            for key, value in status.items():
                print(f"  {key}: {value}")
            return 0
        except Exception as e:
            print(f"❌ Error showing status: {e}")
            return 1

    def _handle_list_agents(self) -> int:
        """Handle listing available agents."""
        try:
            agents = self.messaging_service.list_available_agents()
            print("Available agents:")
            for agent in agents:
                print(f"  • {agent}")
            return 0
        except Exception as e:
            print(f"❌ Error listing agents: {e}")
            return 1

    def _handle_start_onboarding(self, args) -> int:
        """Handle starting agent onboarding sequence."""
        try:
            return self.messaging_service.start_agent_onboarding(
                dry_run=args.dry_run,
                specific_agent=args.agent
            )
        except Exception as e:
            print(f"❌ Error starting onboarding: {e}")
            return 1


if __name__ == "__main__":
    # When run as a script, create a basic CLI instance
    print("Messaging CLI - Run from consolidated_messaging_service.py")
    print("Example: python -m src.services.messaging.consolidated_messaging_service")

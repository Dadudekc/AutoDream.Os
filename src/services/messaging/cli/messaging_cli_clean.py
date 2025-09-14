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

from ..models.messaging_models import UnifiedMessage
from ..models.messaging_enums import UnifiedMessagePriority, UnifiedMessageType

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

        # Broadcast command
        broadcast_parser = subparsers.add_parser("broadcast", help="Broadcast message to all agents")
        broadcast_parser.add_argument("--message", "-m", required=True, help="Message content")
        broadcast_parser.add_argument("--priority", "-p", choices=["low", "normal", "high", "urgent"],
                                     default="normal", help="Message priority")

        # History command
        history_parser = subparsers.add_parser("history", help="Show message history")
        history_parser.add_argument("--agent", "-a", help="Agent to show history for")
        history_parser.add_argument("--limit", "-l", type=int, default=10, help="Number of messages to show")

        return parser

    def send_message(self, message: str, recipient: str, priority: str = "normal", msg_type: str = "direct") -> bool:
        """Send a message to an agent."""
        try:
            priority_map = {
                "low": UnifiedMessagePriority.LOW,
                "normal": UnifiedMessagePriority.NORMAL,
                "high": UnifiedMessagePriority.HIGH,
                "urgent": UnifiedMessagePriority.URGENT
            }

            type_map = {
                "direct": UnifiedMessageType.DIRECT,
                "broadcast": UnifiedMessageType.BROADCAST,
                "system": UnifiedMessageType.SYSTEM
            }

            unified_message = UnifiedMessage(
                content=message,
                recipient=recipient,
                sender="CLI",
                message_type=type_map.get(msg_type, UnifiedMessageType.DIRECT),
                priority=priority_map.get(priority, UnifiedMessagePriority.NORMAL)
            )

            return self.messaging_service.send_message(unified_message)

        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

    def broadcast_message(self, message: str, priority: str = "normal") -> dict[str, bool]:
        """Broadcast message to all agents."""
        try:
            return self.messaging_service.broadcast_message(message, sender="CLI")
        except Exception as e:
            logger.error(f"Error broadcasting message: {e}")
            return {}

    def show_history(self, agent: Optional[str] = None, limit: int = 10) -> None:
        """Show message history."""
        try:
            history = self.messaging_service.show_message_history(agent)
            if history:
                print(f"\nMessage History (last {limit} messages):")
                print("=" * 50)
                for i, msg in enumerate(history[-limit:], 1):
                    print(f"{i}. [{msg.timestamp}] {msg.sender} -> {msg.recipient}")
                    print(f"   {msg.content}")
                    print(f"   Priority: {msg.priority}, Type: {msg.message_type}")
                    print()
            else:
                print("No message history found.")
        except Exception as e:
            logger.error(f"Error showing history: {e}")

    def run_cli(self):
        """Run the CLI interface."""
        parser = self.create_parser()
        args = parser.parse_args()

        if not args.command:
            parser.print_help()
            return

        if args.command == "send":
            success = self.send_message(args.message, args.recipient, args.priority, args.type)
            if success:
                print(f"✅ Message sent to {args.recipient}")
            else:
                print(f"❌ Failed to send message to {args.recipient}")

        elif args.command == "broadcast":
            results = self.broadcast_message(args.message, args.priority)
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            print(f"📢 Broadcast sent to {total} agents ({successful} successful)")

        elif args.command == "history":
            self.show_history(args.agent, args.limit)


if __name__ == "__main__":
    # When run as a script, create a basic CLI instance
    # This would typically be called from the consolidated messaging service
    print("Messaging CLI - Run from consolidated_messaging_service.py")
    print("Example: python -m src.services.messaging.consolidated_messaging_service")

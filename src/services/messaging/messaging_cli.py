#!/usr/bin/env python3
"""
Messaging CLI Interface - V2 Compliant Module
============================================

CLI interface for the messaging service.
V2 Compliance: < 400 lines, single responsibility.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Mission: V2 Compliance - Messaging Service Modularization
License: MIT
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

# Add project root to path for imports
if __name__ == "__main__":
    script_dir = Path(__file__).parent.parent.parent.parent
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))

from src.services.messaging.messaging_core import ConsolidatedMessagingService


class MessagingCLI:
    """CLI interface for messaging service operations."""

    def __init__(self):
        """Initialize CLI interface."""
        self.messaging_service = ConsolidatedMessagingService()

    def create_parser(self) -> argparse.ArgumentParser:
        """Create command line argument parser."""
        parser = argparse.ArgumentParser(
            description="Consolidated Messaging Service CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python messaging_cli.py --agent Agent-1 --message "Hello from CLI"
  python messaging_cli.py --broadcast --message "Broadcast message"
  python messaging_cli.py --status
  python messaging_cli.py --help
            """
        )

        # Main command group
        command_group = parser.add_mutually_exclusive_group(required=True)
        
        # Send message to specific agent
        command_group.add_argument(
            "--agent",
            type=str,
            help="Send message to specific agent (e.g., Agent-1)"
        )
        
        # Broadcast message to all agents
        command_group.add_argument(
            "--broadcast",
            action="store_true",
            help="Broadcast message to all agents"
        )
        
        # Show status
        command_group.add_argument(
            "--status",
            action="store_true",
            help="Show messaging service status"
        )

        # Message content
        parser.add_argument(
            "--message",
            type=str,
            help="Message content to send"
        )

        # Message priority
        parser.add_argument(
            "--priority",
            type=str,
            choices=["LOW", "NORMAL", "HIGH", "URGENT"],
            default="NORMAL",
            help="Message priority (default: NORMAL)"
        )

        # Message tags
        parser.add_argument(
            "--tags",
            type=str,
            nargs="+",
            help="Message tags (e.g., GENERAL COORDINATION)"
        )

        # Sender identification
        parser.add_argument(
            "--sender",
            type=str,
            default="CLI",
            help="Sender identification (default: CLI)"
        )

        # Verbose output
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose output"
        )

        return parser

    def send_agent_message(self, agent: str, message: str, priority: str, tags: List[str], sender: str) -> bool:
        """Send message to specific agent."""
        try:
            result = self.messaging_service.send_message_to_agent(
                agent_id=agent,
                message=message,
                sender=sender,
                priority=priority,
                tags=tags
            )
            
            if result:
                print(f"✅ Message sent to {agent}")
                return True
            else:
                print(f"❌ Failed to send message to {agent}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending message to {agent}: {e}")
            return False

    def send_broadcast_message(self, message: str, priority: str, tags: List[str], sender: str) -> bool:
        """Broadcast message to all agents."""
        try:
            result = self.messaging_service.broadcast_message(
                message=message,
                sender=sender,
                priority=priority,
                tags=tags
            )
            
            if result:
                print("✅ Broadcast message sent to all agents")
                return True
            else:
                print("❌ Failed to send broadcast message")
                return False
                
        except Exception as e:
            print(f"❌ Error sending broadcast message: {e}")
            return False

    def show_status(self) -> None:
        """Show messaging service status."""
        try:
            status = self.messaging_service.get_service_status()
            
            print("📊 Messaging Service Status:")
            print(f"  Service: {'✅ Active' if status.get('active', False) else '❌ Inactive'}")
            print(f"  PyAutoGUI: {'✅ Available' if status.get('pyautogui_available', False) else '❌ Not Available'}")
            print(f"  Pyperclip: {'✅ Available' if status.get('pyperclip_available', False) else '❌ Not Available'}")
            print(f"  Coordinates: {'✅ Loaded' if status.get('coordinates_loaded', False) else '❌ Not Loaded'}")
            print(f"  Active Agents: {status.get('active_agents', 0)}")
            
        except Exception as e:
            print(f"❌ Error getting status: {e}")

    def run(self, args: Optional[List[str]] = None) -> int:
        """Run CLI interface."""
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)
        
        try:
            if parsed_args.status:
                self.show_status()
                return 0
                
            elif parsed_args.agent:
                if not parsed_args.message:
                    print("❌ Error: --message is required when using --agent")
                    return 1
                    
                return 0 if self.send_agent_message(
                    agent=parsed_args.agent,
                    message=parsed_args.message,
                    priority=parsed_args.priority,
                    tags=parsed_args.tags or [],
                    sender=parsed_args.sender
                ) else 1
                
            elif parsed_args.broadcast:
                if not parsed_args.message:
                    print("❌ Error: --message is required when using --broadcast")
                    return 1
                    
                return 0 if self.send_broadcast_message(
                    message=parsed_args.message,
                    priority=parsed_args.priority,
                    tags=parsed_args.tags or [],
                    sender=parsed_args.sender
                ) else 1
                
            else:
                parser.print_help()
                return 1
                
        except KeyboardInterrupt:
            print("\n⚠️ Operation cancelled by user")
            return 1
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return 1


def main():
    """Main entry point for CLI."""
    cli = MessagingCLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()

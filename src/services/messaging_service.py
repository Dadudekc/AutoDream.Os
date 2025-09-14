#!/usr/bin/env python3
"""
Messaging Service - V2 Compliant Orchestrator
============================================

Main messaging service orchestrator.
V2 Compliance: < 400 lines, single responsibility.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Mission: V2 Compliance - Messaging Service Modularization
License: MIT
"""

import sys
from pathlib import Path

# Add project root to path for imports
if __name__ == "__main__":
    script_dir = Path(__file__).parent.parent
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))

from src.services.messaging.messaging_core import ConsolidatedMessagingService
from src.services.messaging.messaging_cli import MessagingCLI


class MessagingService:
    """Main messaging service orchestrator."""

    def __init__(self):
        """Initialize messaging service."""
        self.core_service = ConsolidatedMessagingService()
        self.cli = MessagingCLI()

    def send_message(
        self,
        agent_id: str,
        message: str,
        sender: str = "System",
        priority: str = "NORMAL",
        tags: list = None
    ) -> bool:
        """Send message to specific agent."""
        return self.core_service.send_message_to_agent(
            agent_id=agent_id,
            message=message,
            sender=sender,
            priority=priority,
            tags=tags
        )

    def broadcast_message(
        self,
        message: str,
        sender: str = "System",
        priority: str = "NORMAL",
        tags: list = None
    ) -> bool:
        """Broadcast message to all agents."""
        return self.core_service.broadcast_message(
            message=message,
            sender=sender,
            priority=priority,
            tags=tags
        )

    def get_status(self) -> dict:
        """Get messaging service status."""
        return self.core_service.get_service_status()

    def run_cli(self, args: list = None) -> int:
        """Run CLI interface."""
        return self.cli.run(args)

    def shutdown(self) -> None:
        """Shutdown messaging service."""
        self.core_service.shutdown()


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # CLI mode
        service = MessagingService()
        return service.run_cli()
    else:
        # Interactive mode
        print("🚀 Messaging Service - V2 Compliant")
        print("=" * 40)
        print("Available commands:")
        print("  --help                    Show help")
        print("  --status                  Show service status")
        print("  --agent <agent> --message <msg>  Send message to agent")
        print("  --broadcast --message <msg>      Broadcast message")
        print()
        print("Examples:")
        print("  python messaging_service.py --status")
        print("  python messaging_service.py --agent Agent-1 --message 'Hello'")
        print("  python messaging_service.py --broadcast --message 'Broadcast'")
        return 0


if __name__ == "__main__":
    sys.exit(main())

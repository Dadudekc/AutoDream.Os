#!/usr/bin/env python3
"""
Consolidated Messaging Service V2 - Modular Architecture
========================================================

Modular messaging service for V2 compliance.
Orchestrates core messaging, status monitoring, and onboarding services.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import after adding project root to path
try:
    from src.services.messaging.core.messaging_service import MessagingService
    from src.services.messaging.status.status_monitor import StatusMonitor
    from src.services.messaging.onboarding.onboarding_service import OnboardingService
    from src.services.messaging.enhanced_messaging_service import get_enhanced_messaging_service
except ImportError:
    # Fallback for direct execution
    from messaging.core.messaging_service import MessagingService
    from messaging.status.status_monitor import StatusMonitor
    from messaging.onboarding.onboarding_service import OnboardingService
    from messaging.enhanced_messaging_service import get_enhanced_messaging_service

logger = logging.getLogger(__name__)


class ConsolidatedMessagingService:
    """Consolidated messaging service - main interface."""
    
    def __init__(self, coord_path: str = "config/coordinates.json") -> None:
        """Initialize consolidated messaging service with vector database integration."""
        self.coord_path = coord_path
        self.messaging_service = get_enhanced_messaging_service()  # Use enhanced version with vector DB
        self.status_monitor = StatusMonitor(self.messaging_service)
        self.onboarding_service = OnboardingService(self.messaging_service)
    
    def send_message(self, agent_id: str, message: str, from_agent: str = "Agent-2", priority: str = "NORMAL") -> bool:
        """Send message to specific agent."""
        return self.messaging_service.send_message(agent_id, message, from_agent, priority)
    
    def broadcast_message(self, message: str, from_agent: str = "Agent-2", priority: str = "NORMAL") -> dict:
        """Send message to all active agents."""
        return self.messaging_service.broadcast_message(message, from_agent, priority)
    
    def get_status(self) -> dict:
        """Get comprehensive system status."""
        return self.status_monitor.get_comprehensive_status()
    
    def hard_onboard_agent(self, agent_id: str) -> bool:
        """Hard onboard specific agent."""
        return self.onboarding_service.hard_onboard_agent(agent_id)
    
    def hard_onboard_all_agents(self) -> dict:
        """Hard onboard all active agents."""
        return self.onboarding_service.hard_onboard_all_agents()


def build_parser() -> argparse.ArgumentParser:
    """Build command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Consolidated Messaging Service V2 - Modular Architecture"
    )
    
    parser.add_argument(
        "--coords",
        default="config/coordinates.json",
        help="Path to coordinates configuration file"
    )
    
    subparsers = parser.add_subparsers(dest="cmd", help="Available commands")
    
    # Send message command
    send_parser = subparsers.add_parser("send", help="Send message to specific agent")
    send_parser.add_argument("--agent", required=True, help="Target agent ID")
    send_parser.add_argument("--message", required=True, help="Message to send")
    send_parser.add_argument("--from-agent", default="Agent-2", help="Source agent ID")
    send_parser.add_argument("--priority", default="NORMAL", help="Message priority")
    
    # Broadcast message command
    broadcast_parser = subparsers.add_parser("broadcast", help="Send message to all agents")
    broadcast_parser.add_argument("--message", required=True, help="Message to broadcast")
    broadcast_parser.add_argument("--from-agent", default="Agent-2", help="Source agent ID")
    broadcast_parser.add_argument("--priority", default="NORMAL", help="Message priority")
    
    # Status command
    subparsers.add_parser("status", help="Get system status")
    
    # Hard onboard command
    onboard_parser = subparsers.add_parser("hard-onboard", help="Hard onboard agents")
    onboard_group = onboard_parser.add_mutually_exclusive_group(required=True)
    onboard_group.add_argument("--agent", help="Specific agent to onboard")
    onboard_group.add_argument("--all-agents", action="store_true", help="Onboard all agents")
    
    return parser


def main(argv: List[str] | None = None) -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)
    
    if not args.cmd:
        parser.print_help()
        return 1
    
    try:
        # Initialize services
        messaging_service = MessagingService(args.coords)
        status_monitor = StatusMonitor(messaging_service)
        onboarding_service = OnboardingService(messaging_service)
        
        # Handle commands
        if args.cmd == "send":
            success = messaging_service.send_message(args.agent, args.message, args.from_agent)
            return 0 if success else 1
            
        elif args.cmd == "broadcast":
            results = messaging_service.broadcast_message(args.message, args.from_agent)
            success_count = sum(1 for success in results.values() if success)
            return 0 if success_count == len(results) else 1
            
        elif args.cmd == "status":
            status = status_monitor.get_comprehensive_status()
            logging.info(f"Service Status: {status}")
            return 0
            
        elif args.cmd == "hard-onboard":
            if args.agent:
                success = onboarding_service.hard_onboard_agent(args.agent)
                return 0 if success else 1
            elif args.all_agents:
                results = onboarding_service.hard_onboard_all_agents()
                successful = sum(1 for success in results.values() if success)
                return 0 if successful == len(results) else 1
            else:
                logging.error("Error: Must specify either --agent or --all-agents")
                return 1
            
        else:
            parser.print_help()
            return 1
            
    except Exception as e:
        logging.error("Service error: %s", e)
        return 2


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())

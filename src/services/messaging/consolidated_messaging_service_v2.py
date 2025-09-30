#!/usr/bin/env python3
"""
Consolidated Messaging Service V2 - V2 Compliant
===============================================

V2 compliant version of consolidated messaging service using modular architecture.
Maintains all functionality while achieving V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import argparse
import logging
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.messaging.coordination_tracker import CoordinationTracker
from src.services.messaging.message_validator import MessageValidator
from src.services.messaging.messaging_core import MessagingCore
from src.services.messaging.pyautogui_handler import PyAutoGUIHandler

logger = logging.getLogger(__name__)


class ConsolidatedMessagingServiceV2:
    """V2 compliant consolidated messaging service."""

    def __init__(self, coord_path: str = "config/coordinates.json") -> None:
        """Initialize V2 compliant messaging service."""
        self.messaging_core = MessagingCore(coord_path)
        self.coordination_tracker = CoordinationTracker()
        self.pyautogui_handler = PyAutoGUIHandler()
        self.validator = MessageValidator()

        # Enhanced functionality
        self.auto_devlog_enabled = True
        self.response_protocol_enabled = True

    def send_message(
        self, agent_id: str, message: str, from_agent: str = None, priority: str = "NORMAL"
    ) -> bool:
        """Send message to specific agent."""
        if from_agent is None:
            logger.error("from_agent is required - agents must specify their own ID")
            return False

        # Validate parameters
        available_agents = self.messaging_core.list_agents()
        validation = self.validator.validate_send_message_params(
            agent_id, message, from_agent, priority, available_agents
        )

        if not validation["valid"]:
            logger.error(f"Validation failed: {validation['errors']}")
            return False

        # Get agent coordinates
        coordinates = self.messaging_core.get_agent_coordinates(agent_id)
        if not coordinates:
            logger.error(f"No coordinates found for agent {agent_id}")
            return False

        # Create message metadata
        metadata = self.messaging_core.create_message_metadata(from_agent, agent_id, priority)

        # Format message
        formatted_message = self.messaging_core.format_message(message, metadata)

        # Track coordination request
        self.coordination_tracker.track_coordination_request(from_agent, agent_id, message)

        # Send via PyAutoGUI
        success = self.pyautogui_handler.send_message_to_agent(coordinates, formatted_message)

        # Log delivery
        self.messaging_core.log_message_delivery(metadata, success)

        return success

    def broadcast_message(
        self, message: str, from_agent: str = None, priority: str = "NORMAL"
    ) -> dict:
        """Broadcast message to all agents."""
        if from_agent is None:
            from_agent = "Captain Agent-4"

        # Validate parameters
        validation = self.validator.validate_broadcast_params(message, from_agent, priority)
        if not validation["valid"]:
            logger.error(f"Broadcast validation failed: {validation['errors']}")
            return {"success": [], "failed": []}

        # Get all agents with coordinates
        agent_list = []
        for agent_id in self.messaging_core.list_agents():
            coordinates = self.messaging_core.get_agent_coordinates(agent_id)
            if coordinates:
                agent_list.append((agent_id, coordinates))

        # Create message metadata
        metadata = self.messaging_core.create_message_metadata(from_agent, "ALL", priority)
        formatted_message = self.messaging_core.format_message(message, metadata)

        # Send to all agents
        results = self.pyautogui_handler.send_bulk_messages(agent_list, formatted_message)

        # Track coordination for each agent
        for agent_id, _ in agent_list:
            self.coordination_tracker.track_coordination_request(from_agent, agent_id, message)

        return results

    def get_service_status(self) -> dict:
        """Get comprehensive service status."""
        base_status = self.messaging_core.get_service_status()
        coordination_stats = self.coordination_tracker.get_coordination_stats()
        pyautogui_info = self.pyautogui_handler.get_screen_info()

        return {
            **base_status,
            "coordination_requests": coordination_stats["total_requests"],
            "pyautogui_available": pyautogui_info["available"],
            "auto_devlog_enabled": self.auto_devlog_enabled,
            "response_protocol_enabled": self.response_protocol_enabled,
        }

    def check_protocol_compliance(self) -> dict:
        """Check protocol compliance status."""
        violations = self.coordination_tracker.check_response_protocol()
        return {"violations": violations, "has_violations": any(violations.values())}

    def onboard_agent(
        self, agent_id: str, message: str = None, from_agent: str = "Captain Agent-4"
    ) -> bool:
        """Send onboarding message to agent."""
        if message is None:
            message = f"Welcome to the swarm, {agent_id}! You are now onboarded."

        return self.send_message(agent_id, message, from_agent, "URGENT")

    def onboard_all_agents(self, message: str = None, from_agent: str = "Captain Agent-4") -> dict:
        """Send onboarding message to all agents."""
        if message is None:
            message = "Welcome to the swarm! All agents are now onboarded."

        return self.broadcast_message(message, from_agent, "URGENT")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="V2 Compliant Consolidated Messaging Service")
    parser.add_argument("--agent", "-a", help="Target agent ID")
    parser.add_argument("--message", "-m", help="Message content")
    parser.add_argument("--from-agent", help="Source agent ID")
    parser.add_argument("--priority", "-p", default="NORMAL", help="Message priority")
    parser.add_argument("--broadcast", action="store_true", help="Broadcast to all agents")
    parser.add_argument("--onboard", action="store_true", help="Onboard agent(s)")
    parser.add_argument("--status", action="store_true", help="Show service status")
    parser.add_argument("--protocol-check", action="store_true", help="Check protocol compliance")

    args = parser.parse_args()

    service = ConsolidatedMessagingServiceV2()

    if args.status:
        status = service.get_service_status()
        print(f"📊 Service Status: {status}")
        print("🐝 WE ARE SWARM - Status check complete")
        return

    if args.protocol_check:
        compliance = service.check_protocol_compliance()
        print(f"📋 Protocol Compliance: {compliance}")
        return

    if args.onboard:
        if args.agent:
            success = service.onboard_agent(args.agent, args.message, args.from_agent)
            print(f"✅ Onboarded {args.agent}" if success else f"❌ Failed to onboard {args.agent}")
        else:
            results = service.onboard_all_agents(args.message, args.from_agent)
            print(f"✅ Onboarded {len(results['success'])} agents")
        return

    if args.broadcast:
        if not args.message:
            print("❌ ERROR: --message is required for broadcast")
            return
        results = service.broadcast_message(args.message, args.from_agent, args.priority)
        print(f"✅ Broadcast sent to {len(results['success'])} agents")
        return

    if args.agent and args.message:
        success = service.send_message(args.agent, args.message, args.from_agent, args.priority)
        print(f"✅ Message sent to {args.agent}" if success else f"❌ Failed to send to {args.agent}")
        return

    print("❌ ERROR: Invalid arguments. Use --help for usage information")


if __name__ == "__main__":
    main()

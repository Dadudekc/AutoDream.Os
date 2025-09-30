#!/usr/bin/env python3
"""
Consolidated Messaging Service - Main
====================================

Main messaging service with sending, onboarding, and CLI functionality.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import argparse
import json
import logging
import sys
import time
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.append(str(project_root))

# Lazy import to prevent hard dep at import time
try:
    import pyautogui  # noqa: F401
    import pyperclip  # noqa: F401
except Exception as e:
    pyautogui = None  # type: ignore
    pyperclip = None  # type: ignore
    logging.warning(f"PyAutoGUI import failed: {e}")

from src.services.consolidated_messaging_service_core import ConsolidatedMessagingServiceCore
from src.services.consolidated_messaging_service_utils import (
    AgentOnboarder,
    MessageFormatter,
    MessageSender,
)

logger = logging.getLogger(__name__)


class ConsolidatedMessagingService(ConsolidatedMessagingServiceCore):
    """Complete messaging service with all functionality."""

    def __init__(self, coord_path: str = "config/coordinates.json") -> None:
        """Initialize complete messaging service."""
        super().__init__(coord_path)
        self.formatter = MessageFormatter()
        self.sender = MessageSender(self.enhanced_handler, self.enhanced_validator)
        self.onboarder = AgentOnboarder(coord_path)

    def send_message(
        self, agent_id: str, message: str, from_agent: str, priority: str = "NORMAL"
    ) -> bool:
        """Send message to specific agent."""
        if not self.is_agent_active(agent_id):
            logger.warning(f"Agent {agent_id} not active, skipping message")
            return False

        formatted_message = self.formatter.format_a2a_message(from_agent, agent_id, message, priority)

        coords = self.get_agent_coordinates(agent_id)
        if not coords:
            logger.error(f"No coordinates found for {agent_id}")
            return False

        success = self.sender.paste_to_coords(coords, formatted_message)

        if success:
            self.track_coordination_request(from_agent, agent_id, message)
            if self.auto_devlog_enabled:
                self._create_devlog_entry(from_agent, agent_id, message)

        return success

    def broadcast_message(self, message: str, from_agent: str, priority: str = "NORMAL") -> dict:
        """Broadcast message to all active agents."""
        results = {}

        for agent_id in self.agent_data.keys():
            if self.is_agent_active(agent_id):
                results[agent_id] = self.send_message(agent_id, message, from_agent, priority)
            else:
                results[agent_id] = False
                logger.info(f"Skipping inactive agent {agent_id}")

        return results

    def _create_devlog_entry(self, from_agent: str, to_agent: str, message: str) -> None:
        """Create automated devlog entry for message (placeholder)."""
        pass

    def stall_agent(self, agent_id: str, reason: str = None) -> bool:
        """Stall agent by sending Ctrl+Shift+Backspace."""
        try:
            with open(self.coord_path) as f:
                coords_data = json.load(f)

            if agent_id not in coords_data["agents"]:
                logger.error(f"Agent {agent_id} not found in coordinates")
                return False

            agent_coords = coords_data["agents"][agent_id]["chat_input_coordinates"]
            x, y = agent_coords[0], agent_coords[1]

            pyautogui.moveTo(x, y, duration=0.5)
            time.sleep(0.2)
            pyautogui.click()
            time.sleep(0.2)
            pyautogui.hotkey("ctrl", "shift", "backspace")
            time.sleep(0.5)

            logger.info(f"Stall command executed for {agent_id} at ({x}, {y})")
            return True

        except Exception as e:
            logger.error(f"Error stalling agent {agent_id}: {e}")
            return False

    def unstall_agent(self, agent_id: str, message: str = None) -> bool:
        """Unstall agent by sending Ctrl+Enter with optional message."""
        try:
            with open(self.coord_path) as f:
                coords_data = json.load(f)

            if agent_id not in coords_data["agents"]:
                logger.error(f"Agent {agent_id} not found in coordinates")
                return False

            agent_coords = coords_data["agents"][agent_id]["chat_input_coordinates"]
            x, y = agent_coords[0], agent_coords[1]

            pyautogui.moveTo(x, y, duration=0.5)
            time.sleep(0.2)
            pyautogui.click()
            time.sleep(0.2)

            if message:
                pyautogui.write(message)
                time.sleep(0.2)

            pyautogui.hotkey("ctrl", "enter")
            time.sleep(0.5)

            logger.info(f"Unstall command executed for {agent_id} at ({x}, {y})")
            return True

        except Exception as e:
            logger.error(f"Error unstalling agent {agent_id}: {e}")
            return False

    def hard_onboard_agent(self, agent_id: str) -> bool:
        """Comprehensive 7-step hard onboarding sequence for a single agent."""
        try:
            with open(self.coord_path) as f:
                coords_data = json.load(f)

            if agent_id not in coords_data["agents"]:
                logger.error(f"Agent {agent_id} not found in coordinates")
                return False

            agent_data = coords_data["agents"][agent_id]
            chat_coords = agent_data["chat_input_coordinates"]
            onboard_coords = agent_data["onboarding_coordinates"]

            default_role = self.onboarder.get_agent_default_role(agent_id)
            onboarding_message = self.onboarder.create_onboarding_message(agent_id, default_role)

            logger.info(f"Starting 7-step onboarding sequence for {agent_id}")

            # Step 1: Click chat input
            pyautogui.moveTo(chat_coords[0], chat_coords[1], duration=0.5)
            time.sleep(0.2)
            pyautogui.click()
            time.sleep(0.3)

            # Step 2: Press Ctrl+Enter+Backspace
            pyautogui.hotkey("ctrl", "enter")
            time.sleep(0.2)
            pyautogui.press("backspace")
            time.sleep(0.3)

            # Step 3: Press Ctrl+Enter to save
            pyautogui.hotkey("ctrl", "enter")
            time.sleep(0.3)

            # Step 4: Press Ctrl+N for new chat
            pyautogui.hotkey("ctrl", "n")
            time.sleep(0.5)

            # Step 5: Navigate to onboarding coords
            pyautogui.moveTo(onboard_coords[0], onboard_coords[1], duration=0.5)
            time.sleep(0.2)
            pyautogui.click()
            time.sleep(0.3)

            # Step 6: Paste onboarding message
            pyperclip.copy(onboarding_message)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.3)

            # Step 7: Send message
            pyautogui.press("enter")
            time.sleep(0.5)

            logger.info(f"✅ 7-step onboarding sequence completed for {agent_id}")
            return True

        except Exception as e:
            logger.error(f"Error in hard onboarding sequence for {agent_id}: {e}")
            return False

    def hard_onboard_all_agents(self) -> dict:
        """Hard onboard all active agents."""
        results = {}
        active_agents = ["Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

        for agent_id in active_agents:
            logger.info(f"Starting hard onboarding for {agent_id}")
            results[agent_id] = self.hard_onboard_agent(agent_id)
            time.sleep(1)

        return results


def build_parser() -> argparse.ArgumentParser:
    """Build command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Consolidated Messaging Service V2 - Modular Architecture"
    )

    parser.add_argument(
        "--coords", default="config/coordinates.json", help="Path to coordinates configuration file"
    )

    subparsers = parser.add_subparsers(dest="cmd", help="Available commands")

    # Send message
    send_parser = subparsers.add_parser("send", help="Send message to specific agent")
    send_parser.add_argument("--agent", required=True, help="Target agent ID")
    send_parser.add_argument("--message", required=True, help="Message to send")
    send_parser.add_argument("--from-agent", required=True, help="Source agent ID")
    send_parser.add_argument("--priority", default="NORMAL", help="Message priority")

    # Broadcast message
    broadcast_parser = subparsers.add_parser("broadcast", help="Send message to all agents")
    broadcast_parser.add_argument("--message", required=True, help="Message to broadcast")
    broadcast_parser.add_argument("--from-agent", required=True, help="Source agent ID")
    broadcast_parser.add_argument("--priority", default="NORMAL", help="Message priority")

    # Status
    subparsers.add_parser("status", help="Get system status")

    # Protocol check
    subparsers.add_parser("protocol-check", help="Check response protocol compliance")

    # Hard onboard
    onboard_parser = subparsers.add_parser("hard-onboard", help="Hard onboard agents")
    onboard_group = onboard_parser.add_mutually_exclusive_group(required=True)
    onboard_group.add_argument("--agent", help="Specific agent to onboard")
    onboard_group.add_argument("--all-agents", action="store_true", help="Onboard all agents")

    # Stall
    stall_parser = subparsers.add_parser("stall", help="Stall an agent")
    stall_parser.add_argument("--agent", required=True, help="Agent to stall")
    stall_parser.add_argument("--reason", help="Reason for stalling")

    # Unstall
    unstall_parser = subparsers.add_parser("unstall", help="Unstall an agent")
    unstall_parser.add_argument("--agent", required=True, help="Agent to unstall")
    unstall_parser.add_argument("--message", help="Message to send with unstall")

    # Cue
    cue_parser = subparsers.add_parser("cue", help="Send cued message to multiple agents")
    cue_parser.add_argument(
        "--agents", required=True, nargs="+", help="Target agent IDs (space-separated)"
    )
    cue_parser.add_argument("--message", required=True, help="Message to send")
    cue_parser.add_argument(
        "--cue", required=True, help="Queue/cue identifier for agents to respond to"
    )
    cue_parser.add_argument("--from-agent", default="Agent-5", help="Source agent ID")
    cue_parser.add_argument("--priority", default="HIGH", help="Message priority")

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.cmd:
        parser.print_help()
        print("\n🐝 WE ARE SWARM - Messaging Service Help Complete")
        return 1

    try:
        messaging_service = ConsolidatedMessagingService(args.coords)

        if args.cmd == "send":
            success = messaging_service.send_message(args.agent, args.message, args.from_agent)
            print(f"WE ARE SWARM - Message {'sent' if success else 'failed'} to {args.agent}")
            return 0 if success else 1

        elif args.cmd == "broadcast":
            results = messaging_service.broadcast_message(args.message, args.from_agent)
            success_count = sum(1 for success in results.values() if success)
            print(f"WE ARE SWARM - Broadcast complete: {success_count}/{len(results)} agents")
            return 0 if success_count == len(results) else 1

        elif args.cmd == "status":
            status = {
                "service_status": "Active",
                "agents_configured": len(messaging_service.agent_data),
                "active_agents": sum(
                    1
                    for agent_id in messaging_service.agent_data.keys()
                    if messaging_service.is_agent_active(agent_id)
                ),
                "coordination_requests": len(messaging_service.coordination_requests),
                "auto_devlog_enabled": messaging_service.auto_devlog_enabled,
                "response_protocol_enabled": messaging_service.response_protocol_enabled,
            }
            print("WE ARE SWARM - Status check complete")
            print(f"📊 Service Status: {status}")
            return 0

        elif args.cmd == "hard-onboard":
            if args.agent:
                success = messaging_service.hard_onboard_agent(args.agent)
                print(
                    f"WE ARE SWARM - Hard onboard {'successful' if success else 'failed'} for {args.agent}"
                )
                return 0 if success else 1
            elif args.all_agents:
                results = messaging_service.hard_onboard_all_agents()
                successful = sum(1 for success in results.values() if success)
                print(f"WE ARE SWARM - Hard onboard complete: {successful}/{len(results)} agents")
                return 0 if successful == len(results) else 1

        elif args.cmd == "stall":
            success = messaging_service.stall_agent(args.agent, args.reason)
            print(f"WE ARE SWARM - Agent {args.agent} {'stalled' if success else 'stall failed'}")
            return 0 if success else 1

        elif args.cmd == "unstall":
            success = messaging_service.unstall_agent(args.agent, args.message)
            print(
                f"WE ARE SWARM - Agent {args.agent} {'unstalled' if success else 'unstall failed'}"
            )
            return 0 if success else 1

        elif args.cmd == "protocol-check":
            violations = messaging_service.check_response_protocol()
            print("🚨 PROTOCOL COMPLIANCE CHECK")
            print("=" * 50)

            if violations["overdue"]:
                print(f"❌ OVERDUE RESPONSES: {len(violations['overdue'])}")
                for req_id in violations["overdue"]:
                    print(f"   - {req_id}")

            if violations["unacknowledged"]:
                print(f"⚠️ UNACKNOWLEDGED: {len(violations['unacknowledged'])}")
                for req_id in violations["unacknowledged"]:
                    print(f"   - {req_id}")

            if violations["incomplete"]:
                print(f"🔄 INCOMPLETE: {len(violations['incomplete'])}")
                for req_id in violations["incomplete"]:
                    print(f"   - {req_id}")

            if not any(violations.values()):
                print("✅ ALL PROTOCOLS COMPLIANT")

            return 0

        elif args.cmd == "cue":
            cued_message = f"""🔔 CUE: {args.cue}

{args.message}

📋 RESPONSE INSTRUCTIONS:
• Queue: {args.cue}
• Respond via: Agent messaging system
• Priority: {args.priority}
• From: {args.from_agent}

This message sent via PyAutoGUI automation."""

            results = {}
            for agent_id in args.agents:
                if messaging_service.is_agent_active(agent_id):
                    success = messaging_service.send_message(
                        agent_id=agent_id,
                        message=cued_message,
                        from_agent=args.from_agent,
                        priority=args.priority,
                    )
                    results[agent_id] = success
                    print(f"  Agent {agent_id}: {'Sent' if success else 'Failed'}")
                else:
                    results[agent_id] = False
                    print(f"  Agent {agent_id}: Inactive")

            success_count = sum(1 for success in results.values() if success)
            print(
                f"WE ARE SWARM - Cue '{args.cue}' complete: {success_count}/{len(results)} agents"
            )
            return 0 if success_count == len(results) else 1

        else:
            parser.print_help()
            print("WE ARE SWARM - Unknown command")
            return 1

    except Exception as e:
        logging.error("Service error: %s", e)
        print(f"WE ARE SWARM - Service error: {e}")
        return 2


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())

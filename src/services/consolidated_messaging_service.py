#!/usr/bin/env python3
"""
Consolidated Messaging Service - SSOT for All Messaging
=======================================================

Single Source of Truth messaging service that consolidates all messaging functionality.
Handles core messaging, status monitoring, onboarding, and enhanced features.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.append(str(project_root))

from src.services.coordinate_loader import CoordinateLoader

# Lazy import to prevent hard dep at import time
try:
    import pyautogui  # noqa: F401
    import pyperclip  # noqa: F401
except Exception as e:
    pyautogui = None  # type: ignore
    pyperclip = None  # type: ignore
    logging.warning(f"PyAutoGUI import failed: {e}")

logger = logging.getLogger(__name__)


class ConsolidatedMessagingService:
    """Consolidated messaging service - SSOT for all messaging."""

    def __init__(self, coord_path: str = "config/coordinates.json") -> None:
        """Initialize consolidated messaging service - SSOT for all messaging."""
        self.coord_path = coord_path
        self.agent_data = self._load_coordinates()

        # Add enhanced functionality
        self.auto_devlog_enabled = True

    def _load_coordinates(self) -> dict:
        """Load agent coordinates from JSON file."""
        try:
            with open(self.coord_path, 'r') as f:
                data = json.load(f)
            return data.get('agents', {})
        except Exception as e:
            logger.error(f"Error loading coordinates: {e}")
            return {}

    def send_message(self, agent_id: str, message: str, from_agent: str = "Agent-2", priority: str = "NORMAL") -> bool:
        """Send message to specific agent via PyAutoGUI automation."""
        if not self._is_agent_active(agent_id):
            logger.warning(f"Agent {agent_id} is inactive, message not sent")
            return False

        try:
            # Get agent coordinates
            if agent_id not in self.agent_data:
                logger.error(f"Agent {agent_id} not found in coordinates")
                return False

            coords = self.agent_data[agent_id]["chat_input_coordinates"]
            if not isinstance(coords, list) or len(coords) < 2:
                logger.error(f"Invalid coordinates for agent {agent_id}: {coords}")
                return False

            # Format A2A message
            formatted_message = self._format_a2a_message(from_agent, agent_id, message, priority)

            # Send via PyAutoGUI
            success = self._paste_to_coords(coords, formatted_message)

            # Auto-create devlog if enabled (disabled for now)
            # TODO: Implement devlog creation functionality
            # if success and self.auto_devlog_enabled:
            #     logger.info("Auto devlog creation disabled")

            if success:
                logger.info(f"Message sent to {agent_id} from {from_agent}")
            else:
                logger.error(f"Failed to send message to {agent_id}")

            return success

        except Exception as e:
            logger.error(f"Error sending message to {agent_id}: {e}")
            return False

    def broadcast_message(self, message: str, from_agent: str = "Agent-2", priority: str = "NORMAL") -> Dict[str, bool]:
        """Send message to all active agents."""
        results = {}

        for agent_id in self.agent_data.keys():
            if self._is_agent_active(agent_id):
                results[agent_id] = self.send_message(agent_id, message, from_agent, priority)
            else:
                results[agent_id] = False
                logger.info(f"Skipping inactive agent {agent_id}")

        return results

    def _is_agent_active(self, agent_id: str) -> bool:
        """Check if agent is active."""
        return agent_id in self.agent_data and self.agent_data[agent_id].get("active", True)

    def _format_a2a_message(self, from_agent: str, to_agent: str, content: str, priority: str) -> str:
        """Format A2A message with proper headers."""
        priority_indicator = "🚨 " if priority.upper() == "URGENT" else ""

        return f"""============================================================
[A2A] MESSAGE
============================================================
📤 FROM: {from_agent}
📥 TO: {to_agent}
Priority: {priority.upper()}
Tags: GENERAL
------------------------------------------------------------
{content}
📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory
------------------------------------------------------------
{self._get_quality_guidelines()}
============================================================
------------------------------------------------------------"""

    def _get_quality_guidelines(self) -> str:
        """Get quality guidelines reminder for all agent communications."""
        return """🎯 QUALITY GUIDELINES REMINDER
============================================================
📋 V2 Compliance Requirements:
• File Size: ≤400 lines (hard limit)
• Enums: ≤3 per file
• Classes: ≤5 per file
• Functions: ≤10 per file
• Complexity: ≤10 cyclomatic complexity per function
• Parameters: ≤5 per function
• Inheritance: ≤2 levels deep

🚫 Forbidden Patterns (Red Flags):
• Abstract Base Classes (without 2+ implementations)
• Excessive async operations (without concurrency need)
• Complex inheritance chains (>2 levels)
• Event sourcing for simple operations
• Dependency injection for simple objects
• Threading for synchronous operations
• 20+ fields per entity
• 5+ enums per file

✅ Required Patterns (Green Flags):
• Simple data classes with basic fields
• Direct method calls instead of complex event systems
• Synchronous operations for simple tasks
• Basic validation for essential data
• Simple configuration with defaults
• Basic error handling with clear messages

🎯 KISS Principle: Start with the simplest solution that works!
📊 QUALITY GATES: Run `python quality_gates.py` before submitting code!
============================================================"""

    def _paste_to_coords(self, coords: tuple[int, int], text: str) -> bool:
        """Paste text to coordinates using PyAutoGUI."""
        if not pyautogui or not pyperclip:
            logger.error("PyAutoGUI or pyperclip not available")
            return False

        try:
            # Save current clipboard
            original_clipboard = pyperclip.paste()

            # Set new clipboard content
            pyperclip.copy(text)

            # Click at coordinates to focus
            pyautogui.click(coords[0], coords[1])

            # Paste
            pyautogui.hotkey('ctrl', 'v')

            # Restore original clipboard
            pyperclip.copy(original_clipboard)

            return True

        except Exception as e:
            logger.error(f"Failed to paste to coordinates: {e}")
            return False
    
    def stall_agent(self, agent_id: str, reason: str = None) -> bool:
        """Stall an agent by sending Ctrl+Shift+Backspace to their chat input."""
        try:
            import json
            import pyautogui
            import time
            
            # Load coordinates
            with open(self.coord_path, 'r') as f:
                coords_data = json.load(f)
            
            if agent_id not in coords_data['agents']:
                logger.error(f"Agent {agent_id} not found in coordinates")
                return False
            
            agent_coords = coords_data['agents'][agent_id]['chat_input_coordinates']
            x, y = agent_coords[0], agent_coords[1]
            
            # Execute stall command
            pyautogui.moveTo(x, y, duration=0.5)
            time.sleep(0.2)
            pyautogui.click()
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'shift', 'backspace')
            time.sleep(0.5)
            
            logger.info(f"Stall command executed for {agent_id} at ({x}, {y})")
            return True
            
        except Exception as e:
            logger.error(f"Error stalling agent {agent_id}: {e}")
            return False
    
    def unstall_agent(self, agent_id: str, message: str = None) -> bool:
        """Unstall an agent by sending Ctrl+Enter with optional message."""
        try:
            import json
            import pyautogui
            import time
            
            # Load coordinates
            with open(self.coord_path, 'r') as f:
                coords_data = json.load(f)
            
            if agent_id not in coords_data['agents']:
                logger.error(f"Agent {agent_id} not found in coordinates")
                return False
            
            agent_coords = coords_data['agents'][agent_id]['chat_input_coordinates']
            x, y = agent_coords[0], agent_coords[1]
            
            # Execute unstall command
            pyautogui.moveTo(x, y, duration=0.5)
            time.sleep(0.2)
            pyautogui.click()
            time.sleep(0.2)
            
            if message:
                pyautogui.write(message)
                time.sleep(0.2)
            
            pyautogui.hotkey('ctrl', 'enter')
            time.sleep(0.5)
            
            logger.info(f"Unstall command executed for {agent_id} at ({x}, {y})")
            return True
            
        except Exception as e:
            logger.error(f"Error unstalling agent {agent_id}: {e}")
            return False


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
    
    # Stall command
    stall_parser = subparsers.add_parser("stall", help="Stall an agent")
    stall_parser.add_argument("--agent", required=True, help="Agent to stall")
    stall_parser.add_argument("--reason", help="Reason for stalling")
    
    # Unstall command
    unstall_parser = subparsers.add_parser("unstall", help="Unstall an agent")
    unstall_parser.add_argument("--agent", required=True, help="Agent to unstall")
    unstall_parser.add_argument("--message", help="Message to send with unstall")
    
    return parser


def main(argv: List[str] | None = None) -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)
    
    if not args.cmd:
        parser.print_help()
        print("\n🐝 WE ARE SWARM - Messaging Service Help Complete")
        return 1
    
    try:
        # Initialize services
        messaging_service = ConsolidatedMessagingService(args.coords)
        
        # Handle commands
        if args.cmd == "send":
            success = messaging_service.send_message(args.agent, args.message, args.from_agent)
            print(f"🐝 WE ARE SWARM - Message {'sent' if success else 'failed'} to {args.agent}")
            return 0 if success else 1
            
        elif args.cmd == "broadcast":
            results = messaging_service.broadcast_message(args.message, args.from_agent)
            success_count = sum(1 for success in results.values() if success)
            print(f"🐝 WE ARE SWARM - Broadcast complete: {success_count}/{len(results)} agents")
            return 0 if success_count == len(results) else 1
            
        elif args.cmd == "status":
            status = status_monitor.get_comprehensive_status()
            logging.info(f"Service Status: {status}")
            print("🐝 WE ARE SWARM - Status check complete")
            return 0
            
        elif args.cmd == "hard-onboard":
            if args.agent:
                success = onboarding_service.hard_onboard_agent(args.agent)
                print(f"🐝 WE ARE SWARM - Hard onboard {'successful' if success else 'failed'} for {args.agent}")
                return 0 if success else 1
            elif args.all_agents:
                results = onboarding_service.hard_onboard_all_agents()
                successful = sum(1 for success in results.values() if success)
                print(f"🐝 WE ARE SWARM - Hard onboard complete: {successful}/{len(results)} agents")
                return 0 if successful == len(results) else 1
            else:
                logging.error("Error: Must specify either --agent or --all-agents")
                print("🐝 WE ARE SWARM - Hard onboard error")
                return 1
        
        elif args.cmd == "stall":
            # Create consolidated service for stall functionality
            consolidated_service = ConsolidatedMessagingService(args.coords)
            success = consolidated_service.stall_agent(args.agent, args.reason)
            print(f"🐝 WE ARE SWARM - Agent {args.agent} {'stalled' if success else 'stall failed'}")
            return 0 if success else 1
            
        elif args.cmd == "unstall":
            # Create consolidated service for unstall functionality
            consolidated_service = ConsolidatedMessagingService(args.coords)
            success = consolidated_service.unstall_agent(args.agent, args.message)
            print(f"🐝 WE ARE SWARM - Agent {args.agent} {'unstalled' if success else 'unstall failed'}")
            return 0 if success else 1
            
        else:
            parser.print_help()
            print("🐝 WE ARE SWARM - Unknown command")
            return 1
            
    except Exception as e:
        logging.error("Service error: %s", e)
        print(f"🐝 WE ARE SWARM - Service error: {e}")
        return 2


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())

#!/usr/bin/env python3
"""
Simple Messaging Service - Fixed Version
========================================

Working messaging service for agent communication.
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from coordinate_loader import CoordinateLoader

# Lazy import to prevent hard dep at import time
try:
    import pyautogui
    import pyperclip
except Exception as e:
    pyautogui = None
    pyperclip = None
    logging.warning(f"PyAutoGUI import failed: {e}")

logger = logging.getLogger(__name__)


class SimpleMessagingService:
    """Simple messaging service for agent communication."""
    
    def __init__(self, coord_path: str = "config/coordinates.json") -> None:
        """Initialize messaging service with coordinate validation."""
        self.coords_file = coord_path
        self.loader = CoordinateLoader(coord_path)
        self.loader.load()
    
    def send_message(self, agent_id: str, message: str, from_agent: str = "Agent-2", priority: str = "NORMAL") -> bool:
        """Send message to specific agent via PyAutoGUI automation."""
        if not self._is_agent_active(agent_id):
            logger.warning(f"Agent {agent_id} is inactive, message not sent")
            return False
            
        try:
            # Get agent coordinates
            try:
                coords = self.loader.get_agent_coordinates(agent_id)
            except ValueError as e:
                logger.error(f"Agent {agent_id} not found in coordinates: {e}")
                return False
            
            # Format A2A message
            formatted_message = self._format_a2a_message(from_agent, agent_id, message, priority)
            
            # Send via PyAutoGUI
            success = self._paste_to_coords(coords, formatted_message)
            
            if success:
                logger.info(f"Message sent to {agent_id} from {from_agent}")
            else:
                logger.error(f"Failed to send message to {agent_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending message to {agent_id}: {e}")
            return False
    
    def broadcast_message(self, message: str, from_agent: str = "Agent-2", priority: str = "NORMAL") -> dict:
        """Send message to all active agents."""
        results = {}
        
        for agent_id in self.loader.get_agent_ids():
            if self._is_agent_active(agent_id):
                results[agent_id] = self.send_message(agent_id, message, from_agent, priority)
            else:
                results[agent_id] = False
                logger.info(f"Skipping inactive agent {agent_id}")
        
        return results
    
    def _format_a2a_message(self, from_agent: str, to_agent: str, message: str, priority: str = "NORMAL") -> str:
        """Format agent-to-agent message with standard template."""
        return f"""============================================================
[A2A] MESSAGE
============================================================
📤 FROM: {from_agent}
📥 TO: {to_agent}
Priority: {priority}
Tags: GENERAL
------------------------------------------------------------
{message}
📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory
------------------------------------------------------------
🎯 QUALITY GUIDELINES REMINDER
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
============================================================
------------------------------------------------------------
"""
    
    def _paste_to_coords(self, coords, message: str) -> bool:
        """Paste message to coordinates using PyAutoGUI."""
        if not pyautogui or not pyperclip:
            logger.error("PyAutoGUI or Pyperclip not available")
            return False
        
        try:
            # Copy message to clipboard
            pyperclip.copy(message)
            
            # Click coordinates
            pyautogui.click(coords[0], coords[1])
            pyautogui.sleep(0.5)
            
            # Paste message
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.sleep(0.5)
            
            # Send message
            pyautogui.press('enter')
            
            return True
            
        except Exception as e:
            logger.error(f"Error pasting to coordinates: {e}")
            return False
    
    def _is_agent_active(self, agent_id: str) -> bool:
        """Check if agent is active."""
        try:
            agents = self.loader.coordinates.get("agents", {})
            agent_data = agents.get(agent_id, {})
            return agent_data.get("active", True)
        except Exception:
            return True  # Default to active if check fails


def build_parser() -> argparse.ArgumentParser:
    """Build command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Simple Messaging Service - Fixed Version"
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
    
    return parser


def main(argv: List[str] | None = None) -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)
    
    if not args.cmd:
        parser.print_help()
        return 1
    
    try:
        # Initialize service
        messaging_service = SimpleMessagingService(args.coords)
        
        # Handle commands
        if args.cmd == "send":
            success = messaging_service.send_message(args.agent, args.message, args.from_agent, args.priority)
            if success:
                print(f"✅ Message sent successfully to {args.agent}")
            else:
                print(f"❌ Failed to send message to {args.agent}")
            return 0 if success else 1
            
        elif args.cmd == "broadcast":
            results = messaging_service.broadcast_message(args.message, args.from_agent, args.priority)
            success_count = sum(1 for success in results.values() if success)
            print(f"📡 Broadcast results: {success_count}/{len(results)} agents")
            for agent_id, success in results.items():
                status = "✅" if success else "❌"
                print(f"  {status} {agent_id}")
            return 0 if success_count == len(results) else 1
            
        elif args.cmd == "status":
            agent_ids = messaging_service.loader.get_agent_ids()
            print(f"🤖 Messaging Service Status:")
            print(f"  Active agents: {len(agent_ids)}")
            print(f"  Agent IDs: {', '.join(agent_ids)}")
            return 0
            
        else:
            parser.print_help()
            return 1
            
    except Exception as e:
        logging.error("Service error: %s", e)
        return 2


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())




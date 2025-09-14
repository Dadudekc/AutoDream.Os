#!/usr/bin/env python3
"""
Working Messaging System - Agent-5 Co-Captain Implementation
============================================================

This is a functional messaging system that actually works, created by Agent-5
as Co-Captain to restore swarm communication capabilities.

Author: Agent-5 (Business Intelligence Specialist & Co-Captain)
Mission: Debug and restore messaging system functionality
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path

# Check PyAutoGUI availability (used by messaging_pyautogui module)
try:
    import pyautogui  # noqa: F401
    import pyperclip  # noqa: F401
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

logger = logging.getLogger(__name__)

class WorkingMessagingSystem:
    """Functional messaging system for swarm coordination"""

    def __init__(self):
        self.coordinates_file = Path("cursor_agent_coords.json")
        self.agent_workspaces = Path("agent_workspaces")
        self.coordinates = self._load_coordinates()

    def _load_coordinates(self) -> dict:
        """Load agent coordinates from JSON file"""
        try:
            if self.coordinates_file.exists():
                with open(self.coordinates_file) as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Failed to load coordinates: {e}")
            return {}

    def list_agents(self) -> list[str]:
        """List all available agents"""
        if "agents" in self.coordinates:
            return list(self.coordinates["agents"].keys())
        return []

    def send_message_pyautogui(self, agent_id: str, message: str) -> bool:
        """Send message using enhanced PyAutoGUI SSOT"""
        if not PYAUTOGUI_AVAILABLE:
            logger.warning("PyAutoGUI not available - using inbox fallback")
            return self.send_message_inbox(agent_id, message)

        try:
            # Use the enhanced PyAutoGUI SSOT from src/core/messaging_pyautogui.py
            import sys
            from pathlib import Path

            # Add project root to path if needed
            project_root = Path(__file__).parent
            if str(project_root) not in sys.path:
                sys.path.insert(0, str(project_root))

            from src.core.messaging_pyautogui import (
                deliver_message_pyautogui,
                get_agent_coordinates,
            )

            # Create unified message format for enhanced delivery
            unified_message = {
                "sender": "WorkingMessagingSystem-Agent5",
                "recipient": agent_id,
                "message_type": "agent_to_agent",
                "priority": "NORMAL",
                "tags": ["COORDINATION"],
                "content": message,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }

            # Get coordinates using SSOT
            coords = get_agent_coordinates(agent_id)
            if not coords:
                logger.error(f"No coordinates found for {agent_id}")
                return False

            # Use enhanced delivery system
            success = deliver_message_pyautogui(unified_message, coords)
            if success:
                logger.info(f"✅ Enhanced message sent to {agent_id} via PyAutoGUI SSOT")
            return success

        except Exception as e:
            logger.error(f"❌ Failed to send enhanced PyAutoGUI message to {agent_id}: {e}")
            # Fallback to inbox if SSOT fails
            logger.info("Falling back to inbox delivery...")
            return self.send_message_inbox(agent_id, message)

    def send_message_inbox(self, agent_id: str, message: str, sender: str = "Agent-5 (Co-Captain)") -> bool:
        """Send message to agent's inbox"""
        try:
            inbox_dir = self.agent_workspaces / agent_id / "inbox"
            inbox_dir.mkdir(parents=True, exist_ok=True)

            # Create message filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            message_filename = f"CO_CAPTAIN_MESSAGE_{timestamp}.md"

            # Create message content
            message_content = f"""# 🚨 CO-CAPTAIN MESSAGE - {agent_id}

**From**: {sender}
**To**: {agent_id}
**Priority**: normal
**Message ID**: co_captain_{timestamp}
**Timestamp**: {datetime.now().isoformat()}

---

{message}

---

*Message delivered via Working Messaging System*
*Co-Captain Agent-5 - Business Intelligence Specialist*
"""

            # Write message to agent's inbox
            message_file_path = inbox_dir / message_filename
            with open(message_file_path, "w", encoding="utf-8") as f:
                f.write(message_content)

            logger.info(f"✅ Message sent to {agent_id}'s inbox: {message_filename}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send inbox message to {agent_id}: {e}")
            return False

    def send_message(self, agent_id: str, message: str, method: str = "auto") -> bool:
        """Send message using specified method"""
        if method == "pyautogui":
            return self.send_message_pyautogui(agent_id, message)
        elif method == "inbox":
            return self.send_message_inbox(agent_id, message)
        else:  # auto
            # Try PyAutoGUI first, fallback to inbox
            if PYAUTOGUI_AVAILABLE:
                success = self.send_message_pyautogui(agent_id, message)
                if success:
                    return True

            return self.send_message_inbox(agent_id, message)

    def broadcast_message(self, message: str, method: str = "auto") -> dict[str, bool]:
        """Broadcast message to all agents"""
        results = {}
        agents = self.list_agents()

        for agent_id in agents:
            success = self.send_message(agent_id, message, method)
            results[agent_id] = success
            time.sleep(0.5)  # Small delay between messages

        return results

    def get_agent_status(self, agent_id: str) -> dict:
        """Get agent status from status.json"""
        try:
            status_file = self.agent_workspaces / agent_id / "status.json"
            if status_file.exists():
                with open(status_file) as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Failed to get status for {agent_id}: {e}")
            return {}

    def check_system_status(self) -> dict:
        """Check overall system status"""
        agents = self.list_agents()
        status = {
            "total_agents": len(agents),
            "pyautogui_available": PYAUTOGUI_AVAILABLE,
            "coordinates_loaded": bool(self.coordinates),
            "agent_workspaces_exist": self.agent_workspaces.exists(),
            "agents": {}
        }

        for agent_id in agents:
            agent_status = self.get_agent_status(agent_id)
            status["agents"][agent_id] = {
                "has_status_file": bool(agent_status),
                "last_updated": agent_status.get("last_updated", "unknown"),
                "status": agent_status.get("status", "unknown")
            }

        return status

# Global instance
working_messaging = WorkingMessagingSystem()

def main():
    """CLI interface for the working messaging system"""
    import argparse

    parser = argparse.ArgumentParser(description="Working Messaging System - Agent-5 Co-Captain")
    parser.add_argument("--list-agents", action="store_true", help="List all agents")
    parser.add_argument("--status", action="store_true", help="Check system status")
    parser.add_argument("--agent", "-a", help="Target agent ID")
    parser.add_argument("--message", "-m", help="Message to send")
    parser.add_argument("--broadcast", "-b", action="store_true", help="Broadcast to all agents")
    parser.add_argument("--method", choices=["pyautogui", "inbox", "auto"], default="auto", help="Delivery method")

    args = parser.parse_args()

    if args.list_agents:
        agents = working_messaging.list_agents()
        print("Available agents:")
        for agent in agents:
            print(f"  - {agent}")
        return

    if args.status:
        status = working_messaging.check_system_status()
        print("System Status:")
        print(f"  Total agents: {status['total_agents']}")
        print(f"  PyAutoGUI available: {status['pyautogui_available']}")
        print(f"  Coordinates loaded: {status['coordinates_loaded']}")
        print(f"  Agent workspaces exist: {status['agent_workspaces_exist']}")
        print("\nAgent Status:")
        for agent_id, agent_status in status['agents'].items():
            print(f"  {agent_id}: {agent_status['status']} (last updated: {agent_status['last_updated']})")
        return

    if args.broadcast and args.message:
        print("Broadcasting message to all agents...")
        results = working_messaging.broadcast_message(args.message, args.method)
        print("Results:")
        for agent_id, success in results.items():
            status = "✅" if success else "❌"
            print(f"  {status} {agent_id}")
        return

    if args.agent and args.message:
        print(f"Sending message to {args.agent}...")
        success = working_messaging.send_message(args.agent, args.message, args.method)
        status = "✅" if success else "❌"
        print(f"{status} Message delivery {'successful' if success else 'failed'}")
        return

    parser.print_help()

if __name__ == "__main__":
    main()

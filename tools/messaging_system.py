#!/usr/bin/env python3
"""
Unified Agent Messaging System
Single source of truth for all agent communication protocols
Includes soft and hard onboarding capabilities
"""

import json
import sys
import time
from pathlib import Path

# Use UI Ops facade for PyAutoGUI operations
# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.libs.uiops import UI


# Load coordinates configuration
def load_coordinates():
    """Load agent coordinates from configuration."""
    coord_file = Path("config/coordinates.json")
    if coord_file.exists():
        with open(coord_file) as f:
            return json.load(f)
    else:
        print("❌ Error: config/coordinates.json not found!")
        print("Please ensure coordinate configuration exists.")
        sys.exit(1)


class MessagingSystem:
    """Unified messaging system for all agent communication."""

    def __init__(self):
        self.coords = load_coordinates()

    def send_message(self, from_agent, to_agent, message, priority="NORMAL", execution_mode=False):
        """Send a message from one agent to another."""
        try:
            # Get target agent coordinates (where to deliver the message)
            chat_coords = self.coords["agents"][to_agent]["chat_input_coordinates"]

            # Format message appropriately
            if execution_mode:
                formatted_message = self._format_execution_message(message)
            else:
                formatted_message = self._format_a2a_message(
                    from_agent, to_agent, message, priority
                )

            # Send via UI Ops facade
            UI.click(chat_coords[0], chat_coords[1])
            UI.sleep(0.5)
            UI.paste(formatted_message)
            UI.sleep(0.5)
            UI.press("enter")

            print(f"INFO:__main__:✅ Message sent from {from_agent} to {to_agent}")
            return {"success": True}

        except Exception as e:
            print(f"ERROR:__main__:❌ Failed to send message: {e}")
            return {"success": False, "error": str(e)}

    def _format_execution_message(self, message):
        """Format message in execution mode."""
        return f"""EXECUTION ORDER
═══════════════════════════════════════════════════════════════════════════════

{message}

═══════════════════════════════════════════════════════════════════════════════
📝 READ AND EXECUTE"""

    def _format_a2a_message(self, from_agent, to_agent, message, priority):
        """Format agent-to-agent message."""
        priority_labels = {"NORMAL": "NORMAL", "HIGH": "HIGH", "CRITICAL": "CRITICAL"}

        return f"""============================================================
[A2A] MESSAGE
============================================================
📤 FROM: {from_agent}
📥 TO: {to_agent}
Priority: {priority_labels.get(priority, 'NORMAL')}
Tags: TASK_ASSIGNMENT
------------------------------------------------------------

{message}

🎯 QUALITY GATES REMINDER
============================================================
📋 V2 COMPLIANCE: ≤400 lines • ≤5 classes • ≤10 functions
🚫 NO: Abstract classes • Complex inheritance • Threading
✅ USE: Simple data classes • Direct calls • Basic validation
🎯 KISS: Keep it simple! • Run `python quality_gates.py`
============================================================
📝 DEVLOG: Use 'python src/services/agent_devlog_posting.py --agent <flag> --action <desc>'
============================================================
📤 MESSAGING: Use 'python messaging_system.py <from_agent> <to_agent> "<message>" <priority>'
📋 PRIORITIES: NORMAL, HIGH, CRITICAL
📋 EXAMPLE: python messaging_system.py Agent-5 Agent-4 "Task completed successfully" NORMAL
============================================================
------------------------------------------------------------"""


# Initialize coordinates
coords = load_coordinates()


def soft_onboard_handler(target_agent_id):
    """Handle soft onboarding (passdown preparation)."""
    try:
        from src.services.agent_passdown import AgentPassdownCreator

        current_agent = "Agent-4"  # Captain sending passdown
        passdown_creator = AgentPassdownCreator()
        message = passdown_creator.create_passdown_message(target_agent_id, current_agent)

        return {"current_agent": current_agent, "target_agent": target_agent_id, "message": message}

    except Exception as e:
        print(f"❌ Soft onboard handler failed: {e}")
        return None


def hard_onboard_handler(target_agent_id=None):
    """Handle hard onboarding (agent activation)."""
    try:
        import time

        import pyautogui

        from src.services.agent_hard_onboarding import AgentHardOnboarder

        if not target_agent_id:
            # Hard onboard all agents
            print("🎯 Hard onboarding ALL agents...")
            onboarder = AgentHardOnboarder()
            result = onboarder.hard_onboard_agent(target_agent_id)
            return result

        # Hard onboard specific agent
        print(f"🎯 Hard onboarding {target_agent_id}...")

        # Get coordinates for target agent
        agent_coords = coords["agents"][target_agent_id]
        chat_coords = agent_coords["chat_input_coordinates"]
        onboard_coords = agent_coords.get("onboarding_coordinates", chat_coords)

        # Execute hard onboarding sequence
        # Step 1: Click chat input coordinates
        UI.click(chat_coords[0], chat_coords[1])
        UI.sleep(0.5)

        # Step 2: Press ctrl+shift+backspace (clear input)
        UI.hotkey("ctrl", "shift", "backspace")
        UI.sleep(0.3)

        # Step 3: Press ctrl+n (new window/tab)
        UI.hotkey("ctrl", "n")
        UI.sleep(1.0)

        # Step 4: Navigate to onboarding input location and wait
        UI.click(onboard_coords[0], onboard_coords[1])
        UI.sleep(1.0)

        # Step 5: Generate and paste onboarding message
        onboarder = AgentHardOnboarder()
        onboarding_message = onboarder.create_onboarding_message(target_agent_id, "TASK_EXECUTOR")

        UI.paste(onboarding_message)
        UI.sleep(0.3)
        UI.press("enter")

        print("✅ Hard onboarding successful! Agent(s) ready for interaction.")
        return {"success": True, "message": onboarding_message}

    except Exception as e:
        print(f"❌ Hard onboard handler failed: {e}")
        return {"success": False, "error": str(e)}


def main():
    """Main entry point for messaging system."""

    # Handle help/usage
    if len(sys.argv) < 2 or "--help" in sys.argv:
        print("🤖 AGENT MESSAGING SYSTEM - UNIFIED COMMUNICATION")
        print("=" * 60)
        print("Usage:")
        print(
            "  python messaging_system.py <from_agent> <to_agent> '<message>' [priority] [--execution-mode]"  # noqa: E501
        )
        print("  python messaging_system.py --soft-onboard <target_agent>")
        print("  python messaging_system.py --hard-onboard [target_agent]")
        print()
        print("Examples:")
        print("  python messaging_system.py Agent-4 Agent-5 'Execute cleanup' HIGH")
        print(
            "  python messaging_system.py Agent-4 Agent-5 'Direct command' NORMAL --execution-mode"
        )
        print("  python messaging_system.py --soft-onboard Agent-6")
        print("  python messaging_system.py --hard-onboard Agent-6")
        print("  python messaging_system.py --hard-onboard  # All agents")
        sys.exit(1)

    # Check for soft-onboard command
    if len(sys.argv) == 3 and sys.argv[1] == "--soft-onboard":
        target_agent_id = sys.argv[2]

        print("\n🎯 SOFT ONBOARDING SEQUENCE INITIATED")
        print("=" * 50)
        print(f"Target: {target_agent_id}")
        print(
            "Sequence: 1) Click chat input 2) Send passdown 3) Ctrl+T 4) Move to onboard coords 5) Paste onboard message"
        )

        try:
            # Step 1: Click to chat input coordinates (current agent)
            print("\n📍 Step 1: Clicking chat input coordinates...")
            chat_coords = coords["agents"]["Agent-4"]["chat_input_coordinates"]
            UI.click(chat_coords[0], chat_coords[1])
            UI.sleep(0.5)
            print("✅ Chat input clicked")

            # Step 2: Generate and send passdown message
            print("\n📤 Step 2: Generating and sending passdown message...")
            result = soft_onboard_handler(target_agent_id)

            if not result:
                print("❌ Failed to generate passdown message")
                sys.exit(1)

            # Send the passdown message to target agent
            messaging = MessagingSystem()
            send_result = messaging.send_message(
                result["current_agent"], target_agent_id, result["message"], "NORMAL"
            )

            if not send_result["success"]:
                print(
                    f"❌ Failed to send passdown message: {send_result.get('error', 'Unknown error')}"  # noqa: E501
                )
                sys.exit(1)

            print("✅ Passdown message sent successfully")

            # Step 3: Press Ctrl+T
            print("\n🔄 Step 3: Pressing Ctrl+T for agent transition...")
            UI.hotkey("ctrl", "t")
            UI.sleep(2.0)  # Wait for agent transition
            print("✅ Ctrl+T pressed")

            # Step 4: Move to onboarding input coordinates
            print("\n📍 Step 4: Moving to onboarding input coordinates...")
            onboard_coords = coords["agents"][target_agent_id].get("onboarding_coordinates")
            if not onboard_coords:
                onboard_coords = coords["agents"][target_agent_id]["chat_input_coordinates"]

            UI.click(onboard_coords[0], onboard_coords[1])
            UI.sleep(1.0)
            print("✅ Onboarding coordinates clicked")

            # Step 5: Generate and paste onboarding message
            print("\n📝 Step 5: Generating and pasting onboarding message...")
            hard_result = hard_onboard_handler(target_agent_id)

            if hard_result and hard_result.get("success"):
                print("✅ Onboarding message pasted")

                print("\n✅ COMPLETE SOFT ONBOARDING SEQUENCE COMPLETE")
                print(f"🎯 {target_agent_id} onboarded with passdown context in inbox")
            else:
                print("❌ Failed to generate onboarding message")

        except Exception as e:
            print(f"❌ Soft onboarding sequence failed: {e}")
            sys.exit(1)

        return

    # Check for hard-onboard command
    if len(sys.argv) >= 2 and sys.argv[1] == "--hard-onboard":
        target_agent_id = sys.argv[2] if len(sys.argv) == 3 else None

        # Use modular handler
        result = hard_onboard_handler(target_agent_id)

        if not result or not result.get("success", False):
            print("❌ Hard onboarding failed")
            sys.exit(1)

        print("\n🚀 Hard onboarding completed successfully!")
        return

    # Standard message sending
    if len(sys.argv) < 4:
        print("❌ Error: Missing required arguments")
        print(
            "Usage: python messaging_system.py <from_agent> <to_agent> '<message>' [priority] [--execution-mode]"  # noqa: E501
        )
        sys.exit(1)

    from_agent = sys.argv[1]
    to_agent = sys.argv[2]
    message = sys.argv[3]
    priority = sys.argv[4] if len(sys.argv) > 4 else "NORMAL"
    execution_mode = "--execution-mode" in sys.argv

    # Initialize messaging system
    messaging = MessagingSystem()

    # Send message
    result = messaging.send_message(from_agent, to_agent, message, priority, execution_mode)

    if not result["success"]:
        print(f"❌ Failed to send message: {result.get('error', 'Unknown error')}")
        sys.exit(1)

    print("✅ Message sent successfully!")


if __name__ == "__main__":
    main()

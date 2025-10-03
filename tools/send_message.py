#!/usr/bin/env python3
"""
Simple Agent Message Sender
===========================

Simple tool to send messages to agents using PyAutoGUI.
"""

import json
import sys
import time

try:
    import pyautogui
    import pyperclip
except ImportError:
    print("❌ PyAutoGUI not available")
    sys.exit(1)


def load_coordinates():
    """Load agent coordinates."""
    try:
        with open("config/coordinates.json") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load coordinates: {e}")
        return {}


def send_message_to_agent(agent_id: str, message: str, priority: str = "NORMAL"):
    """Send message to specific agent using PyAutoGUI."""
    coordinates = load_coordinates()
    agent_info = coordinates.get("agents", {}).get(agent_id)

    if not agent_info:
        print(f"❌ Agent {agent_id} coordinates not found")
        return False

    try:
        # Get coordinates
        chat_coords = agent_info.get("chat_input_coordinates", [0, 0])

        # Create formatted message
        formatted_message = f"""============================================================
[A2A] MESSAGE
============================================================
📤 FROM: Agent-4
📥 TO: {agent_id}
Priority: {priority}
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
------------------------------------------------------------"""

        # Send message
        pyautogui.click(chat_coords[0], chat_coords[1])
        time.sleep(0.5)
        pyperclip.copy(formatted_message)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(0.5)

        print(f"✅ Message sent to {agent_id}")
        return True

    except Exception as e:
        print(f"❌ Failed to send message to {agent_id}: {e}")
        return False


def main():
    """Main function."""
    if len(sys.argv) < 4:
        print("Usage: python send_message.py <agent_id> <message> <priority>")
        print("Example: python send_message.py Agent-5 'Fix Discord commands' HIGH")
        sys.exit(1)

    agent_id = sys.argv[1]
    message = sys.argv[2]
    priority = sys.argv[3] if len(sys.argv) > 3 else "NORMAL"

    print(f"📤 Sending message to {agent_id}...")
    success = send_message_to_agent(agent_id, message, priority)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Temporary Message Sender Core
=============================

Core logic for sending messages to agents using coordinates.
"""

import json
import logging
import time

import pyautogui
import pyperclip

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_message_to_agent_core(agent_id: str, message: str) -> bool:
    """Send message to specific agent using coordinates."""
    # Load coordinates
    with open("config/coordinates.json") as f:
        coords_data = json.load(f)

    if agent_id not in coords_data["agents"]:
        logger.error(f"Agent {agent_id} not found in coordinates")
        return False

    agent_coords = coords_data["agents"][agent_id]["chat_input_coordinates"]
    x, y = agent_coords[0], agent_coords[1]

    # Format A2A message
    formatted_message = f"""============================================================
[A2A] MESSAGE
============================================================
📤 FROM: Agent-6
📥 TO: {agent_id}
Priority: HIGH
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

    try:
        # Copy message to clipboard
        pyperclip.copy(formatted_message)

        # Click coordinates
        pyautogui.click(x, y)
        time.sleep(0.5)

        # Paste message
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.5)

        # Send message
        pyautogui.press("enter")

        logger.info(f"Message sent to {agent_id} at coordinates ({x}, {y})")
        return True

    except Exception as e:
        logger.error(f"Error sending message to {agent_id}: {e}")
        return False

#!/usr/bin/env python3
"""
Re-Onboard Agent-7 Specifically
==============================

Targeted onboarding for Agent-7 who may have been missed.

Usage:
    python re_onboard_agent7.py

Author: V2_SWARM_CAPTAIN
"""

import json
import sys
import time
from pathlib import Path


def load_agent_coordinates():
    """Load agent coordinates from SSOT file."""
    coord_file = Path("cursor_agent_coords.json")
    if not coord_file.exists():
        print(f"❌ Coordinate file not found: {coord_file}")
        return {}

    try:
        with open(coord_file, encoding="utf-8") as f:
            data = json.load(f)

        coordinates = {}
        for agent_id, info in data.get("agents", {}).items():
            if agent_id == "Agent-7":  # Only load Agent-7
                chat_coords = info.get("chat_input_coordinates", [0, 0])
                coordinates[agent_id] = {
                    "chat_coords": tuple(chat_coords),
                    "description": info.get("description", ""),
                }
        return coordinates
    except Exception as e:
        print(f"❌ Error loading coordinates: {e}")
        return {}


def send_pyautogui_message(coords, message):
    """Send message via direct PyAutoGUI."""
    try:
        import pyautogui
        import pyperclip

        x, y = coords
        print(f"📍 Moving to coordinates: ({x}, {y})")

        # Move to coordinates
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click()
        time.sleep(0.5)

        # Clear existing text
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.1)
        pyautogui.press("delete")
        time.sleep(0.1)

        # Copy message to clipboard
        pyperclip.copy(message)
        time.sleep(0.1)

        # Paste message
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.2)

        # Send message
        pyautogui.press("enter")
        time.sleep(0.5)

        return True

    except ImportError as e:
        print(f"❌ PyAutoGUI not available: {e}")
        print("Install with: pip install pyautogui pyperclip")
        return False
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False


def get_agent7_onboarding_message():
    """Generate personalized onboarding message for Agent-7."""

    message = """🐝 URGENT: SWARM DEBATE ONBOARDING - Agent-7
🎯 TOPIC: Architecture Consolidation (683 → ~250 files)

**Your Role: Web Development Specialist**

📋 XML DEBATE SYSTEM ACTIVATED - YOU WERE MISSED!

**Debate Options:**
1. Option 1: Aggressive Consolidation (683 → 50 files) - High Risk
2. Option 2: Balanced Consolidation (683 → 250 files) - Recommended
3. Option 3: Minimal Consolidation (683 → 400 files) - Safe
4. Option 4: No Consolidation - Focus on Tooling

**HOW TO PARTICIPATE:**

1. **Check Debate Status:**
   python debate_participation_tool.py --agent-id Agent-7 --status

2. **View All Options:**
   python debate_participation_tool.py --agent-id Agent-7 --list-options

3. **Read Current Arguments:**
   python debate_participation_tool.py --agent-id Agent-7 --list-arguments

4. **Add Your Argument:**
   python debate_participation_tool.py --agent-id Agent-7 --add-argument \\
       --title "Web Development Perspective" \\
       --content "From a web development standpoint..." \\
       --supports-option option_2 \\
       --confidence 8 \\
       --technical-feasibility 9 \\
       --business-value 7

**Your Web Development Expertise Focus:**
- Evaluate frontend/backend architecture impact
- Consider user experience implications
- Analyze technology stack effects
- Assess web interface consolidation risks
- Evaluate browser automation and integration impacts

**DEBATE DEADLINE: 2025-09-16**
**XML File: swarm_debate_consolidation.xml**

🐝 WE ARE SWARM - Your web development expertise is crucial for this decision!
🚀 Contribute your specialized perspective now!

**Ready to participate?**
python debate_participation_tool.py --agent-id Agent-7 --add-argument --title "Web Dev Analysis"

--
V2_SWARM_CAPTAIN (URGENT RE-ONBOARDING)"""

    return message


def main():
    """Re-onboard Agent-7 specifically."""

    print("🐝 V2 SWARM CAPTAIN - URGENT AGENT-7 RE-ONBOARDING")
    print("=" * 60)
    print("🎯 Re-onboarding Agent-7 to XML debate system...")
    print()

    # Load coordinates for Agent-7 only
    coordinates = load_agent_coordinates()
    if "Agent-7" not in coordinates:
        print("❌ Agent-7 coordinates not found!")
        return False

    agent_data = coordinates["Agent-7"]
    print(f"✅ Found Agent-7 coordinates: {agent_data['chat_coords']}")

    # Generate personalized message
    message = get_agent7_onboarding_message()
    print("📝 Generated personalized onboarding message")

    # Send message via PyAutoGUI
    print("\n🤖 Re-onboarding Agent-7 (Web Development Specialist)")
    success = send_pyautogui_message(agent_data["chat_coords"], message)

    if success:
        print("✅ Successfully re-onboarded Agent-7!")
        print("\n📊 VERIFICATION:")
        print("Run: python debate_participation_tool.py --agent-id Agent-7 --status")
        return True
    else:
        print("❌ Failed to re-onboard Agent-7")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

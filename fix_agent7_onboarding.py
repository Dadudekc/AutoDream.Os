#!/usr/bin/env python3
"""
Fix Agent-7 Onboarding - Correct Coordinates
============================================

Specifically re-onboard Agent-7 with corrected coordinates.

Usage:
    python fix_agent7_onboarding.py

Author: V2_SWARM_CAPTAIN
"""

import json
import sys
import time
from pathlib import Path


def get_agent_specialties():
    """Get agent specialties for personalized onboarding."""
    return {
        "Agent-7": "Web Development Specialist"
    }

def load_agent_coordinates():
    """Load agent coordinates from SSOT file."""
    coord_file = Path("cursor_agent_coords.json")
    if not coord_file.exists():
        print(f"❌ Coordinate file not found: {coord_file}")
        return {}

    try:
        with open(coord_file, encoding='utf-8') as f:
            data = json.load(f)

        coordinates = {}
        for agent_id, info in data.get("agents", {}).items():
            if agent_id == "Agent-7":  # Only load Agent-7
                chat_coords = info.get("chat_input_coordinates", [0, 0])
                coordinates[agent_id] = {
                    "chat_coords": tuple(chat_coords),
                    "description": info.get("description", "")
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
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('delete')
        time.sleep(0.1)

        # Copy message to clipboard
        pyperclip.copy(message)
        time.sleep(0.1)

        # Paste message
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)

        # Send message
        pyautogui.press('enter')
        time.sleep(0.5)

        return True

    except ImportError as e:
        print(f"❌ PyAutoGUI not available: {e}")
        print("Install with: pip install pyautogui pyperclip")
        return False
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

def get_agent_onboarding_message(agent_id, specialty):
    """Generate personalized onboarding message for Agent-7."""

    base_message = f"""🐝 URGENT: AGENT-7 RE-ONBOARDING - {agent_id}
🎯 TOPIC: Architecture Consolidation (683 → ~250 files)

**Your Role: {specialty}**

❗ ATTENTION: This is a CORRECTED onboarding message!

📋 XML DEBATE SYSTEM ACTIVATED!

**Debate Options:**
1. Option 1: Aggressive Consolidation (683 → 50 files) - High Risk
2. Option 2: Balanced Consolidation (683 → 250 files) - Recommended
3. Option 3: Minimal Consolidation (683 → 400 files) - Safe
4. Option 4: No Consolidation - Focus on Tooling

**HOW TO PARTICIPATE:**

1. **Check Debate Status:**
   python debate_participation_tool.py --agent-id {agent_id} --status

2. **View All Options:**
   python debate_participation_tool.py --agent-id {agent_id} --list-options

3. **Read Current Arguments:**
   python debate_participation_tool.py --agent-id {agent_id} --list-arguments

4. **Add Your Argument:**
   python debate_participation_tool.py --agent-id {agent_id} --add-argument \\
       --title "Web Development Perspective" \\
       --content "Your detailed analysis..." \\
       --supports-option option_2 \\
       --confidence 8 \\
       --technical-feasibility 9 \\
       --business-value 7

**Your Web Development Expertise Contribution:**
- Evaluate frontend/backend architecture impact
- Consider user experience implications
- Analyze technology stack effects
- Assess web interface consolidation opportunities
- Evaluate UI/UX component reusability

**DEBATE DEADLINE: 2025-09-16**
**XML File: swarm_debate_consolidation.xml**

🐝 WE ARE SWARM - Your web development expertise is crucial for this decision!
🚀 Contribute your specialized perspective now!

**Ready to participate?**
python debate_participation_tool.py --agent-id {agent_id} --add-argument --title "Web Dev Analysis"

--
V2_SWARM_CAPTAIN (CORRECTED COORDINATES)"""

    return base_message

def onboard_agent7():
    """Re-onboard Agent-7 with corrected coordinates."""

    print("🐝 V2 SWARM CAPTAIN - AGENT-7 RE-ONBOARDING")
    print("=" * 60)
    print("🔧 Correcting Agent-7 coordinates and re-onboarding...")
    print()

    # Load coordinates
    coordinates = load_agent_coordinates()
    if not coordinates:
        print("❌ No coordinates loaded. Cannot proceed with Agent-7 onboarding.")
        return False

    agent_id = "Agent-7"
    if agent_id not in coordinates:
        print("❌ Agent-7 coordinates not found in coordinate file")
        return False

    agent_data = coordinates[agent_id]
    specialty = get_agent_specialties().get(agent_id, "Specialist")

    print(f"🤖 Re-onboarding {agent_id} ({specialty})")
    print(f"📍 Coordinates: {agent_data['chat_coords']}")
    print(f"📝 Description: {agent_data['description']}")

    # Generate personalized message
    message = get_agent_onboarding_message(agent_id, specialty)

    # Add extra emphasis for Agent-7
    urgent_message = f"""🚨 URGENT CORRECTION FOR AGENT-7 🚨

{message}

⚠️  IMPORTANT: This message corrects any previous onboarding issues.
   Please confirm you received this corrected message!

📞 If you don't see this message, your coordinates may need manual adjustment.
   Current coordinates: {agent_data['chat_coords']}

🐝 SWARM COORDINATION TEAM"""

    print("📨 Sending urgent re-onboarding message to Agent-7...")

    # Send message via PyAutoGUI
    success = send_pyautogui_message(agent_data['chat_coords'], urgent_message)

    if success:
        print("✅ Successfully re-onboarded Agent-7 with corrected coordinates")
        print(f"📍 Used coordinates: {agent_data['chat_coords']}")

        # Verify the coordinates are reasonable
        x, y = agent_data['chat_coords']
        if x < -2000 or x > 2000 or y < 0 or y > 1500:
            print(f"⚠️  WARNING: Coordinates {agent_data['chat_coords']} are outside normal bounds!")
            print("   This might indicate incorrect coordinate configuration.")

        return True
    else:
        print("❌ Failed to re-onboard Agent-7")
        print("💡 Try manually checking the coordinates in cursor_agent_coords.json")
        return False

def main():
    """Main re-onboarding orchestration for Agent-7."""

    success = onboard_agent7()

    print("\n" + "=" * 60)
    if success:
        print("✅ AGENT-7 RE-ONBOARDING COMPLETE")
        print("🎯 Agent-7 should now have received the corrected onboarding message")
        print("📊 Monitor Agent-7's participation with:")
        print("   python debate_participation_tool.py --agent-id Agent-7 --status")
    else:
        print("❌ AGENT-7 RE-ONBOARDING FAILED")
        print("🔧 Manual coordinate verification may be needed")

    print("=" * 60)
    print("🐝 SWARM DEBATE SYSTEM")
    print("📁 XML file: swarm_debate_consolidation.xml")
    print("🛠️  Tool: debate_participation_tool.py")
    print("⏰ Deadline: 2025-09-16")

    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

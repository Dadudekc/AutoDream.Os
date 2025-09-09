#!/usr/bin/env python3
"""
Fix Agent Onboarding - Target Specific Agents
=============================================

Re-onboard specific agents that may have been missed or need refresh.

Usage:
    python fix_agent_onboarding.py --agents Agent-1 Agent-7

Author: V2_SWARM_CAPTAIN
"""

import sys
import os
import time
import json
from pathlib import Path

def load_agent_coordinates():
    """Load agent coordinates from SSOT file."""
    coord_file = Path("cursor_agent_coords.json")
    if not coord_file.exists():
        print(f"❌ Coordinate file not found: {coord_file}")
        return {}

    try:
        with open(coord_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        coordinates = {}
        for agent_id, info in data.get("agents", {}).items():
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

def get_agent_specialties():
    """Get agent specialties for personalized onboarding."""
    return {
        "Agent-1": "Integration & Core Systems Specialist",
        "Agent-2": "Architecture & Design Specialist",
        "Agent-3": "Infrastructure & DevOps Specialist",
        "Agent-4": "Quality Assurance Specialist (CAPTAIN)",
        "Agent-5": "Business Intelligence Specialist",
        "Agent-6": "Coordination & Communication Specialist",
        "Agent-7": "Web Development Specialist",
        "Agent-8": "Operations & Support Specialist"
    }

def get_agent_onboarding_message(agent_id, specialty):
    """Generate personalized onboarding message for each agent."""

    base_message = f"""🐝 SWARM DEBATE ONBOARDING - {agent_id} (REFRESH)
🎯 TOPIC: Architecture Consolidation (683 → ~250 files)

**Your Role: {specialty}**

📋 XML DEBATE SYSTEM REFRESH - You may have missed the initial onboarding!

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
       --title "Your Perspective" \\
       --content "Your detailed analysis..." \\
       --supports-option option_2 \\
       --confidence 8 \\
       --technical-feasibility 9 \\
       --business-value 7

**Your Expertise Contribution:**
"""

    # Add specialty-specific guidance
    if "Integration" in specialty:
        base_message += "- Analyze system dependencies and coupling\n- Evaluate consolidation impact on existing integrations\n- Assess vector database and service integration risks"
    elif "Architecture" in specialty:
        base_message += "- Assess design patterns and architectural principles\n- Evaluate long-term maintainability and scalability\n- Consider the impact on architectural consistency"
    elif "DevOps" in specialty:
        base_message += "- Analyze deployment and operational impact\n- Consider CI/CD pipeline effects\n- Evaluate monitoring and maintenance implications"
    elif "Quality Assurance" in specialty:
        base_message += "- Focus on testing strategy and coverage\n- Analyze regression risk and testing effort\n- Consider quality assurance implications"
    elif "Business Intelligence" in specialty:
        base_message += "- Analyze business value and ROI\n- Consider development velocity impact\n- Evaluate long-term maintenance costs"
    elif "Communication" in specialty:
        base_message += "- Assess communication and coordination impact\n- Analyze team collaboration effects\n- Consider documentation and knowledge sharing"
    elif "Web Development" in specialty:
        base_message += "- Evaluate frontend/backend architecture impact\n- Consider user experience implications\n- Analyze technology stack effects"
    elif "Operations" in specialty:
        base_message += "- Focus on operational stability and reliability\n- Analyze system performance implications\n- Consider support and maintenance burden"

    base_message += """

**DEBATE DEADLINE: 2025-09-16**
**XML File: swarm_debate_consolidation.xml**

🐝 WE ARE SWARM - Your expertise is crucial for this decision!
🚀 Contribute your specialized perspective now!

**Ready to participate?**
python debate_participation_tool.py --agent-id {agent_id} --add-argument --title "My Expert Analysis"

--
V2_SWARM_CAPTAIN (REFRESH ONBOARDING)"""

    return base_message

def onboard_specific_agent(agent_id, coordinates):
    """Onboard a specific agent using PyAutoGUI."""

    if agent_id not in coordinates:
        print(f"❌ Agent {agent_id} not found in coordinates")
        return False

    agent_data = coordinates[agent_id]
    specialty = get_agent_specialties().get(agent_id, "Specialist")

    print(f"\n🎯 REFRESH ONBOARDING: {agent_id} ({specialty})")
    print(f"📍 Coordinates: {agent_data['chat_coords']}")

    # Generate personalized message
    message = get_agent_onboarding_message(agent_id, specialty)

    # Send message via PyAutoGUI
    success = send_pyautogui_message(agent_data['chat_coords'], message)

    if success:
        print(f"✅ Successfully refreshed onboarding for {agent_id}")
        return True
    else:
        print(f"❌ Failed to refresh onboarding for {agent_id}")
        return False

def main():
    """Main function to fix specific agent onboarding."""

    print("🐝 V2 SWARM CAPTAIN - REFRESH AGENT ONBOARDING")
    print("=" * 60)
    print("🎯 Fixing onboarding for specific agents...")
    print()

    # Load coordinates
    coordinates = load_agent_coordinates()
    if not coordinates:
        print("❌ No coordinates loaded. Cannot proceed with onboarding.")
        return False

    print(f"✅ Loaded coordinates for {len(coordinates)} agents")

    # Target agents that may have been missed
    target_agents = ["Agent-1", "Agent-7"]  # Focus on the ones mentioned

    print(f"🎯 Targeting agents: {', '.join(target_agents)}")

    # Track results
    successful_onboardings = []
    failed_onboardings = []

    for agent_id in target_agents:
        print(f"\n🚀 Refreshing onboarding for {agent_id}...")

        # Add delay between messages
        if successful_onboardings:
            print("⏳ Waiting 2 seconds before next agent...")
            time.sleep(2)

        success = onboard_specific_agent(agent_id, coordinates)

        if success:
            successful_onboardings.append(agent_id)
        else:
            failed_onboardings.append(agent_id)

    # Final report
    print("\n" + "=" * 60)
    print("📊 REFRESH ONBOARDING COMPLETE")
    print("=" * 60)

    print(f"✅ Successful refreshes: {len(successful_onboardings)}")
    for agent in successful_onboardings:
        print(f"   • {agent}")

    if failed_onboardings:
        print(f"❌ Failed refreshes: {len(failed_onboardings)}")
        for agent in failed_onboardings:
            print(f"   • {agent}")

    print(f"\n📋 Total agents targeted: {len(target_agents)}")
    print(f"🎯 Debate system: ACTIVE")
    print(f"📁 XML file: swarm_debate_consolidation.xml")
    print(f"🛠️  Tool: debate_participation_tool.py")

    print("\n🐝 AGENTS NOW HAVE FRESH ONBOARDING MESSAGES!")
    print("🎯 They can participate immediately with refreshed instructions")

    return len(successful_onboardings) > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

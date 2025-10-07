#!/usr/bin/env python3
"""
Onboard Agents to XML Debate System
====================================

Uses PyAutoGUI to send onboarding messages to all 8 agents about the XML debate system.
Each agent receives personalized instructions for participating in the consolidation debate.

Usage:
    python onboard_agents_xml_debate.py

Author: V2_SWARM_CAPTAIN
"""

import sys
import time

# Import modules directly (no src prefix needed when running from project root)
try:
    from core.coordinate_loader import get_coordinate_loader
    from services.messaging_pyautogui import deliver_message_pyautogui
    from services.models.messaging_models import (
        RecipientType,
        SenderType,
        UnifiedMessage,
        UnifiedMessagePriority,
        UnifiedMessageTag,
        UnifiedMessageType,
    )

    print("✅ Successfully imported coordinate and messaging modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure src/ directory structure is correct")
    sys.exit(1)


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
        "Agent-8": "Operations & Support Specialist",
    }


def get_agent_onboarding_message(agent_id, specialty):
    """Generate personalized onboarding message for each agent."""

    base_message = f"""🐝 SWARM DEBATE ONBOARDING - {agent_id}
🎯 TOPIC: Architecture Consolidation (683 → ~250 files)

**Your Role: {specialty}**

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
V2_SWARM_CAPTAIN"""

    return base_message


def onboard_single_agent(agent_id, coordinate_loader):
    """Onboard a single agent using PyAutoGUI."""

    if not coordinate_loader.is_agent_active(agent_id):
        print(f"❌ Agent {agent_id} not found in coordinates")
        return False

    # Get coordinates for the agent
    try:
        agent_coords = coordinate_loader.get_chat_coordinates(agent_id)
        print(f"📍 Coordinates for {agent_id}: {agent_coords}")
    except ValueError as e:
        print(f"❌ Failed to get coordinates for {agent_id}: {e}")
        return False

    specialty = get_agent_specialties().get(agent_id, "Specialist")

    print(f"\n🤖 Onboarding {agent_id} ({specialty})")

    # Generate personalized message
    message_content = get_agent_onboarding_message(agent_id, specialty)

    # Create UnifiedMessage object
    unified_message = UnifiedMessage(
        content=message_content,
        recipient=agent_id,
        recipient_type=RecipientType.AGENT,
        sender="V2_SWARM_CAPTAIN",
        sender_type=SenderType.SYSTEM,
        message_type=UnifiedMessageType.ONBOARDING,
        priority=UnifiedMessagePriority.URGENT,
        tags=[UnifiedMessageTag.ONBOARDING, UnifiedMessageTag.CAPTAIN],
    )

    try:
        # Send message using PyAutoGUI
        success = deliver_message_pyautogui(unified_message, agent_coords)

        if success:
            print(f"✅ Successfully onboarded {agent_id}")
            return True
        else:
            print(f"❌ Failed to onboard {agent_id}")
            return False

    except Exception as e:
        print(f"❌ Error onboarding {agent_id}: {e}")
        return False


def main():
    """Main onboarding orchestration."""

    print("🐝 V2 SWARM CAPTAIN - XML DEBATE ONBOARDING")
    print("=" * 60)
    print("📋 Onboarding all 8 agents to XML debate system...")
    print()

    # Load coordinates
    try:
        coordinate_loader = get_coordinate_loader()
        print("✅ Loaded coordinate loader")
        print(f"📊 Available agents: {coordinate_loader.get_all_agents()}")
    except Exception as e:
        print(f"❌ Failed to load coordinate loader: {e}")
        return False

    # Get agent specialties
    specialties = get_agent_specialties()
    print(f"📊 Found {len(specialties)} agent specialties")

    # Track results
    successful_onboardings = []
    failed_onboardings = []

    # Onboard each agent (skip Agent-1 since they already contributed)
    agents_to_onboard = [
        "Agent-2",
        "Agent-3",
        "Agent-4",
        "Agent-5",
        "Agent-6",
        "Agent-7",
        "Agent-8",
    ]

    for agent_id in agents_to_onboard:
        print(f"\n🚀 Preparing to onboard {agent_id}...")

        # Add delay between messages to prevent overwhelming the system
        if successful_onboardings:  # Not the first agent
            print("⏳ Waiting 3 seconds before next onboarding...")
            time.sleep(3)

        success = onboard_single_agent(agent_id, coordinate_loader)

        if success:
            successful_onboardings.append(agent_id)
        else:
            failed_onboardings.append(agent_id)

    # Final report
    print("\n" + "=" * 60)
    print("📊 ONBOARDING COMPLETE")
    print("=" * 60)

    print(f"✅ Successful onboardings: {len(successful_onboardings)}")
    for agent in successful_onboardings:
        print(f"   • {agent}")

    if failed_onboardings:
        print(f"❌ Failed onboardings: {len(failed_onboardings)}")
        for agent in failed_onboardings:
            print(f"   • {agent}")

    print(f"\n📋 Total agents: {len(agents_to_onboard)}")
    print("🎯 Debate system: ACTIVE")
    print("📁 XML file: swarm_debate_consolidation.xml")
    print("🛠️  Tool: debate_participation_tool.py")
    print("⏰ Deadline: 2025-09-16")

    print("\n🐝 SWARM DEBATE SYSTEM READY!")
    print("🎯 Agents are now onboarded and can participate immediately")
    print(
        "📊 Monitor contributions with: python debate_participation_tool.py --agent-id Agent-X --status"
    )

    return len(successful_onboardings) > 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

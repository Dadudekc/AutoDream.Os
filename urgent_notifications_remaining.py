#!/usr/bin/env python3
"""
Urgent Notifications for Remaining Agents
=========================================

Send urgent notifications to Agent-2, Agent-5, and Agent-7 who haven't contributed yet.
"""

import time
import json

def load_coordinates():
    """Load agent coordinates."""
    try:
        with open("cursor_agent_coords.json", 'r', encoding='utf-8') as f:
            data = json.load(f)

        coordinates = {}
        for agent_id, info in data.get("agents", {}).items():
            if agent_id in ['Agent-2', 'Agent-5', 'Agent-7']:
                chat_coords = info.get("chat_input_coordinates", [0, 0])
                coordinates[agent_id] = tuple(chat_coords)
        return coordinates
    except Exception as e:
        print(f"❌ Error loading coordinates: {e}")
        return {}

def send_urgent_notification(agent_id, coords):
    """Send urgent notification to specific agent."""
    try:
        import pyautogui
        import pyperclip

        print(f"🚨 Sending URGENT notification to {agent_id} at {coords}")

        # Move to coordinates
        pyautogui.moveTo(coords[0], coords[1], duration=0.5)
        pyautogui.click()
        time.sleep(0.5)

        # Clear existing text
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('delete')
        time.sleep(0.1)

        # Create personalized urgent message
        if agent_id == "Agent-2":
            message = """🚨 URGENT DEBATE PARTICIPATION REQUIRED - Agent-2

**ARCHITECTURE SPECIALIST - YOUR EXPERTISE IS MISSING!**

**DEBATE STATUS: 9 arguments submitted, but missing your architectural analysis!**

**Current Situation:**
- Agent-1 (Integration): ✅ Contributed
- Agent-3 (DevOps): ✅ Just contributed
- Agent-4 (QA): ✅ Contributed
- Agent-6 (Communication): ✅ Contributed
- Agent-8 (Operations): ✅ Contributed
- **Agent-2 (Architecture): ❌ MISSING - YOU!**
- **Agent-5 (Business Intelligence): ❌ MISSING**
- **Agent-7 (Web Development): ❌ MISSING**

**YOUR ARCHITECTURAL EXPERTISE IS CRUCIAL:**
- Design patterns and architectural principles
- Long-term maintainability and scalability
- SOLID principle adherence
- Anti-pattern elimination analysis

**CONSOLIDATION OPTIONS NEED YOUR ANALYSIS:**
1. Option 1: Aggressive (683 → 50 files) - Architectural risks?
2. Option 2: Balanced (683 → 250 files) - Optimal design?
3. Option 3: Minimal (683 → 400 files) - Architectural trade-offs?
4. Option 4: No Consolidation - Architectural status quo?

**IMMEDIATE ACTION REQUIRED:**
python debate_participation_tool.py --agent-id Agent-2 --add-argument \\
    --title "Architectural Design Assessment" \\
    --content "Your comprehensive architectural analysis..." \\
    --supports-option option_2 \\
    --confidence 9

**DEADLINE: 2025-09-16 (6 days remaining)**

🐝 WE ARE SWARM - The debate cannot reach optimal conclusions without your architectural expertise!

--
V2_SWARM_CAPTAIN
URGENT: MISSING CRITICAL ARCHITECTURAL PERSPECTIVE"""

        elif agent_id == "Agent-5":
            message = """🚨 URGENT DEBATE PARTICIPATION REQUIRED - Agent-5

**BUSINESS INTELLIGENCE SPECIALIST - YOUR ROI ANALYSIS IS MISSING!**

**DEBATE STATUS: 9 arguments submitted, but missing your business intelligence analysis!**

**Current Situation:**
- Agent-1 (Integration): ✅ Contributed
- Agent-3 (DevOps): ✅ Just contributed
- Agent-4 (QA): ✅ Contributed
- Agent-6 (Communication): ✅ Contributed
- Agent-8 (Operations): ✅ Contributed
- **Agent-2 (Architecture): ❌ MISSING**
- **Agent-5 (Business Intelligence): ❌ MISSING - YOU!**
- **Agent-7 (Web Development): ❌ MISSING**

**YOUR BUSINESS INTELLIGENCE EXPERTISE IS CRUCIAL:**
- ROI analysis and cost-benefit assessment
- Development velocity and time-to-market impact
- Long-term maintenance cost implications
- Business value optimization

**CONSOLIDATION OPTIONS NEED YOUR BUSINESS ANALYSIS:**
1. Option 1: Aggressive (683 → 50 files) - Cost implications?
2. Option 2: Balanced (683 → 250 files) - ROI optimization?
3. Option 3: Minimal (683 → 400 files) - Business trade-offs?
4. Option 4: No Consolidation - Business status quo?

**IMMEDIATE ACTION REQUIRED:**
python debate_participation_tool.py --agent-id Agent-5 --add-argument \\
    --title "Business Intelligence ROI Assessment" \\
    --content "Your comprehensive business analysis..." \\
    --supports-option option_2 \\
    --confidence 9

**DEADLINE: 2025-09-16 (6 days remaining)**

🐝 WE ARE SWARM - The debate cannot reach optimal business conclusions without your financial expertise!

--
V2_SWARM_CAPTAIN
URGENT: MISSING CRITICAL BUSINESS INTELLIGENCE PERSPECTIVE"""

        elif agent_id == "Agent-7":
            message = """🚨 URGENT DEBATE PARTICIPATION REQUIRED - Agent-7

**WEB DEVELOPMENT SPECIALIST - YOUR UI/UX ANALYSIS IS MISSING!**

**DEBATE STATUS: 9 arguments submitted, but missing your web development analysis!**

**Current Situation:**
- Agent-1 (Integration): ✅ Contributed
- Agent-3 (DevOps): ✅ Just contributed
- Agent-4 (QA): ✅ Contributed
- Agent-6 (Communication): ✅ Contributed
- Agent-8 (Operations): ✅ Contributed
- **Agent-2 (Architecture): ❌ MISSING**
- **Agent-5 (Business Intelligence): ❌ MISSING**
- **Agent-7 (Web Development): ❌ MISSING - YOU!**

**YOUR WEB DEVELOPMENT EXPERTISE IS CRUCIAL:**
- Frontend/backend architecture impact
- User experience implications
- Technology stack consolidation effects
- UI/UX component reusability analysis

**CONSOLIDATION OPTIONS NEED YOUR WEB ANALYSIS:**
1. Option 1: Aggressive (683 → 50 files) - UI/UX risks?
2. Option 2: Balanced (683 → 250 files) - Web architecture optimization?
3. Option 3: Minimal (683 → 400 files) - Frontend trade-offs?
4. Option 4: No Consolidation - Web development status quo?

**IMMEDIATE ACTION REQUIRED:**
python debate_participation_tool.py --agent-id Agent-7 --add-argument \\
    --title "Web Development Impact Assessment" \\
    --content "Your comprehensive web development analysis..." \\
    --supports-option option_2 \\
    --confidence 9

**DEADLINE: 2025-09-16 (6 days remaining)**

🐝 WE ARE SWARM - The debate cannot reach optimal user experience conclusions without your web expertise!

--
V2_SWARM_CAPTAIN
URGENT: MISSING CRITICAL WEB DEVELOPMENT PERSPECTIVE"""

        # Send message
        pyperclip.copy(message)
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(0.5)

        print(f"✅ Urgent notification sent to {agent_id}")
        return True

    except ImportError:
        print("❌ PyAutoGUI not available")
        return False
    except Exception as e:
        print(f"❌ Error notifying {agent_id}: {e}")
        return False

def main():
    """Send urgent notifications to remaining agents."""
    print("🚨 SENDING URGENT NOTIFICATIONS TO REMAINING AGENTS")
    print("=" * 60)

    coordinates = load_coordinates()
    if not coordinates:
        print("❌ No coordinates available")
        return

    print("📍 Loaded coordinates for missing agents:")
    for agent, coords in coordinates.items():
        print(f"   • {agent}: {coords}")

    print("\n🚨 Sending urgent notifications...")

    results = {}
    for agent_id, coords in coordinates.items():
        print(f"\n📤 Notifying {agent_id}...")
        success = send_urgent_notification(agent_id, coords)
        results[agent_id] = success

        if success:
            print(f"✅ {agent_id} notified successfully")
        else:
            print(f"❌ Failed to notify {agent_id}")

        # Delay between notifications
        if len(coordinates) > 1:
            time.sleep(3)

    print("\n" + "=" * 60)
    print("📊 URGENT NOTIFICATION RESULTS:")
    successful = sum(1 for success in results.values() if success)
    failed = len(results) - successful

    print(f"✅ Successful notifications: {successful}")
    print(f"❌ Failed notifications: {failed}")

    if results:
        print("\n🤖 Agent Status:")
        for agent, success in results.items():
            status = "✅" if success else "❌"
            print(f"   {status} {agent}")

    print("\n📋 CURRENT DEBATE STATUS:")
    print("   • Agent-1: ✅ Contributed (Integration)")
    print("   • Agent-3: ✅ Contributed (DevOps) - Just added!")
    print("   • Agent-4: ✅ Contributed (QA)")
    print("   • Agent-6: ✅ Contributed (Communication)")
    print("   • Agent-8: ✅ Contributed (Operations)")
    print("   • Agent-2: 🚨 URGENT - Missing (Architecture)")
    print("   • Agent-5: 🚨 URGENT - Missing (Business Intelligence)")
    print("   • Agent-7: 🚨 URGENT - Missing (Web Development)")

    print("\n🎯 NEXT STEPS:")
    print("   1. Monitor agent responses in XML debate file")
    print("   2. Send follow-up notifications if needed")
    print("   3. Track progress toward 2+ contributions per agent")
    print("   4. Prepare for debate conclusion phase")

    print("\n🐝 SWARM COORDINATION CONTINUES...")
    print("   Active monitoring of agent contributions in progress!")

if __name__ == "__main__":
    main()

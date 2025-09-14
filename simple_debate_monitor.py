#!/usr/bin/env python3
"""
Simple Debate Monitor & Notifier
================================

Monitors debate participation and sends urgent notifications via PyAutoGUI.

Usage:
    python simple_debate_monitor.py --check
    python simple_debate_monitor.py --notify-pending

Author: V2_SWARM_CAPTAIN
"""

import os
import time
import json
from pathlib import Path

def load_coordinates():
    """Load agent coordinates."""
    coord_file = Path("cursor_agent_coords.json")
    if not coord_file.exists():
        print("❌ Coordinate file not found")
        return {}

    try:
        with open(coord_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        coordinates = {}
        for agent_id, info in data.get("agents", {}).items():
            chat_coords = info.get("chat_input_coordinates", [0, 0])
            coordinates[agent_id] = tuple(chat_coords)
        return coordinates
    except Exception as e:
        print(f"❌ Error loading coordinates: {e}")
        return {}

def analyze_debate():
    """Analyze current debate participation."""
    debate_file = "swarm_debate_consolidation.xml"

    if not os.path.exists(debate_file):
        return {"error": "Debate file not found"}

    try:
        with open(debate_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Count basic metrics
        agent_references = {}
        for i in range(1, 9):  # Agent-1 through Agent-8
            agent_id = f"Agent-{i}"
            count = content.count(agent_id)
            agent_references[agent_id] = count

        # Count arguments
        argument_count = content.count('<argument>')

        # Identify low participation agents
        low_participation = []
        for agent, count in agent_references.items():
            if count < 3:  # Less than 3 mentions (name + contributions)
                low_participation.append(agent)

        return {
            "total_arguments": argument_count,
            "agent_participation": agent_references,
            "low_participation_agents": low_participation,
            "high_participation_agents": [a for a, c in agent_references.items() if c >= 3]
        }

    except Exception as e:
        return {"error": f"Analysis failed: {e}"}

def send_notification(coords, message):
    """Send PyAutoGUI notification."""
    try:
        import pyautogui
        import pyperclip

        x, y = coords
        print(f"📍 Sending notification to coordinates: ({x}, {y})")

        # Move to coordinates
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click()
        time.sleep(0.5)

        # Clear existing text
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('delete')
        time.sleep(0.1)

        # Paste message
        pyperclip.copy(message)
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)

        # Send
        pyautogui.press('enter')
        time.sleep(0.5)

        return True

    except ImportError:
        print("❌ PyAutoGUI not available - install with: pip install pyautogui pyperclip")
        return False
    except Exception as e:
        print(f"❌ Notification failed: {e}")
        return False

def create_urgent_message(agent_id, analysis):
    """Create urgent notification message."""
    participation = analysis.get('agent_participation', {}).get(agent_id, 0)
    total_args = analysis.get('total_arguments', 0)

    message = f"""🚨 URGENT DEBATE PARTICIPATION REQUIRED - {agent_id}

**DEBATE STATUS: ACTIVE**
- Total arguments submitted: {total_args}
- Your current participation: {participation} references
- Deadline: 2025-09-16 (7 days remaining)

**YOUR EXPERTISE IS CRITICALLY NEEDED NOW!**

The swarm consolidation debate requires your specialized perspective to make the optimal architectural decision.

**CONSOLIDATION DECISIONS PENDING:**
1. Option 1: Aggressive (683 → 50 files) - High Technical Risk
2. Option 2: Balanced (683 → 250 files) - Recommended Approach
3. Option 3: Minimal (683 → 400 files) - Conservative Path
4. Option 4: No Consolidation - Tooling Focus

**IMMEDIATE ACTION REQUIRED:**

1. **Review Current Debate:**
   python debate_participation_tool.py --agent-id {agent_id} --list-arguments

2. **Submit Your Expert Analysis:**
   python debate_participation_tool.py --agent-id {agent_id} --add-argument \\
       --title "My Technical Assessment" \\
       --content "Detailed analysis of consolidation options..." \\
       --supports-option option_2 \\
       --confidence 8

**WHY YOUR CONTRIBUTION MATTERS:**
- Other agents have already contributed valuable insights
- Your specialized expertise is essential for optimal decision-making
- The swarm needs your perspective on technical feasibility and risks
- Early contributions help shape the final consolidation strategy

**DEADLINE: 2025-09-16**

🐝 WE ARE SWARM - Your expert analysis is needed NOW for optimal consolidation strategy!

--
V2_SWARM_CAPTAIN
URGENT PARTICIPATION REQUEST"""

    return message

def check_debate_status():
    """Check and display debate status."""
    print("🐝 DEBATE STATUS MONITOR")
    print("=" * 50)

    analysis = analyze_debate()

    if "error" in analysis:
        print(f"❌ {analysis['error']}")
        return

    print(f"💬 Total Arguments: {analysis['total_arguments']}")
    print(f"🤖 High Participation: {len(analysis['high_participation_agents'])}")
    print(f"⏳ Low Participation: {len(analysis['low_participation_agents'])}")

    print("
🤖 AGENT PARTICIPATION:"    for agent, count in analysis['agent_participation'].items():
        status = "✅" if count >= 3 else "⏳" if count >= 1 else "❌"
        print(f"   {status} {agent}: {count} references")

    low_part = analysis['low_participation_agents']
    if low_part:
        print("
🚨 AGENTS NEEDING URGENT NOTIFICATION:"        for agent in low_part:
            print(f"   • {agent}")

    print("
📅 Deadline: 2025-09-16"    print("🎯 Status: ACTIVE - Contributions Needed"

def notify_pending_agents():
    """Notify agents with low participation."""
    print("🚨 NOTIFICATION SYSTEM ACTIVATED")
    print("=" * 50)

    analysis = analyze_debate()
    if "error" in analysis:
        print(f"❌ {analysis['error']}")
        return

    coordinates = load_coordinates()
    if not coordinates:
        print("❌ No coordinates available")
        return

    pending_agents = analysis.get('low_participation_agents', [])
    print(f"📊 Notifying {len(pending_agents)} agents...")

    results = {}

    for agent_id in pending_agents:
        if agent_id not in coordinates:
            print(f"❌ No coordinates for {agent_id}")
            results[agent_id] = False
            continue

        print(f"\n🚨 Notifying {agent_id}...")

        # Create personalized message
        message = create_urgent_message(agent_id, analysis)

        # Send notification
        coords = coordinates[agent_id]
        success = send_notification(coords, message)

        results[agent_id] = success

        if success:
            print(f"✅ Successfully notified {agent_id}")
        else:
            print(f"❌ Failed to notify {agent_id}")

        # Delay between notifications
        if len(pending_agents) > 1:
            time.sleep(3)

    # Summary
    print("
📊 NOTIFICATION RESULTS:"    successful = sum(1 for success in results.values() if success)
    failed = len(results) - successful

    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")

    if results:
        print("
🤖 Agent Results:"        for agent, success in results.items():
            status = "✅" if success else "❌"
            print(f"   {status} {agent}")

def main():
    """Main interface."""
    import sys

    if len(sys.argv) < 2:
        print("🐝 Simple Debate Monitor")
        print("Usage:")
        print("  python simple_debate_monitor.py --check")
        print("  python simple_debate_monitor.py --notify-pending")
        return

    if sys.argv[1] == "--check":
        check_debate_status()
    elif sys.argv[1] == "--notify-pending":
        notify_pending_agents()
    else:
        print("❌ Unknown command. Use --check or --notify-pending")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Debate Notification System
==========================

Active notification system that monitors debate status and alerts agents
when their contributions are needed via PyAutoGUI messages.

Usage:
    python debate_notification_system.py --check-status
    python debate_notification_system.py --notify-agent Agent-7
    python debate_notification_system.py --notify-all-pending

Author: V2_SWARM_CAPTAIN
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

# Import coordinate loader directly (no src prefix needed when running from project root)
try:
    from core.coordinate_loader import get_coordinate_loader
    print("✅ Successfully imported coordinate loader")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class DebateNotificationSystem:
    """Active notification system for debate participation."""

    def __init__(self, debate_file: str = "swarm_debate_consolidation.xml"):
        self.debate_file = debate_file
        self.coordinate_loader = get_coordinate_loader()
        self.notification_log = []

    def load_agent_coordinates(self) -> Dict[str, tuple]:
        """Load agent coordinates from SSOT file."""
        coordinates = {}
        for agent_id in self.coordinate_loader.get_all_agents():
            if self.coordinate_loader.is_agent_active(agent_id):
                try:
                    coords = self.coordinate_loader.get_chat_coordinates(agent_id)
                    coordinates[agent_id] = coords
                except ValueError:
                    print(f"⚠️  No coordinates for {agent_id}")
        return coordinates

    def parse_debate_status(self) -> Dict[str, any]:
        """Parse debate status from XML file."""
        if not os.path.exists(self.debate_file):
            return {"error": "Debate file not found"}

        try:
            # Simple text-based parsing since XML parsing has issues
            with open(self.debate_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract basic information
            participants = []
            contributions = {}

            # Count participant entries
            lines = content.split('\n')
            in_participants = False
            for line in lines:
                if '<participants>' in line:
                    in_participants = True
                elif '</participants>' in line:
                    in_participants = False
                elif in_participants and '<participant>' in line:
                    # Look for agent_id in next few lines
                    continue
                elif in_participants and '<agent_id>' in line:
                    agent_id = line.strip().replace('<agent_id>', '').replace('</agent_id>', '').strip()
                    if agent_id.startswith('Agent-'):
                        participants.append(agent_id)
                elif in_participants and '<contribution_count>' in line:
                    count = line.strip().replace('<contribution_count>', '').replace('</contribution_count>', '').strip()
                    if participants and count.isdigit():
                        contributions[participants[-1]] = int(count)

            # Count arguments by agent
            argument_authors = []
            for line in lines:
                if '<author_agent>' in line:
                    author = line.strip().replace('<author_agent>', '').replace('</author_agent>', '').strip()
                    if author.startswith('Agent-'):
                        argument_authors.append(author)

            # Calculate participation stats
            total_participants = len(participants)
            active_participants = len([p for p in contributions.keys() if contributions[p] > 0])
            total_arguments = len(argument_authors)

            # Find agents with low participation
            pending_agents = []
            for agent in participants:
                contrib_count = contributions.get(agent, 0)
                if contrib_count < 2:  # Less than 2 contributions
                    pending_agents.append(agent)

            return {
                "total_participants": total_participants,
                "active_participants": active_participants,
                "total_arguments": total_arguments,
                "pending_agents": pending_agents,
                "contributions": contributions,
                "argument_authors": argument_authors
            }

        except Exception as e:
            return {"error": f"Failed to parse debate: {e}"}

    def send_pyautogui_notification(self, agent_id: str, message: str) -> bool:
        """Send notification via PyAutoGUI."""
        try:
            import pyautogui
            import pyperclip

            # Get agent coordinates
            try:
                coords = self.coordinate_loader.get_chat_coordinates(agent_id)
            except ValueError:
                print(f"❌ No coordinates for {agent_id}")
                return False

            x, y = coords
            print(f"📍 Notifying {agent_id} at coordinates: ({x}, {y})")

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

            self.notification_log.append({
                "agent": agent_id,
                "timestamp": time.time(),
                "message": message[:100] + "..." if len(message) > 100 else message
            })

            return True

        except ImportError as e:
            print(f"❌ PyAutoGUI not available: {e}")
            return False
        except Exception as e:
            print(f"❌ Error notifying {agent_id}: {e}")
            return False

    def create_urgent_notification(self, agent_id: str, status: Dict) -> str:
        """Create urgent notification message for agent."""

        agent_contributions = status.get('contributions', {}).get(agent_id, 0)
        total_arguments = status.get('total_arguments', 0)

        notification = f"""🚨 URGENT DEBATE NOTIFICATION - {agent_id}

**DEBATE STATUS UPDATE:**
- Total arguments submitted: {total_arguments}
- Your contributions: {agent_contributions}
- Debate deadline: 2025-09-16

**YOUR EXPERTISE IS NEEDED NOW!**

The swarm consolidation debate is active and your specialized perspective is critical for making the optimal architectural decision.

**CONSOLIDATION OPTIONS UNDER DEBATE:**
1. Option 1: Aggressive (683 → 50 files) - High Risk
2. Option 2: Balanced (683 → 250 files) - Recommended
3. Option 3: Minimal (683 → 400 files) - Safe
4. Option 4: No Consolidation - Focus on Tooling

**HOW TO CONTRIBUTE IMMEDIATELY:**

1. **Check Current Arguments:**
   python debate_participation_tool.py --agent-id {agent_id} --list-arguments

2. **Add Your Expert Analysis:**
   python debate_participation_tool.py --agent-id {agent_id} --add-argument \\
       --title "Your Expert Perspective" \\
       --content "Your detailed technical analysis..." \\
       --supports-option option_2 \\
       --confidence 8

**WHY YOUR INPUT MATTERS:**
The swarm is waiting for your specialized expertise to make the optimal consolidation decision. Your analysis of the architectural, technical, and operational implications will guide our path forward.

**DEADLINE: 2025-09-16**

🐝 WE ARE SWARM - Your contribution is essential for optimal decision-making!

--
V2_SWARM_CAPTAIN
URGENT NOTIFICATION SYSTEM"""

        return notification

    def notify_pending_agents(self) -> Dict[str, bool]:
        """Notify all agents with low participation."""
        print("🔍 Analyzing debate status...")

        status = self.parse_debate_status()
        if "error" in status:
            print(f"❌ Error: {status['error']}")
            return {}

        pending_agents = status.get('pending_agents', [])
        print(f"📊 Found {len(pending_agents)} agents needing notification")

        results = {}

        for agent_id in pending_agents:
            print(f"\n🚨 Notifying {agent_id}...")

            # Create personalized notification
            notification = self.create_urgent_notification(agent_id, status)

            # Send notification
            success = self.send_pyautogui_notification(agent_id, notification)

            results[agent_id] = success

            if success:
                print(f"✅ Successfully notified {agent_id}")
            else:
                print(f"❌ Failed to notify {agent_id}")

            # Brief delay between notifications
            if len(pending_agents) > 1:
                time.sleep(2)

        return results

    def check_debate_status(self) -> None:
        """Check and display current debate status."""
        print("🐝 DEBATE STATUS ANALYSIS")
        print("=" * 50)

        status = self.parse_debate_status()

        if "error" in status:
            print(f"❌ Error: {status['error']}")
            return

        print(f"📊 Total Participants: {status['total_participants']}")
        print(f"🎯 Active Participants: {status['active_participants']}")
        print(f"💬 Total Arguments: {status['total_arguments']}")
        print(f"⏳ Pending Agents: {len(status.get('pending_agents', []))}")

        print(f"\n🤖 PARTICIPATION BREAKDOWN:")
        for agent, count in status.get('contributions', {}).items():
            status_icon = "✅" if count >= 2 else "⏳" if count >= 1 else "❌"
            print(f"   {status_icon} {agent}: {count} contributions")

        pending = status.get('pending_agents', [])
        if pending:
            print(f"\n🚨 AGENTS NEEDING URGENT NOTIFICATION:")
            for agent in pending:
                print(f"   • {agent}")

        print(f"\n📅 Deadline: 2025-09-16")
        print(f"🎯 Debate Status: ACTIVE")

    def show_notification_log(self) -> None:
        """Show recent notification log."""
        if not self.notification_log:
            print("📝 No notifications sent yet")
            return

        print("📝 RECENT NOTIFICATIONS:")
        for notification in self.notification_log[-10:]:  # Last 10
            timestamp = time.strftime('%H:%M:%S', time.localtime(notification['timestamp']))
            print(f"   {timestamp} - {notification['agent']}: {notification['message']}")

def main():
    """Main notification system interface."""
    import argparse

    parser = argparse.ArgumentParser(description="Debate Notification System")
    parser.add_argument("--check-status", action="store_true", help="Check current debate status")
    parser.add_argument("--notify-agent", help="Notify specific agent")
    parser.add_argument("--notify-all-pending", action="store_true", help="Notify all agents with low participation")
    parser.add_argument("--show-log", action="store_true", help="Show notification log")

    args = parser.parse_args()

    system = DebateNotificationSystem()

    if args.check_status:
        system.check_debate_status()

    elif args.notify_agent:
        status = system.parse_debate_status()
        if "error" not in status:
            notification = system.create_urgent_notification(args.notify_agent, status)
            success = system.send_pyautogui_notification(args.notify_agent, notification)
            if success:
                print(f"✅ Successfully notified {args.notify_agent}")
            else:
                print(f"❌ Failed to notify {args.notify_agent}")

    elif args.notify_all_pending:
        results = system.notify_pending_agents()

        print("
📊 NOTIFICATION RESULTS:"        successful = sum(1 for success in results.values() if success)
        failed = len(results) - successful

        print(f"✅ Successful notifications: {successful}")
        print(f"❌ Failed notifications: {failed}")

        if results:
            print("
🤖 Agent Results:"            for agent, success in results.items():
                status = "✅" if success else "❌"
                print(f"   {status} {agent}")

    elif args.show_log:
        system.show_notification_log()

    else:
        print("🐝 Debate Notification System")
        print("=" * 40)
        print("Usage:")
        print("  python debate_notification_system.py --check-status")
        print("  python debate_notification_system.py --notify-agent Agent-7")
        print("  python debate_notification_system.py --notify-all-pending")
        print("  python debate_notification_system.py --show-log")

if __name__ == "__main__":
    main()

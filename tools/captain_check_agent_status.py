"""
Captain's Tool: Check All Agent Status
=======================================

Quickly check status.json for all 8 agents to see who needs tasks.

Usage: python tools/captain_check_agent_status.py

Author: Agent-4 (Captain)
Date: 2025-10-13
"""

import json
from pathlib import Path


def check_all_agent_status():
    """Check status.json for all agents."""

    agents = [
        "Agent-1",
        "Agent-2",
        "Agent-3",
        "Agent-4",
        "Agent-5",
        "Agent-6",
        "Agent-7",
        "Agent-8",
    ]

    print("\n" + "=" * 80)
    print("📊 AGENT STATUS OVERVIEW")
    print("=" * 80 + "\n")

    needs_tasks = []
    active = []

    for agent in agents:
        status_file = Path(f"agent_workspaces/{agent}/status.json")

        if status_file.exists():
            try:
                with open(status_file) as f:
                    status = json.load(f)

                current_task = status.get("current_task", "None")
                last_updated = status.get("last_updated", "Unknown")
                agent_status = status.get("status", "Unknown")

                # Determine if needs task
                if current_task == "None" or agent_status == "idle":
                    needs_tasks.append(agent)
                    marker = "⚠️  NEEDS TASK"
                else:
                    active.append(agent)
                    marker = "🟢 ACTIVE"

                print(f"{marker} {agent}")
                print(f"   Task: {current_task}")
                print(f"   Status: {agent_status}")
                print(f"   Updated: {last_updated}")
                print()

            except Exception as e:
                print(f"❌ {agent}: Error reading status - {e}\n")
        else:
            needs_tasks.append(agent)
            print(f"⚠️  {agent}: No status.json found (likely needs task)\n")

    print("=" * 80)
    print(f"SUMMARY: {len(active)} active, {len(needs_tasks)} need tasks")
    print("=" * 80)

    if needs_tasks:
        print(f"\n⚠️  AGENTS NEEDING TASKS: {', '.join(needs_tasks)}")

    return {"active": active, "needs_tasks": needs_tasks}


if __name__ == "__main__":
    check_all_agent_status()

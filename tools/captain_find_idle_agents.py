"""
Captain's Tool: Find Idle Agents
=================================

Finds agents that need new tasks (no GAS = idle!).
Prevents agents from sitting idle without prompts.

Usage: python tools/captain_find_idle_agents.py

Author: Agent-4 (Captain)
Date: 2025-10-13
"""

import json
from pathlib import Path


def find_idle_agents(hours_threshold: int = 1):
    """
    Find agents that are idle or haven't been updated recently.

    Idle = No GAS = Need prompts!
    """

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
    print("🔍 FINDING IDLE AGENTS (Agents without GAS!)")
    print("=" * 80 + "\n")

    idle_agents = []
    active_agents = []

    for agent in agents:
        status_file = Path(f"agent_workspaces/{agent}/status.json")

        if not status_file.exists():
            idle_agents.append({"agent": agent, "reason": "No status.json", "urgency": "HIGH"})
            print(f"⚠️  {agent}: NO STATUS FILE (likely idle!)")
            continue

        try:
            with open(status_file) as f:
                status = json.load(f)

            current_task = status.get("current_task", "")
            agent_status = status.get("status", "").lower()

            # Check if idle
            if not current_task or current_task == "None" or "idle" in agent_status:
                idle_agents.append(
                    {
                        "agent": agent,
                        "reason": f"Status: {agent_status}, Task: {current_task}",
                        "urgency": "HIGH",
                    }
                )
                print(f"⚠️  {agent}: IDLE (needs task assignment!)")
            else:
                active_agents.append(agent)
                print(f"🟢 {agent}: ACTIVE - {current_task}")

        except Exception as e:
            idle_agents.append({"agent": agent, "reason": f"Error: {e}", "urgency": "MEDIUM"})
            print(f"⚠️  {agent}: ERROR reading status")

    print("\n" + "=" * 80)
    print(f"SUMMARY: {len(active_agents)} active, {len(idle_agents)} need tasks")
    print("=" * 80 + "\n")

    if idle_agents:
        print("⛽ AGENTS NEED GAS (Prompts!):")
        for item in idle_agents:
            print(f"  - {item['agent']}: {item['reason']}")
        print("\n💡 ACTION: Send prompts + assign tasks to activate!")
    else:
        print("✅ ALL AGENTS ACTIVE - Full utilization!")

    return {"idle": idle_agents, "active": active_agents}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Find idle agents needing tasks")
    parser.add_argument(
        "--hours", type=int, default=1, help="Hours threshold for considering agent idle"
    )

    args = parser.parse_args()

    find_idle_agents(args.hours)

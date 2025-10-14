"""
Captain's Tool: Gas Check (Message Status)
===========================================

Checks when agents last received messages (GAS!).
Identifies agents running low on fuel.

Usage: python tools/captain_gas_check.py

Author: Agent-4 (Captain)
Date: 2025-10-13
"""

from datetime import datetime
from pathlib import Path


def check_agent_gas_levels():
    """
    Check when agents last received messages.

    Low gas = No recent messages = May need activation!
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
    print("⛽ AGENT GAS LEVELS CHECK (Last Message Times)")
    print("=" * 80 + "\n")

    low_gas = []
    good_gas = []

    for agent in agents:
        inbox_path = Path(f"agent_workspaces/{agent}/inbox")

        if not inbox_path.exists():
            low_gas.append(agent)
            print(f"⛽ {agent}: NO INBOX (Out of gas!)")
            continue

        # Find most recent message
        message_files = list(inbox_path.glob("*.md")) + list(inbox_path.glob("*.txt"))

        if not message_files:
            low_gas.append(agent)
            print(f"⛽ {agent}: EMPTY INBOX (Out of gas!)")
            continue

        # Get most recent
        most_recent = max(message_files, key=lambda p: p.stat().st_mtime)
        modified_time = datetime.fromtimestamp(most_recent.st_mtime)
        age_hours = (datetime.now() - modified_time).total_seconds() / 3600

        if age_hours > 2:
            low_gas.append(agent)
            marker = "⚠️ "
        else:
            good_gas.append(agent)
            marker = "✅"

        print(f"{marker} {agent}: Last message {age_hours:.1f}h ago")
        print(f"   File: {most_recent.name}")
        print()

    print("=" * 80)
    print(f"SUMMARY: {len(good_gas)} have gas, {len(low_gas)} running low")
    print("=" * 80 + "\n")

    if low_gas:
        print("⛽ AGENTS NEED GAS (Send prompts!):")
        for agent in low_gas:
            print(f"  - {agent}")
        print("\n💡 ACTION: Message these agents to activate them!")
    else:
        print("✅ ALL AGENTS HAVE RECENT GAS - Good prompting!")

    return {"low_gas": low_gas, "good_gas": good_gas}


if __name__ == "__main__":
    check_agent_gas_levels()

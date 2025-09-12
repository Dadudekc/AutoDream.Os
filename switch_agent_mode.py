#!/usr/bin/env python3
"""
🐝 SWARM AGENT MODE SWITCHER
===========================

Switch between different agent configurations:
- 4-agent mode: Only Agents 1-4 active (left monitor)
- 8-agent mode: All Agents 1-8 active (dual monitor)

Usage:
    python switch_agent_mode.py --mode 4    # Activate 4-agent mode
    python switch_agent_mode.py --mode 8    # Activate 8-agent mode
    python switch_agent_mode.py --status    # Show current mode
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


def switch_agent_mode(mode: int) -> None:
    """Switch agent configuration to specified mode."""
    coord_file = Path("cursor_agent_coords.json")

    if not coord_file.exists():
        print("❌ cursor_agent_coords.json not found!")
        return

    # Load current configuration
    data = json.loads(coord_file.read_text(encoding="utf-8"))

    if mode == 4:
        # 4-agent mode: Agents 1-4 active, 5-8 inactive
        print("🐝 Switching to 4-AGENT MODE")
        print("   • Agents 1-4: ACTIVE (Left Monitor)")
        print("   • Agents 5-8: INACTIVE (Right Monitor)")

        for i in range(1, 5):
            agent_id = f"Agent-{i}"
            if agent_id in data["agents"]:
                data["agents"][agent_id]["active"] = True

        for i in range(5, 9):
            agent_id = f"Agent-{i}"
            if agent_id in data["agents"]:
                data["agents"][agent_id]["active"] = False

    elif mode == 8:
        # 8-agent mode: All agents active
        print("🐝 Switching to 8-AGENT MODE")
        print("   • All Agents 1-8: ACTIVE (Dual Monitor)")

        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            if agent_id in data["agents"]:
                data["agents"][agent_id]["active"] = True

    else:
        print(f"❌ Invalid mode: {mode}. Use 4 or 8.")
        return

    # Update timestamp
    data["last_updated"] = datetime.now().isoformat()

    # Save configuration
    coord_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(f"\n✅ Agent mode switched to {mode}-agent configuration!")
    print("📋 Changes will take effect on next system restart or coordinate reload.")


def show_current_status() -> None:
    """Show current agent configuration status."""
    coord_file = Path("cursor_agent_coords.json")

    if not coord_file.exists():
        print("❌ cursor_agent_coords.json not found!")
        return

    data = json.loads(coord_file.read_text(encoding="utf-8"))

    print("🐝 CURRENT AGENT CONFIGURATION STATUS")
    print("=" * 50)

    active_count = 0
    active_agents = []
    inactive_agents = []

    for agent_id, info in data.get("agents", {}).items():
        if info.get("active", True):
            active_count += 1
            active_agents.append(agent_id)
        else:
            inactive_agents.append(agent_id)

    print(f"📊 Mode: {active_count}-AGENT CONFIGURATION")
    print(f"🤖 Active Agents ({len(active_agents)}): {', '.join(active_agents)}")
    if inactive_agents:
        print(f"⏸️  Inactive Agents ({len(inactive_agents)}): {', '.join(inactive_agents)}")
    else:
        print("✅ All agents active!")

    print(f"\n📅 Last Updated: {data.get('last_updated', 'Unknown')}")


def main():
    parser = argparse.ArgumentParser(description="Switch swarm agent modes")
    parser.add_argument("--mode", type=int, choices=[4, 8], help="Switch to 4-agent or 8-agent mode")
    parser.add_argument("--status", action="store_true", help="Show current agent configuration status")

    args = parser.parse_args()

    if args.status:
        show_current_status()
    elif args.mode:
        switch_agent_mode(args.mode)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

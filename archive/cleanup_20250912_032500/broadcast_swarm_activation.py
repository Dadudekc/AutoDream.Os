#!/usr/bin/env python3
"""
🐝 SWARM ACTIVATION BROADCAST SCRIPT
====================================

Broadcasts the comprehensive swarm activation message to all agents.
Captain Agent-4 - Supreme Command Authority
"""

import os
from pathlib import Path
from datetime import datetime

def main():
    # Read the activation broadcast
    broadcast_file = Path("CAPTAIN_SWARM_ACTIVATION_BROADCAST.md")
    if not broadcast_file.exists():
        print("❌ Broadcast file not found!")
        return

    with open(broadcast_file, 'r', encoding='utf-8') as f:
        broadcast_content = f.read()

    # List of agents
    agents = [
        "Agent-1", "Agent-2", "Agent-3", "Agent-4",
        "Agent-5", "Agent-6", "Agent-7", "Agent-8"
    ]

    print("🚨 CAPTAIN AGENT-4 SWARM ACTIVATION BROADCAST")
    print("=" * 60)
    print("🐝 Broadcasting comprehensive testing and documentation mission")
    print("=" * 60)

    successful = 0
    for i, agent in enumerate(agents, 1):
        try:
            print(f"📤 [{i}/{len(agents)}] Broadcasting to {agent}...")

            # Create inbox directory
            inbox_dir = Path(f"agent_workspaces/{agent}/inbox")
            inbox_dir.mkdir(parents=True, exist_ok=True)

            # Create message file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            message_file = inbox_dir / f"CAPTAIN_SWARM_ACTIVATION_{timestamp}.md"

            with open(message_file, "w", encoding="utf-8") as f:
                f.write(broadcast_content)

            print(f"   ✅ Activation broadcast delivered to {agent}")
            successful += 1

        except Exception as e:
            print(f"   ❌ Failed to deliver to {agent}: {e}")

    print("\n📊 ACTIVATION BROADCAST SUMMARY:")
    print(f"   ✅ Successful deliveries: {successful}")
    print(f"   ❌ Failed deliveries: {len(agents) - successful}")
    print(f"   📈 Success rate: {(successful / len(agents)) * 100:.1f}%")
    if successful == len(agents):
        print("\n🎉 SWARM ACTIVATION BROADCAST COMPLETE!")
        print("   ✅ All agents notified of new command structure")
        print("   📢 Comprehensive testing mission activated")
        print("   🏆 Swarm excellence journey begins!")
    else:
        print("\n⚠️  ACTIVATION BROADCAST PARTIALLY COMPLETE")
        print(f"   ✅ {successful} agents notified successfully")
        print(f"   ❌ {len(agents) - successful} delivery failures")

if __name__ == "__main__":
    main()

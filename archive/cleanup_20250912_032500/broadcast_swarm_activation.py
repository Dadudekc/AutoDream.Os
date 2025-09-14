#!/usr/bin/env python3
"""
🐝 SWARM ACTIVATION BROADCAST SCRIPT
====================================

Broadcasts the comprehensive swarm activation message to all agents.
Captain Agent-4 - Supreme Command Authority
"""

import os
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # Read the activation broadcast
    broadcast_file = Path("CAPTAIN_SWARM_ACTIVATION_BROADCAST.md")
    if not broadcast_file.exists():
        logger.error("❌ Broadcast file not found!")
        return

    with open(broadcast_file, 'r', encoding='utf-8') as f:
        broadcast_content = f.read()

    # List of agents
    agents = [
        "Agent-1", "Agent-2", "Agent-3", "Agent-4",
        "Agent-5", "Agent-6", "Agent-7", "Agent-8"
    ]

    logger.info("🚨 CAPTAIN AGENT-4 SWARM ACTIVATION BROADCAST")
    logger.info("=" * 60)
    logger.info("🐝 Broadcasting comprehensive testing and documentation mission")
    logger.info("=" * 60)

    successful = 0
    for i, agent in enumerate(agents, 1):
        try:
            logger.info(f"📤 [{i}/{len(agents)}] Broadcasting to {agent}...")

            # Create inbox directory
            inbox_dir = Path(f"agent_workspaces/{agent}/inbox")
            inbox_dir.mkdir(parents=True, exist_ok=True)

            # Create message file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            message_file = inbox_dir / f"CAPTAIN_SWARM_ACTIVATION_{timestamp}.md"

            with open(message_file, "w", encoding="utf-8") as f:
                f.write(broadcast_content)

            logger.info(f"   ✅ Activation broadcast delivered to {agent}")
            successful += 1

        except Exception as e:
            logger.error(f"   ❌ Failed to deliver to {agent}: {e}")

    logger.info("\n📊 ACTIVATION BROADCAST SUMMARY:")
    logger.info(f"   ✅ Successful deliveries: {successful}")
    logger.info(f"   ❌ Failed deliveries: {len(agents) - successful}")
    logger.info(f"   📈 Success rate: {(successful / len(agents)) * 100:.1f}%")
    if successful == len(agents):
        logger.info("\n🎉 SWARM ACTIVATION BROADCAST COMPLETE!")
        logger.info("   ✅ All agents notified of new command structure")
        logger.info("   📢 Comprehensive testing mission activated")
        logger.info("   🏆 Swarm excellence journey begins!")
    else:
        logger.warning("\n⚠️  ACTIVATION BROADCAST PARTIALLY COMPLETE")
        logger.info(f"   ✅ {successful} agents notified successfully")
        logger.error(f"   ❌ {len(agents) - successful} delivery failures")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Automated Agent Coordinator - V2 System
=======================================

Automatically sends the resume operations message to all 8 agents every 10 minutes.
This ensures continuous coordination and task management across the agent network.

Features:
- Automated 10-minute intervals
- Broadcast to all 8 agents
- Progress tracking
- Discord integration preparation
- Task assignment coordination
"""

import time
import schedule
import threading

from src.utils.stability_improvements import stability_manager, safe_import
from datetime import datetime
from pathlib import Path
from services.messaging import UnifiedMessagingService as V2MessageDeliveryService  # Backward compatibility alias


class AutomatedAgentCoordinator:
    """Automated coordinator for continuous agent communication"""

    def __init__(self):
        self.delivery_service = V2MessageDeliveryService()
        self.message_file = Path("agent_resume_operations.txt")
        self.running = False
        self.cycle_count = 0

    def load_resume_message(self) -> str:
        """Load the resume operations message from file"""
        if not self.message_file.exists():
            return "ERROR: agent_resume_operations.txt not found"

        try:
            return self.message_file.read_text(encoding="utf-8")
        except Exception as e:
            return f"ERROR: Failed to read message file: {e}"

    def broadcast_resume_message(self) -> dict:
        """Broadcast the resume operations message to all agents"""
        print(
            f"\n🔄 [CYCLE {self.cycle_count + 1}] Broadcasting Resume Operations Message"
        )
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        # Load message content
        message_content = self.load_resume_message()

        # Broadcast to all agents
        print("📢 Sending message to all 8 agents...")
        results = self.delivery_service.broadcast_message(
            "coordination", message_content
        )

        # Process results
        success_count = sum(1 for success in results.values() if success)
        total_agents = len(results)

        print(f"✅ Broadcast completed: {success_count}/{total_agents} agents")
        print(f"📊 Results: {results}")

        # Update cycle count
        self.cycle_count += 1

        # Prepare Discord update
        discord_message = self.prepare_discord_update(success_count, total_agents)
        print(f"📱 Discord Update: {discord_message}")

        return results

    def prepare_discord_update(self, success_count: int, total_agents: int) -> str:
        """Prepare Discord update message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        return f"[{timestamp}] 🔄 Agent Coordination Cycle {self.cycle_count}: {success_count}/{total_agents} agents updated. Resume operations message sent."

    def run_coordination_cycle(self):
        """Run a single coordination cycle"""
        try:
            self.broadcast_resume_message()
        except Exception as e:
            print(f"❌ Error in coordination cycle: {e}")

    def start_automated_coordination(self):
        """Start the automated coordination system"""
        print("🚀 Starting Automated Agent Coordinator")
        print("=" * 50)
        print("📋 Configuration:")
        print(f"   • Message File: {self.message_file}")
        print(f"   • Interval: 10 minutes")
        print(f"   • Target: All 8 agents")
        print(f"   • Message Type: Coordination")
        print("=" * 50)

        # Schedule the coordination task every 10 minutes
        schedule.every(10).minutes.do(self.run_coordination_cycle)

        # Run initial cycle immediately
        print("\n🎯 Running initial coordination cycle...")
        self.run_coordination_cycle()

        self.running = True
        print(
            f"\n✅ Automated coordination started at {datetime.now().strftime('%H:%M:%S')}"
        )
        print("🔄 Will run every 10 minutes. Press Ctrl+C to stop.")

        try:
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping automated coordination...")
            self.running = False
            print("✅ Automated coordination stopped.")

    def stop_coordination(self):
        """Stop the automated coordination"""
        self.running = False
        print("🛑 Stopping automated coordination...")


def main():
    """Main function to run the automated coordinator"""
    print("🤖 AUTOMATED AGENT COORDINATOR - V2 SYSTEM")
    print("=" * 50)

    # Create coordinator
    coordinator = AutomatedAgentCoordinator()

    # Check if message file exists
    if not coordinator.message_file.exists():
        print(f"❌ ERROR: {coordinator.message_file} not found!")
        print("Please ensure the resume operations message file exists.")
        return 1

    # Start automated coordination
    try:
        coordinator.start_automated_coordination()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())

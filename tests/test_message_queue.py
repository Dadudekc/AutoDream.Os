#!/usr/bin/env python3
"""
Test Script for V1-V2 Message Queue System
Demonstrates the system and sends a message to Agent-7
"""

import sys
import time

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from services.simple_message_queue import SimpleMessageQueueSystem, UnifiedMessagePriority


def main():
    print("🚀 Testing V1-V2 Message Queue System")
    print("=" * 50)

    # Create message queue system
    mq_system = SimpleMessageQueueSystem()

    try:
        # Start the system
        print("📡 Starting message queue system...")
        mq_system.start_system()
        time.sleep(1)

        # Show system status
        status = mq_system.get_queue_status()
        print(f"📊 System Status: {status}")

        # Show agent status
        agents = mq_system.get_all_agents_status()
        print(
            f"👥 Agents: {agents['total_agents']} registered, {agents['available_agents']} available"
        )

        # Send message to Agent-7
        print("\n📨 Sending message to Agent-7...")
        message_content = """
🎬 MULTIMEDIA & CONTENT SPECIALIST - MESSAGE QUEUE TEST

Hello Agent-7! This is a test message from the V1-V2 Message Queue System.

SYSTEM FEATURES:
✅ PyAutoGUI integration with V2 architecture
✅ High-priority flag system (Ctrl+Enter x2)
✅ Multi-agent communication
✅ Message queuing and persistence
✅ Real-time processing

STATUS: System operational and ready for production use.

Please respond with your current status and readiness for multimedia integration tasks.

- Multimedia & Content Specialist
        """.strip()

        message_id = mq_system.send_message("agent_7", message_content, "normal")
        print(f"✅ Message sent successfully! ID: {message_id}")

        # Wait for processing
        print("⏳ Waiting for message processing...")
        time.sleep(3)

        # Show updated status
        updated_status = mq_system.get_queue_status()
        print(f"📊 Updated Status: {updated_status}")

        # Test high priority message
        print("\n🚨 Testing high priority message...")
        high_priority_content = "🚨 HIGH PRIORITY: Agent-7, please acknowledge receipt of this message immediately!"
        high_priority_id = mq_system.send_high_priority_message(
            "agent_7", high_priority_content
        )
        print(f"🚨 High priority message sent! ID: {high_priority_id}")

        # Wait for processing
        time.sleep(2)

        # Show final status
        final_status = mq_system.get_queue_status()
        print(f"📊 Final Status: {final_status}")

        print("\n✅ Test completed successfully!")

    except Exception as e:
        print(f"❌ Error during test: {e}")

    finally:
        # Stop the system
        print("\n🛑 Stopping message queue system...")
        mq_system.stop_system()
        print("✅ System stopped successfully")


if __name__ == "__main__":
    main()

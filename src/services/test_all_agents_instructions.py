#!/usr/bin/env python3
"""
Test script to send instructions to ALL 8 agents on how to reply back
"""

from src.services import UnifiedMessagingService
import time

from src.utils.stability_improvements import stability_manager, safe_import


def test_all_agents_instructions():
    print("🚀 Testing message instructions to ALL 8 agents...")

    # Initialize system
    mq = UnifiedMessagingService()
    print("✅ System initialized")

    # Start the system
    mq.start_system()
    print("✅ System started")

    # Wait a moment for system to stabilize
    time.sleep(2)

    # Read system broadcast message from text file
    try:
        with open("system_broadcast_message.txt", "r", encoding="utf-8") as f:
            instructions = f.read().strip()
        print("✅ System broadcast message loaded from file")
    except FileNotFoundError:
        print("❌ system_broadcast_message.txt not found - using fallback message")
        instructions = (
            "[SYSTEM] Fallback message: Please check system_broadcast_message.txt file"
        )
    except Exception as e:
        print(f"❌ Error reading file: {e} - using fallback message")
        instructions = "[SYSTEM] Error reading message file - please check system_broadcast_message.txt"

    print(f"\n📨 Sending instructions to ALL 8 agents...")
    print(f"Instructions length: {len(instructions)} characters")

    # Send instructions to all agents
    message_ids = mq.send_message_to_all_agents(
        sender_agent="[SYSTEM]",
        content=instructions,
        priority="high",
        message_type="system_broadcast",
    )

    print(f"✅ Instructions sent to {len(message_ids)} agents")
    print(f"Message IDs: {message_ids}")

    # Wait for messages to be processed
    print("\n⏳ Waiting for messages to be processed...")
    time.sleep(5)

    # Check message history
    print(f"\n📊 Message History Status:")
    print(f"Total messages: {len(mq.message_history)}")

    # Show recent messages
    recent_messages = (
        mq.message_history[-8:] if len(mq.message_history) >= 8 else mq.message_history
    )
    for i, msg_wrapper in enumerate(recent_messages):
        msg = msg_wrapper.get("message", {})
        print(
            f"  {i+1}. {msg.get('sender_agent', 'unknown')} → {msg.get('target_agent', 'unknown')}: {msg.get('content', '')[:50]}..."
        )

    # Check queue status
    status = mq.get_queue_status()
    print(f"\n📈 Queue Status:")
    print(f"  Regular queue: {status['regular_queue_size']}")
    print(f"  High priority queue: {status['high_priority_queue_size']}")
    print(f"  Total processed: {status['total_messages_processed']}")
    print(f"  Agents registered: {status['agents_registered']}")

    # Check agent status
    agent_status = mq.get_all_agents_status()
    print(f"\n🤖 Agent Status:")
    print(f"  Total agents: {agent_status['total_agents']}")
    print(f"  Available agents: {agent_status['available_agents']}")

    for agent_id, info in agent_status["agents"].items():
        coords = info["coordinates"]
        print(f"    {agent_id}: {coords['x']}, {coords['y']} - {info['status']}")

    # Stop system
    print("\n🛑 Stopping system...")
    mq.stop_system()
    print("✅ System stopped")

    print("\n🎉 ALL AGENTS INSTRUCTIONS TEST COMPLETED!")
    print("📱 All 8 agents should now have received instructions on how to reply back!")
    print("🔍 Check your agent chat windows for the instructions message!")


if __name__ == "__main__":
    test_all_agents_instructions()

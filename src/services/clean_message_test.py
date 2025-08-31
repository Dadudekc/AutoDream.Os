#!/usr/bin/env python3
"""
Clean Message Delivery Test
===========================

Clean test to see exactly what's happening with message delivery to all agents.
"""

from src.services import UnifiedMessagingService
import time

from src.utils.stability_improvements import stability_manager, safe_import


def clean_message_test():
    print("🧹 CLEAN MESSAGE DELIVERY TEST")
    print("=" * 50)

    # Initialize system
    mq = UnifiedMessagingService()
    print(f"✅ System initialized with {len(mq.agent_registry)} agents")

    # Show agent registry
    print("\n🤖 AGENT REGISTRY:")
    for agent_id, info in mq.agent_registry.items():
        coords = info["coordinates"]
        print(f"  {agent_id}: x={coords['x']}, y={coords['y']}")

    # Start the system
    mq.start_system()
    print("\n✅ System started")

    # Wait for system to stabilize
    time.sleep(2)

    # Simple test message
    test_message = "[SYSTEM] CLEAN TEST - Please confirm receipt"

    print(f"\n📨 SENDING TEST MESSAGE TO ALL {len(mq.agent_registry)} AGENTS...")
    print(f"Message: {test_message}")

    # Send to all agents
    message_ids = mq.send_message_to_all_agents(
        sender_agent="[SYSTEM]", content=test_message, priority="high"
    )

    print(f"\n✅ Messages queued: {len(message_ids)} message IDs generated")

    # Wait for processing
    print("\n⏳ Waiting for message processing...")
    time.sleep(8)  # Give more time for processing

    # Check delivery status
    print(f"\n📊 DELIVERY STATUS:")
    print(f"Total messages in history: {len(mq.message_history)}")

    # Show recent messages with clear status
    recent_messages = (
        mq.message_history[-len(message_ids) :] if len(mq.agent_registry) > 0 else []
    )

    print(f"\n📋 RECENT MESSAGE STATUS:")
    for i, msg_wrapper in enumerate(recent_messages):
        msg = msg_wrapper.get("message", {})
        status = msg_wrapper.get("status", "unknown")
        target = msg.get("target_agent", "unknown")
        print(f"  {i+1}. {target}: {status}")

    # Check which agents actually received messages
    print(f"\n🎯 AGENT RECEIPT SUMMARY:")
    for agent_id in mq.agent_registry.keys():
        # Check if this agent received a message
        received = any(
            msg.get("message", {}).get("target_agent") == agent_id
            for msg in recent_messages
        )
        status = "✅ RECEIVED" if received else "❌ NOT RECEIVED"
        print(f"  {agent_id}: {status}")

    # Stop system
    print("\n🛑 Stopping system...")
    mq.stop_system()
    print("✅ System stopped")

    print(f"\n🎯 TEST COMPLETED!")
    print(f"📱 Check which agents actually received the message in their chat windows!")


if __name__ == "__main__":
    clean_message_test()

#!/usr/bin/env python3
"""
Debug Message Test
=================

Simple test to verify message content is being sent correctly to agents.
"""

from src.services.messaging import UnifiedMessagingService
import time

from src.utils.stability_improvements import stability_manager, safe_import


def debug_message_test():
    print("🔍 Debug Message Test - Verifying message content delivery...")

    # Initialize system
    mq = UnifiedMessagingService()
    print("✅ System initialized")

    # Start the system
    mq.start_system()
    print("✅ System started")

    # Wait a moment for system to stabilize
    time.sleep(2)

    # Test message with clear content
    test_message = """[SYSTEM] DEBUG TEST MESSAGE

This is a test message to verify content delivery.

Message Details:
• Sender: [SYSTEM]
• Target: Agent-3 (for testing)
• Content: This debug message
• Priority: Normal

If you see this message in Agent-3's chat window, the system is working correctly!

End of Test Message"""

    print(f"\n📝 Test Message Content:")
    print("=" * 60)
    print(test_message)
    print("=" * 60)
    print(f"📊 Message length: {len(test_message)} characters")
    print(f"📊 Number of lines: {len(test_message.split(chr(10)))}")

    # Send test message to Agent-3 only (for testing)
    print(f"\n📤 Sending test message to Agent-3...")
    message_id = mq.send_message(
        sender_agent="[SYSTEM]",
        target_agent="agent_3",
        content=test_message,
        priority="normal",
        message_type="debug_test",
    )

    print(f"✅ Test message sent with ID: {message_id}")

    # Wait for message to be processed
    print("\n⏳ Waiting for message to be processed...")
    time.sleep(3)

    # Check message history
    print(f"\n📊 Message History Status:")
    print(f"Total messages: {len(mq.message_history)}")

    # Show the test message details
    if mq.message_history:
        last_message = mq.message_history[-1]
        msg = last_message.get("message", {})
        print(f"\n🔍 Last Message Details:")
        print(f"  ID: {msg.get('id', 'unknown')}")
        print(f"  Sender: {msg.get('sender_agent', 'unknown')}")
        print(f"  Target: {msg.get('target_agent', 'unknown')}")
        print(f"  Type: {msg.get('type', 'unknown')}")
        print(f"  Priority: {msg.get('priority', 'unknown')}")
        print(f"  Status: {last_message.get('status', 'unknown')}")
        print(f"  Content Preview: {msg.get('content', '')[:100]}...")

    # Check queue status
    status = mq.get_queue_status()
    print(f"\n📈 Queue Status:")
    print(f"  Regular queue: {status['regular_queue_size']}")
    print(f"  High priority queue: {status['high_priority_queue_size']}")
    print(f"  Total processed: {status['total_messages_processed']}")

    # Stop system
    print("\n🛑 Stopping system...")
    mq.stop_system()
    print("✅ System stopped")

    print("\n🎯 DEBUG TEST COMPLETED!")
    print("📱 Check Agent-3's chat window for the test message!")
    print("🔍 The message should contain the full debug content above!")


if __name__ == "__main__":
    debug_message_test()

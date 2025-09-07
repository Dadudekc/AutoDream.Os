#!/usr/bin/env python3
"""
Test script to verify Shift+Enter line break functionality
"""

from src.services import UnifiedMessagingService
import time

from src.utils.stability_improvements import stability_manager, safe_import

def test_line_breaks():
    print("🚀 Testing Shift+Enter line break functionality...")

    # Initialize system
    mq = UnifiedMessagingService()
    print("✅ System initialized")

    # Start the system
    mq.start_system()
    print("✅ System started")

    # Wait a moment for system to stabilize
    time.sleep(2)

    # Test message with line breaks
    test_message = """This is a test message with line breaks.

Line 2: Testing multi-line formatting
Line 3: Each line should be separated properly
Line 4: Using Shift+Enter for line breaks

Final line: Ready to test!""".strip()

    print(f"\n📨 Testing message with line breaks:")
    print(f"Message length: {len(test_message)} characters")
    print(f"Number of lines: {len(test_message.split('\\n'))}")
    print(f"Message content:")
    print("=" * 50)
    print(test_message)
    print("=" * 50)

    # Send test message to Agent-3 (using real coordinates)
    print(f"\n📤 Sending test message to Agent-3...")
    message_id = mq.send_message(
        sender_agent="SYSTEM_TESTER",
        target_agent="agent_3",
        content=test_message,
        priority="normal",
        message_type="test_line_breaks"
    )

    print(f"✅ Test message sent with ID: {message_id}")

    # Wait for message to be processed
    print("\n⏳ Waiting for message to be processed...")
    time.sleep(3)

    # Check message history
    print(f"\n📊 Message History Status:")
    print(f"Total messages: {len(mq.message_history)}")

    # Show the test message
    if mq.message_history:
        last_message = mq.message_history[-1]
        msg = last_message.get('message', {})
        print(f"Last message: {msg.get('sender_agent', 'unknown')} → {msg.get('target_agent', 'unknown')}")
        print(f"Content preview: {msg.get('content', '')[:100]}...")
        print(f"Status: {last_message.get('status', 'unknown')}")

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

    print("\n🎉 LINE BREAK TEST COMPLETED!")
    print("📱 Check Agent-3's chat window for the multi-line message!")
    print("🔍 The message should display with proper line breaks using Shift+Enter!")

if __name__ == "__main__":
    test_line_breaks()

#!/usr/bin/env python3
"""Test script to verify fixed message routing"""

from v1_v2_message_queue_system import V1V2MessageQueueSystem


def test_fixed_routing():
    print("Testing fixed message routing...")

    # Initialize system
    mq = V1V2MessageQueueSystem()
    print("System initialized")

    # Start system
    mq.start_system()
    print("System started")

    # Send test message
    msg_id = mq.send_message(
        "agent_5", "agent_3", "TEST: Fixed routing - this should go to Agent-3!"
    )
    print(f"Message ID: {msg_id}")

    # Wait for processing
    import time

    time.sleep(3)

    # Check message history
    print(f"Message history length: {len(mq.message_history)}")

    if mq.message_history:
        print("Last message wrapper:")
        last_wrapper = mq.message_history[-1]
        print(f"  Timestamp: {last_wrapper.get('timestamp')}")
        print(f"  Status: {last_wrapper.get('status')}")

        print("Message object keys:")
        message = last_wrapper.get("message", {})
        print(f"  {list(message.keys())}")

        print("Actual message content:")
        print(f"  Sender: {message.get('sender_agent')}")
        print(f"  Target: {message.get('target_agent')}")
        print(f"  Content: {message.get('content')}")

        # Verify routing is correct
        if (
            message.get("sender_agent") == "agent_5"
            and message.get("target_agent") == "agent_3"
            and "Fixed routing" in message.get("content", "")
        ):
            print("✅ ROUTING FIXED SUCCESSFULLY!")
        else:
            print("❌ Routing still broken!")
    else:
        print("No messages in history")

    # Stop system
    mq.stop_system()
    print("System stopped")


if __name__ == "__main__":
    test_fixed_routing()

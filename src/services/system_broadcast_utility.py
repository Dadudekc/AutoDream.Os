#!/usr/bin/env python3
"""
System Broadcast Utility
=======================

Utility for sending system broadcasts to all agents from text files.
Perfect for [SYSTEM] messages, announcements, and instructions.
"""

from v1_v2_message_queue_system import V1V2MessageQueueSystem
import time
import os

from src.utils.stability_improvements import stability_manager, safe_import


def send_system_broadcast(
    message_file: str,
    priority: str = "high",
    sender: str = "[SYSTEM]",
    agent_mode: str = "5",
):
    """
    Send a system broadcast message to all agents from a text file.

    Args:
        message_file: Path to the text file containing the message
        priority: Message priority ("normal", "high")
        sender: Sender agent name (default: "[SYSTEM]")
        agent_mode: Number of agents ("5" or "8") - default is "5" for reliability
    """
    print(f"🚀 System Broadcast Utility - Sending message from: {message_file}")
    print(f"🤖 Agent Mode: {agent_mode}-agent mode")

    # Initialize system with custom config for agent mode
    if agent_mode == "8":
        # 8-agent configuration
        config = {
            "max_queue_size": 1000,
            "high_priority_timeout": 5.0,
            "message_retry_attempts": 3,
            "retry_delay": 2.0,
            "enable_pyautogui": True,
            "enable_keyboard_monitoring": True,
            "ctrl_enter_double_timeout": 1.0,
            "message_persistence": True,
            "persistence_file": "message_history.json",
            "agent_coordinates": {
                "agent_1": {"x": -1399, "y": 486},
                "agent_2": {"x": -303, "y": 486},
                "agent_3": {"x": -1292, "y": 1005},
                "agent_4": {"x": -328, "y": 1008},
                "agent_5": {"x": 1587, "y": 940},
                "agent_6": {"x": 1587, "y": 486},
                "agent_7": {"x": -1399, "y": 1005},
                "agent_8": {"x": -303, "y": 1005},
            },
        }
        mq = V1V2MessageQueueSystem(config)
    else:
        # Default 5-agent configuration (more reliable)
        mq = V1V2MessageQueueSystem()

    print("✅ System initialized")

    # Start the system
    mq.start_system()
    print("✅ System started")

    # Wait a moment for system to stabilize
    time.sleep(2)

    # Read system broadcast message from text file
    try:
        with open(message_file, "r", encoding="utf-8") as f:
            message_content = f.read().strip()
        print("✅ System broadcast message loaded from file")
        print(f"📄 Message length: {len(message_content)} characters")
        print(f"📄 Number of lines: {len(message_content.split(chr(10)))}")

    except FileNotFoundError:
        print(f"❌ {message_file} not found!")
        print("💡 Create a text file with your system message and try again.")
        mq.stop_system()
        return False

    except Exception as e:
        print(f"❌ Error reading file: {e}")
        mq.stop_system()
        return False

    # Show message preview
    print(f"\n📋 Message Preview:")
    print("=" * 60)
    print(message_content[:200] + ("..." if len(message_content) > 200 else ""))
    print("=" * 60)

    # Show agent information
    print(f"\n🤖 Agent Registry:")
    for agent_id, info in mq.agent_registry.items():
        coords = info["coordinates"]
        print(f"  {agent_id}: x={coords['x']}, y={coords['y']}")

    # Confirm before sending
    print(f"\n📨 Ready to broadcast to ALL {len(mq.agent_registry)} agents...")
    print(f"📤 Sender: {sender}")
    print(f"🚨 Priority: {priority}")

    # Send system broadcast to all agents
    message_ids = mq.send_message_to_all_agents(
        sender_agent=sender,
        content=message_content,
        priority=priority,
        message_type="system_broadcast",
    )

    print(f"✅ System broadcast sent to {len(message_ids)} agents")
    print(f"🆔 Message IDs: {message_ids}")

    # Wait for messages to be processed
    print("\n⏳ Waiting for messages to be processed...")
    time.sleep(5)

    # Check delivery status
    print(f"\n📊 Delivery Status:")
    print(f"Total messages in history: {len(mq.message_history)}")

    # Show recent system messages
    system_messages = [
        msg
        for msg in mq.message_history[-len(message_ids) :]
        if msg.get("message", {}).get("sender_agent") == sender
    ]

    for i, msg_wrapper in enumerate(system_messages):
        msg = msg_wrapper.get("message", {})
        status = msg_wrapper.get("status", "unknown")
        print(f"  {i+1}. {msg.get('target_agent', 'unknown')}: {status}")

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

    print(f"\n🎉 SYSTEM BROADCAST COMPLETED!")
    print(
        f"📱 All {len(mq.agent_registry)} agents should now have received the [SYSTEM] message!"
    )
    print(f"🔍 Check your agent chat windows for the broadcast message!")

    return True


def create_sample_message_file(filename: str = "sample_system_message.txt"):
    """Create a sample system message file for testing"""
    sample_message = """[SYSTEM] IMPORTANT ANNOUNCEMENT

This is a sample system broadcast message.

Key Points:
• This message was sent from a text file
• All agents receive it simultaneously
• Easy to edit and update messages
• Perfect for system announcements

Instructions:
1. Edit this file to change the message
2. Run system_broadcast_utility.py to send it
3. All agents will receive the updated message

Status: READY FOR TESTING
Timestamp: {timestamp}

End of System Message""".format(
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
    )

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(sample_message)
        print(f"✅ Sample message file created: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error creating sample file: {e}")
        return False


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Use command line argument as message file
        message_file = sys.argv[1]
        priority = sys.argv[2] if len(sys.argv) > 2 else "high"
        sender = sys.argv[3] if len(sys.argv) > 3 else "[SYSTEM]"
        agent_mode = (
            sys.argv[4] if len(sys.argv) > 4 else "5"
        )  # Default to 5-agent mode

        send_system_broadcast(message_file, priority, sender, agent_mode)
    else:
        # Interactive mode
        print("🚀 System Broadcast Utility")
        print("=" * 40)
        print("Usage:")
        print(
            "  python system_broadcast_utility.py <message_file> [priority] [sender] [agent_mode]"
        )
        print(
            "  Example: python system_broadcast_utility.py message.txt high [SYSTEM] 5"
        )
        print("  Agent modes: 5 (default, reliable) or 8 (extended)")
        print("=" * 40)

        # Check if default message file exists
        default_file = "system_broadcast_message.txt"

        # Ask for agent mode
        print("\n🤖 Agent Mode Selection:")
        print("  5-agent mode: More reliable, tested coordinates")
        print("  8-agent mode: Extended coverage, may need coordinate adjustment")
        agent_mode = input("Select agent mode (5/8) [default: 5]: ").strip() or "5"

        if os.path.exists(default_file):
            print(f"📁 Found default message file: {default_file}")
            use_default = input("Use this file? (y/n): ").lower().strip()
            if use_default == "y":
                send_system_broadcast(default_file, "high", "[SYSTEM]", agent_mode)
            else:
                message_file = input("Enter message file path: ").strip()
                if message_file:
                    send_system_broadcast(message_file, "high", "[SYSTEM]", agent_mode)
                else:
                    print("❌ No file specified. Exiting.")
        else:
            print("📁 No default message file found.")
            create_sample = input("Create sample message file? (y/n): ").lower().strip()
            if create_sample == "y":
                if create_sample_message_file():
                    send_system_broadcast(
                        "sample_system_message.txt", "high", "[SYSTEM]", agent_mode
                    )
            else:
                message_file = input("Enter message file path: ").strip()
                if message_file:
                    send_system_broadcast(message_file, "high", "[SYSTEM]", agent_mode)
                else:
                    print("❌ No file specified. Exiting.")

from pathlib import Path
import sys

            from src.services import (
        from cdp_send_message import choose_targets, send_to_target
from src.utils.stability_improvements import stability_manager, safe_import
import time

#!/usr/bin/env python3
"""
CDP Messenger Demo
==================

Demonstrates how to use the CDP messenger system to send messages to Cursor agent chats.
"""



# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent))


def demo_basic_messaging():
    """Demonstrate basic CDP messaging"""
    print("🎯 Demo 1: Basic CDP Messaging")
    print("=" * 50)

    try:

        print("📤 Testing CDP connection...")
        targets = choose_targets()

        if not targets:
            print("❌ No CDP targets found")
            print("💡 Launch Cursor with CDP: .\\launch_cursor_with_cdp.ps1")
            return False

        print(f"✅ Found {len(targets)} CDP target(s)")

        # Test message
        test_message = (
            "🧪 CDP Demo: This is a test message from the CDP messenger system"
        )
        target = targets[0]

        print(f"📤 Sending test message to: {target.get('title', 'Unknown')}")
        result = send_to_target(
            target["webSocketDebuggerUrl"], test_message, "DemoAgent"
        )

        if result.get("ok"):
            print(f"✅ Message sent successfully!")
            print(f"   Method: {result.get('method', 'unknown')}")
            print(f"   Target: {result.get('target', 'unknown')}")
            return True
        else:
            print(f"❌ Message failed: {result.get('reason', 'unknown error')}")
            return False

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False


def demo_agent_targeting():
    """Demonstrate agent-specific targeting"""
    print("\n🎯 Demo 2: Agent-Specific Targeting")
    print("=" * 50)

    try:

        targets = choose_targets()
        if not targets:
            print("❌ No CDP targets available")
            return False

        # Test targeting Agent-3 specifically
        target = targets[0]
        test_message = (
            "🎯 Agent-3: This is a targeted message specifically for you via CDP"
        )

        print(
            f"📤 Sending targeted message to Agent-3 via: {target.get('title', 'Unknown')}"
        )

        result = send_to_target(target["webSocketDebuggerUrl"], test_message, "Agent-3")

        if result.get("ok"):
            print(f"✅ Targeted message sent successfully!")
            print(f"   Method: {result.get('method', 'unknown')}")
            print(f"   Target Agent: {result.get('target', 'unknown')}")
            return True
        else:
            print(f"❌ Targeted message failed: {result.get('reason', 'unknown error')}")
            return False

    except Exception as e:
        print(f"❌ Agent targeting demo failed: {e}")
        return False


def demo_broadcast_messaging():
    """Demonstrate broadcast messaging to all targets"""
    print("\n🎯 Demo 3: Broadcast Messaging")
    print("=" * 50)

    try:

        targets = choose_targets()
        if len(targets) < 2:
            print("⚠️  Need at least 2 targets for broadcast demo")
            print("💡 Open multiple agent chats in Cursor")
            return True

        broadcast_message = (
            "📢 BROADCAST: This is a demo broadcast message to all agents via CDP"
        )

        print(f"📤 Broadcasting to {len(targets)} targets...")

        success_count = 0
        for i, target in enumerate(targets):
            try:
                print(f"   📤 Target {i+1}: {target.get('title', 'Unknown')}")
                result = send_to_target(
                    target["webSocketDebuggerUrl"], broadcast_message, "Broadcast"
                )

                if result.get("ok"):
                    success_count += 1
                    print(f"   ✅ Success: {result.get('method', 'unknown')}")
                else:
                    print(f"   ❌ Failed: {result.get('reason', 'unknown error')}")

            except Exception as e:
                print(f"   ❌ Error: {e}")

        print(f"\n📊 Broadcast Results: {success_count}/{len(targets)} successful")
        return success_count > 0

    except Exception as e:
        print(f"❌ Broadcast demo failed: {e}")
        return False


def demo_priority_messaging():
    """Demonstrate priority-based messaging"""
    print("\n🎯 Demo 4: Priority-Based Messaging")
    print("=" * 50)

    try:

        targets = choose_targets()
        if not targets:
            print("❌ No CDP targets available")
            return False

        target = targets[0]

        # Test different priority messages
        priority_messages = [
            ("🔵 LOW", "This is a low priority demo message"),
            ("🟢 NORMAL", "This is a normal priority demo message"),
            ("🟡 HIGH", "This is a high priority demo message"),
            ("🟠 URGENT", "This is an urgent priority demo message"),
            ("🔴 CRITICAL", "This is a critical priority demo message"),
        ]

        success_count = 0
        for priority, message in priority_messages:
            try:
                print(f"📤 Sending {priority} priority message...")
                result = send_to_target(
                    target["webSocketDebuggerUrl"], message, "PriorityDemo"
                )

                if result.get("ok"):
                    success_count += 1
                    print(f"   ✅ {priority}: Success")
                else:
                    print(
                        f"   ❌ {priority}: Failed - {result.get('reason', 'unknown error')}"
                    )

                time.sleep(0.5)  # Small delay between messages

            except Exception as e:
                print(f"   ❌ {priority}: Error - {e}")

        print(
            f"\n📊 Priority Messaging Results: {success_count}/{len(priority_messages)} successful"
        )
        return success_count > 0

    except Exception as e:
        print(f"❌ Priority messaging demo failed: {e}")
        return False


def demo_integration_with_queue():
    """Demonstrate integration with V1-V2 Message Queue System"""
    print("\n🎯 Demo 5: Integration with V1-V2 Message Queue")
    print("=" * 50)

    try:
        # Try to import the message queue system
        try:
                UnifiedMessagingService,
                UnifiedMessagePriority,
            )

            print("✅ V1-V2 Message Queue System imported successfully")

            # Create a simple demo
            print("📤 Creating message queue system...")
            mq_system = UnifiedMessagingService(max_workers=1)

            print("📨 Queuing test message...")
            msg_id = mq_system.queue_message(
                "Agent-5",
                "Agent-3",
                "🧪 Queue Integration Demo: Message from V1-V2 Queue System",
                priority=UnifiedMessagePriority.HIGH,
            )

            print(f"✅ Message queued with ID: {msg_id}")

            # Wait for processing
            print("⏳ Waiting for message processing...")
            time.sleep(2)

            # Get status
            status = mq_system.get_queue_status()
            print(
                f"📊 Queue Status: {status['messages_queued']} queued, {status['messages_delivered']} delivered"
            )

            # Cleanup
            mq_system.shutdown()
            print("✅ Message queue system shutdown")

            return True

        except ImportError:
            print("⚠️  V1-V2 Message Queue System not available")
            print("💡 This demo requires the message queue system to be installed")
            return True  # Not a failure, just not available

    except Exception as e:
        print(f"❌ Queue integration demo failed: {e}")
        return False


def main():
    """Run all CDP messenger demos"""
    print("🚀 CDP Messenger Demo Suite")
    print("=" * 60)
    print("This demo shows how to use the CDP messenger system to send")
    print("headless messages to Cursor agent chats without moving the mouse.")
    print("=" * 60)

    print("\n📋 Prerequisites:")
    print("   1. Launch Cursor with CDP: .\\launch_cursor_with_cdp.ps1")
    print("   2. Open agent chats in Cursor")
    print("   3. Ensure websocket-client is installed: pip install websocket-client")
    print("=" * 60)

    demos = [
        ("Basic CDP Messaging", demo_basic_messaging),
        ("Agent-Specific Targeting", demo_agent_targeting),
        ("Broadcast Messaging", demo_broadcast_messaging),
        ("Priority-Based Messaging", demo_priority_messaging),
        ("V1-V2 Queue Integration", demo_integration_with_queue),
    ]

    passed = 0
    total = len(demos)

    for demo_name, demo_func in demos:
        print(f"\n🔍 Running: {demo_name}")
        if demo_func():
            passed += 1
            print(f"✅ {demo_name}: PASSED")
        else:
            print(f"❌ {demo_name}: FAILED")

        # Small delay between demos
        time.sleep(1)

    print(f"\n📊 Demo Results: {passed}/{total} demos passed")

    if passed == total:
        print("🎉 All demos completed successfully!")
        print("\n💡 You can now use the CDP messenger system:")
        print("   • Send messages to specific agents")
        print("   • Broadcast to all agents")
        print("   • Use different priority levels")
        print("   • Integrate with the V1-V2 Message Queue System")
    else:
        print(
            "⚠️  Some demos failed. This is expected if Cursor isn't running with CDP."
        )
        print("\n🔧 To get started:")
        print("   1. Run: .\\launch_cursor_with_cdp.ps1")
        print("   2. Open agent chats in Cursor")
        print("   3. Run the demos again")

    print("\n📚 Next Steps:")
    print("   1. Launch Cursor with CDP: .\\launch_cursor_with_cdp.ps1")
    print(
        "   2. Test messaging: python cdp_send_message.py 'Hello Agent-3!' --target 'Agent-3'"
    )
    print("   3. Run full demo: python demo_cdp_messenger.py")
    print("   4. Integrate with your automation systems")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test CDP Messenger
==================

Test script to verify the CDP messenger functionality works correctly.
"""

import sys
import time

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent))


def test_cdp_connection():
    """Test basic CDP connection"""
    print("🧪 Testing CDP connection...")

    try:
        from cdp_send_message import choose_targets, CDP_PORT

        targets = choose_targets()
        if targets:
            print(f"✅ CDP connection successful! Found {len(targets)} target(s)")
            for i, target in enumerate(targets):
                print(
                    f"   {i+1}. {target.get('title', 'Unknown')} ({target.get('type', 'unknown')})"
                )
            return True
        else:
            print("❌ No CDP targets found")
            print(
                f"💡 Make sure Cursor is running with --remote-debugging-port={CDP_PORT}"
            )
            return False

    except Exception as e:
        print(f"❌ CDP connection test failed: {e}")
        return False


def test_message_sending():
    """Test message sending functionality"""
    print("\n🧪 Testing message sending...")

    try:
        from cdp_send_message import choose_targets, send_to_target

        targets = choose_targets()
        if not targets:
            print("❌ No targets available for testing")
            return False

        # Use first target for testing
        target = targets[0]
        test_message = (
            "🧪 CDP Test Message - This is a test from the CDP messenger system"
        )

        print(f"📤 Sending test message to: {target.get('title', 'Unknown')}")

        result = send_to_target(
            target["webSocketDebuggerUrl"], test_message, "TestAgent"
        )

        if result.get("ok"):
            print(f"✅ Message sent successfully!")
            print(f"   Method: {result.get('method', 'unknown')}")
            print(f"   Target: {result.get('target', 'unknown')}")
            return True
        else:
            print(f"❌ Message sending failed: {result.get('reason', 'unknown error')}")
            if result.get("message"):
                print(f"   Details: {result['message']}")
            return False

    except Exception as e:
        print(f"❌ Message sending test failed: {e}")
        return False


def test_agent_targeting():
    """Test agent-specific targeting"""
    print("\n🧪 Testing agent targeting...")

    try:
        from cdp_send_message import choose_targets, send_to_target

        targets = choose_targets()
        if not targets:
            print("❌ No targets available for testing")
            return False

        # Test with Agent-3 specifically
        target = targets[0]
        test_message = "🎯 Agent-3: This is a targeted test message via CDP"

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
        print(f"❌ Agent targeting test failed: {e}")
        return False


def test_broadcast():
    """Test broadcast messaging"""
    print("\n🧪 Testing broadcast messaging...")

    try:
        from cdp_send_message import choose_targets, send_to_target

        targets = choose_targets()
        if len(targets) < 2:
            print("⚠️  Need at least 2 targets for broadcast testing")
            return True  # Not a failure, just not enough targets

        broadcast_message = (
            "📢 BROADCAST: This is a test broadcast message to all agents"
        )

        print(f"📤 Broadcasting to {len(targets)} targets...")

        success_count = 0
        for i, target in enumerate(targets):
            try:
                result = send_to_target(
                    target["webSocketDebuggerUrl"], broadcast_message, "Broadcast"
                )
                if result.get("ok"):
                    success_count += 1
                    print(f"   ✅ Target {i+1}: Success")
                else:
                    print(f"   ❌ Target {i+1}: {result.get('reason', 'failed')}")
            except Exception as e:
                print(f"   ❌ Target {i+1}: Error - {e}")

        print(f"📊 Broadcast results: {success_count}/{len(targets)} successful")
        return success_count > 0

    except Exception as e:
        print(f"❌ Broadcast test failed: {e}")
        return False


def main():
    """Run all CDP messenger tests"""
    print("🧪 CDP Messenger Test Suite")
    print("=" * 50)
    print("Testing headless messaging to Cursor agent chats via CDP")
    print("=" * 50)

    tests = [
        ("CDP Connection", test_cdp_connection),
        ("Message Sending", test_message_sending),
        ("Agent Targeting", test_agent_targeting),
        ("Broadcast Messaging", test_broadcast),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED")

        # Small delay between tests
        time.sleep(1)

    print(f"\n📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The CDP messenger is working correctly.")
        print("\n💡 You can now use it to send messages to Agent-3:")
        print(
            "   python cdp_send_message.py 'Agent-3: begin integration tests' --target 'Agent-3'"
        )
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure Cursor is running with --remote-debugging-port=9222")
        print("   2. Check that agent chats are open")
        print(
            "   3. Verify websocket-client is installed: pip install websocket-client"
        )

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

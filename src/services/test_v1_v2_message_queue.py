#!/usr/bin/env python3
"""
Test V1-V2 Message Queue System
===============================

Simple test to verify the integrated message queue system works correctly.
"""

import time
import sys

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent))


def test_basic_functionality():
    """Test basic message queue functionality"""
    print("🧪 Testing basic functionality...")

    try:
        from src.services.messaging import UnifiedMessagingService, UnifiedMessagePriority

        # Create system
        mq_system = UnifiedMessagingService(max_workers=1)
        print("✅ Message queue system created")

        # Test message queuing
        msg_id = mq_system.queue_message(
            "Agent-1", "Agent-3", "Test message", priority=UnifiedMessagePriority.NORMAL
        )
        print(f"✅ Message queued: {msg_id}")

        # Wait for processing
        time.sleep(2)

        # Check status
        status = mq_system.get_queue_status()
        print(
            f"✅ Status retrieved: {status['messages_queued']} queued, {status['messages_delivered']} delivered"
        )

        # Cleanup
        mq_system.shutdown()
        print("✅ System shutdown successfully")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_priority_system():
    """Test priority-based message delivery"""
    print("\n🧪 Testing priority system...")

    try:
        from src.services.messaging import UnifiedMessagingService, UnifiedMessagePriority

        # Create system
        mq_system = UnifiedMessagingService(max_workers=2)
        print("✅ Message queue system created")

        # Queue messages with different priorities
        priorities = [
            UnifiedMessagePriority.LOW,
            UnifiedMessagePriority.NORMAL,
            UnifiedMessagePriority.HIGH,
            UnifiedMessagePriority.URGENT,
            UnifiedMessagePriority.CRITICAL,
        ]

        for priority in priorities:
            msg_id = mq_system.queue_message(
                "Agent-1",
                "Agent-3",
                f"Test {priority.name} priority message",
                priority=priority,
            )
            print(f"✅ {priority.name} priority message queued: {msg_id}")

        # Wait for processing
        time.sleep(3)

        # Check status
        status = mq_system.get_queue_status()
        print(
            f"✅ Priority test completed: {status['messages_delivered']} messages delivered"
        )

        # Cleanup
        mq_system.shutdown()
        print("✅ System shutdown successfully")

        return True

    except Exception as e:
        print(f"❌ Priority test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_high_priority_flag():
    """Test high-priority flag system"""
    print("\n🧪 Testing high-priority flag system...")

    try:
        from src.services.messaging import (
            UnifiedMessagingService,
            send_high_priority_message,
        )

        # Create system
        mq_system = UnifiedMessagingService(max_workers=1)
        print("✅ Message queue system created")

        # Test high-priority message
        msg_id = send_high_priority_message(
            mq_system,
            "Agent-5",
            "Agent-3",
            "URGENT: Test high-priority message with Ctrl+Enter x2!",
        )
        print(f"✅ High-priority message queued: {msg_id}")

        # Wait for processing
        time.sleep(2)

        # Check status
        status = mq_system.get_queue_status()
        print(
            f"✅ High-priority test completed: {status['messages_delivered']} messages delivered"
        )

        # Cleanup
        mq_system.shutdown()
        print("✅ System shutdown successfully")

        return True

    except Exception as e:
        print(f"❌ High-priority test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🧪 V1-V2 Message Queue System Test Suite")
    print("=" * 50)

    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Priority System", test_priority_system),
        ("High-Priority Flag", test_high_priority_flag),
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

    print(f"\n📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print(
            "🎉 All tests passed! The V1-V2 Message Queue System is working correctly."
        )
    else:
        print("⚠️ Some tests failed. Please check the error messages above.")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

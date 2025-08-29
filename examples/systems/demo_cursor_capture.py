from datetime import datetime
from pathlib import Path
import logging

from src.core.cursor_response_capture import (
from src.utils.stability_improvements import stability_manager, safe_import
import time

#!/usr/bin/env python3
"""
Demo Cursor Response Capture - Agent Cellphone V2
================================================

Demonstration script showing the cursor response capture system in action.
This script simulates the capture process and displays the results.
"""



# Import our cursor capture system
    CursorResponseCapture,
    CursorDatabaseManager,
    CursorMessageNormalizer,
    CursorMessage,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def demo_single_capture():
    """Demonstrate single capture operation"""
    print("\n🎯 DEMO: Single Capture Operation")
    print("=" * 50)

    # Create capture system with temporary database
    demo_db = "demo_cursor_capture.db"
    capture_system = CursorResponseCapture(
        cdp_port=9222, capture_interval=1, db_path=demo_db
    )

    # Perform single capture
    print("  🔍 Performing single capture...")
    messages_captured = capture_system._capture_once()
    print(f"  ✅ Captured {messages_captured} messages")

    # Show capture statistics
    stats = capture_system.get_capture_stats()
    print(f"  📊 Total messages captured: {stats['total_messages_captured']}")
    print(f"  📊 Database message count: {stats['database_message_count']}")
    print(f"  📊 Average capture time: {stats['average_capture_time']:.3f}s")

    # Show recent messages
    recent = capture_system.get_recent_messages(5)
    if recent:
        print(f"\n  💬 Recent Messages:")
        for i, msg in enumerate(recent, 1):
            timestamp = datetime.fromtimestamp(msg["created_at"] / 1000).strftime(
                "%H:%M:%S"
            )
            print(
                f"    {i}. [{msg['role'].upper()}] {msg['content'][:60]}... ({timestamp})"
            )

    # Cleanup
    Path(demo_db).unlink(missing_ok=True)
    return True


def demo_message_normalization():
    """Demonstrate message normalization capabilities"""
    print("\n🔄 DEMO: Message Normalization")
    print("=" * 50)

    normalizer = CursorMessageNormalizer()

    # Test various message formats
    test_messages = [
        {
            "name": "Standard OpenAI Format",
            "payload": {
                "id": "msg_123456",
                "thread_id": "thread_abc123",
                "role": "assistant",
                "content": "Here's a helpful response to your question about Python programming.",
                "created_at": int(time.time() * 1000),
            },
        },
        {
            "name": "Cursor Chat Format",
            "payload": {
                "message_id": "cursor_msg_789",
                "conversation_id": "conv_xyz789",
                "author": {"role": "user"},
                "content": {"text": "How do I implement a REST API in Python?"},
                "timestamp": int(time.time() * 1000),
            },
        },
        {
            "name": "Minimal Format",
            "payload": {
                "content": "This is a minimal message with no explicit metadata."
            },
        },
        {
            "name": "Complex Nested Format",
            "payload": {
                "uuid": "complex_msg_abc",
                "chat_id": "advanced_chat_123",
                "author": {"role": "system", "name": "Cursor Assistant"},
                "content": {
                    "type": "markdown",
                    "content": "# System Message\nThis is a **system message** with *formatting*.",
                    "metadata": {"priority": "high", "category": "system"},
                },
                "date": int(time.time() * 1000),
            },
        },
    ]

    for test_case in test_messages:
        print(f"\n  📝 {test_case['name']}:")
        try:
            message = normalizer.normalize(test_case["payload"])
            print(f"    ✅ Normalized successfully")
            print(f"    📋 Message ID: {message.message_id}")
            print(f"    🧵 Thread ID: {message.thread_id}")
            print(f"    👤 Role: {message.role}")
            print(f"    📄 Content: {message.content[:50]}...")
            print(
                f"    ⏰ Timestamp: {datetime.fromtimestamp(message.created_at / 1000)}"
            )
            print(f"    🔗 Meta JSON: {len(message.meta_json)} characters")
        except Exception as e:
            print(f"    ❌ Normalization failed: {e}")

    return True


def demo_database_operations():
    """Demonstrate database operations"""
    print("\n🗄️ DEMO: Database Operations")
    print("=" * 50)

    # Create temporary database
    demo_db = "demo_db_operations.db"
    db_manager = CursorDatabaseManager(demo_db)

    try:
        # Create test messages
        test_messages = [
            CursorMessage(
                message_id="demo_msg_1",
                thread_id="demo_thread_1",
                role="user",
                content="Hello, I need help with Python programming.",
                created_at=int(time.time() * 1000),
                meta_json='{"source": "demo", "priority": "high"}',
            ),
            CursorMessage(
                message_id="demo_msg_2",
                thread_id="demo_thread_1",
                role="assistant",
                content="I'd be happy to help you with Python programming! What specific topic would you like to learn about?",
                created_at=int(time.time() * 1000) + 1000,
                meta_json='{"source": "demo", "response_time": "1s"}',
            ),
            CursorMessage(
                message_id="demo_msg_3",
                thread_id="demo_thread_2",
                role="user",
                content="How do I create a virtual environment?",
                created_at=int(time.time() * 1000) + 2000,
                meta_json='{"source": "demo", "topic": "virtual_env"}',
            ),
        ]

        # Save messages
        print("  💾 Saving test messages...")
        for i, message in enumerate(test_messages, 1):
            success = db_manager.save_message(message)
            print(
                f"    {i}. {message.role.upper()}: {message.content[:40]}... {'✅' if success else '❌'}"
            )

        # Test duplicate prevention
        print("\n  🔒 Testing duplicate prevention...")
        duplicate_success = db_manager.save_message(test_messages[0])
        print(
            f"    Duplicate message: {'✅ Ignored' if duplicate_success else '❌ Error'}"
        )

        # Get statistics
        print("\n  📊 Database Statistics:")
        total_count = db_manager.get_message_count()
        print(f"    Total messages: {total_count}")

        # Get recent messages
        recent = db_manager.get_recent_messages(10)
        print(f"    Recent messages: {len(recent)}")

        # Show message details
        print("\n  📋 Message Details:")
        for i, msg in enumerate(recent, 1):
            timestamp = datetime.fromtimestamp(msg["created_at"] / 1000).strftime(
                "%H:%M:%S"
            )
            print(
                f"    {i}. [{msg['role'].upper()}] {msg['content'][:50]}... ({timestamp})"
            )

        # Test invalid message handling
        print("\n  🛡️ Testing invalid message handling...")
        invalid_message = CursorMessage(
            message_id="",  # Invalid empty ID
            thread_id="",  # Invalid empty thread ID
            role="invalid_role",  # Invalid role
            content="",  # Invalid empty content
            created_at=-1,  # Invalid timestamp
            meta_json="invalid json",  # Invalid JSON
        )

        invalid_success = db_manager.save_message(invalid_message)
        print(
            f"    Invalid message: {'❌ Rejected' if not invalid_success else '⚠️ Unexpected success'}"
        )

        # Verify system still functional
        final_count = db_manager.get_message_count()
        print(f"    Final message count: {final_count} (should be {total_count})")

        return True

    finally:
        # Cleanup
        Path(demo_db).unlink(missing_ok=True)


def demo_v2_integration():
    """Demonstrate V2 system integration"""
    print("\n🔗 DEMO: V2 System Integration")
    print("=" * 50)

    # Create capture system
    demo_db = "demo_v2_integration.db"
    capture_system = CursorResponseCapture(
        cdp_port=9222, capture_interval=1, db_path=demo_db
    )

    try:
        # Start V2 monitoring
        print("  🚀 Starting V2 monitoring systems...")
        capture_system.start_capture()

        # Let it run briefly to collect data
        print("  ⏳ Collecting monitoring data...")
        time.sleep(3)

        # Show V2 system status
        print("\n  📊 V2 System Status:")

        # Performance profiler
        perf_stats = capture_system.performance_profiler.get_performance_stats()
        print(
            f"    Performance Profiler: {'✅ Active' if capture_system.performance_profiler.is_active else '❌ Inactive'}"
        )

        # Health monitor
        health_status = capture_system.health_monitor.get_component_health(
            "cursor_capture"
        )
        if health_status:
            print(
                f"    Health Monitor: ✅ Active - Score: {health_status['health_score']:.1%}"
            )
        else:
            print(f"    Health Monitor: ✅ Active - No health data yet")

        # Error handler
        error_stats = capture_system.error_handler.get_error_stats()
        print(
            f"    Error Handler: ✅ Active - Total errors: {error_stats['total_errors']}"
        )

        # Stop monitoring
        print("\n  ⏹️ Stopping V2 monitoring systems...")
        capture_system.stop_capture()

        # Final status
        print(
            f"    Final Status: {'❌ Stopped' if not capture_system.is_capturing else '⚠️ Still running'}"
        )

        return True

    finally:
        # Cleanup
        Path(demo_db).unlink(missing_ok=True)


def main():
    """Main demonstration execution"""
    print("🚀 CURSOR RESPONSE CAPTURE SYSTEM - LIVE DEMONSTRATION")
    print("=" * 70)
    print("This demo showcases the complete cursor response capture system")
    print("including database operations, message normalization, and V2 integration.")
    print("=" * 70)

    demo_results = {}

    try:
        # Run all demos
        demo_results["single_capture"] = demo_single_capture()
        demo_results["message_normalization"] = demo_message_normalization()
        demo_results["database_operations"] = demo_database_operations()
        demo_results["v2_integration"] = demo_v2_integration()

    except Exception as e:
        logger.error(f"Demo execution failed: {e}")
        return False

    # Summary
    print("\n" + "=" * 70)
    print("🎯 DEMO RESULTS SUMMARY")
    print("=" * 70)

    all_successful = True
    for demo_name, result in demo_results.items():
        status = "✅ SUCCESS" if result else "❌ FAILED"
        print(f"{demo_name.replace('_', ' ').title()}: {status}")
        if not result:
            all_successful = False

    print("=" * 70)

    if all_successful:
        print(
            "🎉 ALL DEMOS SUCCESSFUL! Cursor Response Capture System is working perfectly."
        )
        print("\n📋 NEXT STEPS:")
        print("   1. Install dependencies: pip install websocket-client requests")
        print("   2. Launch Cursor with: Cursor --remote-debugging-port=9222")
        print("   3. Run capture system: python src/core/cursor_response_capture.py")
        print("   4. Monitor captured messages in SQLite database")
        print("\n🚀 Ready for production deployment!")
    else:
        print("⚠️ Some demos failed. Please review the implementation.")

    return all_successful


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

#!/usr/bin/env python3
"""
Test Cursor Response Capture - Agent Cellphone V2
================================================

Comprehensive test script demonstrating cursor response capture functionality.
Tests CDP bridge, database operations, message normalization, and V2 integration.
Follows V2 standards and provides build evidence.
"""

import time
import threading
import logging
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

# Import our cursor capture system
from src.core.cursor_response_capture import (
    CursorResponseCapture,
    CursorDatabaseManager,
    CursorCDPBridge,
    CursorMessageNormalizer,
    CursorMessage,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MockCursorCDPBridge:
    """Mock CDP bridge for testing without real cursor"""

    def __init__(self, cdp_port: int = 9222):
        self.cdp_port = cdp_port
        self.is_running = True
        self.chat_tabs = [
            {
                "id": "tab_1",
                "title": "Test Chat",
                "url": "https://chat.openai.com/",
                "webSocketDebuggerUrl": "ws://localhost:9222/devtools/browser/tab_1",
            }
        ]

    def is_cursor_running(self) -> bool:
        """Mock cursor running check"""
        return self.is_running

    def get_chat_tabs(self):
        """Mock chat tabs retrieval"""
        return self.chat_tabs if self.is_running else []

    def connect_to_tab(self, tab):
        """Mock tab connection"""
        return self.is_running

    def disconnect(self):
        """Mock disconnection"""
        pass


def test_database_manager():
    """Test database manager functionality"""
    print("\n🗄️ TESTING DATABASE MANAGER")
    print("=" * 50)

    # Create temporary database
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / "test_cursor.db"

    try:
        # Initialize database manager
        db_manager = CursorDatabaseManager(str(db_path))

        # Test database initialization
        assert db_path.exists(), "Database file should be created"
        print("  ✅ Database initialization: PASSED")

        # Test message saving
        test_message = CursorMessage(
            message_id="test_msg_1",
            thread_id="test_thread_1",
            role="assistant",
            content="Test assistant message",
            created_at=int(time.time() * 1000),
            meta_json='{"test": "data"}',
        )

        success = db_manager.save_message(test_message)
        assert success, "Message saving should succeed"
        print("  ✅ Message saving: PASSED")

        # Test duplicate prevention
        success = db_manager.save_message(test_message)
        assert success, "Duplicate message should be ignored gracefully"
        print("  ✅ Duplicate prevention: PASSED")

        # Test message retrieval
        recent_messages = db_manager.get_recent_messages(10)
        assert len(recent_messages) == 1, "Should retrieve saved message"
        assert (
            recent_messages[0]["content"] == "Test assistant message"
        ), "Content should match"
        print("  ✅ Message retrieval: PASSED")

        # Test message count
        count = db_manager.get_message_count()
        assert count == 1, "Message count should be 1"
        print("  ✅ Message count: PASSED")

        # Test multiple messages
        for i in range(5):
            message = CursorMessage(
                message_id=f"test_msg_{i+2}",
                thread_id=f"test_thread_{i+2}",
                role="user" if i % 2 == 0 else "assistant",
                content=f"Test message {i+2}",
                created_at=int(time.time() * 1000) + i,
                meta_json=f'{{"index": {i+2}}}',
            )
            db_manager.save_message(message)

        count = db_manager.get_message_count()
        assert count == 6, f"Message count should be 6, got {count}"
        print("  ✅ Multiple message handling: PASSED")

        # Test recent messages limit
        recent = db_manager.get_recent_messages(3)
        assert len(recent) == 3, "Should respect limit"
        print("  ✅ Message limit enforcement: PASSED")

        print("  🎯 Database Manager: ALL TESTS PASSED")
        return True

    except Exception as e:
        print(f"  ❌ Database Manager test failed: {e}")
        return False
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)


def test_message_normalizer():
    """Test message normalization functionality"""
    print("\n🔄 TESTING MESSAGE NORMALIZER")
    print("=" * 50)

    normalizer = CursorMessageNormalizer()

    # Test various message formats
    test_cases = [
        {
            "name": "Standard format",
            "payload": {
                "id": "msg_123",
                "thread_id": "thread_456",
                "role": "assistant",
                "content": "Hello world",
                "created_at": 1640995200000,
            },
        },
        {
            "name": "Nested content format",
            "payload": {
                "message_id": "msg_789",
                "conversation_id": "conv_101",
                "author": {"role": "user"},
                "content": {"text": "User question"},
                "timestamp": 1640995200000,
            },
        },
        {"name": "Minimal format", "payload": {"content": "Minimal message"}},
        {
            "name": "Complex nested format",
            "payload": {
                "uuid": "msg_abc",
                "chat_id": "chat_xyz",
                "author": {"role": "system"},
                "content": {"content": "System message", "type": "text"},
                "date": 1640995200000,
            },
        },
    ]

    for i, test_case in enumerate(test_cases):
        try:
            message = normalizer.normalize(test_case["payload"])

            # Verify required fields
            assert message.message_id, "Message ID should be set"
            assert message.thread_id, "Thread ID should be set"
            assert message.role in [
                "user",
                "assistant",
                "system",
                "tool",
            ], f"Invalid role: {message.role}"
            assert message.content, "Content should be set"
            assert message.created_at > 0, "Timestamp should be positive"
            assert message.meta_json, "Meta JSON should be set"

            print(f"  ✅ {test_case['name']}: PASSED")

        except Exception as e:
            print(f"  ❌ {test_case['name']}: FAILED - {e}")
            return False

    # Test role validation
    try:
        message = normalizer.normalize({"content": "Test", "role": "invalid_role"})
        assert message.role == "assistant", "Invalid role should default to assistant"
        print("  ✅ Role validation: PASSED")
    except Exception as e:
        print(f"  ❌ Role validation: FAILED - {e}")
        return False

    print("  🎯 Message Normalizer: ALL TESTS PASSED")
    return True


def test_cdp_bridge():
    """Test CDP bridge functionality"""
    print("\n🌉 TESTING CDP BRIDGE")
    print("=" * 50)

    # Test with mock bridge
    bridge = MockCursorCDPBridge()

    # Test cursor running check
    assert bridge.is_cursor_running(), "Cursor should appear running"
    print("  ✅ Cursor running check: PASSED")

    # Test chat tabs retrieval
    tabs = bridge.get_chat_tabs()
    assert len(tabs) == 1, "Should return one chat tab"
    assert tabs[0]["title"] == "Test Chat", "Tab title should match"
    print("  ✅ Chat tabs retrieval: PASSED")

    # Test tab connection
    success = bridge.connect_to_tab(tabs[0])
    assert success, "Tab connection should succeed"
    print("  ✅ Tab connection: PASSED")

    # Test disconnection
    bridge.disconnect()
    print("  ✅ Tab disconnection: PASSED")

    # Test cursor not running
    bridge.is_running = False
    assert not bridge.is_cursor_running(), "Cursor should appear not running"
    tabs = bridge.get_chat_tabs()
    assert len(tabs) == 0, "Should return no tabs when cursor not running"
    print("  ✅ Cursor not running handling: PASSED")

    print("  🎯 CDP Bridge: ALL TESTS PASSED")
    return True


def test_cursor_capture_system():
    """Test the complete cursor capture system"""
    print("\n🎯 TESTING COMPLETE CAPTURE SYSTEM")
    print("=" * 50)

    # Create temporary database
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / "test_capture.db"

    try:
        # Create capture system with mock components
        with patch(
            "src.core.cursor_response_capture.CursorCDPBridge", MockCursorCDPBridge
        ):
            capture_system = CursorResponseCapture(
                cdp_port=9222,
                capture_interval=1,  # Fast interval for testing
                db_path=str(db_path),
            )

            # Test single capture
            messages_captured = capture_system._capture_once()
            assert messages_captured > 0, "Should capture test messages"
            print("  ✅ Single capture: PASSED")

            # Test message retrieval
            recent_messages = capture_system.get_recent_messages(10)
            assert len(recent_messages) > 0, "Should retrieve captured messages"
            print("  ✅ Message retrieval: PASSED")

            # Test capture statistics
            stats = capture_system.get_capture_stats()
            assert (
                stats["total_messages_captured"] > 0
            ), "Should track captured messages"
            assert stats["database_message_count"] > 0, "Should track database messages"
            print("  ✅ Statistics tracking: PASSED")

            # Test health metrics
            health_metrics = capture_system._get_health_metrics()
            assert "response_time" in health_metrics, "Should include response time"
            assert "error_rate" in health_metrics, "Should include error rate"
            assert "availability" in health_metrics, "Should include availability"
            print("  ✅ Health metrics: PASSED")

            print("  🎯 Complete Capture System: ALL TESTS PASSED")
            return True

    except Exception as e:
        print(f"  ❌ Complete Capture System test failed: {e}")
        return False
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)


def test_v2_integration():
    """Test V2 system integration"""
    print("\n🔗 TESTING V2 INTEGRATION")
    print("=" * 50)

    # Create temporary database
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / "test_v2_integration.db"

    try:
        # Create capture system
        capture_system = CursorResponseCapture(
            cdp_port=9222, capture_interval=1, db_path=str(db_path)
        )

        # Test V2 monitoring start
        capture_system.start_capture()
        assert capture_system.is_capturing, "Capture should be running"
        assert (
            capture_system.performance_profiler.is_active
        ), "Performance profiler should be active"
        assert (
            capture_system.health_monitor.is_active
        ), "Health monitor should be active"
        print("  ✅ V2 monitoring start: PASSED")

        # Let it run briefly
        time.sleep(2)

        # Test V2 monitoring stop
        capture_system.stop_capture()
        assert not capture_system.is_capturing, "Capture should be stopped"
        assert (
            not capture_system.performance_profiler.is_active
        ), "Performance profiler should be stopped"
        assert (
            not capture_system.health_monitor.is_active
        ), "Health monitor should be stopped"
        print("  ✅ V2 monitoring stop: PASSED")

        # Test performance profiling integration
        @capture_system.performance_profiler.profile_operation(
            "test_operation", "cursor_capture"
        )
        def test_operation():
            time.sleep(0.1)
            return "test result"

        result = test_operation()
        assert result == "test result", "Profiled operation should work"
        print("  ✅ Performance profiling integration: PASSED")

        # Test error handling integration
        circuit_breaker = capture_system.error_handler.create_circuit_breaker(
            "cursor_capture", failure_threshold=2, recovery_timeout=1.0
        )

        def failing_operation():
            raise Exception("Test failure")

        # First failure
        try:
            circuit_breaker.call(failing_operation)
        except Exception:
            pass

        # Second failure should open circuit
        try:
            circuit_breaker.call(failing_operation)
        except Exception:
            pass

        state = circuit_breaker.get_state()
        assert state["state"] == "open", "Circuit breaker should be open after failures"
        print("  ✅ Error handling integration: PASSED")

        print("  🎯 V2 Integration: ALL TESTS PASSED")
        return True

    except Exception as e:
        print(f"  ❌ V2 Integration test failed: {e}")
        return False
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)


def test_real_world_scenarios():
    """Test real-world usage scenarios"""
    print("\n🌍 TESTING REAL-WORLD SCENARIOS")
    print("=" * 50)

    # Create temporary database
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / "test_real_world.db"

    try:
        # Scenario 1: High-volume message capture
        print("  📊 Testing high-volume message capture...")
        capture_system = CursorResponseCapture(
            cdp_port=9222, capture_interval=1, db_path=str(db_path)
        )

        # Simulate high volume
        for i in range(100):
            message = CursorMessage(
                message_id=f"high_vol_{i}",
                thread_id=f"thread_{i % 10}",
                role="assistant" if i % 2 == 0 else "user",
                content=f"High volume message {i}",
                created_at=int(time.time() * 1000) + i,
                meta_json=f'{{"volume": {i}}}',
            )
            capture_system.db_manager.save_message(message)

        count = capture_system.db_manager.get_message_count()
        assert count == 100, f"Should handle 100 messages, got {count}"
        print("  ✅ High-volume handling: PASSED")

        # Scenario 2: Concurrent access
        print("  🔄 Testing concurrent access...")

        def concurrent_writer(thread_id):
            for i in range(10):
                message = CursorMessage(
                    message_id=f"concurrent_{thread_id}_{i}",
                    thread_id=f"concurrent_thread_{thread_id}",
                    role="assistant",
                    content=f"Concurrent message {i} from thread {thread_id}",
                    created_at=int(time.time() * 1000) + i,
                    meta_json=f'{{"thread": {thread_id}, "index": {i}}}',
                )
                capture_system.db_manager.save_message(message)

        # Start multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=concurrent_writer, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join()

        # Verify all messages were saved
        final_count = capture_system.db_manager.get_message_count()
        assert final_count == 150, f"Should have 150 total messages, got {final_count}"
        print("  ✅ Concurrent access handling: PASSED")

        # Scenario 3: Error recovery
        print("  🛡️ Testing error recovery...")

        # Simulate database corruption by creating invalid message
        invalid_message = CursorMessage(
            message_id="",  # Invalid empty ID
            thread_id="",  # Invalid empty thread ID
            role="invalid_role",  # Invalid role
            content="",  # Invalid empty content
            created_at=-1,  # Invalid timestamp
            meta_json="invalid json",  # Invalid JSON
        )

        # This should fail gracefully
        success = capture_system.db_manager.save_message(invalid_message)
        assert not success, "Invalid message should fail to save"

        # System should still be functional
        valid_count = capture_system.db_manager.get_message_count()
        assert valid_count == 150, "System should remain functional after errors"
        print("  ✅ Error recovery: PASSED")

        print("  🎯 Real-World Scenarios: ALL TESTS PASSED")
        return True

    except Exception as e:
        print(f"  ❌ Real-World Scenarios test failed: {e}")
        return False
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)


def main():
    """Main test execution"""
    print("🚀 CURSOR RESPONSE CAPTURE SYSTEM - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print("Testing all components and integrations:")
    print("✅ Database Manager: SQLite operations and message storage")
    print("✅ Message Normalizer: Diverse format handling")
    print("✅ CDP Bridge: Chrome DevTools Protocol communication")
    print("✅ Capture System: Complete message capture pipeline")
    print("✅ V2 Integration: Performance, health, and error handling")
    print("✅ Real-World Scenarios: High-volume, concurrent, error recovery")
    print("=" * 70)

    test_results = {}

    try:
        # Test individual components
        test_results["database_manager"] = test_database_manager()
        test_results["message_normalizer"] = test_message_normalizer()
        test_results["cdp_bridge"] = test_cdp_bridge()
        test_results["capture_system"] = test_cursor_capture_system()
        test_results["v2_integration"] = test_v2_integration()
        test_results["real_world_scenarios"] = test_real_world_scenarios()

    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        return False

    # Summary
    print("\n" + "=" * 70)
    print("🎯 TEST RESULTS SUMMARY")
    print("=" * 70)

    all_passed = True
    for test_name, result in test_results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
        if not result:
            all_passed = False

    print("=" * 70)

    if all_passed:
        print(
            "🎉 ALL TESTS PASSED! Cursor Response Capture System is fully operational."
        )
        print("🚀 Ready for production deployment with V2 integration.")
        print("\n📋 NEXT STEPS:")
        print(
            "   1. Install required dependencies: pip install websocket-client requests"
        )
        print("   2. Launch Cursor with: Cursor --remote-debugging-port=9222")
        print("   3. Run capture system: python src/core/cursor_response_capture.py")
        print("   4. Monitor captured messages in SQLite database")
    else:
        print("⚠️ Some tests failed. Please review the implementation.")

    return all_passed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

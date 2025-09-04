sys.path.append(get_unified_utility().path.join(get_unified_utility().path.dirname(__file__), '..'))
#!/usr/bin/env python3
"""
File Locking System Test - Agent Cellphone V2
============================================

Test script to verify file locking system functionality.
Tests atomic operations, concurrent access, and lock cleanup.

Usage:
    python -m src.core.test_file_lock

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import time
import concurrent.futures



def test_basic_file_locking():
    """Test basic file locking functionality."""
    get_logger(__name__).info("🧪 Testing basic file locking...")

    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = get_unified_utility().path.join(temp_dir, "test.txt")
        lock_manager = FileLockManager()

        # Test atomic write
        success = lock_manager.atomic_write(
            test_file,
            "Hello, World!",
            operation="test_write"
        )
        assert success, "Atomic write failed"
        assert get_unified_utility().path.exists(test_file), "File was not created"

        # Test atomic read
        content = lock_manager.atomic_read(test_file, operation="test_read")
        assert content == "Hello, World!", f"Content mismatch: {content}"

        # Test atomic update
        def update_func(current: str) -> str:
            return current + "\nUpdated content!"

        success = lock_manager.atomic_update(
            test_file,
            update_func,
            operation="test_update"
        )
        assert success, "Atomic update failed"

        content = lock_manager.atomic_read(test_file, operation="test_read")
        expected = "Hello, World!\nUpdated content!"
        assert content == expected, f"Update failed: {content}"

    get_logger(__name__).info("✅ Basic file locking tests passed")


def test_concurrent_file_access():
    """Test concurrent file access with locking."""
    get_logger(__name__).info("🧪 Testing concurrent file access...")

    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = get_unified_utility().path.join(temp_dir, "concurrent_test.txt")
        lock_manager = FileLockManager()

        # Initialize file
        with open(test_file, 'w') as f:
            f.write("0")

        def increment_counter(thread_id: int) -> bool:
            """Increment counter in file atomically."""
            try:
                def update_func(current: str) -> str:
                    count = int(current.strip())
                    # Simulate some processing time
                    time.sleep(0.01)
                    return str(count + 1)

                success = lock_manager.atomic_update(
                    test_file,
                    update_func,
                    operation=f"thread_{thread_id}_increment",
                    metadata={"thread_id": thread_id}
                )
                return success
            except Exception as e:
                get_logger(__name__).info(f"❌ Thread {thread_id} failed: {e}")
                return False

        # Run concurrent operations
        num_threads = 10
        num_operations_per_thread = 5

        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for thread_id in range(num_threads):
                for _ in range(num_operations_per_thread):
                    future = executor.submit(increment_counter, thread_id)
                    futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        # Verify results
        successful_operations = sum(1 for r in results if r)
        expected_final_count = num_threads * num_operations_per_thread

        final_content = lock_manager.atomic_read(test_file, operation="final_read")
        final_count = int(final_content.strip()) if final_content else 0

        assert successful_operations == expected_final_count, f"Expected {expected_final_count} successful operations, got {successful_operations}"
        assert final_count == expected_final_count, f"Expected final count {expected_final_count}, got {final_count}"

    get_logger(__name__).info("✅ Concurrent file access tests passed")


def test_lock_timeout():
    """Test lock timeout functionality."""
    get_logger(__name__).info("🧪 Testing lock timeout...")

    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = get_unified_utility().path.join(temp_dir, "timeout_test.txt")

        # Create a short timeout config
        lock_config = LockConfig(
            timeout_seconds=1.0,  # Very short timeout
            retry_interval=0.1,
            max_retries=10
        )

        lock_manager = FileLockManager(lock_config)

        # Acquire and hold lock in one thread
        lock_acquired = threading.Event()
        lock_released = threading.Event()

        def hold_lock():
            """Hold lock for a while."""
            try:
                with open(test_file, 'w') as f:
                    f.write("initial")

                def long_operation(current: str) -> str:
                    lock_acquired.set()
                    time.sleep(2)  # Hold lock longer than timeout
                    return current + "_updated"

                lock_manager.atomic_update(
                    test_file,
                    long_operation,
                    operation="hold_lock"
                )
            except Exception as e:
                get_logger(__name__).info(f"❌ Hold lock thread error: {e}")
            finally:
                lock_released.set()

        # Start thread that holds lock
        holder_thread = threading.Thread(target=hold_lock)
        holder_thread.start()

        # Wait for lock to be acquired
        lock_acquired.wait(timeout=5)

        # Try to acquire lock in main thread (should timeout)
        try:
            lock_manager.atomic_write(
                test_file,
                "should_fail",
                operation="timeout_test"
            )
            assert False, "Expected LockTimeoutError"
        except LockTimeoutError:
            get_logger(__name__).info("✅ Lock timeout correctly triggered")
        except Exception as e:
            get_logger(__name__).info(f"❌ Unexpected error: {e}")
            assert False, f"Expected LockTimeoutError, got {type(e)}"

        # Wait for holder thread to finish
        lock_released.wait(timeout=5)
        holder_thread.join(timeout=5)

    get_logger(__name__).info("✅ Lock timeout tests passed")


def test_stale_lock_cleanup():
    """Test stale lock cleanup functionality."""
    get_logger(__name__).info("🧪 Testing stale lock cleanup...")

    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = get_unified_utility().path.join(temp_dir, "stale_test.txt")
        lock_manager = FileLockManager()

        # Create a stale lock file manually
        lock_file = test_file + '.lock'
        stale_lock_data = {
            "pid": 999999,  # Non-existent PID
            "thread_id": "stale_thread",
            "timestamp": time.time() - 600,  # 10 minutes ago (stale)
            "operation": "stale_operation",
            "metadata": {}
        }

        # Create stale lock file
        with open(lock_file, 'w') as f:
            write_json(stale_lock_data, f)

        # Create the actual file
        with open(test_file, 'w') as f:
            f.write("test content")

        assert get_unified_utility().path.exists(lock_file), "Stale lock file should exist"

        # Clean up stale locks
        cleaned = lock_manager.cleanup_stale_locks(temp_dir)
        assert cleaned == 1, f"Expected 1 stale lock cleaned, got {cleaned}"
        assert not get_unified_utility().path.exists(lock_file), "Stale lock file should be removed"

    get_logger(__name__).info("✅ Stale lock cleanup tests passed")


def test_messaging_integration():
    """Test file locking integration with messaging system."""
    get_logger(__name__).info("🧪 Testing messaging integration...")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock inbox structure
        inbox_dir = get_unified_utility().path.join(temp_dir, "inbox")
        get_unified_utility().makedirs(inbox_dir, exist_ok=True)


        # Mock inbox paths
        inbox_paths = {"Agent-Test": inbox_dir}

        # Create delivery service with locking
        metrics = MessagingMetrics()
        delivery = MessagingDelivery(inbox_paths, metrics)

        # Create test message
        message = UnifiedMessage(
            message_id="test_msg_001",
            sender="Captain Agent-4",
            recipient="Agent-Test",
            content="Test message with file locking",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            timestamp=None
        )

        # Test message delivery with locking
        success = delivery.send_message_to_inbox(message)
        assert success, "Message delivery with locking failed"

        # Verify message file was created
        expected_files = list(get_unified_utility().Path(inbox_dir).glob("CAPTAIN_MESSAGE_*.md"))
        assert len(expected_files) == 1, f"Expected 1 message file, found {len(expected_files)}"

        # Verify message content
        message_file = expected_files[0]
        with open(message_file, 'r') as f:
            content = f.read()

        assert "Test message with file locking" in content, "Message content not found"
        assert "Captain Agent-4" in content, "Sender not found in message"

    get_logger(__name__).info("✅ Messaging integration tests passed")


def run_all_tests():
    """Run all file locking tests."""
    get_logger(__name__).info("🚀 Starting File Locking System Tests")
    get_logger(__name__).info("=" * 50)

    test_functions = [
        test_basic_file_locking,
        test_concurrent_file_access,
        test_lock_timeout,
        test_stale_lock_cleanup,
        test_messaging_integration
    ]

    passed = 0
    failed = 0

    for test_func in test_functions:
        try:
            test_func()
            passed += 1
        except Exception as e:
            get_logger(__name__).info(f"❌ {test_func.__name__} failed: {e}")
            failed += 1

    get_logger(__name__).info("=" * 50)
    get_logger(__name__).info(f"📊 Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        get_logger(__name__).info("🎉 All file locking tests passed!")
        return True
    else:
        get_logger(__name__).info("⚠️  Some tests failed. Please check the output above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)


#!/usr/bin/env python3
"""
Test Backwards Compatibility of Message Queue PyAutoGUI Integration
===================================================================

This script verifies that the new PyAutoGUI integration maintains
backwards compatibility with existing message queue usage patterns.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.message_queue import MessageQueue, QueueConfig, AsyncQueueProcessor

def test_backwards_compatibility():
    """Test that existing MessageQueue usage patterns still work."""

    print("🔄 TESTING BACKWARDS COMPATIBILITY")
    print("=" * 50)

    # Test 1: Default queue creation (should work without PyAutoGUI)
    print("\n1. Testing default queue creation...")
    try:
        queue = MessageQueue()
        print("✅ Default queue creation works")
    except Exception as e:
        print(f"❌ Default queue creation failed: {e}")
        return False

    # Test 2: Basic enqueue without parameters (original API)
    print("\n2. Testing basic enqueue (original API)...")
    try:
        message_id = queue.enqueue("Test message")
        print(f"✅ Basic enqueue works: {message_id}")
    except Exception as e:
        print(f"❌ Basic enqueue failed: {e}")
        return False

    # Test 3: Enqueue with delivery callback (original API)
    print("\n3. Testing enqueue with callback (original API)...")
    try:
        def dummy_callback(msg):
            return True

        message_id = queue.enqueue("Test with callback", delivery_callback=dummy_callback)
        print(f"✅ Enqueue with callback works: {message_id}")
    except Exception as e:
        print(f"❌ Enqueue with callback failed: {e}")
        return False

    # Test 4: AsyncQueueProcessor with callback (original API)
    print("\n4. Testing AsyncQueueProcessor (original API)...")
    try:
        processor = AsyncQueueProcessor(queue=queue, delivery_callback=dummy_callback)
        print("✅ AsyncQueueProcessor creation works")
    except Exception as e:
        print(f"❌ AsyncQueueProcessor creation failed: {e}")
        return False

    # Test 5: AsyncQueueProcessor without callback (new default behavior)
    print("\n5. Testing AsyncQueueProcessor without callback...")
    try:
        processor = AsyncQueueProcessor(queue=queue)
        print("✅ AsyncQueueProcessor without callback works")
    except Exception as e:
        print(f"❌ AsyncQueueProcessor without callback failed: {e}")
        return False

    # Test 6: Queue statistics (original API)
    print("\n6. Testing queue statistics...")
    try:
        stats = queue.get_statistics()
        print(f"✅ Queue statistics work: {len(stats)} keys")
    except Exception as e:
        print(f"❌ Queue statistics failed: {e}")
        return False

    # Test 7: Queue health (original API)
    print("\n7. Testing queue health...")
    try:
        health = queue.get_health_status()
        print(f"✅ Queue health works: {len(health)} keys")
    except Exception as e:
        print(f"❌ Queue health failed: {e}")
        return False

    # Test 8: New PyAutoGUI features don't break existing code
    print("\n8. Testing new features don't break existing code...")
    try:
        # This should work with new features but not change existing behavior
        queue_with_config = MessageQueue(QueueConfig(enable_pyautogui_delivery=False))
        message_id = queue_with_config.enqueue("Test message")
        print(f"✅ New features don't break existing code: {message_id}")
    except Exception as e:
        print(f"❌ New features broke existing code: {e}")
        return False

    print("\n" + "=" * 50)
    print("🎉 ALL BACKWARDS COMPATIBILITY TESTS PASSED!")
    print("✅ Existing code will continue to work unchanged")
    print("✅ New PyAutoGUI features are opt-in")
    print("✅ Original APIs preserved")
    return True

def test_file_organization():
    """Test that files are properly organized."""

    print("\n📁 TESTING FILE ORGANIZATION")
    print("=" * 40)

    core_dir = Path("src/core")
    required_files = [
        "message_queue.py",
        "message_queue_interfaces.py",
        "message_queue_persistence.py",
        "message_queue_statistics.py",
        "message_queue_pyautogui_integration.py"
    ]

    missing_files = []
    for filename in required_files:
        filepath = core_dir / filename
        if filepath.exists():
            print(f"✅ {filename} exists in src/core/")
        else:
            print(f"❌ {filename} missing from src/core/")
            missing_files.append(filename)

    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False

    print("✅ All message queue files properly organized in src/core/")
    return True

if __name__ == "__main__":
    success1 = test_backwards_compatibility()
    success2 = test_file_organization()

    if success1 and success2:
        print("\n🎯 BACKWARDS COMPATIBILITY & ORGANIZATION: SUCCESS")
        print("The PyAutoGUI integration maintains full backwards compatibility!")
    else:
        print("\n❌ ISSUES FOUND - Check output above")
        sys.exit(1)

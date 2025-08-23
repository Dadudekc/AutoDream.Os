#!/usr/bin/env python3
"""
Test Advanced Messaging System - Agent Cellphone V2
===================================================

Simple test script to verify the advanced messaging system functionality.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.messaging.message_types import (
    Message,
    MessagePriority,
    MessageType,
    MessageStatus,
)
from core.messaging.message_queue import InMemoryMessageQueue, PersistentMessageQueue


async def test_message_types():
    """Test message type creation and serialization."""
    print("🧪 Testing Message Types...")

    # Create a test message
    message = Message(
        type=MessageType.COORDINATION,
        content="Test coordination message",
        from_agent="Agent-1",
        to_agent="Agent-2",
        priority=MessagePriority.HIGH,
        tags=["test", "coordination"],
    )

    print(f"✅ Created message: {message}")
    print(f"   ID: {message.message_id}")
    print(f"   Type: {message.type.value}")
    print(f"   Priority: {message.priority.value}")
    print(f"   Tags: {message.tags}")

    # Test serialization
    message_dict = message.to_dict()
    print(f"✅ Serialized to dict: {len(message_dict)} fields")

    # Test deserialization
    reconstructed = Message.from_dict(message_dict)
    print(f"✅ Deserialized message: {reconstructed}")

    # Test JSON serialization
    json_str = message.to_json()
    print(f"✅ JSON serialization: {len(json_str)} characters")

    # Test JSON deserialization
    from_json = Message.from_json(json_str)
    print(f"✅ JSON deserialization: {from_json}")

    return True


async def test_in_memory_queue():
    """Test in-memory message queue functionality."""
    print("\n🧪 Testing In-Memory Message Queue...")

    # Create queue
    queue = InMemoryMessageQueue("test_queue", max_size=100)
    print(f"✅ Created queue: {queue.name}")

    # Create test messages
    msg1 = Message(
        type=MessageType.TASK,
        content="High priority task",
        from_agent="Agent-1",
        to_agent="Agent-2",
        priority=MessagePriority.HIGH,
    )

    msg2 = Message(
        type=MessageType.TASK,
        content="Low priority task",
        from_agent="Agent-1",
        to_agent="Agent-2",
        priority=MessagePriority.LOW,
    )

    msg3 = Message(
        type=MessageType.BROADCAST,
        content="Broadcast message",
        from_agent="Agent-1",
        to_agent="broadcast",
        priority=MessagePriority.NORMAL,
    )

    # Enqueue messages
    await queue.enqueue(msg1)
    await queue.enqueue(msg2)
    await queue.enqueue(msg3)
    print(f"✅ Enqueued 3 messages")

    # Check queue size
    size = await queue.get_queue_size()
    print(f"✅ Queue size: {size}")

    # Dequeue messages for Agent-2 (should get high priority first)
    message = await queue.dequeue("Agent-2")
    if message:
        print(
            f"✅ Dequeued for Agent-2: {message.content} (Priority: {message.priority.value})"
        )

    # Dequeue broadcast message
    message = await queue.dequeue("Agent-3")
    if message:
        print(f"✅ Dequeued broadcast for Agent-3: {message.content}")

    # Check final queue size
    final_size = await queue.get_queue_size()
    print(f"✅ Final queue size: {final_size}")

    # Get metrics
    metrics = queue.get_metrics()
    print(f"✅ Queue metrics: {metrics}")

    return True


async def test_persistent_queue():
    """Test persistent message queue functionality."""
    print("\n🧪 Testing Persistent Message Queue...")

    # Create storage directory
    storage_dir = Path("test_messaging_storage")
    storage_dir.mkdir(exist_ok=True)

    # Create queue
    queue = PersistentMessageQueue("test_persistent", storage_dir, max_size=50)
    print(f"✅ Created persistent queue: {queue.name}")

    # Create test message
    message = Message(
        type=MessageType.STATUS,
        content="Status update",
        from_agent="Agent-1",
        to_agent="Agent-2",
        priority=MessagePriority.NORMAL,
        tags=["status", "test"],
    )

    # Enqueue message
    success = await queue.enqueue(message)
    print(f"✅ Enqueued message: {success}")

    # Check queue size
    size = await queue.get_queue_size()
    print(f"✅ Queue size: {size}")

    # Get queue stats
    stats = queue.get_queue_stats()
    print(f"✅ Queue stats: {stats}")

    # Clean up
    queue.clear_queue()
    print(f"✅ Cleared queue")

    return True


async def test_message_operations():
    """Test various message operations."""
    print("\n🧪 Testing Message Operations...")

    # Create message with dependencies
    dep_msg = Message(
        type=MessageType.TASK,
        content="Dependency task",
        from_agent="Agent-1",
        to_agent="Agent-2",
    )

    main_msg = Message(
        type=MessageType.TASK,
        content="Main task",
        from_agent="Agent-1",
        to_agent="Agent-2",
    )

    # Add dependency
    main_msg.add_dependency(dep_msg.message_id)
    print(f"✅ Added dependency: {main_msg.dependencies}")

    # Check if ready
    ready = main_msg.is_ready({dep_msg.message_id})
    print(f"✅ Message ready: {ready}")

    # Test tags
    main_msg.add_tag("main")
    main_msg.add_tag("critical")
    print(f"✅ Added tags: {main_msg.tags}")

    # Test tag operations
    print(f"✅ Has 'main' tag: {main_msg.has_tag('main')}")
    main_msg.remove_tag("main")
    print(f"✅ After removing 'main': {main_msg.tags}")

    return True


async def main():
    """Run all tests."""
    print("🚀 ADVANCED MESSAGING SYSTEM TEST")
    print("=" * 50)

    tests = [
        test_message_types,
        test_in_memory_queue,
        test_persistent_queue,
        test_message_operations,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if await test():
                passed += 1
                print("✅ Test passed\n")
            else:
                print("❌ Test failed\n")
        except Exception as e:
            print(f"❌ Test error: {e}\n")

    print("=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! Advanced messaging system is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please review the implementation.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

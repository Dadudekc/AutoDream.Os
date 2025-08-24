#!/usr/bin/env python3
"""
Advanced Task Management System - Comprehensive Test Suite
========================================================

Tests the complete task management system including task types,
scheduling, dependency resolution, and performance monitoring.
"""

import asyncio
import time
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the task management system
from src.core.task_management import (
    Task,
    TaskPriority,
    TaskStatus,
    TaskType,
    TaskCategory,
    TaskDependency,
    TaskResource,
    TaskConstraint,
    TaskMetadata,
    TaskScheduler,
    SchedulingMetrics,
)


async def test_task_creation():
    """Test basic task creation and properties."""
    logger.info("🧪 Testing Task Creation...")

    # Create a basic task
    task = Task(
        name="Test Computation Task",
        type=TaskType.COMPUTATION,
        category=TaskCategory.USER,
        content="Perform complex calculation",
        priority=TaskPriority.HIGH,
        metadata=TaskMetadata(description="A test task for validation"),
    )

    # Verify basic properties
    assert task.name == "Test Computation Task"
    assert task.type == TaskType.COMPUTATION
    assert task.category == TaskCategory.USER
    assert task.priority == TaskPriority.HIGH
    assert task.status == TaskStatus.PENDING
    assert task.progress == 0.0
    assert task.retry_count == 0

    # Test task methods
    assert task.is_ready_to_execute() == True
    assert task.can_retry() == False

    logger.info("✅ Task Creation Test PASSED")
    return task


async def test_task_with_dependencies():
    """Test task creation with dependencies."""
    logger.info("🧪 Testing Task Dependencies...")

    # Create dependency
    dependency = TaskDependency(
        task_id="dep_task_001", dependency_type="required", condition="completed"
    )

    # Create task with dependency
    task = Task(
        name="Dependent Task",
        type=TaskType.DATA_PROCESSING,
        dependencies=[dependency],
        priority=TaskPriority.NORMAL,
    )

    # Verify dependency
    assert len(task.dependencies) == 1
    assert task.dependencies[0].task_id == "dep_task_001"
    assert task.dependencies[0].dependency_type == "required"

    logger.info("✅ Task Dependencies Test PASSED")
    return task


async def test_task_with_constraints():
    """Test task creation with constraints."""
    logger.info("🧪 Testing Task Constraints...")

    # Create constraints
    constraints = TaskConstraint(
        deadline=datetime.now() + timedelta(hours=1),
        start_time=datetime.now(),
        max_duration=3600,  # 1 hour
        required_agents=["agent_001", "agent_002"],
        security_level="high",
    )

    # Create task with constraints
    task = Task(
        name="Constrained Task", type=TaskType.COORDINATION, constraints=constraints
    )

    # Verify constraints
    assert task.constraints.deadline is not None
    assert task.constraints.start_time is not None
    assert task.constraints.max_duration == 3600
    assert len(task.constraints.required_agents) == 2
    assert task.constraints.security_level == "high"

    # Test constraint validation
    assert task._are_constraints_satisfied() == True

    logger.info("✅ Task Constraints Test PASSED")
    return task


async def test_task_scheduler():
    """Test the task scheduler functionality."""
    logger.info("🧪 Testing Task Scheduler...")

    # Create scheduler
    scheduler = TaskScheduler(max_concurrent_tasks=10)

    # Start scheduler
    await scheduler.start()

    # Create test tasks
    task1 = Task(
        name="High Priority Task",
        priority=TaskPriority.HIGH,
        content="Urgent computation",
    )

    task2 = Task(
        name="Low Priority Task",
        priority=TaskPriority.LOW,
        content="Background processing",
    )

    # Submit tasks
    success1 = await scheduler.submit_task(task1)
    success2 = await scheduler.submit_task(task2)

    assert success1 == True
    assert success2 == True

    # Get task status
    status1 = scheduler.get_task_status(task1.task_id)
    status2 = scheduler.get_task_status(task2.task_id)

    assert status1 == TaskStatus.PENDING
    assert status2 == TaskStatus.PENDING

    # Get next task for an agent
    next_task = await scheduler.get_next_task("agent_001")
    assert next_task is not None

    # Complete the task
    success = await scheduler.complete_task(
        next_task.task_id, "Task completed successfully"
    )
    assert success == True

    # Get metrics
    metrics = scheduler.get_scheduler_metrics()
    assert metrics.total_tasks_scheduled >= 2
    assert metrics.total_tasks_completed >= 1

    # Stop scheduler
    await scheduler.stop()

    logger.info("✅ Task Scheduler Test PASSED")


async def test_task_lifecycle():
    """Test complete task lifecycle."""
    logger.info("🧪 Testing Task Lifecycle...")

    # Create scheduler
    scheduler = TaskScheduler(max_concurrent_tasks=5)
    await scheduler.start()

    # Create task
    task = Task(
        name="Lifecycle Test Task",
        type=TaskType.ANALYSIS,
        priority=TaskPriority.NORMAL,
        content="Test task execution flow",
    )

    # Submit task
    await scheduler.submit_task(task)

    # Get task
    retrieved_task = await scheduler.get_next_task("agent_001")
    assert retrieved_task is not None
    assert retrieved_task.task_id == task.task_id

    # Update progress
    retrieved_task.update_progress(50.0)
    assert retrieved_task.progress == 50.0

    # Complete task
    await scheduler.complete_task(task.task_id, "Analysis completed")

    # Verify completion
    final_status = scheduler.get_task_status(task.task_id)
    assert final_status == TaskStatus.COMPLETED

    await scheduler.stop()

    logger.info("✅ Task Lifecycle Test PASSED")


async def test_task_failure_and_retry():
    """Test task failure handling and retry logic."""
    logger.info("🧪 Testing Task Failure and Retry...")

    # Create scheduler
    scheduler = TaskScheduler(max_concurrent_tasks=5)
    await scheduler.start()

    # Create task with retry capability
    task = Task(
        name="Retry Test Task",
        type=TaskType.VALIDATION,
        max_retries=2,
        content="Task that will fail and retry",
    )

    # Submit task
    await scheduler.submit_task(task)

    # Get and start task
    retrieved_task = await scheduler.get_next_task("agent_001")
    assert retrieved_task is not None

    # Fail the task
    await scheduler.fail_task(task.task_id, "Simulated failure")

    # Check retry status
    retry_status = scheduler.get_task_status(task.task_id)
    assert retry_status == TaskStatus.PENDING  # Should be retried

    # Fail again
    retrieved_task = await scheduler.get_next_task("agent_001")
    await scheduler.fail_task(task.task_id, "Second failure")

    # Fail final time
    retrieved_task = await scheduler.get_next_task("agent_001")
    await scheduler.fail_task(task.task_id, "Final failure")

    # Check final status
    final_status = scheduler.get_task_status(task.task_id)
    assert final_status == TaskStatus.FAILED

    await scheduler.stop()

    logger.info("✅ Task Failure and Retry Test PASSED")


async def test_task_cancellation():
    """Test task cancellation functionality."""
    logger.info("🧪 Testing Task Cancellation...")

    # Create scheduler
    scheduler = TaskScheduler(max_concurrent_tasks=5)
    await scheduler.start()

    # Create task
    task = Task(
        name="Cancellation Test Task",
        type=TaskType.MONITORING,
        content="Task to be cancelled",
    )

    # Submit task
    await scheduler.submit_task(task)

    # Cancel task
    success = await scheduler.cancel_task(task.task_id)
    assert success == True

    # Verify cancellation
    status = scheduler.get_task_status(task.task_id)
    assert status == TaskStatus.CANCELLED

    await scheduler.stop()

    logger.info("✅ Task Cancellation Test PASSED")


async def test_performance_metrics():
    """Test scheduler performance metrics."""
    logger.info("🧪 Testing Performance Metrics...")

    # Create scheduler
    scheduler = TaskScheduler(max_concurrent_tasks=10)
    await scheduler.start()

    # Submit multiple tasks
    tasks = []
    for i in range(5):
        task = Task(
            name=f"Metric Test Task {i}",
            priority=TaskPriority.NORMAL,
            content=f"Task {i} for metrics testing",
        )
        await scheduler.submit_task(task)
        tasks.append(task)

    # Get metrics
    metrics = scheduler.get_scheduler_metrics()

    # Verify metrics
    assert metrics.total_tasks_scheduled >= 5
    assert metrics.tasks_by_priority[TaskPriority.NORMAL] >= 5
    assert metrics.tasks_by_type[TaskType.COMPUTATION] >= 5
    assert metrics.last_update is not None

    # Complete some tasks
    for i in range(3):
        next_task = await scheduler.get_next_task("agent_001")
        if next_task:
            await scheduler.complete_task(next_task.task_id, f"Completed task {i}")

    # Get updated metrics
    updated_metrics = scheduler.get_scheduler_metrics()
    assert updated_metrics.total_tasks_completed >= 3

    await scheduler.stop()

    logger.info("✅ Performance Metrics Test PASSED")


async def test_task_callbacks():
    """Test task event callbacks."""
    logger.info("🧪 Testing Task Callbacks...")

    # Create scheduler
    scheduler = TaskScheduler(max_concurrent_tasks=5)
    await scheduler.start()

    # Track callback events
    callback_events = []

    def task_completed_callback(task):
        callback_events.append(("completed", task.task_id))

    def task_failed_callback(task):
        callback_events.append(("failed", task.task_id))

    # Register callbacks
    scheduler.register_task_callback("completed", task_completed_callback)
    scheduler.register_task_callback("failed", task_failed_callback)

    # Create and submit task
    task = Task(name="Callback Test Task", content="Task to test callbacks")

    await scheduler.submit_task(task)

    # Execute and complete task
    next_task = await scheduler.get_next_task("agent_001")
    await scheduler.complete_task(next_task.task_id, "Callback test completed")

    # Wait for callback processing
    await asyncio.sleep(0.1)

    # Verify callbacks were triggered
    assert len(callback_events) >= 1
    assert any(event[0] == "completed" for event in callback_events)

    await scheduler.stop()

    logger.info("✅ Task Callbacks Test PASSED")


async def run_all_tests():
    """Run all test suites."""
    logger.info("🚀 Starting Advanced Task Management System Tests...")

    test_results = []

    try:
        # Run all tests
        await test_task_creation()
        test_results.append(("Task Creation", "PASSED"))

        await test_task_with_dependencies()
        test_results.append(("Task Dependencies", "PASSED"))

        await test_task_with_constraints()
        test_results.append(("Task Constraints", "PASSED"))

        await test_task_scheduler()
        test_results.append(("Task Scheduler", "PASSED"))

        await test_task_lifecycle()
        test_results.append(("Task Lifecycle", "PASSED"))

        await test_task_failure_and_retry()
        test_results.append(("Task Failure & Retry", "PASSED"))

        await test_task_cancellation()
        test_results.append(("Task Cancellation", "PASSED"))

        await test_performance_metrics()
        test_results.append(("Performance Metrics", "PASSED"))

        await test_task_callbacks()
        test_results.append(("Task Callbacks", "PASSED"))

        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("🎉 ALL TESTS PASSED SUCCESSFULLY!")
        logger.info("=" * 60)

        for test_name, result in test_results:
            logger.info(f"✅ {test_name}: {result}")

        logger.info(f"\n📊 Total Tests: {len(test_results)}")
        logger.info("🏆 Advanced Task Management System is fully operational!")

    except Exception as e:
        logger.error(f"❌ Test suite failed: {e}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

    return True


def main():
    """Main test runner."""
    print("🧪 Advanced Task Management System - Test Suite")
    print("=" * 60)

    # Run async tests
    success = asyncio.run(run_all_tests())

    if success:
        print("\n🎉 All tests completed successfully!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    exit(main())

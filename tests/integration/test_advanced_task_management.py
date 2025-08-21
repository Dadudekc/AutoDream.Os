#!/usr/bin/env python3
"""
Advanced Task Management System - Integration Test Suite
=======================================================

Tests the complete task management system including task types,
scheduling, dependency resolution, and performance monitoring.

Moved from root to tests/integration/ for better organization.
Foundation & Testing Specialist - Test Structure Reorganization
"""

import asyncio
import time
import logging
import pytest
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the task management system
from src.core.task_management import (
    Task, TaskPriority, TaskStatus, TaskType, TaskCategory,
    TaskDependency, TaskResource, TaskConstraint, TaskMetadata,
    TaskScheduler, SchedulingMetrics
)


@pytest.mark.integration
@pytest.mark.asyncio
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
        metadata=TaskMetadata(description="A test task for validation")
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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_task_with_dependencies():
    """Test task creation with dependencies."""
    logger.info("🧪 Testing Task Dependencies...")
    
    # Create dependency
    dependency = TaskDependency(
        task_id="dep_task_001",
        dependency_type="required",
        condition="completed"
    )
    
    # Create task with dependency
    task = Task(
        name="Dependent Task",
        type=TaskType.DATA_PROCESSING,
        dependencies=[dependency],
        priority=TaskPriority.NORMAL
    )
    
    # Verify dependency
    assert len(task.dependencies) == 1
    assert task.dependencies[0].task_id == "dep_task_001"
    assert task.dependencies[0].dependency_type == "required"
    
    logger.info("✅ Task Dependencies Test PASSED")
    return task


@pytest.mark.integration
@pytest.mark.asyncio
async def test_task_scheduler():
    """Test the task scheduler functionality."""
    logger.info("🧪 Testing Task Scheduler...")
    
    # Create scheduler
    scheduler = TaskScheduler(max_concurrent_tasks=10)
    
    # Start scheduler
    await scheduler.start()
    
    try:
        # Create test tasks
        task1 = Task(
            name="High Priority Task",
            priority=TaskPriority.HIGH,
            content="Urgent computation"
        )
        
        task2 = Task(
            name="Low Priority Task", 
            priority=TaskPriority.LOW,
            content="Background processing"
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
        success = await scheduler.complete_task(next_task.task_id, "Task completed successfully")
        assert success == True
        
        # Get metrics
        metrics = scheduler.get_scheduler_metrics()
        assert metrics.total_tasks_scheduled >= 2
        assert metrics.total_tasks_completed >= 1
        
    finally:
        # Stop scheduler
        await scheduler.stop()
    
    logger.info("✅ Task Scheduler Test PASSED")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_task_lifecycle():
    """Test complete task lifecycle."""
    logger.info("🧪 Testing Task Lifecycle...")
    
    # Create scheduler
    scheduler = TaskScheduler(max_concurrent_tasks=5)
    await scheduler.start()
    
    try:
        # Create task
        task = Task(
            name="Lifecycle Test Task",
            type=TaskType.ANALYSIS,
            priority=TaskPriority.NORMAL,
            content="Test task execution flow"
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
        
    finally:
        await scheduler.stop()
    
    logger.info("✅ Task Lifecycle Test PASSED")


# Additional test methods can be added here following the same pattern
# This consolidates the test into the proper test structure with pytest markers

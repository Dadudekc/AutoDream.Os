#!/usr/bin/env python3
"""
SSOT Execution Coordinator Integration Tests

Comprehensive integration tests for the canonical SSOT execution coordinator.
Tests cover task execution, dependency resolution, error handling, and performance.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Version: 1.0.0
License: MIT
"""

import time

    SSOTExecutionCoordinator,
    get_ssot_execution_coordinator,
    create_ssot_execution_coordinator,
)
    ExecutionPhase,
    ExecutionStatus,
    ExecutionTask,
    CoordinationContext,
)


class TestSSOTExecutionCoordinator:
    """Test suite for SSOT Execution Coordinator."""

    @pytest.fixture
    async def coordinator(self):
        """Create a fresh coordinator instance for each test."""
        coordinator = create_ssot_execution_coordinator(max_concurrent_tasks=3)
        yield coordinator
        coordinator.shutdown()

    @pytest.fixture
    def sample_tasks(self):
        """Create sample tasks for testing."""
        return [
            ExecutionTask(
                task_id="task_1",
                task_name="Test Task 1",
                task_phase=ExecutionPhase.INITIALIZATION,
                task_function="test_function_1",
                timeout_seconds=30,
                priority=1,
            ),
            ExecutionTask(
                task_id="task_2",
                task_name="Test Task 2",
                task_phase=ExecutionPhase.INTEGRATION,
                task_function="test_function_2",
                dependencies=["task_1"],
                timeout_seconds=30,
                priority=2,
            ),
            ExecutionTask(
                task_id="task_3",
                task_name="Test Task 3",
                task_phase=ExecutionPhase.VALIDATION,
                task_function="test_function_3",
                dependencies=["task_2"],
                timeout_seconds=30,
                priority=3,
            ),
        ]

    @pytest.mark.asyncio
    async def test_coordinator_initialization(self, coordinator):
        """Test coordinator initialization."""
        assert coordinator is not None
        assert coordinator.max_concurrent_tasks == 3
        assert len(coordinator.tasks) == 0
        assert len(coordinator.results) == 0
        assert not coordinator._running

    @pytest.mark.asyncio
    async def test_add_single_task(self, coordinator, sample_tasks):
        """Test adding a single task."""
        task = sample_tasks[0]
        coordinator.add_task(task)
        
        assert task.task_id in coordinator.tasks
        assert coordinator.tasks[task.task_id] == task

    @pytest.mark.asyncio
    async def test_add_multiple_tasks(self, coordinator, sample_tasks):
        """Test adding multiple tasks."""
        coordinator.add_tasks(sample_tasks)
        
        assert len(coordinator.tasks) == 3
        for task in sample_tasks:
            assert task.task_id in coordinator.tasks

    @pytest.mark.asyncio
    async def test_create_context(self, coordinator):
        """Test context creation."""
        context = coordinator.create_context(
            context_id="test_context",
            coordination_level="agent",
            agent_id="Agent-3"
        )
        
        assert context.context_id == "test_context"
        assert context.coordination_level == "agent"
        assert context.agent_id == "Agent-3"
        assert context.status == ExecutionStatus.PENDING
        assert "test_context" in coordinator.contexts

    @pytest.mark.asyncio
    async def test_execution_coordination_success(self, coordinator, sample_tasks):
        """Test successful execution coordination."""
        # Add tasks
        coordinator.add_tasks(sample_tasks)
        
        # Create context
        context = coordinator.create_context(
            context_id="test_context",
            coordination_level="agent",
            agent_id="Agent-3"
        )
        
        # Mock the task execution to avoid actual function calls
        original_execute = coordinator._execute_single_task
        
        async def mock_execute(task_id: str, context: CoordinationContext):
            return {
                "task_id": task_id,
                "status": ExecutionStatus.COMPLETED,
                "start_time": datetime.now(),
                "execution_time": 0.1,
            }
        
        coordinator._execute_single_task = mock_execute
        
        try:
            # Execute coordination
            result = await coordinator.execute_coordination("test_context")
            
            # Verify results
            assert result["context_id"] == "test_context"
            assert result["status"] == "completed"
            assert result["total_tasks"] == 3
            assert result["completed_tasks"] == 3
            
            # Verify context status
            assert context.status == ExecutionStatus.COMPLETED
            assert context.end_time is not None
            
        finally:
            coordinator._execute_single_task = original_execute

    @pytest.mark.asyncio
    async def test_execution_coordination_with_dependencies(self, coordinator, sample_tasks):
        """Test execution coordination with task dependencies."""
        # Add tasks with dependencies
        coordinator.add_tasks(sample_tasks)
        
        # Create context
        context = coordinator.create_context(
            context_id="test_context",
            coordination_level="agent",
            agent_id="Agent-3"
        )
        
        # Mock task execution
        execution_order = []
        
        async def mock_execute(task_id: str, context: CoordinationContext):
            execution_order.append(task_id)
            return {
                "task_id": task_id,
                "status": ExecutionStatus.COMPLETED,
                "start_time": datetime.now(),
                "execution_time": 0.1,
            }
        
        coordinator._execute_single_task = mock_execute
        
        try:
            # Execute coordination
            await coordinator.execute_coordination("test_context")
            
            # Verify execution order respects dependencies
            assert execution_order[0] == "task_1"  # No dependencies
            assert execution_order[1] == "task_2"  # Depends on task_1
            assert execution_order[2] == "task_3"  # Depends on task_2
            
        finally:
            coordinator._execute_single_task = original_execute

    @pytest.mark.asyncio
    async def test_execution_coordination_failure(self, coordinator, sample_tasks):
        """Test execution coordination with task failure."""
        # Add tasks
        coordinator.add_tasks(sample_tasks)
        
        # Create context
        context = coordinator.create_context(
            context_id="test_context",
            coordination_level="agent",
            agent_id="Agent-3"
        )
        
        # Mock task execution with failure
        async def mock_execute(task_id: str, context: CoordinationContext):
            if task_id == "task_2":
                raise Exception("Task execution failed")
            return {
                "task_id": task_id,
                "status": ExecutionStatus.COMPLETED,
                "start_time": datetime.now(),
                "execution_time": 0.1,
            }
        
        coordinator._execute_single_task = mock_execute
        
        try:
            # Execute coordination
            result = await coordinator.execute_coordination("test_context")
            
            # Verify results
            assert result["context_id"] == "test_context"
            assert result["status"] == "completed"  # Coordinator continues despite failures
            assert result["total_tasks"] == 3
            assert result["completed_tasks"] == 3  # All tasks attempted
            
            # Verify failed task result
            assert "task_2" in coordinator.results
            assert coordinator.results["task_2"]["status"] == ExecutionStatus.FAILED
            
        finally:
            coordinator._execute_single_task = original_execute

    @pytest.mark.asyncio
    async def test_get_execution_status(self, coordinator):
        """Test getting execution status."""
        # Create context
        context = coordinator.create_context(
            context_id="test_context",
            coordination_level="agent",
            agent_id="Agent-3"
        )
        
        # Get status
        status = coordinator.get_execution_status("test_context")
        
        assert status["context_id"] == "test_context"
        assert status["status"] == ExecutionStatus.PENDING.value
        assert "start_time" in status
        assert status["end_time"] is None
        assert not status["running"]

    @pytest.mark.asyncio
    async def test_get_task_status(self, coordinator, sample_tasks):
        """Test getting task status."""
        # Add task
        task = sample_tasks[0]
        coordinator.add_task(task)
        
        # Get status for pending task
        status = coordinator.get_task_status("task_1")
        assert status["task_id"] == "task_1"
        assert status["status"] == "pending"
        assert status["task_name"] == "Test Task 1"
        
        # Get status for non-existent task
        status = coordinator.get_task_status("non_existent")
        assert "error" in status

    @pytest.mark.asyncio
    async def test_clear_results(self, coordinator, sample_tasks):
        """Test clearing results."""
        # Add tasks and simulate results
        coordinator.add_tasks(sample_tasks)
        
        # Simulate some results
        coordinator.results["task_1"] = {
            "task_id": "task_1",
            "status": ExecutionStatus.COMPLETED,
            "start_time": datetime.now(),
            "execution_time": 0.1,
        }
        
        # Clear results
        coordinator.clear_results()
        
        assert len(coordinator.results) == 0

    @pytest.mark.asyncio
    async def test_global_instance(self):
        """Test global instance management."""
        # Get global instance
        coordinator1 = get_ssot_execution_coordinator()
        coordinator2 = get_ssot_execution_coordinator()
        
        # Should be the same instance
        assert coordinator1 is coordinator2

    @pytest.mark.asyncio
    async def test_concurrent_execution(self, coordinator, sample_tasks):
        """Test concurrent task execution."""
        # Add tasks
        coordinator.add_tasks(sample_tasks)
        
        # Create context
        context = coordinator.create_context(
            context_id="test_context",
            coordination_level="agent",
            agent_id="Agent-3"
        )
        
        # Mock task execution with timing
        execution_times = {}
        
        async def mock_execute(task_id: str, context: CoordinationContext):
            start_time = time.time()
            await asyncio.sleep(0.1)  # Simulate work
            execution_times[task_id] = time.time() - start_time
            return {
                "task_id": task_id,
                "status": ExecutionStatus.COMPLETED,
                "start_time": datetime.now(),
                "execution_time": execution_times[task_id],
            }
        
        coordinator._execute_single_task = mock_execute
        
        try:
            # Execute coordination
            start_time = time.time()
            await coordinator.execute_coordination("test_context")
            total_time = time.time() - start_time
            
            # Verify concurrent execution (should be faster than sequential)
            # With max_concurrent_tasks=3, all tasks should run concurrently
            assert total_time < 0.2  # Should be much less than 3 * 0.1
            
        finally:
            coordinator._execute_single_task = original_execute

    @pytest.mark.asyncio
    async def test_error_handling_invalid_context(self, coordinator):
        """Test error handling for invalid context."""
        with pytest.raises(ValueError, match="Context invalid_context not found"):
            await coordinator.execute_coordination("invalid_context")

    @pytest.mark.asyncio
    async def test_error_handling_invalid_task(self, coordinator):
        """Test error handling for invalid task."""
        # Create context
        context = coordinator.create_context(
            context_id="test_context",
            coordination_level="agent",
            agent_id="Agent-3"
        )
        
        # Mock task execution to reference non-existent task
        async def mock_execute(task_id: str, context: CoordinationContext):
            get_unified_validator().raise_validation_error(f"Task {task_id} not found")
        
        coordinator._execute_single_task = mock_execute
        
        try:
            # This should not raise an exception, but should handle the error gracefully
            result = await coordinator.execute_coordination("test_context")
            assert result["status"] == "completed"
            
        finally:
            coordinator._execute_single_task = original_execute


# Performance tests
class TestSSOTExecutionCoordinatorPerformance:
    """Performance tests for SSOT Execution Coordinator."""

    @pytest.mark.asyncio
    async def test_large_task_set_performance(self):
        """Test performance with a large number of tasks."""
        coordinator = create_ssot_execution_coordinator(max_concurrent_tasks=10)
        
        try:
            # Create many tasks
            tasks = []
            for i in range(100):
                task = ExecutionTask(
                    task_id=f"task_{i}",
                    task_name=f"Test Task {i}",
                    task_phase=ExecutionPhase.INITIALIZATION,
                    task_function=f"test_function_{i}",
                    timeout_seconds=30,
                    priority=i,
                )
                tasks.append(task)
            
            # Add tasks
            coordinator.add_tasks(tasks)
            
            # Create context
            context = coordinator.create_context(
                context_id="performance_test",
                coordination_level="system",
            )
            
            # Mock fast execution
            async def mock_execute(task_id: str, context: CoordinationContext):
                return {
                    "task_id": task_id,
                    "status": ExecutionStatus.COMPLETED,
                    "start_time": datetime.now(),
                    "execution_time": 0.001,
                }
            
            coordinator._execute_single_task = mock_execute
            
            # Measure execution time
            start_time = time.time()
            result = await coordinator.execute_coordination("performance_test")
            execution_time = time.time() - start_time
            
            # Verify results
            assert result["total_tasks"] == 100
            assert result["completed_tasks"] == 100
            assert execution_time < 5.0  # Should complete within 5 seconds
            
        finally:
            coordinator.shutdown()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

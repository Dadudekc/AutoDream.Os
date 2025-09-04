#!/usr/bin/env python3
"""
SSOT System Integration Tests

End-to-end integration tests for the complete SSOT system.
Tests cover coordination between execution coordinator and validation system.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Version: 1.0.0
License: MIT
"""

import time

    SSOTExecutionCoordinator,
    get_ssot_execution_coordinator,
)
    SSOTValidationSystem,
    get_ssot_validation_system,
)
    ExecutionPhase,
    ExecutionStatus,
    ExecutionTask,
)


class TestSSOTSystemIntegration:
    """End-to-end integration tests for the SSOT system."""

    @pytest.fixture
    async def integrated_system(self):
        """Create integrated SSOT system for testing."""
        coordinator = get_ssot_execution_coordinator()
        validation_system = get_ssot_validation_system()
        await validation_system.initialize()
        
        yield {
            "coordinator": coordinator,
            "validation_system": validation_system,
        }
        
        await validation_system.shutdown()

    @pytest.mark.asyncio
    async def test_full_ssot_integration_workflow(self, integrated_system):
        """Test complete SSOT integration workflow."""
        coordinator = integrated_system["coordinator"]
        validation_system = integrated_system["validation_system"]
        
        # Create integration tasks
        tasks = [
            ExecutionTask(
                task_id="init_ssot",
                task_name="Initialize SSOT System",
                task_phase=ExecutionPhase.INITIALIZATION,
                task_function="initialize_ssot_system",
                timeout_seconds=60,
                priority=10,
            ),
            ExecutionTask(
                task_id="validate_ssot",
                task_name="Validate SSOT System",
                task_phase=ExecutionPhase.VALIDATION,
                task_function="validate_ssot_system",
                dependencies=["init_ssot"],
                timeout_seconds=120,
                priority=9,
            ),
            ExecutionTask(
                task_id="integrate_ssot",
                task_name="Integrate SSOT System",
                task_phase=ExecutionPhase.INTEGRATION,
                task_function="integrate_ssot_system",
                dependencies=["validate_ssot"],
                timeout_seconds=180,
                priority=8,
            ),
        ]
        
        # Add tasks to coordinator
        coordinator.add_tasks(tasks)
        
        # Create execution context
        context = coordinator.create_context(
            context_id="full_integration_test",
            coordination_level="system",
            agent_id="Agent-3"
        )
        
        # Mock task execution
        async def mock_execute_task(task_id: str, context):
            if task_id == "init_ssot":
                return {
                    "task_id": task_id,
                    "status": ExecutionStatus.COMPLETED,
                    "start_time": datetime.now(),
                    "execution_time": 0.1,
                    "metadata": {"message": "SSOT system initialized"},
                }
            elif task_id == "validate_ssot":
                # Run actual validation
                validation_result = await validation_system.validate_ssot_integration(
                    "Agent-3", {"validation_type": "comprehensive"}
                )
                return {
                    "task_id": task_id,
                    "status": ExecutionStatus.COMPLETED,
                    "start_time": datetime.now(),
                    "execution_time": 0.2,
                    "metadata": {"validation_result": validation_result},
                }
            elif task_id == "integrate_ssot":
                return {
                    "task_id": task_id,
                    "status": ExecutionStatus.COMPLETED,
                    "start_time": datetime.now(),
                    "execution_time": 0.3,
                    "metadata": {"message": "SSOT system integrated"},
                }
            else:
                get_unified_validator().raise_validation_error(f"Unknown task: {task_id}")
        
        coordinator._execute_single_task = mock_execute_task
        
        try:
            # Execute full integration workflow
            result = await coordinator.execute_coordination("full_integration_test")
            
            # Verify results
            assert result["context_id"] == "full_integration_test"
            assert result["status"] == "completed"
            assert result["total_tasks"] == 3
            assert result["completed_tasks"] == 3
            
            # Verify task execution order
            task_results = coordinator.get_all_results()
            assert "init_ssot" in task_results
            assert "validate_ssot" in task_results
            assert "integrate_ssot" in task_results
            
            # Verify validation was executed
            validation_task_result = task_results["validate_ssot"]
            assert "validation_result" in validation_task_result["metadata"]
            
        finally:
            # Restore original method
            coordinator._execute_single_task = original_execute

    @pytest.mark.asyncio
    async def test_coordinator_validation_integration(self, integrated_system):
        """Test integration between coordinator and validation system."""
        coordinator = integrated_system["coordinator"]
        validation_system = integrated_system["validation_system"]
        
        # Create validation task
        task = ExecutionTask(
            task_id="validation_task",
            task_name="SSOT Validation Task",
            task_phase=ExecutionPhase.VALIDATION,
            task_function="run_ssot_validation",
            timeout_seconds=60,
            priority=5,
        )
        
        coordinator.add_task(task)
        
        # Create context
        context = coordinator.create_context(
            context_id="validation_integration_test",
            coordination_level="agent",
            agent_id="Agent-3"
        )
        
        # Mock task execution that calls validation system
        async def mock_execute_task(task_id: str, context):
            if task_id == "validation_task":
                # Call actual validation system
                validation_result = await validation_system.validate_ssot_integration(
                    "Agent-3", {"validation_type": "basic"}
                )
                
                return {
                    "task_id": task_id,
                    "status": ExecutionStatus.COMPLETED,
                    "start_time": datetime.now(),
                    "execution_time": 0.1,
                    "metadata": {
                        "validation_summary": validation_result.get("summary", {}),
                        "validation_passed": validation_result.get("summary", {}).get("failed_tests", 0) == 0,
                    },
                }
            else:
                get_unified_validator().raise_validation_error(f"Unknown task: {task_id}")
        
        coordinator._execute_single_task = mock_execute_task
        
        try:
            # Execute validation task
            result = await coordinator.execute_coordination("validation_integration_test")
            
            # Verify results
            assert result["status"] == "completed"
            assert result["completed_tasks"] == 1
            
            # Verify validation was executed and passed
            task_results = coordinator.get_all_results()
            validation_result = task_results["validation_task"]
            assert validation_result["status"] == ExecutionStatus.COMPLETED
            assert "validation_summary" in validation_result["metadata"]
            
        finally:
            coordinator._execute_single_task = original_execute

    @pytest.mark.asyncio
    async def test_error_propagation_between_systems(self, integrated_system):
        """Test error propagation between coordinator and validation system."""
        coordinator = integrated_system["coordinator"]
        validation_system = integrated_system["validation_system"]
        
        # Create task that will fail
        task = ExecutionTask(
            task_id="failing_task",
            task_name="Failing Task",
            task_phase=ExecutionPhase.VALIDATION,
            task_function="run_failing_validation",
            timeout_seconds=30,
            priority=5,
        )
        
        coordinator.add_task(task)
        
        # Create context
        context = coordinator.create_context(
            context_id="error_propagation_test",
            coordination_level="agent",
            agent_id="Agent-3"
        )
        
        # Mock task execution that fails
        async def mock_execute_task(task_id: str, context):
            if task_id == "failing_task":
                # Simulate validation failure
                try:
                    await validation_system.validate_ssot_integration(
                        "Agent-3", {"validation_type": "invalid_type"}
                    )
                except Exception as e:
                    raise Exception(f"Validation failed: {str(e)}")
            else:
                get_unified_validator().raise_validation_error(f"Unknown task: {task_id}")
        
        coordinator._execute_single_task = mock_execute_task
        
        try:
            # Execute failing task
            result = await coordinator.execute_coordination("error_propagation_test")
            
            # Verify error handling
            assert result["status"] == "completed"  # Coordinator continues despite failures
            assert result["completed_tasks"] == 1
            
            # Verify error is captured in results
            task_results = coordinator.get_all_results()
            failing_result = task_results["failing_task"]
            assert failing_result["status"] == ExecutionStatus.FAILED
            assert "error_message" in failing_result
            
        finally:
            coordinator._execute_single_task = original_execute

    @pytest.mark.asyncio
    async def test_concurrent_system_operations(self, integrated_system):
        """Test concurrent operations across both systems."""
        coordinator = integrated_system["coordinator"]
        validation_system = integrated_system["validation_system"]
        
        # Create multiple contexts for concurrent execution
        contexts = []
        for i in range(3):
            context = coordinator.create_context(
                context_id=f"concurrent_test_{i}",
                coordination_level="agent",
                agent_id=f"Agent-{i}"
            )
            contexts.append(context)
        
        # Create tasks for each context
        for i, context in enumerate(contexts):
            task = ExecutionTask(
                task_id=f"task_{i}",
                task_name=f"Concurrent Task {i}",
                task_phase=ExecutionPhase.VALIDATION,
                task_function=f"run_concurrent_validation_{i}",
                timeout_seconds=60,
                priority=5,
            )
            coordinator.add_task(task)
        
        # Mock concurrent task execution
        async def mock_execute_task(task_id: str, context):
            # Simulate some work
            await asyncio.sleep(0.1)
            
            # Run validation for the specific agent
            agent_id = context.agent_id
            validation_result = await validation_system.validate_ssot_integration(
                agent_id, {"validation_type": "basic"}
            )
            
            return {
                "task_id": task_id,
                "status": ExecutionStatus.COMPLETED,
                "start_time": datetime.now(),
                "execution_time": 0.1,
                "metadata": {
                    "agent_id": agent_id,
                    "validation_passed": validation_result.get("summary", {}).get("failed_tests", 0) == 0,
                },
            }
        
        coordinator._execute_single_task = mock_execute_task
        
        try:
            # Execute all contexts concurrently
            start_time = time.time()
            tasks = [
                coordinator.execute_coordination(f"concurrent_test_{i}")
                for i in range(3)
            ]
            results = await asyncio.gather(*tasks)
            execution_time = time.time() - start_time
            
            # Verify all completed successfully
            assert len(results) == 3
            for i, result in enumerate(results):
                assert result["context_id"] == f"concurrent_test_{i}"
                assert result["status"] == "completed"
                assert result["completed_tasks"] == 1
            
            # Verify concurrent execution (should be faster than sequential)
            assert execution_time < 0.5  # Should be much less than 3 * 0.1
            
            # Verify all task results
            all_results = coordinator.get_all_results()
            assert len(all_results) == 3
            for i in range(3):
                assert f"task_{i}" in all_results
                assert all_results[f"task_{i}"]["status"] == ExecutionStatus.COMPLETED
            
        finally:
            coordinator._execute_single_task = original_execute

    @pytest.mark.asyncio
    async def test_system_health_monitoring(self, integrated_system):
        """Test system health monitoring across both systems."""
        coordinator = integrated_system["coordinator"]
        validation_system = integrated_system["validation_system"]
        
        # Get status from both systems
        coordinator_status = coordinator.get_execution_status("non_existent_context")
        validation_status = await validation_system.get_validation_status()
        
        # Verify coordinator status
        assert "error" in coordinator_status  # Context doesn't exist
        
        # Verify validation system status
        assert validation_status["initialized"] is True
        assert validation_status["system_health"] == "healthy"
        
        # Test with actual context
        context = coordinator.create_context(
            context_id="health_monitoring_test",
            coordination_level="system",
        )
        
        coordinator_status = coordinator.get_execution_status("health_monitoring_test")
        assert coordinator_status["context_id"] == "health_monitoring_test"
        assert coordinator_status["status"] == ExecutionStatus.PENDING.value
        assert not coordinator_status["running"]

    @pytest.mark.asyncio
    async def test_system_cleanup_and_shutdown(self, integrated_system):
        """Test proper system cleanup and shutdown."""
        coordinator = integrated_system["coordinator"]
        validation_system = integrated_system["validation_system"]
        
        # Create some state
        context = coordinator.create_context(
            context_id="cleanup_test",
            coordination_level="system",
        )
        
        task = ExecutionTask(
            task_id="cleanup_task",
            task_name="Cleanup Task",
            task_phase=ExecutionPhase.INITIALIZATION,
            task_function="cleanup_function",
            timeout_seconds=30,
        )
        coordinator.add_task(task)
        
        # Verify state exists
        assert "cleanup_test" in coordinator.contexts
        assert "cleanup_task" in coordinator.tasks
        
        # Shutdown validation system
        await validation_system.shutdown()
        
        # Verify validation system is shutdown
        validation_status = await validation_system.get_validation_status()
        assert validation_status["initialized"] is False
        assert validation_status["system_health"] == "not_initialized"
        
        # Shutdown coordinator
        coordinator.shutdown()
        
        # Verify coordinator is shutdown
        assert not coordinator._running


# Performance integration tests
class TestSSOTSystemPerformanceIntegration:
    """Performance integration tests for the complete SSOT system."""

    @pytest.mark.asyncio
    async def test_large_scale_integration_performance(self):
        """Test performance with large-scale integration."""
        coordinator = get_ssot_execution_coordinator()
        validation_system = get_ssot_validation_system()
        await validation_system.initialize()
        
        try:
            # Create many tasks
            tasks = []
            for i in range(50):
                task = ExecutionTask(
                    task_id=f"perf_task_{i}",
                    task_name=f"Performance Task {i}",
                    task_phase=ExecutionPhase.VALIDATION,
                    task_function=f"perf_function_{i}",
                    timeout_seconds=30,
                    priority=i,
                )
                tasks.append(task)
            
            coordinator.add_tasks(tasks)
            
            # Create context
            context = coordinator.create_context(
                context_id="large_scale_performance_test",
                coordination_level="system",
            )
            
            # Mock fast execution
            async def mock_execute_task(task_id: str, context):
                # Quick validation
                await validation_system.validate_ssot_integration(
                    "Agent-Performance", {"validation_type": "basic"}
                )
                return {
                    "task_id": task_id,
                    "status": ExecutionStatus.COMPLETED,
                    "start_time": datetime.now(),
                    "execution_time": 0.001,
                }
            
            coordinator._execute_single_task = mock_execute_task
            
            # Measure execution time
            start_time = time.time()
            result = await coordinator.execute_coordination("large_scale_performance_test")
            execution_time = time.time() - start_time
            
            # Verify results
            assert result["total_tasks"] == 50
            assert result["completed_tasks"] == 50
            assert execution_time < 10.0  # Should complete within 10 seconds
            
        finally:
            await validation_system.shutdown()
            coordinator.shutdown()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

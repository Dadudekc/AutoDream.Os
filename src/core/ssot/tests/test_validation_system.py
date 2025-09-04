#!/usr/bin/env python3
"""
SSOT Validation System Integration Tests

Comprehensive integration tests for the canonical SSOT validation system.
Tests cover validation execution, reporting, error handling, and performance.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Version: 1.0.0
License: MIT
"""

import time

    SSOTValidationSystem,
    get_ssot_validation_system,
    create_ssot_validation_system,
)
    ValidationLevel,
    ValidationResult,
    ValidationTest,
    ValidationSuite,
)


class TestSSOTValidationSystem:
    """Test suite for SSOT Validation System."""

    @pytest.fixture
    async def validation_system(self):
        """Create a fresh validation system instance for each test."""
        system = create_ssot_validation_system(ValidationLevel.COMPREHENSIVE)
        await system.initialize()
        yield system
        await system.shutdown()

    @pytest.fixture
    def sample_validation_config(self):
        """Create sample validation configuration."""
        return {
            "validation_type": "comprehensive",
            "timeout": 300,
            "include_stress_tests": True,
            "agent_id": "Agent-3",
        }

    @pytest.mark.asyncio
    async def test_validation_system_initialization(self, validation_system):
        """Test validation system initialization."""
        assert validation_system is not None
        assert validation_system.validation_level == ValidationLevel.COMPREHENSIVE
        assert validation_system._initialized
        assert validation_system.report_generator is not None
        assert validation_system.suite_executor is not None

    @pytest.mark.asyncio
    async def test_validate_ssot_integration_success(self, validation_system, sample_validation_config):
        """Test successful SSOT integration validation."""
        # Mock the suite executor to return successful results
        original_execute = validation_system.suite_executor.execute_suite
        
        async def mock_execute_suite(context):
            return [
                {
                    "test_id": "basic_validation_Agent-3",
                    "status": ValidationResult.PASSED,
                    "execution_time": 0.1,
                    "details": {"message": "Basic validation passed"},
                },
                {
                    "test_id": "integration_validation_Agent-3",
                    "status": ValidationResult.PASSED,
                    "execution_time": 0.2,
                    "details": {"message": "Integration validation passed"},
                },
                {
                    "test_id": "comprehensive_validation_Agent-3",
                    "status": ValidationResult.PASSED,
                    "execution_time": 0.3,
                    "details": {"message": "Comprehensive validation passed"},
                },
            ]
        
        validation_system.suite_executor.execute_suite = mock_execute_suite
        
        try:
            # Execute validation
            result = await validation_system.validate_ssot_integration(
                "Agent-3", sample_validation_config
            )
            
            # Verify results
            assert "summary" in result
            assert result["summary"]["total_tests"] == 3
            assert result["summary"]["passed_tests"] == 3
            assert result["summary"]["failed_tests"] == 0
            
        finally:
            validation_system.suite_executor.execute_suite = original_execute

    @pytest.mark.asyncio
    async def test_validate_ssot_integration_with_failures(self, validation_system, sample_validation_config):
        """Test SSOT integration validation with some failures."""
        # Mock the suite executor to return mixed results
        original_execute = validation_system.suite_executor.execute_suite
        
        async def mock_execute_suite(context):
            return [
                {
                    "test_id": "basic_validation_Agent-3",
                    "status": ValidationResult.PASSED,
                    "execution_time": 0.1,
                    "details": {"message": "Basic validation passed"},
                },
                {
                    "test_id": "integration_validation_Agent-3",
                    "status": ValidationResult.FAILED,
                    "execution_time": 0.2,
                    "details": {"message": "Integration validation failed", "error": "Connection timeout"},
                },
                {
                    "test_id": "comprehensive_validation_Agent-3",
                    "status": ValidationResult.PASSED,
                    "execution_time": 0.3,
                    "details": {"message": "Comprehensive validation passed"},
                },
            ]
        
        validation_system.suite_executor.execute_suite = mock_execute_suite
        
        try:
            # Execute validation
            result = await validation_system.validate_ssot_integration(
                "Agent-3", sample_validation_config
            )
            
            # Verify results
            assert "summary" in result
            assert result["summary"]["total_tests"] == 3
            assert result["summary"]["passed_tests"] == 2
            assert result["summary"]["failed_tests"] == 1
            
        finally:
            validation_system.suite_executor.execute_suite = original_execute

    @pytest.mark.asyncio
    async def test_create_validation_suite(self, validation_system, sample_validation_config):
        """Test validation suite creation."""
        suite = validation_system._create_validation_suite("Agent-3", sample_validation_config)
        
        assert suite.suite_id == "ssot_validation_Agent-3"
        assert suite.suite_name == "SSOT Validation Suite for Agent-3"
        assert len(suite.tests) == 3  # Basic, Integration, Comprehensive
        
        # Verify test structure
        test_ids = [test.test_id for test in suite.tests]
        assert "basic_validation_Agent-3" in test_ids
        assert "integration_validation_Agent-3" in test_ids
        assert "comprehensive_validation_Agent-3" in test_ids
        
        # Verify dependencies
        integration_test = next(t for t in suite.tests if t.test_id == "integration_validation_Agent-3")
        assert "basic_validation_Agent-3" in integration_test.dependencies
        
        comprehensive_test = next(t for t in suite.tests if t.test_id == "comprehensive_validation_Agent-3")
        assert "integration_validation_Agent-3" in comprehensive_test.dependencies

    @pytest.mark.asyncio
    async def test_run_validation_tests(self, validation_system):
        """Test running specific validation tests."""
        # Mock the test execution handler
        original_handler = validation_system.suite_executor
        
        class MockHandler:
            async def execute_test(self, context):
                return {
                    "test_id": context["test_id"],
                    "status": ValidationResult.PASSED,
                    "execution_time": 0.1,
                    "details": {"message": "Test passed"},
                }
        
        validation_system.suite_executor = MockHandler()
        
        try:
            # Run specific tests
            test_ids = ["test_1", "test_2", "test_3"]
            results = await validation_system.run_validation_tests(test_ids)
            
            # Verify results
            assert len(results) == 3
            for test_id in test_ids:
                assert test_id in results
                assert results[test_id]["status"] == ValidationResult.PASSED
                
        finally:
            validation_system.suite_executor = original_handler

    @pytest.mark.asyncio
    async def test_get_validation_status(self, validation_system):
        """Test getting validation system status."""
        status = await validation_system.get_validation_status()
        
        assert status["initialized"] is True
        assert status["validation_level"] == ValidationLevel.COMPREHENSIVE.value
        assert status["total_reports"] == 0  # No reports yet
        assert status["system_health"] == "healthy"

    @pytest.mark.asyncio
    async def test_validation_levels(self):
        """Test different validation levels."""
        # Test basic level
        basic_system = create_ssot_validation_system(ValidationLevel.BASIC)
        await basic_system.initialize()
        
        suite = basic_system._create_validation_suite("Agent-3", {})
        assert len(suite.tests) == 2  # Only basic and integration
        
        await basic_system.shutdown()
        
        # Test comprehensive level
        comprehensive_system = create_ssot_validation_system(ValidationLevel.COMPREHENSIVE)
        await comprehensive_system.initialize()
        
        suite = comprehensive_system._create_validation_suite("Agent-3", {})
        assert len(suite.tests) == 3  # Basic, integration, and comprehensive
        
        await comprehensive_system.shutdown()

    @pytest.mark.asyncio
    async def test_global_instance(self):
        """Test global instance management."""
        # Get global instance
        system1 = get_ssot_validation_system()
        system2 = get_ssot_validation_system()
        
        # Should be the same instance
        assert system1 is system2

    @pytest.mark.asyncio
    async def test_error_handling_initialization_failure(self):
        """Test error handling during initialization."""
        # Create system without proper initialization
        system = SSOTValidationSystem()
        
        # Try to validate without initialization
        result = await system.validate_ssot_integration("Agent-3", {})
        
        # Should auto-initialize and return results
        assert "summary" in result

    @pytest.mark.asyncio
    async def test_concurrent_validation(self, sample_validation_config):
        """Test concurrent validation execution."""
        # Create multiple validation systems
        systems = []
        for i in range(3):
            system = create_ssot_validation_system(ValidationLevel.BASIC)
            await system.initialize()
            systems.append(system)
        
        try:
            # Mock successful execution
            async def mock_execute_suite(context):
                return [
                    {
                        "test_id": f"test_{context['agent_id']}",
                        "status": ValidationResult.PASSED,
                        "execution_time": 0.1,
                        "details": {"message": "Test passed"},
                    }
                ]
            
            # Run validations concurrently
            tasks = []
            for i, system in enumerate(systems):
                system.suite_executor.execute_suite = mock_execute_suite
                task = system.validate_ssot_integration(f"Agent-{i}", sample_validation_config)
                tasks.append(task)
            
            # Execute all validations concurrently
            start_time = time.time()
            results = await asyncio.gather(*tasks)
            execution_time = time.time() - start_time
            
            # Verify all completed successfully
            assert len(results) == 3
            for result in results:
                assert "summary" in result
                assert result["summary"]["passed_tests"] == 1
            
            # Should complete quickly due to concurrency
            assert execution_time < 1.0
            
        finally:
            for system in systems:
                await system.shutdown()


# Performance tests
class TestSSOTValidationSystemPerformance:
    """Performance tests for SSOT Validation System."""

    @pytest.mark.asyncio
    async def test_large_validation_suite_performance(self):
        """Test performance with a large validation suite."""
        system = create_ssot_validation_system(ValidationLevel.COMPREHENSIVE)
        await system.initialize()
        
        try:
            # Create large validation suite
            config = get_unified_config().get_config()"agent_id": "Agent-Performance", "timeout": 300}
            
            # Mock fast execution
            async def mock_execute_suite(context):
                # Simulate 50 tests
                results = []
                for i in range(50):
                    results.append({
                        "test_id": f"test_{i}",
                        "status": ValidationResult.PASSED,
                        "execution_time": 0.001,
                        "details": {"message": f"Test {i} passed"},
                    })
                return results
            
            system.suite_executor.execute_suite = mock_execute_suite
            
            # Measure execution time
            start_time = time.time()
            result = await system.validate_ssot_integration("Agent-Performance", config)
            execution_time = time.time() - start_time
            
            # Verify results
            assert result["summary"]["total_tests"] == 50
            assert result["summary"]["passed_tests"] == 50
            assert execution_time < 2.0  # Should complete within 2 seconds
            
        finally:
            await system.shutdown()

    @pytest.mark.asyncio
    async def test_memory_usage_validation(self):
        """Test memory usage during validation."""
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Create and run validation
        system = create_ssot_validation_system(ValidationLevel.COMPREHENSIVE)
        await system.initialize()
        
        try:
            # Mock execution
            async def mock_execute_suite(context):
                return [
                    {
                        "test_id": "memory_test",
                        "status": ValidationResult.PASSED,
                        "execution_time": 0.1,
                        "details": {"message": "Memory test passed"},
                    }
                ]
            
            system.suite_executor.execute_suite = mock_execute_suite
            
            # Run validation
            result = await system.validate_ssot_integration("Agent-Memory", {})
            
            # Check memory usage
            final_memory = process.memory_info().rss
            memory_increase = final_memory - initial_memory
            
            # Memory increase should be reasonable (less than 10MB)
            assert memory_increase < 10 * 1024 * 1024
            
        finally:
            await system.shutdown()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

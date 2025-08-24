#!/usr/bin/env python3
"""
Testing Framework Core Tests - TDD Implementation
=================================================

Tests for core enums and data classes of the modular testing framework.
"""

import pytest

from src.core.testing_framework import (
    TestStatus,
    TestType,
    TestPriority,
    TestResult,
    TestScenario,
    TestEnvironment,
)


class TestTestStatus:
    """Test TestStatus enum following TDD principles"""

    @pytest.mark.unit
    def test_status_values(self):
        """Test that all status values are valid."""
        statuses = [
            TestStatus.PENDING,
            TestStatus.RUNNING,
            TestStatus.PASSED,
            TestStatus.FAILED,
            TestStatus.SKIPPED,
            TestStatus.TIMEOUT,
            TestStatus.ERROR,
        ]

        for status in statuses:
            assert status.value in [
                "pending",
                "running",
                "passed",
                "failed",
                "skipped",
                "timeout",
                "error",
            ]


class TestTestType:
    """Test TestType enum following TDD principles"""

    @pytest.mark.unit
    def test_type_values(self):
        """Test that all type values are valid."""
        types = [
            TestType.UNIT,
            TestType.INTEGRATION,
            TestType.END_TO_END,
            TestType.PERFORMANCE,
            TestType.LOAD,
            TestType.STRESS,
            TestType.SECURITY,
            TestType.COMPATIBILITY,
        ]

        for test_type in types:
            assert test_type.value in [
                "unit",
                "integration",
                "end_to_end",
                "performance",
                "load",
                "stress",
                "security",
                "compatibility",
            ]


class TestTestPriority:
    """Test TestPriority enum following TDD principles"""

    @pytest.mark.unit
    def test_priority_values(self):
        """Test that all priority values are valid."""
        priorities = [
            TestPriority.LOW,
            TestPriority.NORMAL,
            TestPriority.HIGH,
            TestPriority.CRITICAL,
        ]

        for priority in priorities:
            assert priority.value in [1, 2, 3, 4]

    @pytest.mark.unit
    def test_priority_ordering(self):
        """Test that priority values are properly ordered."""
        assert TestPriority.LOW.value < TestPriority.NORMAL.value
        assert TestPriority.NORMAL.value < TestPriority.HIGH.value
        assert TestPriority.HIGH.value < TestPriority.CRITICAL.value


class TestTestResult:
    """Test TestResult dataclass following TDD principles"""

    @pytest.mark.unit
    def test_result_creation_with_all_parameters(self):
        """Test creating TestResult with all parameters."""
        result = TestResult(
            test_id="test_123",
            test_name="Test Name",
            test_type=TestType.INTEGRATION,
            status=TestStatus.PASSED,
            start_time=100.0,
            end_time=110.0,
            duration=10.0,
        )

        assert result.test_id == "test_123"
        assert result.test_name == "Test Name"
        assert result.test_type == TestType.INTEGRATION
        assert result.status == TestStatus.PASSED
        assert result.start_time == 100.0
        assert result.end_time == 110.0
        assert result.duration == 10.0
        assert result.error_message is None
        assert result.error_traceback is None
        assert result.metrics == {}
        assert result.logs == []
        assert result.assertions_passed == 0
        assert result.assertions_failed == 0
        assert result.test_data == {}

    @pytest.mark.unit
    def test_result_with_optional_fields(self):
        """Test creating TestResult with optional fields."""
        result = TestResult(
            test_id="test_456",
            test_name="Test With Data",
            test_type=TestType.PERFORMANCE,
            status=TestStatus.FAILED,
            start_time=200.0,
            end_time=205.0,
            duration=5.0,
            error_message="Test failed due to timeout",
            error_traceback="Traceback...",
            metrics={"response_time": 2.5, "throughput": 100},
            logs=["Starting test", "Test completed"],
            assertions_passed=5,
            assertions_failed=1,
            test_data={"input": "test_input", "output": "test_output"},
        )

        assert result.error_message == "Test failed due to timeout"
        assert result.error_traceback == "Traceback..."
        assert result.metrics["response_time"] == 2.5
        assert result.metrics["throughput"] == 100
        assert len(result.logs) == 2
        assert result.assertions_passed == 5
        assert result.assertions_failed == 1
        assert result.test_data["input"] == "test_input"

    @pytest.mark.unit
    def test_result_auto_duration_calculation(self):
        """Test that duration is auto-calculated if not provided."""
        result = TestResult(
            test_id="test_789",
            test_name="Auto Duration Test",
            test_type=TestType.UNIT,
            status=TestStatus.PASSED,
            start_time=100.0,
            end_time=110.0,
            duration=0.0,  # Will be auto-calculated
        )

        assert result.duration == 10.0  # Auto-calculated


class TestTestScenario:
    """Test TestScenario dataclass following TDD principles"""

    @pytest.mark.unit
    def test_scenario_creation_with_all_parameters(self):
        """Test creating TestScenario with all parameters."""
        scenario = TestScenario(
            scenario_id="scenario_123",
            name="Test Scenario",
            description="A test scenario description",
            test_type=TestType.INTEGRATION,
            priority=TestPriority.HIGH,
        )

        assert scenario.scenario_id == "scenario_123"
        assert scenario.name == "Test Scenario"
        assert scenario.description == "A test scenario description"
        assert scenario.test_type == TestType.INTEGRATION
        assert scenario.priority == TestPriority.HIGH
        assert scenario.timeout == 300.0
        assert scenario.retry_count == 0
        assert scenario.max_retries == 3
        assert scenario.dependencies == []
        assert scenario.setup_steps == []
        assert scenario.test_steps == []
        assert scenario.cleanup_steps == []
        assert scenario.assertions == []
        assert scenario.metadata == {}

    @pytest.mark.unit
    def test_scenario_with_custom_values(self):
        """Test creating a scenario with custom values."""
        scenario = TestScenario(
            scenario_id="custom_scenario",
            name="Custom Scenario",
            description="Custom scenario with steps",
            test_type=TestType.END_TO_END,
            priority=TestPriority.CRITICAL,
            timeout=600.0,
            retry_count=1,
            max_retries=5,
            dependencies=["dependency1", "dependency2"],
            metadata={"version": "1.0.0", "environment": "production"},
        )

        assert scenario.timeout == 600.0
        assert scenario.retry_count == 1
        assert scenario.max_retries == 5
        assert len(scenario.dependencies) == 2
        assert scenario.metadata["version"] == "1.0.0"

    @pytest.mark.unit
    def test_scenario_validation_timeout(self):
        """Test scenario validation for invalid timeout."""
        with pytest.raises(ValueError, match="Timeout must be positive"):
            TestScenario(
                scenario_id="invalid",
                name="Invalid Scenario",
                description="Invalid scenario",
                test_type=TestType.INTEGRATION,
                priority=TestPriority.NORMAL,
                timeout=0.0
            )

    @pytest.mark.unit
    def test_scenario_validation_retries(self):
        """Test scenario validation for invalid retry count."""
        with pytest.raises(ValueError, match="Retry count cannot exceed max retries"):
            TestScenario(
                scenario_id="invalid",
                name="Invalid Scenario",
                description="Invalid scenario",
                test_type=TestType.INTEGRATION,
                priority=TestPriority.NORMAL,
                retry_count=5,
                max_retries=3
            )


class TestTestEnvironment:
    """Test TestEnvironment dataclass following TDD principles"""

    @pytest.mark.unit
    def test_environment_creation_with_all_parameters(self):
        """Test creating TestEnvironment with all parameters."""
        environment = TestEnvironment(
            environment_id="env_123",
            name="Test Environment",
            description="A test environment",
        )

        assert environment.environment_id == "env_123"
        assert environment.name == "Test Environment"
        assert environment.description == "A test environment"
        assert environment.systems == []
        assert environment.services == []
        assert environment.config_overrides == {}
        assert environment.cleanup_on_exit is True
        assert environment.parallel_execution is False
        assert environment.max_parallel_tests == 5

    @pytest.mark.unit
    def test_environment_with_custom_values(self):
        """Test creating an environment with custom values."""
        environment = TestEnvironment(
            environment_id="custom_env",
            name="Custom Environment",
            description="Custom environment with settings",
            cleanup_on_exit=False,
            parallel_execution=True,
            max_parallel_tests=10,
        )

        assert environment.cleanup_on_exit is False
        assert environment.parallel_execution is True
        assert environment.max_parallel_tests == 10

    @pytest.mark.unit
    def test_environment_validation_parallel_tests(self):
        """Test environment validation for invalid parallel tests."""
        with pytest.raises(ValueError, match="Max parallel tests must be positive"):
            TestEnvironment(
                environment_id="invalid",
                name="Invalid Environment",
                description="Invalid environment",
                max_parallel_tests=0
            )

    @pytest.mark.unit
    def test_environment_auto_disable_parallel(self):
        """Test that parallel execution is auto-disabled for single test."""
        environment = TestEnvironment(
            environment_id="auto_disable",
            name="Auto Disable Environment",
            description="Environment that auto-disables parallel execution",
            parallel_execution=True,
            max_parallel_tests=1
        )

        assert environment.parallel_execution is False


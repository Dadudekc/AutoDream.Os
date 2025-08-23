"""
Test suite for Integration Testing Framework
Comprehensive testing of all integration testing components.
"""

import pytest
import asyncio
import json
import time
import uuid
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from pathlib import Path
import tempfile
import shutil

# Import the components we're testing
from src.services.integration_testing_framework import (
    IntegrationTestRunner,
    IntegrationTestSuite,
    CrossSystemCommunicationTest,
    APIIntegrationTest,
    MiddlewareIntegrationTest,
    TestStatus,
    TestType,
    TestPriority,
    TestResult,
    TestScenario,
    TestEnvironment,
)


class TestTestStatus:
    """Test suite for TestStatus enum."""

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
    """Test suite for TestType enum."""

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
    """Test suite for TestPriority enum."""

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

    def test_priority_ordering(self):
        """Test that priority values are properly ordered."""
        assert TestPriority.LOW.value < TestPriority.NORMAL.value
        assert TestPriority.NORMAL.value < TestPriority.HIGH.value
        assert TestPriority.HIGH.value < TestPriority.CRITICAL.value


class TestTestResult:
    """Test suite for TestResult dataclass."""

    def test_result_creation(self):
        """Test creating a test result."""
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

    def test_result_with_optional_fields(self):
        """Test creating a test result with optional fields."""
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


class TestTestScenario:
    """Test suite for TestScenario dataclass."""

    def test_scenario_creation(self):
        """Test creating a test scenario."""
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

    def test_scenario_with_custom_values(self):
        """Test creating a scenario with custom values."""

        def setup_step():
            pass

        def test_step():
            pass

        def cleanup_step():
            pass

        def assertion():
            pass

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
            setup_steps=[setup_step],
            test_steps=[test_step],
            cleanup_steps=[cleanup_step],
            assertions=[assertion],
            metadata={"version": "1.0.0", "environment": "production"},
        )

        assert scenario.timeout == 600.0
        assert scenario.retry_count == 1
        assert scenario.max_retries == 5
        assert len(scenario.dependencies) == 2
        assert len(scenario.setup_steps) == 1
        assert len(scenario.test_steps) == 1
        assert len(scenario.cleanup_steps) == 1
        assert len(scenario.assertions) == 1
        assert scenario.metadata["version"] == "1.0.0"


class TestTestEnvironment:
    """Test suite for TestEnvironment dataclass."""

    def test_environment_creation(self):
        """Test creating a test environment."""
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


class TestBaseIntegrationTest:
    """Test suite for BaseIntegrationTest abstract class."""

    def test_abstract_class_instantiation(self):
        """Test that BaseIntegrationTest cannot be instantiated."""
        with pytest.raises(TypeError):
            BaseIntegrationTest("test_name", TestType.INTEGRATION)

    def test_abstract_methods(self):
        """Test that abstract methods are defined."""
        # This test ensures the abstract methods exist
        assert hasattr(BaseIntegrationTest, "setup")
        assert hasattr(BaseIntegrationTest, "execute")
        assert hasattr(BaseIntegrationTest, "cleanup")
        assert hasattr(BaseIntegrationTest, "validate")


class TestCrossSystemCommunicationTest:
    """Test suite for CrossSystemCommunicationTest."""

    @pytest.fixture
    def communication_test(self):
        """Create a test communication test instance."""
        return CrossSystemCommunicationTest("test_communication", TestPriority.HIGH)

    def test_test_initialization(self, communication_test):
        """Test test initialization."""
        assert communication_test.test_name == "test_communication"
        assert communication_test.test_type == TestType.INTEGRATION
        assert communication_test.priority == TestPriority.HIGH
        assert communication_test.status == TestStatus.PENDING
        assert communication_test.start_time == 0.0
        assert communication_test.end_time == 0.0
        assert len(communication_test.logs) == 0
        assert communication_test.assertions_passed == 0
        assert communication_test.assertions_failed == 0

    def test_logging(self, communication_test):
        """Test test logging functionality."""
        communication_test.log("Test log message")
        communication_test.log("Error message", "ERROR")

        assert len(communication_test.logs) == 2
        assert "Test log message" in communication_test.logs[0]
        assert "ERROR" in communication_test.logs[1]

    def test_assertions(self, communication_test):
        """Test test assertion methods."""
        # Test assert_true
        communication_test.assert_true(True, "This should pass")
        assert communication_test.assertions_passed == 1
        assert communication_test.assertions_failed == 0

        # Test assert_false
        communication_test.assert_false(False, "This should pass")
        assert communication_test.assertions_passed == 2
        assert communication_test.assertions_failed == 0

        # Test assert_equal
        communication_test.assert_equal(5, 5, "Values should be equal")
        assert communication_test.assertions_passed == 3
        assert communication_test.assertions_failed == 0

        # Test assert_not_equal
        communication_test.assert_not_equal(5, 10, "Values should not be equal")
        assert communication_test.assertions_passed == 4
        assert communication_test.assertions_failed == 0

        # Test assert_in
        communication_test.assert_in(
            "item", ["item", "other"], "Item should be in list"
        )
        assert communication_test.assertions_passed == 5
        assert communication_test.assertions_failed == 0

        # Test assert_not_in
        communication_test.assert_not_in(
            "missing", ["item", "other"], "Item should not be in list"
        )
        assert communication_test.assertions_passed == 6
        assert communication_test.assertions_failed == 0

        # Test assert_is_none
        communication_test.assert_is_none(None, "Value should be None")
        assert communication_test.assertions_passed == 7
        assert communication_test.assertions_failed == 0

        # Test assert_is_not_none
        communication_test.assert_is_not_none("value", "Value should not be None")
        assert communication_test.assertions_passed == 8
        assert communication_test.assertions_failed == 0

    def test_assertion_failures(self, communication_test):
        """Test assertion failure scenarios."""
        # Test assert_true failure
        with pytest.raises(AssertionError):
            communication_test.assert_true(False, "This should fail")
        assert communication_test.assertions_failed == 1

        # Test assert_equal failure
        with pytest.raises(AssertionError):
            communication_test.assert_equal(5, 10, "Values should be equal")
        assert communication_test.assertions_failed == 2

    @pytest.mark.asyncio
    async def test_test_execution_workflow(self, communication_test):
        """Test the complete test execution workflow."""
        # Mock the abstract methods
        communication_test.setup = AsyncMock(return_value=True)
        communication_test.execute = AsyncMock(return_value=True)
        communication_test.cleanup = AsyncMock(return_value=True)
        communication_test.validate = AsyncMock(return_value=True)

        # Run the test
        result = await communication_test.run()

        # Verify all methods were called
        communication_test.setup.assert_called_once()
        communication_test.execute.assert_called_once()
        communication_test.cleanup.assert_called_once()
        communication_test.validate.assert_called_once()

        # Verify result
        assert result.status == TestStatus.PASSED
        assert result.duration > 0
        assert result.assertions_passed >= 0
        assert result.assertions_failed == 0

    @pytest.mark.asyncio
    async def test_test_execution_with_failure(self, communication_test):
        """Test test execution with a failure."""
        # Mock the abstract methods with a failure
        communication_test.setup = AsyncMock(return_value=True)
        communication_test.execute = AsyncMock(return_value=False)
        communication_test.cleanup = AsyncMock(return_value=True)
        communication_test.validate = AsyncMock(return_value=True)

        # Run the test
        result = await communication_test.run()

        # Verify result shows failure
        assert result.status == TestStatus.FAILED
        assert result.error_message == "Test execution failed"
        assert result.duration > 0

    @pytest.mark.asyncio
    async def test_test_execution_with_exception(self, communication_test):
        """Test test execution with an exception."""
        # Mock the execute method to raise an exception
        communication_test.setup = AsyncMock(return_value=True)
        communication_test.execute = AsyncMock(side_effect=Exception("Test exception"))
        communication_test.cleanup = AsyncMock(return_value=True)
        communication_test.validate = AsyncMock(return_value=True)

        # Run the test
        result = await communication_test.run()

        # Verify result shows error
        assert result.status == TestStatus.FAILED
        assert "Test exception" in result.error_message
        assert result.error_traceback is not None
        assert result.duration > 0


class TestAPIIntegrationTest:
    """Test suite for APIIntegrationTest."""

    @pytest.fixture
    def api_test(self):
        """Create a test API integration test instance."""
        return APIIntegrationTest("test_api", TestPriority.NORMAL)

    def test_test_initialization(self, api_test):
        """Test test initialization."""
        assert api_test.test_name == "test_api"
        assert api_test.test_type == TestType.INTEGRATION
        assert api_test.priority == TestPriority.NORMAL
        assert api_test.status == TestStatus.PENDING

    @pytest.mark.asyncio
    async def test_test_execution_workflow(self, api_test):
        """Test the complete test execution workflow."""
        # Mock the abstract methods
        api_test.setup = AsyncMock(return_value=True)
        api_test.execute = AsyncMock(return_value=True)
        api_test.cleanup = AsyncMock(return_value=True)
        api_test.validate = AsyncMock(return_value=True)

        # Run the test
        result = await api_test.run()

        # Verify result
        assert result.status == TestStatus.PASSED
        assert result.duration > 0


class TestMiddlewareIntegrationTest:
    """Test suite for MiddlewareIntegrationTest."""

    @pytest.fixture
    def middleware_test(self):
        """Create a test middleware integration test instance."""
        return MiddlewareIntegrationTest("test_middleware", TestPriority.LOW)

    def test_test_initialization(self, middleware_test):
        """Test test initialization."""
        assert middleware_test.test_name == "test_middleware"
        assert middleware_test.test_type == TestType.INTEGRATION
        assert middleware_test.priority == TestPriority.LOW
        assert middleware_test.status == TestStatus.PENDING

    @pytest.mark.asyncio
    async def test_test_execution_workflow(self, middleware_test):
        """Test the complete test execution workflow."""
        # Mock the abstract methods
        middleware_test.setup = AsyncMock(return_value=True)
        middleware_test.execute = AsyncMock(return_value=True)
        middleware_test.cleanup = AsyncMock(return_value=True)
        middleware_test.validate = AsyncMock(return_value=True)

        # Run the test
        result = await middleware_test.run()

        # Verify result
        assert result.status == TestStatus.PASSED
        assert result.duration > 0


class TestIntegrationTestSuite:
    """Test suite for IntegrationTestSuite."""

    @pytest.fixture
    def test_suite(self):
        """Create a test suite instance."""
        return IntegrationTestSuite("Test Suite", "A test suite description")

    @pytest.fixture
    def mock_test(self):
        """Create a mock test."""
        test = Mock()
        test.test_name = "Mock Test"
        test.run = AsyncMock(return_value=Mock(status=TestStatus.PASSED))
        return test

    def test_suite_initialization(self, test_suite):
        """Test suite initialization."""
        assert test_suite.name == "Test Suite"
        assert test_suite.description == "A test suite description"
        assert len(test_suite.tests) == 0
        assert len(test_suite.results) == 0
        assert test_suite.start_time == 0.0
        assert test_suite.end_time == 0.0
        assert test_suite.running is False
        assert test_suite.parallel_execution is False
        assert test_suite.max_parallel_tests == 5
        assert test_suite.stop_on_failure is False
        assert test_suite.retry_failed_tests is False
        assert test_suite.max_retries == 3

    def test_add_test(self, test_suite, mock_test):
        """Test adding a test to the suite."""
        test_suite.add_test(mock_test)

        assert len(test_suite.tests) == 1
        assert test_suite.tests[0] == mock_test

    def test_remove_test(self, test_suite, mock_test):
        """Test removing a test from the suite."""
        # First add a test
        test_suite.add_test(mock_test)

        # Then remove it
        success = test_suite.remove_test("Mock Test")

        assert success is True
        assert len(test_suite.tests) == 0

    def test_remove_nonexistent_test(self, test_suite):
        """Test removing a non-existent test."""
        success = test_suite.remove_test("Nonexistent Test")

        assert success is False

    def test_get_test(self, test_suite, mock_test):
        """Test getting a test by name."""
        test_suite.add_test(mock_test)

        retrieved_test = test_suite.get_test("Mock Test")

        assert retrieved_test == mock_test

    def test_get_nonexistent_test(self, test_suite):
        """Test getting a non-existent test."""
        retrieved_test = test_suite.get_test("Nonexistent Test")

        assert retrieved_test is None

    @pytest.mark.asyncio
    async def test_run_suite_sequential(self, test_suite, mock_test):
        """Test running the suite sequentially."""
        test_suite.add_test(mock_test)
        test_suite.parallel_execution = False

        results = await test_suite.run_suite()

        assert len(results) == 1
        assert results[0].status == TestStatus.PASSED
        assert test_suite.running is False
        assert test_suite.start_time > 0
        assert test_suite.end_time > 0

    @pytest.mark.asyncio
    async def test_run_suite_parallel(self, test_suite):
        """Test running the suite in parallel."""
        # Add multiple tests
        for i in range(3):
            test = Mock()
            test.test_name = f"Test {i}"
            test.run = AsyncMock(return_value=Mock(status=TestStatus.PASSED))
            test_suite.add_test(test)

        test_suite.parallel_execution = True
        test_suite.max_parallel_tests = 2

        results = await test_suite.run_suite()

        assert len(results) == 3
        assert test_suite.running is False

    @pytest.mark.asyncio
    async def test_run_suite_with_failure(self, test_suite):
        """Test running the suite with a test failure."""
        # Add a failing test
        failing_test = Mock()
        failing_test.test_name = "Failing Test"
        failing_test.run = AsyncMock(return_value=Mock(status=TestStatus.FAILED))
        test_suite.add_test(failing_test)

        test_suite.stop_on_failure = True

        results = await test_suite.run_suite()

        assert len(results) == 1
        assert results[0].status == TestStatus.FAILED

    def test_get_summary(self, test_suite):
        """Test getting suite summary."""
        summary = test_suite.get_summary()

        assert summary["name"] == "Test Suite"
        assert summary["description"] == "A test suite description"
        assert summary["status"] == "not_run"
        assert summary["total_tests"] == 0
        assert summary["executed_tests"] == 0
        assert summary["passed"] == 0
        assert summary["failed"] == 0
        assert summary["duration"] == 0.0

    def test_get_summary_with_results(self, test_suite, mock_test):
        """Test getting suite summary with results."""
        test_suite.add_test(mock_test)
        test_suite.results = [Mock(status=TestStatus.PASSED)]
        test_suite.start_time = 100.0
        test_suite.end_time = 110.0

        summary = test_suite.get_summary()

        assert summary["status"] == "completed"
        assert summary["total_tests"] == 1
        assert summary["executed_tests"] == 1
        assert summary["passed"] == 1
        assert summary["failed"] == 0
        assert summary["duration"] == 10.0
        assert summary["success_rate"] == 100.0

    def test_export_results(self, test_suite, mock_test, tmp_path):
        """Test exporting test results."""
        test_suite.add_test(mock_test)
        test_suite.results = [
            Mock(
                test_id="test_123",
                test_name="Test Name",
                test_type=TestType.INTEGRATION,
                status=TestStatus.PASSED,
                start_time=100.0,
                end_time=110.0,
                duration=10.0,
                error_message=None,
                error_traceback=None,
                metrics={},
                logs=["Test log"],
                assertions_passed=5,
                assertions_failed=0,
                test_data={},
            )
        ]

        export_file = tmp_path / "test_results.json"
        success = test_suite.export_results(str(export_file))

        assert success is True
        assert export_file.exists()

        # Verify exported content
        with open(export_file, "r") as f:
            exported_data = json.load(f)

        assert "summary" in exported_data
        assert "results" in exported_data
        assert len(exported_data["results"]) == 1
        assert exported_data["results"][0]["test_name"] == "Test Name"


class TestIntegrationTestRunner:
    """Test suite for IntegrationTestRunner."""

    @pytest.fixture
    def test_runner(self):
        """Create a test runner instance."""
        return IntegrationTestRunner()

    @pytest.fixture
    def mock_suite(self):
        """Create a mock test suite."""
        suite = Mock()
        suite.name = "Mock Suite"
        suite.run_suite = AsyncMock(return_value=[Mock(status=TestStatus.PASSED)])
        suite.get_summary = Mock(return_value={"name": "Mock Suite", "total_tests": 1})
        return suite

    def test_runner_initialization(self, test_runner):
        """Test runner initialization."""
        assert len(test_runner.test_suites) == 0
        assert test_runner.global_config == {}
        assert test_runner.running is False

    def test_add_test_suite(self, test_runner, mock_suite):
        """Test adding a test suite to the runner."""
        test_runner.add_test_suite(mock_suite)

        assert len(test_runner.test_suites) == 1
        assert test_runner.test_suites["Mock Suite"] == mock_suite

    def test_remove_test_suite(self, test_runner, mock_suite):
        """Test removing a test suite from the runner."""
        # First add a suite
        test_runner.add_test_suite(mock_suite)

        # Then remove it
        success = test_runner.remove_test_suite("Mock Suite")

        assert success is True
        assert len(test_runner.test_suites) == 0

    def test_remove_nonexistent_suite(self, test_runner):
        """Test removing a non-existent suite."""
        success = test_runner.remove_test_suite("Nonexistent Suite")

        assert success is False

    def test_get_test_suite(self, test_runner, mock_suite):
        """Test getting a test suite by name."""
        test_runner.add_test_suite(mock_suite)

        retrieved_suite = test_runner.get_test_suite("Mock Suite")

        assert retrieved_suite == mock_suite

    def test_get_nonexistent_suite(self, test_runner):
        """Test getting a non-existent suite."""
        retrieved_suite = test_runner.get_test_suite("Nonexistent Suite")

        assert retrieved_suite is None

    @pytest.mark.asyncio
    async def test_run_all_suites(self, test_runner, mock_suite):
        """Test running all test suites."""
        test_runner.add_test_suite(mock_suite)

        results = await test_runner.run_all_suites()

        assert "Mock Suite" in results
        assert len(results["Mock Suite"]) == 1
        assert test_runner.running is False

    @pytest.mark.asyncio
    async def test_run_specific_suite(self, test_runner, mock_suite):
        """Test running a specific test suite."""
        test_runner.add_test_suite(mock_suite)

        results = await test_runner.run_specific_suite("Mock Suite")

        assert len(results) == 1
        assert results[0].status == TestStatus.PASSED

    @pytest.mark.asyncio
    async def test_run_nonexistent_suite(self, test_runner):
        """Test running a non-existent suite."""
        results = await test_runner.run_specific_suite("Nonexistent Suite")

        assert results is None

    def test_get_global_summary(self, test_runner, mock_suite):
        """Test getting global summary."""
        test_runner.add_test_suite(mock_suite)

        summary = test_runner.get_global_summary()

        assert summary["total_suites"] == 1
        assert summary["total_tests"] == 1
        assert summary["status"] == "ready"
        assert "Mock Suite" in summary["suite_statuses"]

    def test_export_global_results(self, test_runner, mock_suite, tmp_path):
        """Test exporting global results."""
        test_runner.add_test_suite(mock_suite)

        export_file = tmp_path / "global_results.json"
        success = test_runner.export_global_results(str(export_file))

        assert success is True
        assert export_file.exists()

        # Verify exported content
        with open(export_file, "r") as f:
            exported_data = json.load(f)

        assert "global_summary" in exported_data
        assert "suite_results" in exported_data
        assert "export_timestamp" in exported_data


class TestIntegrationEndToEnd:
    """End-to-end integration tests."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.mark.asyncio
    async def test_full_test_workflow(self, temp_dir):
        """Test a complete test workflow."""
        # Create test runner
        runner = IntegrationTestRunner()

        # Create test suite
        suite = IntegrationTestSuite("E2E Test Suite", "End-to-end test suite")

        # Add mock tests
        for i in range(3):
            test = Mock()
            test.test_name = f"Test {i}"
            test.run = AsyncMock(return_value=Mock(status=TestStatus.PASSED))
            suite.add_test(test)

        # Add suite to runner
        runner.add_test_suite(suite)

        # Run all suites
        results = await runner.run_all_suites()

        # Verify results
        assert "E2E Test Suite" in results
        assert len(results["E2E Test Suite"]) == 3

        # Get global summary
        summary = runner.get_global_summary()
        assert summary["total_suites"] == 1
        assert summary["total_tests"] == 3
        assert summary["status"] == "ready"

    @pytest.mark.asyncio
    async def test_test_execution_with_different_statuses(self, temp_dir):
        """Test test execution with different statuses."""
        # Create test suite
        suite = IntegrationTestSuite(
            "Status Test Suite", "Test suite with different statuses"
        )

        # Add tests with different outcomes
        passed_test = Mock()
        passed_test.test_name = "Passed Test"
        passed_test.run = AsyncMock(return_value=Mock(status=TestStatus.PASSED))

        failed_test = Mock()
        failed_test.test_name = "Failed Test"
        failed_test.run = AsyncMock(return_value=Mock(status=TestStatus.FAILED))

        suite.add_test(passed_test)
        suite.add_test(failed_test)

        # Run suite
        results = await suite.run_suite()

        # Verify results
        assert len(results) == 2
        statuses = [result.status for result in results]
        assert TestStatus.PASSED in statuses
        assert TestStatus.FAILED in statuses

        # Get summary
        summary = suite.get_summary()
        assert summary["passed"] == 1
        assert summary["failed"] == 1
        assert summary["success_rate"] == 50.0


class TestPerformanceAndLoad:
    """Performance and load testing."""

    @pytest.mark.asyncio
    async def test_suite_performance(self):
        """Test suite performance under load."""
        suite = IntegrationTestSuite("Performance Suite", "Performance test suite")

        # Add many tests
        start_time = time.time()
        for i in range(100):
            test = Mock()
            test.test_name = f"Performance Test {i}"
            test.run = AsyncMock(return_value=Mock(status=TestStatus.PASSED))
            suite.add_test(test)

        end_time = time.time()
        add_time = end_time - start_time

        # Should add 100 tests in reasonable time
        assert add_time < 0.1  # Less than 100ms for 100 tests
        assert len(suite.tests) == 100

        # Test summary retrieval performance
        start_time = time.time()
        summary = suite.get_summary()
        end_time = time.time()
        summary_time = end_time - start_time

        # Should get summary in reasonable time
        assert summary_time < 0.01  # Less than 10ms for summary
        assert summary["total_tests"] == 100

    @pytest.mark.asyncio
    async def test_runner_performance(self):
        """Test runner performance under load."""
        runner = IntegrationTestRunner()

        # Add many suites
        start_time = time.time()
        for i in range(50):
            suite = Mock()
            suite.name = f"Suite {i}"
            suite.run_suite = AsyncMock(return_value=[])
            suite.get_summary = Mock(
                return_value={"name": f"Suite {i}", "total_tests": 10}
            )
            runner.add_test_suite(suite)

        end_time = time.time()
        add_time = end_time - start_time

        # Should add 50 suites in reasonable time
        assert add_time < 0.1  # Less than 100ms for 50 suites
        assert len(runner.test_suites) == 50

        # Test global summary retrieval performance
        start_time = time.time()
        summary = runner.get_global_summary()
        end_time = time.time()
        summary_time = end_time - start_time

        # Should get global summary in reasonable time
        assert summary_time < 0.01  # Less than 10ms for global summary
        assert summary["total_suites"] == 50
        assert summary["total_tests"] == 500


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])

"""
Smoke Tests for Cross-System Communication and Integration Testing
Lightweight tests to verify basic functionality and integration.
"""

import pytest
import asyncio
import tempfile
import shutil
from pathlib import Path

# Import the components we're testing
from src.services.cross_system_communication import (
    CrossSystemCommunicationManager,
    SystemEndpoint,
    CrossSystemMessage,
    CommunicationProtocol,
    MessageType,
    MessagePriority,
)
from src.services.integration_testing_framework import (
    IntegrationTestRunner,
    IntegrationTestSuite,
    CrossSystemCommunicationTest,
    APIIntegrationTest,
    MiddlewareIntegrationTest,
    TestStatus,
    TestType,
    TestPriority,
)


class TestCrossSystemCommunicationSmoke:
    """Smoke tests for cross-system communication."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.mark.asyncio
    async def test_communication_manager_initialization(self, temp_dir):
        """Test that communication manager initializes correctly."""
        manager = CrossSystemCommunicationManager()

        # Verify initial state
        assert len(manager.endpoints) == 0
        assert len(manager.handlers) == 0
        assert manager.running is False
        assert len(manager.connection_callbacks) == 0
        assert len(manager.message_callbacks) == 0
        assert len(manager.error_callbacks) == 0

        # Verify metrics
        metrics = manager.get_metrics()
        assert metrics.total_messages_sent == 0
        assert metrics.total_messages_received == 0
        assert metrics.successful_communications == 0
        assert metrics.failed_communications == 0
        assert metrics.active_connections == 0

    @pytest.mark.asyncio
    async def test_endpoint_management(self, temp_dir):
        """Test basic endpoint management functionality."""
        manager = CrossSystemCommunicationManager()

        # Create test endpoint
        endpoint = SystemEndpoint(
            system_id="test_system",
            name="Test System",
            protocol=CommunicationProtocol.HTTP,
            host="localhost",
            port=8000,
        )

        # Add endpoint
        success = manager.add_endpoint(endpoint)
        assert success is True
        assert len(manager.endpoints) == 1
        assert "test_system" in manager.endpoints

        # Get system status
        status = manager.get_system_status()
        assert "test_system" in status
        assert status["test_system"]["name"] == "Test System"
        assert status["test_system"]["protocol"] == "http"
        assert status["test_system"]["host"] == "localhost"
        assert status["test_system"]["port"] == 8000

        # Remove endpoint
        success = manager.remove_endpoint("test_system")
        assert success is True
        assert len(manager.endpoints) == 0

    @pytest.mark.asyncio
    async def test_message_creation(self, temp_dir):
        """Test message creation and validation."""
        # Create test message
        message = CrossSystemMessage(
            message_id="test_msg_123",
            source_system="system_a",
            target_system="system_b",
            message_type=MessageType.REQUEST,
            priority=MessagePriority.HIGH,
            timestamp=1234567890.0,
            payload={"test": "data", "value": 42},
        )

        # Verify message structure
        assert message.message_id == "test_msg_123"
        assert message.source_system == "system_a"
        assert message.target_system == "system_b"
        assert message.message_type == MessageType.REQUEST
        assert message.priority == MessagePriority.HIGH
        assert message.timestamp == 1234567890.0
        assert message.payload["test"] == "data"
        assert message.payload["value"] == 42

        # Verify default values
        assert message.headers == {}
        assert message.correlation_id is None
        assert message.reply_to is None
        assert message.ttl is None
        assert message.retry_count == 0
        assert message.max_retries == 3

    @pytest.mark.asyncio
    async def test_protocol_enumeration(self, temp_dir):
        """Test communication protocol enumeration."""
        protocols = [
            CommunicationProtocol.HTTP,
            CommunicationProtocol.HTTPS,
            CommunicationProtocol.WEBSOCKET,
            CommunicationProtocol.TCP,
            CommunicationProtocol.UDP,
        ]

        # Verify all protocols have valid values
        for protocol in protocols:
            assert protocol.value in ["http", "https", "websocket", "tcp", "udp"]

        # Verify protocol creation from string
        assert CommunicationProtocol("http") == CommunicationProtocol.HTTP
        assert CommunicationProtocol("https") == CommunicationProtocol.HTTPS
        assert CommunicationProtocol("websocket") == CommunicationProtocol.WEBSOCKET
        assert CommunicationProtocol("tcp") == CommunicationProtocol.TCP
        assert CommunicationProtocol("udp") == CommunicationProtocol.UDP

    @pytest.mark.asyncio
    async def test_message_types_and_priorities(self, temp_dir):
        """Test message types and priorities."""
        # Test message types
        message_types = [
            MessageType.REQUEST,
            MessageType.RESPONSE,
            MessageType.EVENT,
            MessageType.COMMAND,
            MessageType.QUERY,
            MessageType.NOTIFICATION,
            MessageType.HEARTBEAT,
            MessageType.ERROR,
        ]

        for msg_type in message_types:
            assert msg_type.value in [
                "request",
                "response",
                "event",
                "command",
                "query",
                "notification",
                "heartbeat",
                "error",
            ]

        # Test priorities
        priorities = [
            MessagePriority.LOW,
            MessagePriority.NORMAL,
            MessagePriority.HIGH,
            MessagePriority.CRITICAL,
            MessagePriority.EMERGENCY,
        ]

        for priority in priorities:
            assert priority.value in [1, 2, 3, 4, 5]

        # Verify priority ordering
        assert MessagePriority.LOW.value < MessagePriority.NORMAL.value
        assert MessagePriority.NORMAL.value < MessagePriority.HIGH.value
        assert MessagePriority.HIGH.value < MessagePriority.CRITICAL.value
        assert MessagePriority.CRITICAL.value < MessagePriority.EMERGENCY.value

    @pytest.mark.asyncio
    async def test_manager_lifecycle(self, temp_dir):
        """Test communication manager lifecycle."""
        manager = CrossSystemCommunicationManager()

        # Start manager
        success = await manager.start()
        assert success is True
        assert manager.running is True
        assert manager._message_processor_task is not None
        assert manager._health_check_task is not None

        # Stop manager
        success = await manager.stop()
        assert success is True
        assert manager.running is False
        assert manager._message_processor_task is None
        assert manager._health_check_task is None


class TestIntegrationTestingFrameworkSmoke:
    """Smoke tests for integration testing framework."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.mark.asyncio
    async def test_test_runner_initialization(self, temp_dir):
        """Test that test runner initializes correctly."""
        runner = IntegrationTestRunner()

        # Verify initial state
        assert len(runner.test_suites) == 0
        assert runner.global_config == {}
        assert runner.running is False

    @pytest.mark.asyncio
    async def test_test_suite_creation(self, temp_dir):
        """Test test suite creation and basic functionality."""
        suite = IntegrationTestSuite("Test Suite", "A test suite description")

        # Verify suite initialization
        assert suite.name == "Test Suite"
        assert suite.description == "A test suite description"
        assert len(suite.tests) == 0
        assert len(suite.results) == 0
        assert suite.start_time == 0.0
        assert suite.end_time == 0.0
        assert suite.running is False

        # Verify default settings
        assert suite.parallel_execution is False
        assert suite.max_parallel_tests == 5
        assert suite.stop_on_failure is False
        assert suite.retry_failed_tests is False
        assert suite.max_retries == 3

    @pytest.mark.asyncio
    async def test_test_suite_management(self, temp_dir):
        """Test test suite management functionality."""
        suite = IntegrationTestSuite("Management Suite", "Test suite management")

        # Create mock test
        mock_test = type(
            "MockTest",
            (),
            {
                "test_name": "Mock Test",
                "run": asyncio.coroutine(
                    lambda: type("MockResult", (), {"status": TestStatus.PASSED})()
                ),
            },
        )()

        # Add test
        suite.add_test(mock_test)
        assert len(suite.tests) == 1
        assert suite.tests[0] == mock_test

        # Get test
        retrieved_test = suite.get_test("Mock Test")
        assert retrieved_test == mock_test

        # Remove test
        success = suite.remove_test("Mock Test")
        assert success is True
        assert len(suite.tests) == 0

    @pytest.mark.asyncio
    async def test_test_suite_summary(self, temp_dir):
        """Test test suite summary functionality."""
        suite = IntegrationTestSuite("Summary Suite", "Test suite summary")

        # Get empty summary
        summary = suite.get_summary()
        assert summary["name"] == "Summary Suite"
        assert summary["description"] == "Test suite summary"
        assert summary["status"] == "not_run"
        assert summary["total_tests"] == 0
        assert summary["executed_tests"] == 0
        assert summary["passed"] == 0
        assert summary["failed"] == 0
        assert summary["duration"] == 0.0

    @pytest.mark.asyncio
    async def test_test_runner_management(self, temp_dir):
        """Test test runner management functionality."""
        runner = IntegrationTestRunner()

        # Create mock suite
        mock_suite = type(
            "MockSuite",
            (),
            {
                "name": "Mock Suite",
                "run_suite": asyncio.coroutine(lambda: []),
                "get_summary": lambda: {"name": "Mock Suite", "total_tests": 1},
            },
        )()

        # Add suite
        runner.add_test_suite(mock_suite)
        assert len(runner.test_suites) == 1
        assert runner.test_suites["Mock Suite"] == mock_suite

        # Get suite
        retrieved_suite = runner.get_test_suite("Mock Suite")
        assert retrieved_suite == mock_suite

        # Remove suite
        success = runner.remove_test_suite("Mock Suite")
        assert success is True
        assert len(runner.test_suites) == 0

    @pytest.mark.asyncio
    async def test_test_runner_summary(self, temp_dir):
        """Test test runner summary functionality."""
        runner = IntegrationTestRunner()

        # Get empty summary
        summary = runner.get_global_summary()
        assert summary["total_suites"] == 0
        assert summary["total_tests"] == 0
        assert summary["status"] == "no_suites"

        # Add mock suite
        mock_suite = type(
            "MockSuite",
            (),
            {
                "name": "Mock Suite",
                "run_suite": asyncio.coroutine(lambda: []),
                "get_summary": lambda: {"name": "Mock Suite", "total_tests": 1},
            },
        )()

        runner.add_test_suite(mock_suite)

        # Get summary with suite
        summary = runner.get_global_summary()
        assert summary["total_suites"] == 1
        assert summary["total_tests"] == 1
        assert summary["status"] == "ready"
        assert "Mock Suite" in summary["suite_statuses"]


class TestIntegrationTestClassesSmoke:
    """Smoke tests for integration test classes."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.mark.asyncio
    async def test_cross_system_communication_test(self, temp_dir):
        """Test CrossSystemCommunicationTest basic functionality."""
        test = CrossSystemCommunicationTest("test_communication", TestPriority.HIGH)

        # Verify test initialization
        assert test.test_name == "test_communication"
        assert test.test_type == TestType.INTEGRATION
        assert test.priority == TestPriority.HIGH
        assert test.status == TestStatus.PENDING
        assert test.start_time == 0.0
        assert test.end_time == 0.0
        assert len(test.logs) == 0
        assert test.assertions_passed == 0
        assert test.assertions_failed == 0

        # Test logging
        test.log("Test log message")
        assert len(test.logs) == 1
        assert "Test log message" in test.logs[0]

        # Test assertions
        test.assert_true(True, "This should pass")
        assert test.assertions_passed == 1
        assert test.assertions_failed == 0

        test.assert_equal(5, 5, "Values should be equal")
        assert test.assertions_passed == 2
        assert test.assertions_failed == 0

    @pytest.mark.asyncio
    async def test_api_integration_test(self, temp_dir):
        """Test APIIntegrationTest basic functionality."""
        test = APIIntegrationTest("test_api", TestPriority.NORMAL)

        # Verify test initialization
        assert test.test_name == "test_api"
        assert test.test_type == TestType.INTEGRATION
        assert test.priority == TestPriority.NORMAL
        assert test.status == TestStatus.PENDING

    @pytest.mark.asyncio
    async def test_middleware_integration_test(self, temp_dir):
        """Test MiddlewareIntegrationTest basic functionality."""
        test = MiddlewareIntegrationTest("test_middleware", TestPriority.LOW)

        # Verify test initialization
        assert test.test_name == "test_middleware"
        assert test.test_type == TestType.INTEGRATION
        assert test.priority == TestPriority.LOW
        assert test.status == TestStatus.PENDING


class TestEndToEndSmoke:
    """End-to-end smoke tests."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.mark.asyncio
    async def test_full_integration_workflow(self, temp_dir):
        """Test a complete integration workflow."""
        # Create test runner
        runner = IntegrationTestRunner()

        # Create test suite
        suite = IntegrationTestSuite("Smoke Test Suite", "End-to-end smoke test suite")

        # Add mock tests
        for i in range(3):
            test = type(
                "MockTest",
                (),
                {
                    "test_name": f"Smoke Test {i}",
                    "run": asyncio.coroutine(
                        lambda: type("MockResult", (), {"status": TestStatus.PASSED})()
                    ),
                },
            )()
            suite.add_test(test)

        # Add suite to runner
        runner.add_test_suite(suite)

        # Verify setup
        assert len(runner.test_suites) == 1
        assert len(suite.tests) == 3

        # Get summaries
        suite_summary = suite.get_summary()
        runner_summary = runner.get_global_summary()

        assert suite_summary["total_tests"] == 3
        assert runner_summary["total_suites"] == 1
        assert runner_summary["total_tests"] == 3

    @pytest.mark.asyncio
    async def test_communication_and_testing_integration(self, temp_dir):
        """Test integration between communication and testing components."""
        # Create communication manager
        comm_manager = CrossSystemCommunicationManager()

        # Create test runner
        test_runner = IntegrationTestRunner()

        # Create test suite
        suite = IntegrationTestSuite(
            "Integration Suite", "Communication and testing integration"
        )

        # Add suite to runner
        test_runner.add_test_suite(suite)

        # Verify both components are working
        assert len(comm_manager.endpoints) == 0
        assert len(test_runner.test_suites) == 1

        # Get status from both
        comm_status = comm_manager.get_system_status()
        test_summary = test_runner.get_global_summary()

        assert isinstance(comm_status, dict)
        assert isinstance(test_summary, dict)
        assert test_summary["total_suites"] == 1


if __name__ == "__main__":
    # Run smoke tests with pytest
    pytest.main([__file__, "-v", "-s"])

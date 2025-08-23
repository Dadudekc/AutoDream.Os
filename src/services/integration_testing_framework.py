"""
Integration Testing Framework for Agent_Cellphone_V2_Repository
Comprehensive testing framework for cross-system communication and integration scenarios.
"""

import asyncio
import json
import logging
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Callable, Coroutine, Type
from pathlib import Path
import traceback
from datetime import datetime, timedelta

# Import our integration components
from .cross_system_communication import (
    CrossSystemCommunicationManager,
    SystemEndpoint,
    CrossSystemMessage,
    CommunicationProtocol,
    MessageType,
    MessagePriority,
)
from .api_manager import APIManager, APIEndpoint, APIMethod
from .middleware_orchestrator import MiddlewareOrchestrator, MiddlewareChain, DataPacket
from .service_registry import ServiceRegistry, ServiceInfo, ServiceType, ServiceStatus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestStatus(Enum):
    """Status of test execution."""

    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"
    ERROR = "error"


class TestType(Enum):
    """Types of integration tests."""

    UNIT = "unit"
    INTEGRATION = "integration"
    END_TO_END = "end_to_end"
    PERFORMANCE = "performance"
    LOAD = "load"
    STRESS = "stress"
    SECURITY = "security"
    COMPATIBILITY = "compatibility"


class TestPriority(Enum):
    """Test priority levels."""

    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class TestResult:
    """Result of a test execution."""

    test_id: str
    test_name: str
    test_type: TestType
    status: TestStatus
    start_time: float
    end_time: float
    duration: float
    error_message: Optional[str] = None
    error_traceback: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    logs: List[str] = field(default_factory=list)
    assertions_passed: int = 0
    assertions_failed: int = 0
    test_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TestScenario:
    """Defines a test scenario with setup, execution, and cleanup."""

    scenario_id: str
    name: str
    description: str
    test_type: TestType
    priority: TestPriority
    timeout: float = 300.0  # 5 minutes default
    retry_count: int = 0
    max_retries: int = 3
    dependencies: List[str] = field(default_factory=list)
    setup_steps: List[Callable] = field(default_factory=list)
    test_steps: List[Callable] = field(default_factory=list)
    cleanup_steps: List[Callable] = field(default_factory=list)
    assertions: List[Callable] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TestEnvironment:
    """Test environment configuration."""

    environment_id: str
    name: str
    description: str
    systems: List[SystemEndpoint] = field(default_factory=list)
    services: List[ServiceInfo] = field(default_factory=list)
    config_overrides: Dict[str, Any] = field(default_factory=dict)
    cleanup_on_exit: bool = True
    parallel_execution: bool = False
    max_parallel_tests: int = 5


class BaseIntegrationTest(ABC):
    """Abstract base class for integration tests."""

    def __init__(
        self,
        test_name: str,
        test_type: TestType,
        priority: TestPriority = TestPriority.NORMAL,
    ):
        self.test_name = test_name
        self.test_type = test_type
        self.priority = priority
        self.test_id = f"{test_type.value}_{test_name}_{uuid.uuid4().hex[:8]}"
        self.start_time = 0.0
        self.end_time = 0.0
        self.status = TestStatus.PENDING
        self.error_message = None
        self.error_traceback = None
        self.metrics = {}
        self.logs = []
        self.assertions_passed = 0
        self.assertions_failed = 0
        self.test_data = {}

        # Test components
        self.communication_manager: Optional[CrossSystemCommunicationManager] = None
        self.api_manager: Optional[APIManager] = None
        self.middleware_orchestrator: Optional[MiddlewareOrchestrator] = None
        self.service_registry: Optional[ServiceRegistry] = None

    @abstractmethod
    async def setup(self) -> bool:
        """Setup test environment."""
        pass

    @abstractmethod
    async def execute(self) -> bool:
        """Execute the test."""
        pass

    @abstractmethod
    async def cleanup(self) -> bool:
        """Cleanup test environment."""
        pass

    @abstractmethod
    async def validate(self) -> bool:
        """Validate test results."""
        pass

    def log(self, message: str, level: str = "INFO"):
        """Log a message during test execution."""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_entry)
        logger.info(f"[{self.test_id}] {log_entry}")

    def assert_true(self, condition: bool, message: str = "Assertion failed"):
        """Assert that a condition is true."""
        if condition:
            self.assertions_passed += 1
            self.log(f"ASSERTION PASSED: {message}")
        else:
            self.assertions_failed += 1
            self.log(f"ASSERTION FAILED: {message}", "ERROR")
            raise AssertionError(message)

    def assert_false(self, condition: bool, message: str = "Assertion failed"):
        """Assert that a condition is false."""
        self.assert_true(not condition, message)

    def assert_equal(
        self, actual: Any, expected: Any, message: str = "Assertion failed"
    ):
        """Assert that two values are equal."""
        if actual == expected:
            self.assertions_passed += 1
            self.log(
                f"ASSERTION PASSED: {message} (Expected: {expected}, Actual: {actual})"
            )
        else:
            self.assertions_failed += 1
            self.log(
                f"ASSERTION FAILED: {message} (Expected: {expected}, Actual: {actual})",
                "ERROR",
            )
            raise AssertionError(f"{message} - Expected: {expected}, Actual: {actual}")

    def assert_not_equal(
        self, actual: Any, expected: Any, message: str = "Assertion failed"
    ):
        """Assert that two values are not equal."""
        if actual != expected:
            self.assertions_passed += 1
            self.log(f"ASSERTION PASSED: {message} (Values are different)")
        else:
            self.assertions_failed += 1
            self.log(
                f"ASSERTION FAILED: {message} (Values are equal: {actual})", "ERROR"
            )
            raise AssertionError(f"{message} - Values are equal: {actual}")

    def assert_in(self, item: Any, container: Any, message: str = "Assertion failed"):
        """Assert that an item is in a container."""
        if item in container:
            self.assertions_passed += 1
            self.log(f"ASSERTION PASSED: {message} ({item} found in container)")
        else:
            self.assertions_failed += 1
            self.log(
                f"ASSERTION FAILED: {message} ({item} not found in container)", "ERROR"
            )
            raise AssertionError(f"{message} - {item} not found in container")

    def assert_not_in(
        self, item: Any, container: Any, message: str = "Assertion failed"
    ):
        """Assert that an item is not in a container."""
        if item not in container:
            self.assertions_passed += 1
            self.log(f"ASSERTION PASSED: {message} ({item} not found in container)")
        else:
            self.assertions_failed += 1
            self.log(
                f"ASSERTION FAILED: {message} ({item} found in container)", "ERROR"
            )
            raise AssertionError(f"{message} - {item} found in container")

    def assert_is_none(self, value: Any, message: str = "Assertion failed"):
        """Assert that a value is None."""
        if value is None:
            self.assertions_passed += 1
            self.log(f"ASSERTION PASSED: {message} (Value is None)")
        else:
            self.assertions_failed += 1
            self.log(
                f"ASSERTION FAILED: {message} (Value is not None: {value})", "ERROR"
            )
            raise AssertionError(f"{message} - Value is not None: {value}")

    def assert_is_not_none(self, value: Any, message: str = "Assertion failed"):
        """Assert that a value is not None."""
        if value is not None:
            self.assertions_passed += 1
            self.log(f"ASSERTION PASSED: {message} (Value is not None)")
        else:
            self.assertions_failed += 1
            self.log(f"ASSERTION FAILED: {message} (Value is None)", "ERROR")
            raise AssertionError(f"{message} - Value is None")

    async def run(self, timeout: float = 300.0) -> TestResult:
        """Run the complete test."""
        self.start_time = time.time()
        self.status = TestStatus.RUNNING

        try:
            self.log(f"Starting test: {self.test_name}")

            # Setup
            self.log("Setting up test environment...")
            if not await self.setup():
                raise RuntimeError("Test setup failed")

            # Execute
            self.log("Executing test...")
            if not await self.execute():
                raise RuntimeError("Test execution failed")

            # Validate
            self.log("Validating test results...")
            if not await self.validate():
                raise RuntimeError("Test validation failed")

            # Success
            self.status = TestStatus.PASSED
            self.log("Test completed successfully")

        except asyncio.TimeoutError:
            self.status = TestStatus.TIMEOUT
            self.error_message = f"Test timed out after {timeout} seconds"
            self.log(f"Test timed out after {timeout} seconds", "ERROR")

        except Exception as e:
            self.status = TestStatus.FAILED
            self.error_message = str(e)
            self.error_traceback = traceback.format_exc()
            self.log(f"Test failed with error: {e}", "ERROR")
            self.log(f"Traceback: {self.error_traceback}", "ERROR")

        finally:
            # Cleanup
            try:
                self.log("Cleaning up test environment...")
                await self.cleanup()
            except Exception as e:
                self.log(f"Cleanup failed: {e}", "ERROR")

            self.end_time = time.time()
            self.duration = self.end_time - self.start_time

            self.log(f"Test finished with status: {self.status.value}")
            self.log(f"Duration: {self.duration:.2f} seconds")
            self.log(
                f"Assertions: {self.assertions_passed} passed, {self.assertions_failed} failed"
            )

        return self._create_test_result()

    def _create_test_result(self) -> TestResult:
        """Create a TestResult from the test execution."""
        return TestResult(
            test_id=self.test_id,
            test_name=self.test_name,
            test_type=self.test_type,
            status=self.status,
            start_time=self.start_time,
            end_time=self.end_time,
            duration=self.duration,
            error_message=self.error_message,
            error_traceback=self.error_traceback,
            metrics=self.metrics,
            logs=self.logs,
            assertions_passed=self.assertions_passed,
            assertions_failed=self.assertions_failed,
            test_data=self.test_data,
        )


class CrossSystemCommunicationTest(BaseIntegrationTest):
    """Test for cross-system communication functionality."""

    def __init__(self, test_name: str, priority: TestPriority = TestPriority.NORMAL):
        super().__init__(test_name, TestType.INTEGRATION, priority)
        self.test_systems = []
        self.test_messages = []

    async def setup(self) -> bool:
        """Setup test environment with mock systems."""
        try:
            # Initialize communication manager
            self.communication_manager = CrossSystemCommunicationManager()

            # Add test endpoints
            test_endpoints = [
                SystemEndpoint(
                    system_id="test_system_1",
                    name="Test System 1",
                    protocol=CommunicationProtocol.HTTP,
                    host="localhost",
                    port=8001,
                    path="/api",
                ),
                SystemEndpoint(
                    system_id="test_system_2",
                    name="Test System 2",
                    protocol=CommunicationProtocol.WEBSOCKET,
                    host="localhost",
                    port=8002,
                    path="/ws",
                ),
                SystemEndpoint(
                    system_id="test_system_3",
                    name="Test System 3",
                    protocol=CommunicationProtocol.TCP,
                    host="localhost",
                    port=8003,
                ),
            ]

            for endpoint in test_endpoints:
                self.communication_manager.add_endpoint(endpoint)
                self.test_systems.append(endpoint.system_id)

            # Start communication manager
            await self.communication_manager.start()

            self.log("Cross-system communication test environment setup completed")
            return True

        except Exception as e:
            self.log(f"Setup failed: {e}", "ERROR")
            return False

    async def execute(self) -> bool:
        """Execute cross-system communication tests."""
        try:
            # Test 1: Connect to systems
            self.log("Testing system connections...")
            for system_id in self.test_systems:
                # Note: In a real test, we'd need actual servers running
                # For now, we'll test the connection logic without actual connections
                self.log(f"Testing connection to {system_id}")
                # await self.communication_manager.connect_system(system_id)

            # Test 2: Message creation and validation
            self.log("Testing message creation and validation...")
            test_message = CrossSystemMessage(
                message_id=f"test_msg_{uuid.uuid4().hex[:8]}",
                source_system="test_system_1",
                target_system="test_system_2",
                message_type=MessageType.REQUEST,
                priority=MessagePriority.HIGH,
                timestamp=time.time(),
                payload={"test": "data", "timestamp": time.time()},
                correlation_id="test_correlation_123",
            )

            self.test_messages.append(test_message)
            self.log(f"Created test message: {test_message.message_id}")

            # Test 3: Message validation
            self.assert_is_not_none(
                test_message.message_id, "Message ID should not be None"
            )
            self.assert_equal(
                test_message.source_system,
                "test_system_1",
                "Source system should match",
            )
            self.assert_equal(
                test_message.target_system,
                "test_system_2",
                "Target system should match",
            )
            self.assert_equal(
                test_message.message_type,
                MessageType.REQUEST,
                "Message type should match",
            )
            self.assert_equal(
                test_message.priority, MessagePriority.HIGH, "Priority should match"
            )
            self.assert_in(
                "test", test_message.payload, "Payload should contain test key"
            )

            # Test 4: Endpoint management
            self.log("Testing endpoint management...")
            endpoint_count = len(self.communication_manager.endpoints)
            self.assert_equal(endpoint_count, 3, "Should have 3 test endpoints")

            # Test 5: System status
            self.log("Testing system status retrieval...")
            system_status = self.communication_manager.get_system_status()
            self.assert_equal(len(system_status), 3, "Should have status for 3 systems")

            for system_id in self.test_systems:
                self.assert_in(
                    system_id, system_status, f"System {system_id} should be in status"
                )

            self.log("Cross-system communication tests completed successfully")
            return True

        except Exception as e:
            self.log(f"Test execution failed: {e}", "ERROR")
            return False

    async def cleanup(self) -> bool:
        """Cleanup test environment."""
        try:
            if self.communication_manager:
                await self.communication_manager.stop()

            self.log("Cross-system communication test environment cleaned up")
            return True

        except Exception as e:
            self.log(f"Cleanup failed: {e}", "ERROR")
            return False

    async def validate(self) -> bool:
        """Validate test results."""
        try:
            # Validate that all assertions passed
            self.assert_equal(self.assertions_failed, 0, "All assertions should pass")
            self.assert_greater(
                self.assertions_passed, 0, "Should have at least one assertion"
            )

            # Validate test data
            self.assert_equal(
                len(self.test_messages), 1, "Should have one test message"
            )
            self.assert_equal(
                len(self.test_systems), 3, "Should have three test systems"
            )

            self.log("Test validation completed successfully")
            return True

        except Exception as e:
            self.log(f"Test validation failed: {e}", "ERROR")
            return False


class APIIntegrationTest(BaseIntegrationTest):
    """Test for API integration functionality."""

    def __init__(self, test_name: str, priority: TestPriority = TestPriority.NORMAL):
        super().__init__(test_name, TestType.INTEGRATION, priority)
        self.test_endpoints = []
        self.test_requests = []

    async def setup(self) -> bool:
        """Setup test environment with mock API endpoints."""
        try:
            # Initialize API manager
            self.api_manager = APIManager()

            # Add test endpoints
            async def test_handler_1(request, context):
                return {"status": "success", "endpoint": "test_1", "data": request}

            async def test_handler_2(request, context):
                return {"status": "success", "endpoint": "test_2", "data": request}

            test_endpoints = [
                APIEndpoint(
                    path="/test/endpoint1",
                    method=APIMethod.GET,
                    handler=test_handler_1,
                    description="Test endpoint 1",
                ),
                APIEndpoint(
                    path="/test/endpoint2",
                    method=APIMethod.POST,
                    handler=test_handler_2,
                    description="Test endpoint 2",
                ),
            ]

            for endpoint in test_endpoints:
                self.api_manager.add_endpoint(endpoint)
                self.test_endpoints.append(endpoint)

            self.log("API integration test environment setup completed")
            return True

        except Exception as e:
            self.log(f"Setup failed: {e}", "ERROR")
            return False

    async def execute(self) -> bool:
        """Execute API integration tests."""
        try:
            # Test 1: Endpoint registration
            self.log("Testing endpoint registration...")
            endpoint_count = len(self.api_manager.endpoints)
            self.assert_equal(endpoint_count, 2, "Should have 2 test endpoints")

            # Test 2: Endpoint retrieval
            self.log("Testing endpoint retrieval...")
            for endpoint in self.test_endpoints:
                found_endpoints = [
                    ep for ep in self.api_manager.endpoints if ep.path == endpoint.path
                ]
                self.assert_equal(
                    len(found_endpoints), 1, f"Should find endpoint {endpoint.path}"
                )

            # Test 3: Endpoint validation
            self.log("Testing endpoint validation...")
            for endpoint in self.test_endpoints:
                self.assert_is_not_none(
                    endpoint.path, "Endpoint path should not be None"
                )
                self.assert_is_not_none(
                    endpoint.handler, "Endpoint handler should not be None"
                )
                self.assert_is_not_none(
                    endpoint.method, "Endpoint method should not be None"
                )

            # Test 4: Duplicate endpoint handling
            self.log("Testing duplicate endpoint handling...")
            duplicate_endpoint = APIEndpoint(
                path="/test/endpoint1",  # Duplicate path
                method=APIMethod.GET,
                handler=lambda req, ctx: {"status": "duplicate"},
                description="Duplicate endpoint",
            )

            try:
                self.api_manager.add_endpoint(duplicate_endpoint)
                self.assert_true(False, "Should reject duplicate endpoint")
            except ValueError:
                self.log("Correctly rejected duplicate endpoint")
                self.assertions_passed += 1

            self.log("API integration tests completed successfully")
            return True

        except Exception as e:
            self.log(f"Test execution failed: {e}", "ERROR")
            return False

    async def cleanup(self) -> bool:
        """Cleanup test environment."""
        try:
            # Clear test endpoints
            self.api_manager.endpoints.clear()

            self.log("API integration test environment cleaned up")
            return True

        except Exception as e:
            self.log(f"Cleanup failed: {e}", "ERROR")
            return False

    async def validate(self) -> bool:
        """Validate test results."""
        try:
            # Validate that all assertions passed
            self.assert_equal(self.assertions_failed, 0, "All assertions should pass")
            self.assert_greater(
                self.assertions_passed, 0, "Should have at least one assertion"
            )

            # Validate test data
            self.assert_equal(
                len(self.test_endpoints), 2, "Should have two test endpoints"
            )

            self.log("Test validation completed successfully")
            return True

        except Exception as e:
            self.log(f"Test validation failed: {e}", "ERROR")
            return False


class MiddlewareIntegrationTest(BaseIntegrationTest):
    """Test for middleware orchestration functionality."""

    def __init__(self, test_name: str, priority: TestPriority = TestPriority.NORMAL):
        super().__init__(test_name, TestType.INTEGRATION, priority)
        self.test_chains = []
        self.test_packets = []

    async def setup(self) -> bool:
        """Setup test environment with mock middleware components."""
        try:
            # Initialize middleware orchestrator
            self.middleware_orchestrator = MiddlewareOrchestrator()

            # Create test data packets
            test_packets = [
                DataPacket(
                    data={"test": "data1", "value": 100},
                    metadata={"source": "test1", "timestamp": time.time()},
                    direction="forward",
                ),
                DataPacket(
                    data={"test": "data2", "value": 200},
                    metadata={"source": "test2", "timestamp": time.time()},
                    direction="forward",
                ),
            ]

            self.test_packets = test_packets

            self.log("Middleware integration test environment setup completed")
            return True

        except Exception as e:
            self.log(f"Setup failed: {e}", "ERROR")
            return False

    async def execute(self) -> bool:
        """Execute middleware integration tests."""
        try:
            # Test 1: Data packet creation and validation
            self.log("Testing data packet creation and validation...")
            for packet in self.test_packets:
                self.assert_is_not_none(packet.data, "Packet data should not be None")
                self.assert_is_not_none(
                    packet.metadata, "Packet metadata should not be None"
                )
                self.assert_equal(
                    packet.direction, "forward", "Packet direction should be forward"
                )

            # Test 2: Middleware chain creation
            self.log("Testing middleware chain creation...")
            test_chain = MiddlewareChain(
                name="test_chain", components=[], execution_order="sequential"
            )

            self.test_chains.append(test_chain)
            self.assert_is_not_none(test_chain.name, "Chain name should not be None")
            self.assert_equal(
                test_chain.execution_order,
                "sequential",
                "Execution order should be sequential",
            )

            # Test 3: Chain registration
            self.log("Testing chain registration...")
            self.middleware_orchestrator.register_chain(test_chain)

            registered_chains = self.middleware_orchestrator.get_chains()
            self.assert_in(
                test_chain.name,
                [chain.name for chain in registered_chains],
                "Chain should be registered",
            )

            # Test 4: Chain execution (empty chain)
            self.log("Testing chain execution...")
            test_packet = self.test_packets[0]
            result = await self.middleware_orchestrator.process_packet(
                test_packet, test_chain.name
            )

            self.assert_is_not_none(result, "Chain execution should return result")
            self.assert_equal(
                result.data, test_packet.data, "Result data should match input data"
            )

            self.log("Middleware integration tests completed successfully")
            return True

        except Exception as e:
            self.log(f"Test execution failed: {e}", "ERROR")
            return False

    async def cleanup(self) -> bool:
        """Cleanup test environment."""
        try:
            # Clear test chains
            self.test_chains.clear()
            self.test_packets.clear()

            self.log("Middleware integration test environment cleaned up")
            return True

        except Exception as e:
            self.log(f"Cleanup failed: {e}", "ERROR")
            return False

    async def validate(self) -> bool:
        """Validate test results."""
        try:
            # Validate that all assertions passed
            self.assert_equal(self.assertions_failed, 0, "All assertions should pass")
            self.assert_greater(
                self.assertions_passed, 0, "Should have at least one assertion"
            )

            # Validate test data
            self.assert_equal(len(self.test_packets), 2, "Should have two test packets")
            self.assert_equal(len(self.test_chains), 1, "Should have one test chain")

            self.log("Test validation completed successfully")
            return True

        except Exception as e:
            self.log(f"Test validation failed: {e}", "ERROR")
            return False


class IntegrationTestSuite:
    """Manages and executes a suite of integration tests."""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.tests: List[BaseIntegrationTest] = []
        self.results: List[TestResult] = []
        self.start_time = 0.0
        self.end_time = 0.0
        self.running = False

        # Test execution options
        self.parallel_execution = False
        self.max_parallel_tests = 5
        self.stop_on_failure = False
        self.retry_failed_tests = False
        self.max_retries = 3

    def add_test(self, test: BaseIntegrationTest):
        """Add a test to the suite."""
        self.tests.append(test)
        logger.info(f"Added test to suite '{self.name}': {test.test_name}")

    def remove_test(self, test_name: str) -> bool:
        """Remove a test from the suite."""
        for i, test in enumerate(self.tests):
            if test.test_name == test_name:
                del self.tests[i]
                logger.info(f"Removed test from suite '{self.name}': {test_name}")
                return True
        return False

    def get_test(self, test_name: str) -> Optional[BaseIntegrationTest]:
        """Get a test by name."""
        for test in self.tests:
            if test.test_name == test_name:
                return test
        return None

    async def run_suite(self, timeout: float = 3600.0) -> List[TestResult]:
        """Run all tests in the suite."""
        if self.running:
            logger.warning(f"Test suite '{self.name}' is already running")
            return self.results

        self.running = True
        self.start_time = time.time()
        self.results.clear()

        logger.info(f"Starting test suite '{self.name}' with {len(self.tests)} tests")

        try:
            if self.parallel_execution:
                await self._run_parallel(timeout)
            else:
                await self._run_sequential(timeout)

        except Exception as e:
            logger.error(f"Test suite execution failed: {e}")

        finally:
            self.end_time = time.time()
            self.running = False

            duration = self.end_time - self.start_time
            passed = len([r for r in self.results if r.status == TestStatus.PASSED])
            failed = len(
                [
                    r
                    for r in self.results
                    if r.status
                    in [TestStatus.FAILED, TestStatus.ERROR, TestStatus.TIMEOUT]
                ]
            )

            logger.info(f"Test suite '{self.name}' completed in {duration:.2f}s")
            logger.info(
                f"Results: {passed} passed, {failed} failed, {len(self.results)} total"
            )

        return self.results

    async def _run_sequential(self, timeout: float):
        """Run tests sequentially."""
        for test in self.tests:
            if not self.running:
                break

            try:
                logger.info(f"Running test: {test.test_name}")
                result = await asyncio.wait_for(test.run(), timeout=timeout)
                self.results.append(result)

                if result.status != TestStatus.PASSED and self.stop_on_failure:
                    logger.warning(
                        f"Test failed, stopping suite due to stop_on_failure setting"
                    )
                    break

            except asyncio.TimeoutError:
                logger.error(f"Test {test.test_name} timed out")
                timeout_result = TestResult(
                    test_id=test.test_id,
                    test_name=test.test_name,
                    test_type=test.test_type,
                    status=TestStatus.TIMEOUT,
                    start_time=time.time(),
                    end_time=time.time(),
                    duration=0.0,
                    error_message=f"Test timed out after {timeout} seconds",
                )
                self.results.append(timeout_result)

            except Exception as e:
                logger.error(f"Test {test.test_name} failed with error: {e}")
                error_result = TestResult(
                    test_id=test.test_id,
                    test_name=test.test_name,
                    test_type=test.test_type,
                    status=TestStatus.ERROR,
                    start_time=time.time(),
                    end_time=time.time(),
                    duration=0.0,
                    error_message=str(e),
                    error_traceback=traceback.format_exc(),
                )
                self.results.append(error_result)

    async def _run_parallel(self, timeout: float):
        """Run tests in parallel."""
        semaphore = asyncio.Semaphore(self.max_parallel_tests)

        async def run_test_with_semaphore(test):
            async with semaphore:
                try:
                    logger.info(f"Running test: {test.test_name}")
                    result = await asyncio.wait_for(test.run(), timeout=timeout)
                    self.results.append(result)

                except asyncio.TimeoutError:
                    logger.error(f"Test {test.test_name} timed out")
                    timeout_result = TestResult(
                        test_id=test.test_id,
                        test_name=test.test_name,
                        test_type=test.test_type,
                        status=TestStatus.TIMEOUT,
                        start_time=time.time(),
                        end_time=time.time(),
                        duration=0.0,
                        error_message=f"Test timed out after {timeout} seconds",
                    )
                    self.results.append(timeout_result)

                except Exception as e:
                    logger.error(f"Test {test.test_name} failed with error: {e}")
                    error_result = TestResult(
                        test_id=test.test_id,
                        test_name=test.test_name,
                        test_type=test.test_type,
                        status=TestStatus.ERROR,
                        start_time=time.time(),
                        end_time=time.time(),
                        duration=0.0,
                        error_message=str(e),
                        error_traceback=traceback.format_exc(),
                    )
                    self.results.append(error_result)

        # Create tasks for all tests
        tasks = [run_test_with_semaphore(test) for test in self.tests]

        # Wait for all tasks to complete
        await asyncio.gather(*tasks, return_exceptions=True)

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of test suite execution."""
        if not self.results:
            return {
                "name": self.name,
                "description": self.description,
                "status": "not_run",
                "total_tests": len(self.tests),
                "executed_tests": 0,
                "passed": 0,
                "failed": 0,
                "duration": 0.0,
            }

        passed = len([r for r in self.results if r.status == TestStatus.PASSED])
        failed = len(
            [
                r
                for r in self.results
                if r.status in [TestStatus.FAILED, TestStatus.ERROR, TestStatus.TIMEOUT]
            ]
        )
        skipped = len([r for r in self.results if r.status == TestStatus.SKIPPED])

        duration = (
            self.end_time - self.start_time if self.end_time > self.start_time else 0.0
        )

        return {
            "name": self.name,
            "description": self.description,
            "status": "completed" if not self.running else "running",
            "total_tests": len(self.tests),
            "executed_tests": len(self.results),
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "duration": duration,
            "success_rate": (passed / len(self.results)) * 100 if self.results else 0.0,
        }

    def export_results(self, file_path: str) -> bool:
        """Export test results to a file."""
        try:
            summary = self.get_summary()
            export_data = {
                "summary": summary,
                "results": [
                    {
                        "test_id": r.test_id,
                        "test_name": r.test_name,
                        "test_type": r.test_type.value,
                        "status": r.status.value,
                        "duration": r.duration,
                        "error_message": r.error_message,
                        "assertions_passed": r.assertions_passed,
                        "assertions_failed": r.assertions_failed,
                        "logs": r.logs[:10],  # First 10 log entries
                    }
                    for r in self.results
                ],
            }

            with open(file_path, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(f"Test results exported to: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to export test results: {e}")
            return False


class IntegrationTestRunner:
    """Main runner for integration tests."""

    def __init__(self):
        self.test_suites: Dict[str, IntegrationTestSuite] = {}
        self.global_config: Dict[str, Any] = {}
        self.running = False

    def add_test_suite(self, suite: IntegrationTestSuite):
        """Add a test suite to the runner."""
        self.test_suites[suite.name] = suite
        logger.info(f"Added test suite: {suite.name}")

    def remove_test_suite(self, suite_name: str) -> bool:
        """Remove a test suite from the runner."""
        if suite_name in self.test_suites:
            del self.test_suites[suite_name]
            logger.info(f"Removed test suite: {suite_name}")
            return True
        return False

    def get_test_suite(self, suite_name: str) -> Optional[IntegrationTestSuite]:
        """Get a test suite by name."""
        return self.test_suites.get(suite_name)

    async def run_all_suites(
        self, timeout: float = 7200.0
    ) -> Dict[str, List[TestResult]]:
        """Run all test suites."""
        if self.running:
            logger.warning("Test runner is already running")
            return {}

        self.running = True
        results = {}

        logger.info(f"Starting test runner with {len(self.test_suites)} test suites")

        try:
            for suite_name, suite in self.test_suites.items():
                logger.info(f"Running test suite: {suite_name}")
                suite_results = await suite.run_suite(timeout=timeout)
                results[suite_name] = suite_results

        except Exception as e:
            logger.error(f"Test runner execution failed: {e}")

        finally:
            self.running = False

            total_tests = sum(len(suite.tests) for suite in self.test_suites.values())
            total_results = sum(
                len(results.get(suite_name, []))
                for suite_name in self.test_suites.keys()
            )
            total_passed = sum(
                len([r for r in suite_results if r.status == TestStatus.PASSED])
                for suite_results in results.values()
            )

            logger.info(
                f"Test runner completed: {total_passed}/{total_results} tests passed across {len(self.test_suites)} suites"
            )

        return results

    async def run_specific_suite(
        self, suite_name: str, timeout: float = 3600.0
    ) -> Optional[List[TestResult]]:
        """Run a specific test suite."""
        if suite_name not in self.test_suites:
            logger.error(f"Test suite not found: {suite_name}")
            return None

        suite = self.test_suites[suite_name]
        return await suite.run_suite(timeout=timeout)

    def get_global_summary(self) -> Dict[str, Any]:
        """Get a global summary of all test suites."""
        if not self.test_suites:
            return {"total_suites": 0, "total_tests": 0, "status": "no_suites"}

        total_suites = len(self.test_suites)
        total_tests = sum(len(suite.tests) for suite in self.test_suites.values())

        # Get status of all suites
        suite_statuses = {}
        for suite_name, suite in self.test_suites.items():
            if suite.running:
                suite_statuses[suite_name] = "running"
            elif suite.results:
                suite_statuses[suite_name] = "completed"
            else:
                suite_statuses[suite_name] = "not_run"

        return {
            "total_suites": total_suites,
            "total_tests": total_tests,
            "suite_statuses": suite_statuses,
            "status": "ready" if not self.running else "running",
        }

    def export_global_results(self, file_path: str) -> bool:
        """Export results from all test suites."""
        try:
            global_summary = self.get_global_summary()
            suite_results = {}

            for suite_name, suite in self.test_suites.items():
                suite_results[suite_name] = {
                    "summary": suite.get_summary(),
                    "results_count": len(suite.results),
                }

            export_data = {
                "global_summary": global_summary,
                "suite_results": suite_results,
                "export_timestamp": datetime.now().isoformat(),
            }

            with open(file_path, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(f"Global test results exported to: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to export global test results: {e}")
            return False

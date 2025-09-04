#!/usr/bin/env python3
"""
Pytest Configuration for Messaging System Tests - Agent-1 Integration & Core Systems
=================================================================================

Pytest configuration and fixtures for the messaging system test suite.
Provides shared fixtures and test configuration.

V2 Compliance: Comprehensive test configuration with unified logging integration.

Author: Agent-1 - Integration & Core Systems Specialist
License: MIT
"""

import pytest

# Import messaging components
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    SenderType,
    RecipientType
)


@pytest.fixture(scope="session")
def test_config():
    """Test configuration for messaging system tests."""
    return {
        "test_agents": ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"],
        "test_message_types": [UnifiedMessageType.TEXT, UnifiedMessageType.BROADCAST, UnifiedMessageType.ONBOARDING],
        "test_priorities": [UnifiedMessagePriority.NORMAL, UnifiedMessagePriority.URGENT],
        "test_tags": [UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.ONBOARDING, UnifiedMessageTag.WRAPUP],
        "performance_thresholds": {
            "single_message_timeout": 1.0,
            "bulk_message_timeout": 10.0,
            "concurrent_message_timeout": 5.0,
            "min_throughput": 10.0,
            "max_memory_per_message": 1024
        }
    }


@pytest.fixture
def temp_inbox_dirs():
    """Create temporary inbox directories for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        inbox_dirs = {}
        for i in range(1, 9):  # Create 8 test agents
            agent_dir = get_unified_utility().Path(temp_dir) / f"Agent-{i}" / "inbox"
            agent_dir.mkdir(parents=True)
            inbox_dirs[f"Agent-{i}"] = str(agent_dir)
        yield inbox_dirs


@pytest.fixture
def mock_metrics():
    """Mock metrics service for testing."""
    metrics = Mock()
    metrics.record_delivery = Mock()
    metrics.record_error = Mock()
    metrics.record_retry = Mock()
    metrics.get_stats = Mock(return_value={
        "total_deliveries": 0,
        "total_errors": 0,
        "total_retries": 0,
        "success_rate": 1.0
    })
    return metrics


@pytest.fixture
def mock_unified_logger():
    """Mock unified logger for testing."""
    logger = Mock()
    logger.log = Mock()
    logger.info = Mock()
    logger.error = Mock()
    logger.warning = Mock()
    logger.debug = Mock()
    return logger


@pytest.fixture
def mock_unified_config():
    """Mock unified configuration system for testing."""
    config = Mock()
    config.get_config = Mock(return_value={
        "delivery_method": "inbox",
        "retry_attempts": 3,
        "timeout": 30,
        "max_message_size": 1024 * 1024  # 1MB
    })
    config.get_agent_config = Mock(return_value={
        "coordinates": {"x": 100, "y": 200},
        "inbox_path": "agent_workspaces/Agent-1/inbox"
    })
    return config


@pytest.fixture
def delivery_service(temp_inbox_dirs, mock_metrics):
    """Create MessagingDeliveryService instance for testing."""
    # Create MessagingDelivery with proper parameters
    messaging_delivery = MessagingDelivery(temp_inbox_dirs, mock_metrics)
    
    return MessagingDeliveryService(messaging_delivery=messaging_delivery)


@pytest.fixture
def config_service():
    """Create MessagingConfigService instance for testing."""
    return MessagingConfigService()


@pytest.fixture
def unified_integration(mock_unified_logger, mock_unified_config, mock_metrics):
    """Create MessagingUnifiedIntegration instance for testing."""
    integration = MessagingUnifiedIntegration()
    integration.unified_logger = mock_unified_logger
    integration.unified_config = mock_unified_config
    integration.metrics = mock_metrics
    return integration


@pytest.fixture
def utils_service():
    """Create MessagingUtilsService instance for testing."""
    return MessagingUtilsService()


@pytest.fixture
def messaging_system(delivery_service, config_service, unified_integration, utils_service):
    """Create complete messaging system for testing."""
    return UnifiedMessagingCoreV2(
        delivery_service=delivery_service,
        config_service=config_service,
        unified_integration=unified_integration,
        utils_service=utils_service
    )


@pytest.fixture
def sample_message():
    """Create a sample message for testing."""
    return UnifiedMessage(
        message_id="test_001",
        sender="Agent-1",
        recipient="Agent-2",
        content="Test message content",
        message_type=UnifiedMessageType.TEXT,
        priority=UnifiedMessagePriority.REGULAR
    )


@pytest.fixture
def sample_messages():
    """Create sample messages for testing."""
    return [
        UnifiedMessage(
            message_id=f"test_{i}",
            sender="Agent-1",
            recipient=f"Agent-{i+2}",
            content=f"Test message {i}",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        for i in range(5)
    ]


@pytest.fixture
def urgent_message():
    """Create an urgent message for testing."""
    return UnifiedMessage(
        message_id="urgent_001",
        sender="Agent-1",
        recipient="Agent-2",
        content="Urgent test message",
        message_type=UnifiedMessageType.TEXT,
        priority=UnifiedMessagePriority.URGENT,
        tags=[UnifiedMessageTag.CAPTAIN]
    )


@pytest.fixture
def broadcast_message():
    """Create a broadcast message for testing."""
    return UnifiedMessage(
        message_id="broadcast_001",
        sender="Agent-1",
        recipient="Agent-2",
        content="Broadcast test message",
        message_type=UnifiedMessageType.BROADCAST,
        priority=UnifiedMessagePriority.REGULAR
    )


@pytest.fixture
def onboarding_message():
    """Create an onboarding message for testing."""
    return UnifiedMessage(
        message_id="onboarding_001",
        sender="Agent-1",
        recipient="Agent-2",
        content="Onboarding test message",
        message_type=UnifiedMessageType.ONBOARDING,
        priority=UnifiedMessagePriority.REGULAR,
        tags=[UnifiedMessageTag.ONBOARDING]
    )


@pytest.fixture
def invalid_message():
    """Create an invalid message for testing."""
    return UnifiedMessage(
        message_id="",
        sender="",
        recipient="",
        content="",
        message_type=UnifiedMessageType.TEXT,
        priority=UnifiedMessagePriority.REGULAR
    )


@pytest.fixture
def performance_test_messages():
    """Create messages for performance testing."""
    return [
        UnifiedMessage(
            message_id=f"perf_{i}",
            sender="Agent-1",
            recipient=f"Agent-{(i % 8) + 1}",
            content=f"Performance test message {i}",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        for i in range(100)
    ]


@pytest.fixture
def concurrent_test_messages():
    """Create messages for concurrent testing."""
    return [
        UnifiedMessage(
            message_id=f"concurrent_{i}",
            sender="Agent-1",
            recipient="Agent-2",
            content=f"Concurrent test message {i}",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        for i in range(50)
    ]


@pytest.fixture
def large_message():
    """Create a large message for testing."""
    large_content = "Large message content " * 1000  # ~20KB message
    return UnifiedMessage(
        message_id="large_001",
        sender="Agent-1",
        recipient="Agent-2",
        content=large_content,
        message_type=UnifiedMessageType.TEXT,
        priority=UnifiedMessagePriority.REGULAR
    )


@pytest.fixture
def mixed_priority_messages():
    """Create messages with mixed priorities for testing."""
    messages = []
    for i in range(20):
        priority = UnifiedMessagePriority.URGENT if i % 3 == 0 else UnifiedMessagePriority.REGULAR
        message = UnifiedMessage(
            message_id=f"mixed_priority_{i}",
            sender="Agent-1",
            recipient="Agent-2",
            content=f"Mixed priority test message {i}",
            message_type=UnifiedMessageType.TEXT,
            priority=priority
        )
        messages.append(message)
    return messages


@pytest.fixture
def mixed_type_messages():
    """Create messages with mixed types for testing."""
    message_types = [UnifiedMessageType.TEXT, UnifiedMessageType.BROADCAST, UnifiedMessageType.ONBOARDING]
    messages = []
    for i in range(15):
        message_type = message_types[i % len(message_types)]
        message = UnifiedMessage(
            message_id=f"mixed_type_{i}",
            sender="Agent-1",
            recipient="Agent-2",
            content=f"Mixed type test message {i}",
            message_type=message_type,
            priority=UnifiedMessagePriority.REGULAR
        )
        messages.append(message)
    return messages


@pytest.fixture
def error_test_messages():
    """Create messages for error testing."""
    return [
        UnifiedMessage(
            message_id=f"error_{i}",
            sender="Agent-1",
            recipient="Invalid-Agent",  # Invalid recipient
            content=f"Error test message {i}",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        for i in range(10)
    ]


@pytest.fixture
def cleanup_test_messages():
    """Create messages for cleanup testing."""
    return [
        UnifiedMessage(
            message_id=f"cleanup_{i}",
            sender="Agent-1",
            recipient="Agent-2",
            content=f"Cleanup test message {i}",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        for i in range(100)
    ]


@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Clean up test files after each test."""
    yield
    # Cleanup logic can be added here if needed


@pytest.fixture(autouse=True)
def reset_mocks():
    """Reset all mocks after each test."""
    yield
    # Reset logic can be added here if needed


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "performance: mark test as a performance test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add performance marker to performance tests
        if "performance" in item.name:
            item.add_marker(pytest.mark.performance)
        
        # Add integration marker to integration tests
        if "integration" in item.name:
            item.add_marker(pytest.mark.integration)
        
        # Add unit marker to unit tests
        if "unit" in item.name or "test_" in item.name:
            item.add_marker(pytest.mark.unit)
        
        # Add slow marker to slow tests
        if "slow" in item.name or "benchmark" in item.name:
            item.add_marker(pytest.mark.slow)


# Test data generators
def generate_test_messages(count: int, agent_count: int = 8) -> List[UnifiedMessage]:
    """Generate test messages for testing."""
    messages = []
    for i in range(count):
        message = UnifiedMessage(
            message_id=f"generated_{i}",
            sender="Agent-1",
            recipient=f"Agent-{(i % agent_count) + 1}",
            content=f"Generated test message {i}",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        messages.append(message)
    return messages


def generate_performance_test_data(message_count: int) -> Dict[str, Any]:
    """Generate performance test data."""
    return {
        "message_count": message_count,
        "expected_throughput": message_count / 10.0,  # 10 seconds max
        "expected_memory_per_message": 1024,  # 1KB max
        "expected_cpu_usage": 50.0  # 50% max
    }


# Utility functions for tests
def assert_message_delivered(inbox_path: str, expected_count: int = 1):
    """Assert that messages were delivered to inbox."""
    inbox = get_unified_utility().Path(inbox_path)
    message_files = list(inbox.glob("*.md"))
    assert len(message_files) == expected_count


def assert_message_content(inbox_path: str, expected_content: str):
    """Assert that message content is correct."""
    inbox = get_unified_utility().Path(inbox_path)
    message_files = list(inbox.glob("*.md"))
    assert len(message_files) > 0
    
    with open(message_files[0], 'r') as f:
        content = f.read()
    assert expected_content in content


def assert_performance_metrics(execution_time: float, message_count: int, min_throughput: float = 10.0):
    """Assert performance metrics are within acceptable ranges."""
    throughput = message_count / execution_time
    assert throughput >= min_throughput
    assert execution_time < 10.0  # Should complete within 10 seconds

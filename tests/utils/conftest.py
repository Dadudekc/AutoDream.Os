"""Shared test fixtures and utilities"""


@pytest.fixture
def mock_service():
    """Mock service for testing"""
    service = Mock()
    service.process.return_value = {"status": "success"}
    return service

@pytest.fixture
def test_data():
    """Sample test data"""
    return {
        "agent_id": "test_agent",
        "operation": "test_operation",
        "timestamp": "2025-01-01T00:00:00Z"
    }

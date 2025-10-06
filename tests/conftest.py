#!/usr/bin/env python3
"""
Global test configuration and fixtures for Agent Cellphone V2 Repository.

Author: Agent-3 (QA Lead)
License: MIT
V2 Compliance: ≤400 lines, modular design
"""

import pytest
import asyncio
import tempfile
import json
from unittest.mock import Mock, patch
from pathlib import Path
from datetime import datetime

# Global test configuration
pytest_plugins = ["pytest_asyncio"]


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_discord_api():
    """Mock Discord API responses for testing."""
    mock = Mock()
    mock.channels = Mock()
    mock.webhooks = Mock()
    mock.bot = Mock()
    mock.guilds = Mock()
    
    # Mock common Discord API responses
    mock.channels.send.return_value = Mock(id="test_message_id")
    mock.webhooks.execute.return_value = Mock(id="test_webhook_id")
    
    return mock


@pytest.fixture
def mock_database():
    """Mock database operations for testing."""
    mock = Mock()
    mock.query = Mock()
    mock.execute = Mock()
    mock.commit = Mock()
    mock.rollback = Mock()
    mock.close = Mock()
    
    # Mock query results
    mock.query.return_value.all.return_value = []
    mock.query.return_value.first.return_value = None
    
    return mock


@pytest.fixture
def temp_directory(tmp_path):
    """Temporary directory for file operations testing."""
    return tmp_path


@pytest.fixture
def sample_agent_data():
    """Sample agent configuration data for testing."""
    return {
        "agent_id": "Agent-3",
        "role": "QA Lead",
        "status": "active",
        "coordinates": {"x": 652, "y": 421},
        "capabilities": ["testing", "analysis", "quality_assurance"],
        "created_at": datetime.now().isoformat()
    }


@pytest.fixture
def sample_message_data():
    """Sample message data for testing."""
    return {
        "from_agent": "Agent-4",
        "to_agent": "Agent-3",
        "message": "Test message for QA analysis",
        "priority": "HIGH",
        "tags": ["TASK_ASSIGNMENT", "TEST_COVERAGE"],
        "timestamp": datetime.now().isoformat()
    }


@pytest.fixture
def sample_coordinates():
    """Sample agent coordinates for testing."""
    return {
        "Agent-1": {"x": -1269, "y": 481},
        "Agent-2": {"x": -308, "y": 480},
        "Agent-3": {"x": -1269, "y": 1001},
        "Agent-4": {"x": -308, "y": 1000},
        "Agent-5": {"x": 652, "y": 421}
    }


@pytest.fixture
def mock_file_system(tmp_path):
    """Mock file system for testing file operations."""
    # Create test directory structure
    (tmp_path / "src").mkdir()
    (tmp_path / "tools").mkdir()
    (tmp_path / "config").mkdir()
    (tmp_path / "tests").mkdir()
    
    return tmp_path


@pytest.fixture
def test_config():
    """Test configuration for various components."""
    return {
        "discord": {
            "bot_token": "test_bot_token",
            "channel_id": "test_channel_id",
            "webhook_url": "test_webhook_url"
        },
        "database": {
            "url": "sqlite:///test.db",
            "echo": False
        },
        "agents": {
            "max_agents": 8,
            "default_role": "TASK_EXECUTOR"
        }
    }


@pytest.fixture
def async_mock():
    """Async mock for testing async functions."""
    class AsyncMock:
        def __init__(self, return_value=None):
            self.return_value = return_value
        
        async def __call__(self, *args, **kwargs):
            return self.return_value
        
        async def __aenter__(self):
            return self
        
        async def __aexit__(self, *args):
            pass
    
    return AsyncMock


@pytest.fixture
def mock_environment():
    """Mock environment variables for testing."""
    test_env = {
        "DISCORD_BOT_TOKEN": "test_token",
        "DISCORD_CHANNEL_ID": "test_channel",
        "DATABASE_URL": "sqlite:///test.db",
        "AGENT_COUNT": "8",
        "ENVIRONMENT": "test"
    }
    
    with patch.dict('os.environ', test_env):
        yield test_env


@pytest.fixture
def sample_test_data():
    """Sample test data for various test scenarios."""
    return {
        "agents": [
            {"id": "Agent-1", "role": "Integration", "status": "active"},
            {"id": "Agent-2", "role": "Quality", "status": "active"},
            {"id": "Agent-3", "role": "QA Lead", "status": "active"},
            {"id": "Agent-4", "role": "Captain", "status": "active"},
            {"id": "Agent-5", "role": "Coordinator", "status": "active"}
        ],
        "messages": [
            {"from": "Agent-4", "to": "Agent-3", "content": "Test message 1"},
            {"from": "Agent-3", "to": "Agent-4", "content": "Test response 1"}
        ],
        "tasks": [
            {"id": "task_1", "assigned_to": "Agent-3", "status": "in_progress"},
            {"id": "task_2", "assigned_to": "Agent-1", "status": "pending"}
        ]
    }


# Test utilities
def create_test_file(directory, filename, content=""):
    """Utility to create test files."""
    file_path = directory / filename
    file_path.write_text(content)
    return file_path


def load_test_json(file_path):
    """Utility to load test JSON data."""
    with open(file_path, 'r') as f:
        return json.load(f)


def save_test_json(file_path, data):
    """Utility to save test JSON data."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


# Test markers
pytest.mark.unit = pytest.mark.unit
pytest.mark.integration = pytest.mark.integration
pytest.mark.e2e = pytest.mark.e2e
pytest.mark.slow = pytest.mark.slow


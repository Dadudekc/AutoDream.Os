#!/usr/bin/env python3
"""
Pytest configuration for Discord Bot tests
==========================================

Shared fixtures and configuration for Discord bot testing.
"""

import pytest
import asyncio
import os
import sys
from unittest.mock import Mock, AsyncMock, patch
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_discord_user():
    """Create a mock Discord user."""
    user = Mock()
    user.name = "TestBot"
    user.id = 123456789
    user.discriminator = "0001"
    user.created_at = Mock()
    user.created_at.strftime = Mock(return_value="2025-01-16 15:00:00")
    return user


@pytest.fixture
def mock_discord_guild():
    """Create a mock Discord guild."""
    guild = Mock()
    guild.name = "TestGuild"
    guild.id = 987654321
    guild.channels = []
    return guild


@pytest.fixture
def mock_discord_channel():
    """Create a mock Discord channel."""
    channel = Mock()
    channel.name = "test-channel"
    channel.id = 111222333
    channel.guild = Mock()
    channel.guild.name = "TestGuild"
    channel.send = AsyncMock()
    channel.permissions_for = Mock()
    channel.permissions_for.return_value.send_messages = True
    return channel


@pytest.fixture
def mock_discord_context():
    """Create a mock Discord context."""
    ctx = Mock()
    ctx.reply = AsyncMock()
    ctx.send = AsyncMock()
    ctx.message = Mock()
    ctx.message.author = Mock()
    ctx.message.author.name = "TestUser"
    ctx.message.created_at = Mock()
    ctx.message.created_at.strftime = Mock(return_value="2025-01-16 15:00:00")
    ctx.guild = Mock()
    ctx.guild.name = "TestGuild"
    ctx.channel = Mock()
    ctx.channel.name = "test-channel"
    return ctx


@pytest.fixture
def mock_agent_coordinates():
    """Create mock agent coordinates."""
    return {
        f"Agent-{i}": {
            "coordinates": [100 + i * 50, 200 + i * 50],
            "chat_input_coordinates": [100 + i * 50, 250 + i * 50],
            "onboarding_coordinates": [100 + i * 50, 300 + i * 50],
            "description": f"Agent {i}",
            "active": True,
        }
        for i in range(1, 9)
    }


@pytest.fixture
def mock_messaging_service():
    """Create a mock messaging service."""
    service = Mock()
    service.send_message = Mock(return_value=True)
    service.broadcast_message = Mock(return_value={
        f"Agent-{i}": True for i in range(1, 9)
    })
    service.get_status = Mock(return_value={
        "total_agents": 8,
        "active_agents": 8,
        "status": "active"
    })
    service.hard_onboard_agent = Mock(return_value=True)
    service.hard_onboard_all_agents = Mock(return_value={
        f"Agent-{i}": True for i in range(1, 9)
    })
    return service


@pytest.fixture
def mock_consolidated_messaging_service():
    """Create a mock consolidated messaging service."""
    service = Mock()
    service.send_message = Mock(return_value=True)
    service.broadcast_message = Mock(return_value={
        f"Agent-{i}": True for i in range(1, 9)
    })
    service.get_status = Mock(return_value={
        "total_agents": 8,
        "active_agents": 8,
        "status": "active"
    })
    service.hard_onboard_agent = Mock(return_value=True)
    service.hard_onboard_all_agents = Mock(return_value={
        f"Agent-{i}": True for i in range(1, 9)
    })
    return service


@pytest.fixture
def mock_coordinate_loader():
    """Create a mock coordinate loader."""
    loader = Mock()
    loader.load = Mock()
    loader.validate_all = Mock()
    loader.validate_all.return_value = Mock()
    loader.validate_all.return_value.is_all_ok = Mock(return_value=True)
    loader.validate_all.return_value.issues = []
    return loader


@pytest.fixture(autouse=True)
def mock_environment():
    """Mock environment variables for testing."""
    with patch.dict(os.environ, {
# SECURITY: Token placeholder - replace with environment variable
        'APP_ENV': 'test'
    }):
        yield


@pytest.fixture
def mock_dotenv_load():
    """Mock dotenv load function."""
    with patch('run_discord_agent_bot.load_dotenv') as mock_load:
        mock_load.return_value = True
        yield mock_load


@pytest.fixture
def mock_discord_imports():
    """Mock Discord imports for testing."""
    with patch('run_discord_agent_bot.discord') as mock_discord:
        # Mock discord.Intents
        mock_discord.Intents.default.return_value = Mock()
        mock_discord.Intents.default.return_value.message_content = True
        mock_discord.Intents.default.return_value.members = False
        
        # Mock discord.__version__
        mock_discord.__version__ = "2.5.2"
        
        yield mock_discord


@pytest.fixture
def mock_messaging_imports():
    """Mock messaging system imports."""
    with patch('run_discord_agent_bot.ConsolidatedMessagingService') as mock_service:
        mock_service.return_value = Mock()
        yield mock_service


@pytest.fixture
def mock_json_load():
    """Mock JSON loading for agent coordinates."""
    mock_data = {
        "agents": {
            f"Agent-{i}": {
                "coordinates": [100 + i * 50, 200 + i * 50],
                "chat_input_coordinates": [100 + i * 50, 250 + i * 50],
                "onboarding_coordinates": [100 + i * 50, 300 + i * 50],
                "description": f"Agent {i}",
                "active": True,
            }
            for i in range(1, 9)
        }
    }
    
    with patch('builtins.open', mock_open()) as mock_file:
        with patch('json.load', return_value=mock_data):
            yield mock_file


def mock_open():
    """Create a mock open function."""
    from unittest.mock import mock_open
    return mock_open()


@pytest.fixture
def mock_logging():
    """Mock logging for tests."""
    with patch('run_discord_agent_bot.logger') as mock_logger:
        mock_logger.info = Mock()
        mock_logger.warning = Mock()
        mock_logger.error = Mock()
        yield mock_logger


@pytest.fixture
def mock_asyncio():
    """Mock asyncio for testing."""
    with patch('asyncio.run') as mock_run:
        mock_run.return_value = None
        yield mock_run


@pytest.fixture
def mock_sys_exit():
    """Mock sys.exit for testing."""
    with patch('sys.exit') as mock_exit:
        mock_exit.return_value = None
        yield mock_exit


# Test markers
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )
    config.addinivalue_line(
        "markers", "discord: mark test as Discord-related"
    )
    config.addinivalue_line(
        "markers", "messaging: mark test as messaging-related"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )



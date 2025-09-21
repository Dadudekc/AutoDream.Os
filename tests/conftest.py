#!/usr/bin/env python3
"""
Pytest Configuration and Fixtures
=================================

Global pytest configuration and shared fixtures for V2_SWARM test suite.
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Dict, Any, Generator
from unittest.mock import Mock, MagicMock, patch

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))


@pytest.fixture(scope="session")
def project_root_path():
    """Get project root path."""
    return project_root


@pytest.fixture(scope="session")
def test_data_dir():
    """Get test data directory."""
    return project_root / "tests" / "data"


@pytest.fixture
def temp_dir():
    """Create temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def mock_coordinates():
    """Mock agent coordinates for testing."""
    return {
        "agents": {
            "Agent-1": {
                "chat_input_coordinates": [-1269, 481],
                "onboarding_coordinates": [-1250, 500],
                "description": "Infrastructure Specialist",
                "active": True
            },
            "Agent-2": {
                "chat_input_coordinates": [-308, 480],
                "onboarding_coordinates": [-289, 499],
                "description": "Data Processing Expert",
                "active": True
            },
            "Agent-3": {
                "chat_input_coordinates": [-1269, 1001],
                "onboarding_coordinates": [-1250, 1020],
                "description": "Quality Assurance Lead",
                "active": False
            }
        },
        "onboarding_coordinates": [-1250, 500],
        "chat_input_coordinates": [-1269, 481]
    }


@pytest.fixture
def mock_coordinates_file(temp_dir, mock_coordinates):
    """Create mock coordinates file for testing."""
    coords_file = temp_dir / "test_coordinates.json"
    with open(coords_file, 'w') as f:
        json.dump(mock_coordinates, f, indent=2)
    return str(coords_file)


@pytest.fixture
def mock_pyautogui():
    """Mock PyAutoGUI for testing."""
    with patch('pyautogui.click') as mock_click, \
         patch('pyautogui.press') as mock_press, \
         patch('pyautogui.sleep') as mock_sleep:
        
        mock_click.return_value = None
        mock_press.return_value = None
        mock_sleep.return_value = None
        
        yield {
            'click': mock_click,
# SECURITY: Key placeholder - replace with environment variable
            'press': mock_press,
            'sleep': mock_sleep
        }


@pytest.fixture
def mock_pyperclip():
    """Mock Pyperclip for testing."""
    with patch('pyperclip.copy') as mock_copy, \
         patch('pyperclip.paste') as mock_paste:
        
        mock_copy.return_value = None
        mock_paste.return_value = "test message"
        
        yield {
            'copy': mock_copy,
            'paste': mock_paste
        }


@pytest.fixture
def mock_selenium():
    """Mock Selenium WebDriver for testing."""
    mock_driver = Mock()
    mock_driver.get.return_value = None
    mock_driver.current_url = "https://chat.openai.com"
    mock_driver.title = "ChatGPT"
    mock_driver.find_element.return_value = Mock()
    mock_driver.find_elements.return_value = []
    mock_driver.get_cookies.return_value = []
    mock_driver.add_cookie.return_value = None
    mock_driver.delete_all_cookies.return_value = None
    mock_driver.refresh.return_value = None
    
    return mock_driver


@pytest.fixture
def mock_discord_bot():
    """Mock Discord bot for testing."""
    mock_bot = Mock()
    mock_bot.user = Mock()
    mock_bot.user.name = "V2_SWARM_Bot"
    mock_bot.user.id = 123456789
    mock_bot.latency = 0.1
    mock_bot.guilds = [Mock()]
    mock_bot.guilds[0].name = "Test Guild"
    mock_bot.guilds[0].id = 987654321
    mock_bot.guilds[0].channels = [Mock(), Mock()]
    mock_bot.agent_coordinates = {
        "Agent-1": {"active": True, "description": "Test Agent"},
        "Agent-2": {"active": True, "description": "Test Agent"}
    }
    mock_bot.commands = []
    
    return mock_bot


@pytest.fixture
def mock_discord_context():
    """Mock Discord context for testing."""
    mock_ctx = Mock()
    mock_ctx.reply = Mock()
    mock_ctx.author = Mock()
    mock_ctx.author.name = "TestUser"
    mock_ctx.channel = Mock()
    mock_ctx.channel.name = "test-channel"
    mock_ctx.guild = Mock()
    mock_ctx.guild.name = "test-guild"
    mock_ctx.message = Mock()
    mock_ctx.message.created_at = Mock()
    mock_ctx.message.created_at.strftime.return_value = "2025-01-14 12:00:00"
    
    return mock_ctx


@pytest.fixture
def mock_agent_workspace(temp_dir):
    """Create mock agent workspace for testing."""
    agent_dir = temp_dir / "agent_workspaces" / "Agent-1"
    agent_dir.mkdir(parents=True, exist_ok=True)
    
    # Create working tasks
    working_tasks = {
        "current_task": {
            "id": "TEST-001",
            "title": "Test Task",
            "status": "in_progress",
            "priority": "high"
        },
        "tasks": [
            {
                "id": "TEST-001",
                "title": "Test Task",
                "status": "in_progress",
                "priority": "high"
            }
        ]
    }
    
    with open(agent_dir / "working_tasks.json", 'w') as f:
        json.dump(working_tasks, f, indent=2)
    
    # Create future tasks
    future_tasks = {
        "tasks": [
            {
                "id": "TEST-002",
                "title": "Future Task",
                "status": "pending",
                "priority": "medium"
            }
        ]
    }
    
    with open(agent_dir / "future_tasks.json", 'w') as f:
        json.dump(future_tasks, f, indent=2)
    
    return agent_dir


@pytest.fixture
def mock_fsm_status(temp_dir):
    """Create mock FSM status files for testing."""
    fsm_dir = temp_dir / "data" / "semantic_seed" / "status"
    fsm_dir.mkdir(parents=True, exist_ok=True)
    
    # Create mock FSM status for Agent-1
    agent_status = {
        "current_state": "active",
        "phase": "operational",
        "last_update": "2025-01-14T12:00:00Z"
    }
    
    with open(fsm_dir / "Agent-1.json", 'w') as f:
        json.dump(agent_status, f, indent=2)
    
    return fsm_dir


@pytest.fixture
def mock_project_analysis(temp_dir):
    """Create mock project analysis file for testing."""
    analysis_file = temp_dir / "project_analysis.json"
    
    analysis_data = {
        "scan_timestamp": "2025-01-14T12:00:00Z",
        "total_files": 150,
        "v2_compliance_percentage": 85.5,
        "syntax_errors": 3,
        "file_size_violations": 5
    }
    
    with open(analysis_file, 'w') as f:
        json.dump(analysis_data, f, indent=2)
    
    return analysis_file


@pytest.fixture
def mock_cookies():
    """Mock cookies for testing."""
    return [
        {
# SECURITY: Token placeholder - replace with environment variable
# SECURITY: Token placeholder - replace with environment variable
            "domain": "chat.openai.com",
            "path": "/",
            "expiry": 1735689600
        },
        {
# SECURITY: Token placeholder - replace with environment variable
# SECURITY: Token placeholder - replace with environment variable
            "domain": "openai.com",
            "path": "/",
            "expiry": 1735689600
        }
    ]


@pytest.fixture
def mock_cookie_file(temp_dir, mock_cookies):
    """Create mock cookie file for testing."""
    cookie_file = temp_dir / "test_cookies.json"
    with open(cookie_file, 'w') as f:
        json.dump(mock_cookies, f, indent=2)
    return str(cookie_file)


# Test markers for categorization
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests for individual components"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests for system components"
    )
    config.addinivalue_line(
        "markers", "messaging: Tests for messaging system functionality"
    )
    config.addinivalue_line(
        "markers", "discord: Tests for Discord commander functionality"
    )
    config.addinivalue_line(
        "markers", "database: Tests for database integration"
    )
    config.addinivalue_line(
        "markers", "v2_compliance: Tests for V2 compliance validation"
    )
    config.addinivalue_line(
        "markers", "performance: Performance and load tests"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take longer to run"
    )
    config.addinivalue_line(
        "markers", "requires_selenium: Tests that require Selenium WebDriver"
    )
    config.addinivalue_line(
# SECURITY: Token placeholder - replace with environment variable
    )
    config.addinivalue_line(
        "markers", "requires_pyautogui: Tests that require PyAutoGUI"
    )


# Test collection hooks
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add markers based on test file names
        if "test_messaging" in item.nodeid:
            item.add_marker(pytest.mark.messaging)
        elif "test_discord" in item.nodeid:
            item.add_marker(pytest.mark.discord)
        elif "test_database" in item.nodeid:
            item.add_marker(pytest.mark.database)
        elif "test_v2_compliance" in item.nodeid:
            item.add_marker(pytest.mark.v2_compliance)
        elif "test_performance" in item.nodeid:
            item.add_marker(pytest.mark.performance)
        
        # Add slow marker for tests that might take longer
        if "integration" in item.nodeid or "performance" in item.nodeid:
            item.add_marker(pytest.mark.slow)


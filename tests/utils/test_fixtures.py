#!/usr/bin/env python3
"""
Test Fixtures - Shared Test Utilities
=====================================

Shared fixtures and utilities for the test suite.
Provides common test data, mocks, and helper functions.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import sys
import pytest
import tempfile
import json
import sqlite3
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Any, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestDataFactory:
    """Factory for creating test data."""
    
    @staticmethod
    def create_coordinates_data() -> Dict[str, Any]:
        """Create test coordinates data."""
        return {
            "version": "2.0",
            "last_updated": "2025-09-17T12:00:00Z",
            "agents": {
                "Agent-1": {
                    "active": True,
                    "chat_input_coordinates": [-1269, 481],
                    "onboarding_coordinates": [-1265, 171],
                    "description": "Infrastructure Specialist"
                },
                "Agent-2": {
                    "active": True,
                    "chat_input_coordinates": [-308, 480],
                    "onboarding_coordinates": [-304, 170],
                    "description": "Data Processing Expert"
                },
                "Agent-3": {
                    "active": False,
                    "chat_input_coordinates": [-1269, 1001],
                    "onboarding_coordinates": [-1265, 691],
                    "description": "Quality Assurance Lead"
                },
                "Agent-4": {
                    "active": True,
                    "chat_input_coordinates": [-308, 1000],
                    "onboarding_coordinates": [-304, 690],
                    "description": "Project Coordinator"
                },
                "Agent-5": {
                    "active": True,
                    "chat_input_coordinates": [652, 421],
                    "onboarding_coordinates": [656, 111],
                    "description": "Business Intelligence"
                },
                "Agent-6": {
                    "active": True,
                    "chat_input_coordinates": [1612, 419],
                    "onboarding_coordinates": [1616, 109],
                    "description": "Code Quality Specialist"
                },
                "Agent-7": {
                    "active": True,
                    "chat_input_coordinates": [920, 851],
                    "onboarding_coordinates": [924, 541],
                    "description": "Web Development Expert"
                },
                "Agent-8": {
                    "active": True,
                    "chat_input_coordinates": [1611, 941],
                    "onboarding_coordinates": [1615, 631],
                    "description": "Integration Specialist"
                }
            }
        }
    
    @staticmethod
    def create_agent_status_data(agent_id: str = "Agent-1") -> Dict[str, Any]:
        """Create test agent status data."""
        return {
            "agent_id": agent_id,
            "team": "Team Alpha",
            "specialization": "Database Specialist",
            "captain": "Agent-4",
            "status": "active",
            "cycle_count": 5,
            "tasks_completed": 7,
            "coordination_efficiency": 98.0,
            "v2_compliance": 90.0
        }
    
    @staticmethod
    def create_working_tasks_data() -> Dict[str, Any]:
        """Create test working tasks data."""
        return {
            "current_task": {
                "id": "DB_011",
                "title": "Query Optimization",
                "status": "in_progress",
                "priority": "HIGH",
                "assigned_to": "Agent-3",
                "created_at": "2025-09-17T10:00:00Z",
                "deadline": "2025-09-18T18:00:00Z"
            },
            "task_history": [
                {
                    "id": "DB_010",
                    "title": "Schema Migration",
                    "status": "completed",
                    "completed_at": "2025-09-17T09:30:00Z"
                }
            ]
        }
    
    @staticmethod
    def create_future_tasks_data() -> Dict[str, Any]:
        """Create test future tasks data."""
        return {
            "available_tasks": [
                {
                    "id": "DB_012",
                    "title": "Performance Tuning",
                    "priority": "MEDIUM",
                    "estimated_duration": "2h",
                    "dependencies": ["DB_011"]
                },
                {
                    "id": "DB_013",
                    "title": "Backup Strategy",
                    "priority": "LOW",
                    "estimated_duration": "1h",
                    "dependencies": []
                }
            ]
        }
    
    @staticmethod
    def create_discord_message_data() -> Dict[str, Any]:
        """Create test Discord message data."""
        return {
            "content": "Test message from Discord",
            "author": {
                "id": "123456789",
                "username": "testuser",
                "display_name": "Test User"
            },
            "channel": {
                "id": "987654321",
                "name": "general"
            },
            "timestamp": "2025-09-17T12:00:00Z"
        }


class MockFactory:
    """Factory for creating test mocks."""
    
    @staticmethod
    def create_pyautogui_mock():
        """Create PyAutoGUI mock."""
        mock = MagicMock()
        mock.click.return_value = None
        mock.typewrite.return_value = None
        mock.hotkey.return_value = None
        mock.press.return_value = None
        mock.sleep.return_value = None
        mock.position.return_value = (0, 0)
        mock.size.return_value = (1920, 1080)
        return mock
    
    @staticmethod
    def create_pyperclip_mock():
        """Create Pyperclip mock."""
        mock = MagicMock()
        mock.copy.return_value = None
        mock.paste.return_value = "test clipboard content"
        return mock
    
    @staticmethod
    def create_discord_mock():
        """Create Discord library mock."""
        mock = MagicMock()
        
        # Mock Intents
        mock.Intents.default.return_value = MagicMock()
        mock.Intents.default.return_value.message_content = True
        mock.Intents.default.return_value.guilds = True
        mock.Intents.default.return_value.messages = True
        
        # Mock Bot
        mock.Bot = MagicMock()
        mock.Bot.return_value.command_prefix = '!'
        mock.Bot.return_value.intents = mock.Intents.default.return_value
        
        # Mock Interaction
        mock.Interaction = MagicMock()
        mock.Interaction.response = MagicMock()
        mock.Interaction.response.send_message = MagicMock()
        
        # Mock Embed
        mock.Embed = MagicMock()
        mock.Embed.return_value.title = "Test Embed"
        mock.Embed.return_value.description = "Test Description"
        mock.Embed.return_value.color = MagicMock()
        mock.Embed.return_value.color.value = 0x00ff00
        mock.Embed.return_value.fields = []
        
        return mock
    
    @staticmethod
    def create_database_mock():
        """Create database mock."""
        mock = MagicMock()
        mock.execute.return_value = None
        mock.fetchall.return_value = []
        mock.fetchone.return_value = None
        mock.commit.return_value = None
        mock.rollback.return_value = None
        mock.close.return_value = None
        return mock


class TestFileManager:
    """Manager for test file operations."""
    
    @staticmethod
    def create_temp_file(content: str, suffix: str = '.json') -> str:
        """Create temporary file with content."""
        with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as f:
            f.write(content)
            return f.name
    
    @staticmethod
    def create_temp_json_file(data: Dict[str, Any]) -> str:
        """Create temporary JSON file with data."""
        return TestFileManager.create_temp_file(json.dumps(data, indent=2))
    
    @staticmethod
    def create_temp_sqlite_db() -> str:
        """Create temporary SQLite database."""
        db_path = tempfile.mktemp(suffix='.db')
        conn = sqlite3.connect(db_path)
        conn.close()
        return db_path
    
    @staticmethod
    def cleanup_file(file_path: str):
        """Clean up temporary file."""
        try:
            Path(file_path).unlink()
        except FileNotFoundError:
            pass


# Pytest Fixtures
@pytest.fixture
def test_coordinates():
    """Fixture providing test coordinates."""
    return TestDataFactory.create_coordinates_data()


@pytest.fixture
def temp_coordinates_file(test_coordinates):
    """Fixture providing temporary coordinates file."""
    temp_path = TestFileManager.create_temp_json_file(test_coordinates)
    yield temp_path
    TestFileManager.cleanup_file(temp_path)


@pytest.fixture
def mock_pyautogui():
    """Fixture providing mocked PyAutoGUI."""
    with patch('services.messaging.core.messaging_service.pyautogui') as mock:
        yield MockFactory.create_pyautogui_mock()


@pytest.fixture
def mock_pyperclip():
    """Fixture providing mocked Pyperclip."""
    with patch('services.messaging.core.messaging_service.pyperclip') as mock:
        yield MockFactory.create_pyperclip_mock()


@pytest.fixture
def mock_discord():
    """Fixture providing mocked Discord library."""
    with patch('discord') as mock:
        yield MockFactory.create_discord_mock()


@pytest.fixture
def test_agents():
    """Fixture providing test agent IDs."""
    return ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]


@pytest.fixture
def expected_coordinates():
    """Fixture providing expected coordinates."""
    return {
        "Agent-1": (-1269, 481),
        "Agent-2": (-308, 480),
        "Agent-3": (-1269, 1001),
        "Agent-4": (-308, 1000),
        "Agent-5": (652, 421),
        "Agent-6": (1612, 419),
        "Agent-7": (920, 851),
        "Agent-8": (1611, 941)
    }


@pytest.fixture
def messaging_service(temp_coordinates_file):
    """Fixture providing messaging service instance."""
    from services.messaging.core.messaging_service import MessagingService
    return MessagingService(temp_coordinates_file)


@pytest.fixture
def coordinate_loader(temp_coordinates_file):
    """Fixture providing coordinate loader instance."""
    from core.coordinate_loader import CoordinateLoader
    loader = CoordinateLoader(temp_coordinates_file)
    loader.load()
    return loader


@pytest.fixture
def temp_dir():
    """Fixture providing temporary directory."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    import shutil
    shutil.rmtree(temp_dir)


@pytest.fixture
def temp_database(temp_dir):
    """Fixture providing temporary database."""
    db_path = Path(temp_dir) / "test.db"
    conn = sqlite3.connect(str(db_path))
    conn.close()
    yield str(db_path)
    TestFileManager.cleanup_file(str(db_path))


@pytest.fixture
def agent_status_data():
    """Fixture providing agent status data."""
    return TestDataFactory.create_agent_status_data()


@pytest.fixture
def working_tasks_data():
    """Fixture providing working tasks data."""
    return TestDataFactory.create_working_tasks_data()


@pytest.fixture
def future_tasks_data():
    """Fixture providing future tasks data."""
    return TestDataFactory.create_future_tasks_data()


@pytest.fixture
def discord_message_data():
    """Fixture providing Discord message data."""
    return TestDataFactory.create_discord_message_data()


# Test Helper Functions
def assert_message_formatting(formatted_message: str, sender: str, recipient: str, 
                            content: str, priority: str = "NORMAL"):
    """Assert message formatting is correct."""
    assert f"FROM: {sender}" in formatted_message
    assert f"TO: {recipient}" in formatted_message
    assert f"Priority: {priority}" in formatted_message
    assert content in formatted_message
    assert "[A2A] MESSAGE" in formatted_message
    assert "DISCORD DEVLOG REMINDER" in formatted_message


def assert_coordinate_validation(loader, agent_id: str, expected_coords: tuple):
    """Assert coordinate validation is correct."""
    coords = loader.get_agent_coordinates(agent_id)
    assert coords == expected_coords


def assert_agent_validation(service, agent_id: str, expected_status: bool):
    """Assert agent validation is correct."""
    is_active = service._is_agent_active(agent_id)
    assert is_active == expected_status


def create_test_workspace_structure(temp_dir: str, agent_id: str = "Agent-3"):
    """Create test workspace structure."""
    workspace_dir = Path(temp_dir) / "agent_workspaces" / agent_id
    workspace_dir.mkdir(parents=True, exist_ok=True)
    
    # Create status.json
    status_data = TestDataFactory.create_agent_status_data(agent_id)
    with open(workspace_dir / "status.json", 'w') as f:
        json.dump(status_data, f)
    
    # Create working_tasks.json
    working_tasks_data = TestDataFactory.create_working_tasks_data()
    with open(workspace_dir / "working_tasks.json", 'w') as f:
        json.dump(working_tasks_data, f)
    
    # Create future_tasks.json
    future_tasks_data = TestDataFactory.create_future_tasks_data()
    with open(workspace_dir / "future_tasks.json", 'w') as f:
        json.dump(future_tasks_data, f)
    
    return workspace_dir



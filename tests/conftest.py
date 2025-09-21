#!/usr/bin/env python3
"""
Test Configuration - Pytest Fixtures and Configuration
======================================================

Pytest configuration and shared fixtures for the test suite.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import sys
import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@pytest.fixture
def test_coordinates():
    """Fixture providing test coordinates."""
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
                "active": True,
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

@pytest.fixture
def temp_coordinates_file(test_coordinates):
    """Fixture providing temporary coordinates file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_coordinates, f)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    Path(temp_path).unlink()

@pytest.fixture
def mock_pyautogui():
    """Fixture providing mocked PyAutoGUI."""
    with patch('services.messaging.core.messaging_service.pyautogui') as mock:
        mock.click.return_value = None
        mock.typewrite.return_value = None
        mock.hotkey.return_value = None
        yield mock

@pytest.fixture
def mock_discord():
    """Fixture providing mocked Discord library."""
    with patch('discord') as mock:
        mock.Intents.default.return_value = Mock()
        mock.Interaction = Mock()
        mock.Embed = Mock()
        yield mock

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

# Pytest configuration
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection."""
    for item in items:
        # Add markers based on test names
        if "integration" in item.name:
            item.add_marker(pytest.mark.integration)
        elif "unit" in item.name:
            item.add_marker(pytest.mark.unit)
        elif "slow" in item.name:
            item.add_marker(pytest.mark.slow)
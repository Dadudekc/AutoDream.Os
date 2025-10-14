#!/usr/bin/env python3
"""
Browser Test Fixtures
=====================

Common test fixtures and mocks for browser-related tests.
Extracted for V2 compliance (<400 lines per file).

Author: Agent-6 (Testing Infrastructure Lead)
V2 Compliance: Extracted from test_browser_unified.py
"""

from dataclasses import dataclass
from pathlib import Path
from unittest.mock import MagicMock, Mock


# Mock Configuration Classes
@dataclass
class MockBrowserConfig:
    """Mock browser configuration."""

    headless: bool = False
    user_data_dir: str | None = None
    window_size: tuple[int, int] = (1920, 1080)
    timeout: float = 30.0
    implicit_wait: float = 10.0
    page_load_timeout: float = 120.0


@dataclass
class MockTheaConfig:
    """Mock Thea configuration."""

    conversation_url: str = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
    cookie_file: str = "data/thea_cookies.json"
    auto_save_cookies: bool = True


@dataclass
class MockTheaAutoConfig:
    """Mock Thea automation configuration."""

    thea_url: str = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
    cookie_file: str = "thea_cookies.json"
    responses_dir: str = "thea_responses"
    headless: bool = False
    timeout: int = 120


@dataclass
class MockSessionInfo:
    """Mock session information."""

    session_id: str
    service_name: str
    status: str


class MockChromeBrowserAdapter:
    """Mock Chrome browser adapter."""

    def __init__(self):
        self.driver = None
        self.config = None


class MockTheaAutomation:
    """Mock Thea automation."""

    def __init__(self, config=None):
        self.config = config or MockTheaAutoConfig()
        self.cookie_file = Path(self.config.cookie_file)

    def has_valid_cookies(self):
        return False

    def cleanup(self):
        pass


def create_mock_driver():
    """Create a mock Selenium WebDriver."""
    driver = MagicMock()
    driver.title = "Test Page"
    driver.current_url = "https://example.com"
    driver.get = Mock()
    driver.quit = Mock()
    driver.find_element = Mock()
    driver.find_elements = Mock(return_value=[])
    return driver


def create_mock_chrome_options():
    """Create mock Chrome options."""
    options = Mock()
    options.add_argument = Mock()
    options.add_experimental_option = Mock()
    return options

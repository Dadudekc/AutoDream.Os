#!/usr/bin/env python3
"""
Browser Session Tests - Cookies, ChatGPT Integration & Lifecycle
================================================================

Tests for cookie persistence, ChatGPT/Thea integration compatibility,
and browser lifecycle management.

Part 3 of 3 in refactored browser test suite.
Original: test_browser_unified.py (414L → split into 3 files)

Author: Agent-6 (Testing Infrastructure Lead)
Refactored: Agent-3 (Infrastructure & DevOps)
Mission: C-057 - V2 Compliance Test Refactoring
"""

import json
import sys
import time
from pathlib import Path

import pytest

# Add src and root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Try importing from unified_browser_service
try:
    from infrastructure.unified_browser_service import (
        TheaConfig,
    )

    BROWSER_SERVICE_AVAILABLE = True
except ImportError:
    BROWSER_SERVICE_AVAILABLE = False
    # Create mock classes for testing
    from dataclasses import dataclass

    @dataclass
    class TheaConfig:
        conversation_url: str = (
            "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
        )
        cookie_file: str = "data/thea_cookies.json"
        auto_save_cookies: bool = True


# Import test fixtures - need to go up two levels from tests/browser/
sys.path.insert(0, str(Path(__file__).parent.parent))
from test_fixtures_browser import (
    MockTheaAutoConfig as TheaAutoConfig,
)
from test_fixtures_browser import (
    MockTheaAutomation as TheaAutomation,
)

# Import thea_automation from root
try:
    from thea_automation import TheaAutomation as RealTheaAutomation
    from thea_automation import TheaConfig as RealTheaAutoConfig

    TheaAutomation = RealTheaAutomation
    TheaAutoConfig = RealTheaAutoConfig
    THEA_AUTOMATION_AVAILABLE = True
except ImportError:
    THEA_AUTOMATION_AVAILABLE = False


# ============================================================================
# TEST CATEGORY: COOKIE PERSISTENCE
# ============================================================================


class TestCookiePersistence:
    """Test cookie persistence functionality."""

    def test_cookie_save_load_thea_automation(self):
        """Test 7: Cookie save and load in TheaAutomation."""
        # Create config with test cookie file
        config = TheaAutoConfig(cookie_file="test_cookies_temp.json")

        # Create automation instance
        thea = TheaAutomation(config)

        # Test that cookie file path is set correctly
        assert thea.cookie_file == Path("test_cookies_temp.json")

        # Test has_valid_cookies when file doesn't exist
        assert thea.has_valid_cookies() is False

        # Cleanup
        if thea.cookie_file.exists():
            thea.cookie_file.unlink()

    def test_cookie_expiry_validation(self):
        """Test 8: Cookie expiry validation."""
        config = TheaAutoConfig(cookie_file="test_cookies_expiry.json")
        thea = TheaAutomation(config)

        # Create test cookie file with expired cookies
        test_cookies = [
            {
                "name": "test_cookie",
                "value": "test_value",
                "domain": "chatgpt.com",
                "expiry": time.time() - 1000,  # Expired
            }
        ]

        with open(thea.cookie_file, "w") as f:
            json.dump(test_cookies, f)

        # Should recognize as invalid (expired)
        # Current implementation checks expiry
        result = thea.has_valid_cookies()

        # Cleanup
        if thea.cookie_file.exists():
            thea.cookie_file.unlink()

        # Expired cookies should be filtered out
        assert result is False


# ============================================================================
# TEST CATEGORY: CHATGPT INTEGRATION COMPATIBILITY
# ============================================================================


class TestChatGPTIntegration:
    """Test ChatGPT/Thea integration compatibility."""

    def test_chatgpt_url_configuration(self):
        """Test 9: ChatGPT URL configuration compatibility."""
        # Test TheaConfig
        thea_config = TheaConfig()
        assert (
            "chat.openai.com" in thea_config.conversation_url
            or "chatgpt.com" in thea_config.conversation_url
        )

        # Test TheaAutomation config
        auto_config = TheaAutoConfig()
        assert "chatgpt.com" in auto_config.thea_url
        assert (
            "thea-manager" in auto_config.thea_url
            or "g-67f437d96d7c81918b2dbc12f0423867" in auto_config.thea_url
        )


# ============================================================================
# TEST CATEGORY: BROWSER LIFECYCLE
# ============================================================================


class TestBrowserLifecycle:
    """Test browser lifecycle management."""

    def test_browser_context_manager(self):
        """Test 10: Browser cleanup with context manager."""
        cleanup_called = False

        class TestAutomation(TheaAutomation):
            def cleanup(self):
                nonlocal cleanup_called
                cleanup_called = True
                # Don't call super to avoid actually starting browser

        # Test context manager
        config = TheaAutoConfig()
        with TestAutomation(config) as thea:
            assert thea is not None

        # Cleanup should have been called
        assert cleanup_called is True


# ============================================================================
# TEST FIXTURES
# ============================================================================


@pytest.fixture
def thea_config():
    """Create test Thea configuration."""
    return TheaConfig(
        cookie_file="test_thea_cookies.json",
        auto_save_cookies=False,  # Don't auto-save in tests
    )


@pytest.fixture
def cleanup_test_files():
    """Cleanup test files after tests."""
    yield
    # Cleanup test cookie files
    test_files = ["test_cookies_temp.json", "test_cookies_expiry.json", "test_thea_cookies.json"]
    for file_path in test_files:
        path = Path(file_path)
        if path.exists():
            path.unlink()


# ============================================================================
# RUN CONFIGURATION
# ============================================================================

if __name__ == "__main__":
    # Run with pytest
    import sys

    pytest.main(
        [
            __file__,
            "-v",  # Verbose
            "--tb=short",  # Short traceback
            "-x",  # Stop on first failure
            "--color=yes",
        ]
    )

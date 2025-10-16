"""
Tests for UnifiedCookieManager - DUP-003 Consolidation
=======================================================

Comprehensive test suite for unified cookie management.
Tests both BrowserAdapter and WebDriver interfaces.

Author: Agent-6 (Quality Gates & VSCode Specialist)
Date: 2025-10-16
"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.infrastructure.browser.unified_cookie_manager import UnifiedCookieManager


@pytest.fixture
def temp_cookie_file(tmp_path):
    """Create temporary cookie file path."""
    return str(tmp_path / "test_cookies.json")


@pytest.fixture
def cookie_manager(temp_cookie_file):
    """Create cookie manager instance."""
    return UnifiedCookieManager(cookie_file=temp_cookie_file, auto_save=False)


@pytest.fixture
def sample_cookies():
    """Sample cookies for testing."""
    return [
        {"name": "session_id", "value": "abc123", "domain": "example.com"},
        {"name": "auth_token", "value": "xyz789", "domain": "example.com"},
    ]


# =====================================================================
# BrowserAdapter Interface Tests
# =====================================================================


class TestBrowserAdapterInterface:
    """Tests for BrowserAdapter interface."""

    def test_save_cookies_for_service_success(self, cookie_manager, sample_cookies):
        """Test saving cookies for a service."""
        browser_adapter = Mock()
        browser_adapter.is_running.return_value = True
        browser_adapter.get_cookies.return_value = sample_cookies

        result = cookie_manager.save_cookies_for_service(browser_adapter, "test_service")

        assert result is True
        assert "test_service" in cookie_manager.cookies
        assert len(cookie_manager.cookies["test_service"]) == 2

    def test_save_cookies_for_service_browser_not_running(self, cookie_manager):
        """Test saving cookies when browser not running."""
        browser_adapter = Mock()
        browser_adapter.is_running.return_value = False

        result = cookie_manager.save_cookies_for_service(browser_adapter, "test_service")

        assert result is False
        assert "test_service" not in cookie_manager.cookies

    def test_load_cookies_for_service_success(self, cookie_manager, sample_cookies):
        """Test loading cookies for a service."""
        browser_adapter = Mock()
        browser_adapter.is_running.return_value = True
        cookie_manager.cookies["test_service"] = sample_cookies

        result = cookie_manager.load_cookies_for_service(browser_adapter, "test_service")

        assert result is True
        browser_adapter.add_cookies.assert_called_once_with(sample_cookies)

    def test_load_cookies_for_service_not_found(self, cookie_manager):
        """Test loading cookies when service not found."""
        browser_adapter = Mock()
        browser_adapter.is_running.return_value = True

        result = cookie_manager.load_cookies_for_service(browser_adapter, "missing_service")

        assert result is False

    def test_has_valid_session_true(self, cookie_manager, sample_cookies):
        """Test has_valid_session returns True."""
        cookie_manager.cookies["test_service"] = sample_cookies

        assert cookie_manager.has_valid_session("test_service") is True

    def test_has_valid_session_false(self, cookie_manager):
        """Test has_valid_session returns False."""
        assert cookie_manager.has_valid_session("missing_service") is False

    def test_has_valid_session_empty_cookies(self, cookie_manager):
        """Test has_valid_session with empty cookie list."""
        cookie_manager.cookies["test_service"] = []

        assert cookie_manager.has_valid_session("test_service") is False


# =====================================================================
# WebDriver Interface Tests
# =====================================================================


class TestWebDriverInterface:
    """Tests for Selenium WebDriver interface."""

    def test_save_cookies_webdriver_success(self, cookie_manager, sample_cookies):
        """Test saving cookies from WebDriver."""
        driver = Mock()
        driver.get_cookies.return_value = sample_cookies

        result = cookie_manager.save_cookies(driver)

        assert result is True
        assert "default" in cookie_manager.cookies
        assert len(cookie_manager.cookies["default"]) == 2

    def test_load_cookies_webdriver_success(self, cookie_manager, sample_cookies):
        """Test loading cookies into WebDriver."""
        driver = Mock()
        cookie_manager.cookies["default"] = sample_cookies

        result = cookie_manager.load_cookies(driver)

        assert result is True
        assert driver.add_cookie.call_count == 2

    def test_load_cookies_webdriver_partial_failure(self, cookie_manager, sample_cookies):
        """Test loading cookies with some failures."""
        driver = Mock()
        driver.add_cookie.side_effect = [None, Exception("Cookie error")]
        cookie_manager.cookies["default"] = sample_cookies

        result = cookie_manager.load_cookies(driver)

        # Should return True if at least one cookie loaded
        assert result is True

    def test_load_cookies_webdriver_no_cookies(self, cookie_manager):
        """Test loading cookies when none exist."""
        driver = Mock()

        result = cookie_manager.load_cookies(driver)

        assert result is False

    def test_has_valid_cookies_true(self, cookie_manager, sample_cookies):
        """Test has_valid_cookies returns True."""
        cookie_manager.cookies["default"] = sample_cookies

        assert cookie_manager.has_valid_cookies() is True

    def test_has_valid_cookies_false(self, cookie_manager):
        """Test has_valid_cookies returns False."""
        assert cookie_manager.has_valid_cookies() is False


# =====================================================================
# Common Operations Tests
# =====================================================================


class TestCommonOperations:
    """Tests for common cookie operations."""

    def test_clear_cookies_specific_service(self, cookie_manager, sample_cookies):
        """Test clearing cookies for specific service."""
        cookie_manager.cookies["service1"] = sample_cookies
        cookie_manager.cookies["service2"] = sample_cookies

        result = cookie_manager.clear_cookies("service1")

        assert result is True
        assert "service1" not in cookie_manager.cookies
        assert "service2" in cookie_manager.cookies

    def test_clear_cookies_all(self, cookie_manager, sample_cookies):
        """Test clearing all cookies."""
        cookie_manager.cookies["service1"] = sample_cookies
        cookie_manager.cookies["service2"] = sample_cookies

        result = cookie_manager.clear_cookies()

        assert result is True
        assert len(cookie_manager.cookies) == 0


# =====================================================================
# Persistence Tests
# =====================================================================


class TestPersistence:
    """Tests for cookie persistence."""

    def test_persist_cookies_success(self, cookie_manager, sample_cookies):
        """Test persisting cookies to file."""
        cookie_manager.cookies["test_service"] = sample_cookies

        result = cookie_manager._persist_cookies()

        assert result is True
        assert os.path.exists(cookie_manager.cookie_file)

        with open(cookie_manager.cookie_file) as f:
            data = json.load(f)
            assert "test_service" in data

    def test_load_persisted_cookies_success(self, temp_cookie_file, sample_cookies):
        """Test loading persisted cookies from file."""
        # Create cookie file
        os.makedirs(os.path.dirname(temp_cookie_file), exist_ok=True)
        with open(temp_cookie_file, "w") as f:
            json.dump({"test_service": sample_cookies}, f)

        manager = UnifiedCookieManager(cookie_file=temp_cookie_file, auto_save=False)

        assert "test_service" in manager.cookies
        assert len(manager.cookies["test_service"]) == 2

    def test_auto_save_enabled(self, temp_cookie_file, sample_cookies):
        """Test auto-save functionality."""
        manager = UnifiedCookieManager(cookie_file=temp_cookie_file, auto_save=True)
        browser_adapter = Mock()
        browser_adapter.is_running.return_value = True
        browser_adapter.get_cookies.return_value = sample_cookies

        manager.save_cookies_for_service(browser_adapter, "test_service")

        assert os.path.exists(temp_cookie_file)


# =====================================================================
# Encryption Tests (Optional Feature)
# =====================================================================


class TestEncryption:
    """Tests for optional encryption feature."""

    @pytest.mark.skipif(
        not hasattr(UnifiedCookieManager, "_init_fernet"), reason="Encryption not available"
    )
    def test_encryption_disabled_by_default(self, cookie_manager):
        """Test encryption is disabled by default."""
        assert cookie_manager.enable_encryption is False

    def test_generate_encryption_key(self):
        """Test encryption key generation."""
        try:
            key = UnifiedCookieManager.generate_encryption_key()
            assert isinstance(key, str)
            assert len(key) > 0
        except ImportError:
            # Expected if cryptography not installed
            pytest.skip("Cryptography library not available")


# =====================================================================
# Integration Tests
# =====================================================================


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_complete_workflow_browser_adapter(
        self, cookie_manager, sample_cookies, temp_cookie_file
    ):
        """Test complete workflow with BrowserAdapter."""
        # Save cookies
        browser_adapter = Mock()
        browser_adapter.is_running.return_value = True
        browser_adapter.get_cookies.return_value = sample_cookies

        cookie_manager.save_cookies_for_service(browser_adapter, "test_service")
        cookie_manager._persist_cookies()

        # Create new manager and load
        new_manager = UnifiedCookieManager(cookie_file=temp_cookie_file, auto_save=False)
        assert new_manager.has_valid_session("test_service")

        # Load cookies
        result = new_manager.load_cookies_for_service(browser_adapter, "test_service")
        assert result is True

    def test_complete_workflow_webdriver(self, cookie_manager, sample_cookies, temp_cookie_file):
        """Test complete workflow with WebDriver."""
        # Save cookies
        driver = Mock()
        driver.get_cookies.return_value = sample_cookies

        cookie_manager.save_cookies(driver)
        cookie_manager._persist_cookies()

        # Create new manager and load
        new_manager = UnifiedCookieManager(cookie_file=temp_cookie_file, auto_save=False)
        assert new_manager.has_valid_cookies()

        # Load cookies
        result = new_manager.load_cookies(driver)
        assert result is True

#!/usr/bin/env python3
"""
Unified Browser Service - V2 Compliance Module
==============================================

Consolidated browser management system following SOLID principles.
Combines functionality from:
- chrome_undetected.py (basic Chrome adapter)
- thea_*.py modules (session management, cookies, profile)
- thea_modules/*.py (browser operations, content scraping)

SOLID Implementation:
- SRP: Each service class has single responsibility
- OCP: Extensible browser adapter system
- DIP: Dependencies injected via constructor

Author: Agent-3 (DevOps Specialist)
Refactored by: Agent-6 (VSCode Forking & Quality Gates Specialist)
License: MIT
"""

from typing import Any

from .browser.browser_adapter import ChromeBrowserAdapter
from .browser.browser_models import BrowserConfig, TheaConfig
from .browser.browser_operations import BrowserOperations
from .browser.cookie_manager import CookieManager
from .browser.session_manager import SessionManager


class UnifiedBrowserService:
    """Main unified browser service interface."""

    def __init__(
        self,
        browser_config: BrowserConfig | None = None,
        thea_config: TheaConfig | None = None,
    ):
        """Initialize unified browser service."""
        self.browser_config = browser_config or BrowserConfig()
        self.thea_config = thea_config or TheaConfig()

        # Initialize components
        self.browser_adapter = ChromeBrowserAdapter()
        self.cookie_manager = CookieManager(
            cookie_file=self.thea_config.cookie_file,
            auto_save=self.thea_config.auto_save_cookies,
        )
        self.session_manager = SessionManager(self.thea_config)
        self.operations = BrowserOperations(self.browser_adapter, self.thea_config)

        # Load persisted cookies
        self.cookie_manager._load_persisted_cookies()

    def start_browser(self) -> bool:
        """Start the browser."""
        return self.browser_adapter.start(self.browser_config)

    def stop_browser(self) -> None:
        """Stop the browser."""
        self.browser_adapter.stop()

    def create_session(self, service_name: str) -> str | None:
        """Create a new browser session."""
        return self.session_manager.create_session(service_name)

    def navigate_to_conversation(self, url: str | None = None) -> bool:
        """Navigate to conversation page."""
        return self.operations.navigate_to_conversation(url)

    def send_message(self, message: str) -> bool:
        """Send a message."""
        return self.operations.send_message(message)

    def wait_for_response(self, timeout: float = 30.0) -> bool:
        """Wait for response to be ready."""
        return self.operations.wait_for_response_ready(timeout)

    def save_cookies(self, service_name: str) -> bool:
        """Save cookies for a service."""
        return self.cookie_manager.save_cookies(self.browser_adapter, service_name)

    def load_cookies(self, service_name: str) -> bool:
        """Load cookies for a service."""
        return self.cookie_manager.load_cookies(self.browser_adapter, service_name)

    def can_make_request(self, service_name: str, session_id: str) -> tuple[bool, str]:
        """Check if a request can be made."""
        return self.session_manager.can_make_request(service_name, session_id)

    def record_request(self, service_name: str, session_id: str, success: bool = True) -> None:
        """Record a request."""
        self.session_manager.record_request(service_name, session_id, success)

    def get_session_info(self, session_id: str) -> dict[str, Any]:
        """Get session information."""
        return self.session_manager.get_session_info(session_id)

    def get_rate_limit_status(self, service_name: str) -> dict[str, Any]:
        """Get rate limit status."""
        return self.session_manager.get_rate_limit_status(service_name)

    def get_page_status(self) -> dict[str, Any]:
        """Get current page status."""
        return self.operations.get_page_status()

    def is_browser_running(self) -> bool:
        """Check if browser is running."""
        return self.browser_adapter.is_running()

    def has_valid_session(self, service_name: str) -> bool:
        """Check if there's a valid session."""
        return self.cookie_manager.has_valid_session(service_name)

    def get_browser_info(self) -> dict[str, Any]:
        """Get comprehensive browser information."""
        return {
            "browser_running": self.is_browser_running(),
            "current_url": self.browser_adapter.get_current_url(),
            "page_title": self.browser_adapter.get_title(),
            "sessions": len(self.session_manager.sessions),
            "services_with_cookies": list(self.cookie_manager.cookies.keys()),
            "page_status": self.get_page_status(),
        }


def create_browser_service(
    headless: bool = False,
    user_data_dir: str | None = None,
    conversation_url: str = "https://chat.openai.com/",
) -> UnifiedBrowserService:
    """Factory function to create browser service."""
    browser_config = BrowserConfig(headless=headless, user_data_dir=user_data_dir)
    thea_config = TheaConfig(conversation_url=conversation_url)
    return UnifiedBrowserService(browser_config, thea_config)


if __name__ == "__main__":
    # Example usage
    service = create_browser_service(headless=True)

    if service.start_browser():
        print("✅ Browser service started successfully")

        # Create a session
        session_id = service.create_session("test_service")
        if session_id:
            print(f"✅ Created session: {session_id}")

            # Check if we can make a request
            can_request, reason = service.can_make_request("test_service", session_id)
            print(f"📊 Can make request: {can_request} ({reason})")

        # Get browser info
        info = service.get_browser_info()
        print(f"📊 Browser Info: {info}")

        service.stop_browser()
        print("✅ Browser service stopped")

    else:
        print("❌ Failed to start browser service")

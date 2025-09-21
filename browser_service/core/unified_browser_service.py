#!/usr/bin/env python3
"""
Unified Browser Service
=======================

Main unified browser service for V2 compliance.
"""

import logging
from typing import Optional, Dict, List, Any, Tuple

from ..adapters.chrome_adapter import ChromeBrowserAdapter
from ..managers.cookie_manager import CookieManager
from ..managers.session_manager import SessionManager
from ..operations.browser_operations import BrowserOperations
from ..config.browser_config import BrowserConfig, TheaConfig

logger = logging.getLogger(__name__)


class UnifiedBrowserService:
    """Unified browser service for Thea interactions."""

    def __init__(self, browser_config: Optional[BrowserConfig] = None, thea_config: Optional[TheaConfig] = None):
        """Initialize unified browser service."""
        self.browser_config = browser_config or BrowserConfig()
        self.thea_config = thea_config or TheaConfig()
        
        # Initialize components
        self.browser_adapter = ChromeBrowserAdapter()
        self.cookie_manager = CookieManager()
        self.session_manager = SessionManager(self.thea_config)
        self.browser_operations = BrowserOperations(self.browser_adapter, self.thea_config)

    def start_browser(self) -> bool:
        """Start the browser."""
        return self.browser_adapter.start(self.browser_config)

    def stop_browser(self) -> None:
        """Stop the browser."""
        self.browser_adapter.stop()

    def create_session(self, service_name: str) -> Optional[str]:
        """Create a new session."""
        return self.session_manager.create_session(service_name)

    def navigate_to_conversation(self, url: Optional[str] = None) -> bool:
        """Navigate to conversation page."""
        return self.browser_operations.navigate_to_conversation(url)

    def send_message(self, message: str) -> bool:
        """Send a message."""
        return self.browser_operations.send_message(message)

    def wait_for_response(self, timeout: float = 30.0) -> bool:
        """Wait for response."""
        return self.browser_operations.wait_for_response_ready(timeout)

    def save_cookies(self, service_name: str) -> bool:
        """Save cookies."""
        return self.cookie_manager.save_cookies(self.browser_adapter, service_name)

    def load_cookies(self, service_name: str) -> bool:
        """Load cookies."""
        return self.cookie_manager.load_cookies(self.browser_adapter, service_name)

    def can_make_request(self, service_name: str, session_id: str) -> Tuple[bool, str]:
        """Check if request can be made."""
        return self.session_manager.can_make_request(service_name, session_id)

    def record_request(self, service_name: str, session_id: str, success: bool = True) -> None:
        """Record a request."""
        self.session_manager.record_request(service_name, session_id, success)

    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Get session information."""
        return self.session_manager.get_session_info(session_id)

    def get_rate_limit_status(self, service_name: str) -> Dict[str, Any]:
        """Get rate limit status."""
        return self.session_manager.get_rate_limit_status(service_name)

    def get_page_status(self) -> Dict[str, Any]:
        """Get page status."""
        return self.browser_operations.get_page_status()

    def is_browser_running(self) -> bool:
        """Check if browser is running."""
        return self.browser_adapter.is_running()

    def has_valid_session(self, service_name: str) -> bool:
        """Check if service has valid session."""
        return self.cookie_manager.has_valid_session(service_name)

    def get_browser_info(self) -> Dict[str, Any]:
        """Get browser information."""
        return {
            "browser_running": self.is_browser_running(),
            "current_url": self.browser_adapter.get_current_url(),
            "page_title": self.browser_adapter.get_title(),
            "config": {
                "headless": self.browser_config.headless,
                "window_size": self.browser_config.window_size,
                "timeout": self.browser_config.timeout
            }
        }


def create_browser_service(
    headless: bool = False,
    user_data_dir: Optional[str] = None,
    window_size: Tuple[int, int] = (1920, 1080)
) -> UnifiedBrowserService:
    """Create a browser service with specified configuration."""
    browser_config = BrowserConfig(
        headless=headless,
        user_data_dir=user_data_dir,
        window_size=window_size
    )
    
    return UnifiedBrowserService(browser_config=browser_config)



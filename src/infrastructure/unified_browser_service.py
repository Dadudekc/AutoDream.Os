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
License: MIT
"""

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


# Import enhanced unified configuration system with fallback
try:
    from ..core.enhanced_unified_config import get_enhanced_config
    _unified_config = get_enhanced_config()
except ImportError:
    # Fallback configuration for Agent-7 Web chunk support
    class _FallbackConfig:
        def get_timeout_config(self):
            return {
                "SCRAPE_TIMEOUT": 30.0,
                "QUALITY_CHECK_INTERVAL": 10.0,
                "RESPONSE_WAIT_TIMEOUT": 120.0
            }
    _unified_config = _FallbackConfig()


@dataclass
class BrowserConfig:
    """Configuration for browser operations with enhanced config integration."""

    headless: bool = False  # Use enhanced config for browser settings
    user_data_dir: str | None = None
    window_size: tuple[int, int] = (1920, 1080)
    timeout: float = _unified_config.get_timeout_config().get("SCRAPE_TIMEOUT", 30.0)
    implicit_wait: float = _unified_config.get_timeout_config().get("QUALITY_CHECK_INTERVAL", 10.0)
    page_load_timeout: float = _unified_config.get_timeout_config().get(
        "RESPONSE_WAIT_TIMEOUT", 120.0
    )


@dataclass
class TheaConfig:
    """Configuration for Thea Manager interactions with enhanced config integration."""

    conversation_url: str = (
        "https://chat.openai.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
    )
    cookie_file: str = "data/thea_cookies.json"
    auto_save_cookies: bool = True
    rate_limit_requests_per_minute: int = 10
    rate_limit_burst_limit: int = 5


@dataclass
class SessionInfo:
    """Session information."""

    session_id: str
    service_name: str
    status: str
    created_at: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    request_count: int = 0


@dataclass
class RateLimitStatus:
    """Rate limit status information."""

    requests_remaining: int
    reset_time: float | None = None
    is_rate_limited: bool = False


class BrowserAdapter(ABC):
    """Abstract base class for browser adapters."""

    @abstractmethod
    def start(self, config: BrowserConfig) -> bool:
        """Start the browser."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop the browser."""
        pass

    @abstractmethod
    def navigate(self, url: str) -> bool:
        """Navigate to URL."""
        pass

    @abstractmethod
    def get_current_url(self) -> str:
        """Get current URL."""
        pass

    @abstractmethod
    def get_title(self) -> str:
        """Get page title."""
        pass

    @abstractmethod
    def find_element(self, selector: str) -> Any:
        """Find element by CSS selector."""
        pass

    @abstractmethod
    def find_elements(self, selector: str) -> list[Any]:
        """Find elements by CSS selector."""
        pass

    @abstractmethod
    def execute_script(self, script: str, *args) -> Any:
        """Execute JavaScript."""
        pass

    @abstractmethod
    def is_running(self) -> bool:
        """Check if browser is running."""
        pass


class ChromeBrowserAdapter(BrowserAdapter):
    """Chrome browser adapter implementation."""

    def __init__(self):
        """Initialize Chrome adapter."""
        self.driver = None
        self.config = None

    def start(self, config: BrowserConfig) -> bool:
        """Start Chrome browser."""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options

            options = Options()
            if config.headless:
                options.add_argument("--headless")
            if config.user_data_dir:
                options.add_argument(f"--user-data-dir={config.user_data_dir}")
            options.add_argument(f"--window-size={config.window_size[0]},{config.window_size[1]}")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(config.implicit_wait)
            self.driver.set_page_load_timeout(config.page_load_timeout)
            self.config = config

            logger.info("✅ Chrome browser started successfully")
            return True

        except ImportError:
            logger.error("❌ Selenium not available for Chrome browser")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to start Chrome browser: {e}")
            return False

    def stop(self) -> None:
        """Stop Chrome browser."""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                logger.info("✅ Chrome browser stopped")
            except Exception as e:
                logger.error(f"❌ Error stopping Chrome browser: {e}")

    def navigate(self, url: str) -> bool:
        """Navigate to URL."""
        if not self.driver:
            return False
        try:
            self.driver.get(url)
            return True
        except Exception as e:
            logger.error(f"❌ Navigation failed: {e}")
            return False

    def get_current_url(self) -> str:
        """Get current URL."""
        return self.driver.current_url if self.driver else ""

    def get_title(self) -> str:
        """Get page title."""
        return self.driver.title if self.driver else ""

    def find_element(self, selector: str) -> Any:
        """Find element by CSS selector."""
        if not self.driver:
            return None
        try:
            from selenium.webdriver.common.by import By

            return self.driver.find_element(By.CSS_SELECTOR, selector)
        except Exception:
            return None

    def find_elements(self, selector: str) -> list[Any]:
        """Find elements by CSS selector."""
        if not self.driver:
            return []
        try:
            from selenium.webdriver.common.by import By

            return self.driver.find_elements(By.CSS_SELECTOR, selector)
        except Exception:
            return []

    def execute_script(self, script: str, *args) -> Any:
        """Execute JavaScript."""
        if not self.driver:
            return None
        try:
            return self.driver.execute_script(script, *args)
        except Exception as e:
            logger.error(f"❌ Script execution failed: {e}")
            return None

    def is_running(self) -> bool:
        """Check if browser is running."""
        return self.driver is not None

    def get_cookies(self) -> list[dict]:
        """Get cookies from browser."""
        if not self.driver:
            return []
        try:
            return self.driver.get_cookies()
        except Exception as e:
            logger.error(f"Failed to get cookies: {e}")
            return []

    def add_cookies(self, cookies: list[dict]) -> None:
        """Add cookies to browser."""
        if not self.driver:
            return
        for cookie in cookies:
            try:
                self.driver.add_cookie(cookie)
            except Exception as e:
                logger.error(f"Failed to add cookie: {e}")


class CookieManager:
    """Manages browser cookies for sessions."""

    def __init__(self, cookie_file: str = "data/thea_cookies.json", auto_save: bool = True):
        """Initialize cookie manager."""
        self.cookie_file = cookie_file
        self.auto_save = auto_save
        self.cookies: dict[str, list[dict]] = {}

    def save_cookies(self, browser_adapter: BrowserAdapter, service_name: str) -> bool:
        """Save cookies for a service."""
        if not browser_adapter.is_running():
            return False

        try:
            # Get cookies from browser
            cookies = browser_adapter.get_cookies()
            if cookies:
                self.cookies[service_name] = cookies

            if self.auto_save:
                return self._persist_cookies()

            return True

        except Exception as e:
            logger.error(f"❌ Failed to save cookies for {service_name}: {e}")
            return False

    def load_cookies(self, browser_adapter: BrowserAdapter, service_name: str) -> bool:
        """Load cookies for a service."""
        if not browser_adapter.is_running():
            return False

        try:
            if service_name in self.cookies:
                # Load cookies into browser
                browser_adapter.add_cookies(self.cookies[service_name])
                return True
            return False

        except Exception as e:
            logger.error(f"❌ Failed to load cookies for {service_name}: {e}")
            return False

    def has_valid_session(self, service_name: str) -> bool:
        """Check if there's a valid session for the service."""
        return service_name in self.cookies and len(self.cookies[service_name]) > 0

    def _persist_cookies(self) -> bool:
        """Persist cookies to file."""
        try:
            import json
            import os

            os.makedirs(os.path.dirname(self.cookie_file), exist_ok=True)
            with open(self.cookie_file, "w") as f:
                json.dump(self.cookies, f, indent=2)
            return True

        except Exception as e:
            logger.error(f"❌ Failed to persist cookies: {e}")
            return False

    def _load_persisted_cookies(self) -> bool:
        """Load persisted cookies from file."""
        try:
            import json
            import os

            if os.path.exists(self.cookie_file):
                with open(self.cookie_file) as f:
                    self.cookies = json.load(f)
                return True
            return False

        except Exception as e:
            logger.error(f"❌ Failed to load persisted cookies: {e}")
            return False


class SessionManager:
    """Manages browser sessions and rate limiting."""

    def __init__(self, config: TheaConfig):
        """Initialize session manager."""
        self.config = config
        self.sessions: dict[str, SessionInfo] = {}
        self.rate_limits: dict[str, RateLimitStatus] = {}

    def create_session(self, service_name: str) -> str | None:
        """Create a new session for a service."""
        session_id = f"{service_name}_{int(time.time())}_{hash(service_name) % 1000}"

        session_info = SessionInfo(
            session_id=session_id, service_name=service_name, status="active"
        )

        self.sessions[session_id] = session_info
        self.rate_limits[service_name] = RateLimitStatus(
            requests_remaining=self.config.rate_limit_requests_per_minute
        )

        logger.info(f"✅ Created session {session_id} for {service_name}")
        return session_id

    def can_make_request(self, service_name: str, session_id: str) -> tuple[bool, str]:
        """Check if a request can be made."""
        if session_id not in self.sessions:
            return False, "Session not found"

        if service_name not in self.rate_limits:
            return False, "Rate limit not configured"

        rate_limit = self.rate_limits[service_name]
        if rate_limit.is_rate_limited:
            return False, "Rate limited"

        if rate_limit.requests_remaining <= 0:
            return False, "No requests remaining"

        return True, ""

    def record_request(self, service_name: str, session_id: str, success: bool) -> None:
        """Record a request for rate limiting."""
        if service_name in self.rate_limits:
            rate_limit = self.rate_limits[service_name]
            rate_limit.requests_remaining -= 1

            if rate_limit.requests_remaining <= 0:
                rate_limit.is_rate_limited = True
                rate_limit.reset_time = time.time() + 60  # Reset in 1 minute

        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.last_activity = time.time()
            session.request_count += 1

    def wait_for_rate_limit_reset(self, service_name: str, session_id: str) -> None:
        """Wait for rate limit to reset."""
        if service_name in self.rate_limits:
            rate_limit = self.rate_limits[service_name]
            if rate_limit.reset_time:
                wait_time = rate_limit.reset_time - time.time()
                if wait_time > 0:
                    logger.info(f"⏳ Waiting {wait_time:.1f}s for rate limit reset")
                    time.sleep(wait_time)
                    rate_limit.is_rate_limited = False
                    rate_limit.requests_remaining = self.config.rate_limit_requests_per_minute
                    rate_limit.reset_time = None

    def get_session_info(self, session_id: str) -> dict[str, Any]:
        """Get session information."""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            return {
                "session_id": session.session_id,
                "service_name": session.service_name,
                "status": session.status,
                "created_at": session.created_at,
                "last_activity": session.last_activity,
                "request_count": session.request_count,
            }
        return {"error": "Session not found"}

    def get_rate_limit_status(self, service_name: str) -> dict[str, Any]:
        """Get rate limit status for a service."""
        if service_name in self.rate_limits:
            rate_limit = self.rate_limits[service_name]
            return {
                "requests_remaining": rate_limit.requests_remaining,
                "reset_time": rate_limit.reset_time,
                "is_rate_limited": rate_limit.is_rate_limited,
            }
        return {"error": "Service not configured"}


class BrowserOperations:
    """Handles browser operations and interactions."""

    def __init__(self, browser_adapter: BrowserAdapter, config: TheaConfig):
        """Initialize browser operations."""
        self.browser = browser_adapter
        self.config = config
        self.last_action_time = None

    def navigate_to_conversation(self, url: str | None = None) -> bool:
        """Navigate to conversation page."""
        target_url = url or self.config.conversation_url
        success = self.browser.navigate(target_url)

        if success:
            time.sleep(3)  # Allow page to load
            if self._verify_page_loaded():
                logger.info("✅ Successfully navigated to conversation")
                return True
            else:
                logger.error("❌ Failed to verify page loaded")
                return False
        return False

    def send_message(
        self, message: str, input_selector: str = "textarea", send_selector: str = "button"
    ) -> bool:
        """Send a message."""
        try:
            # Find input field
            input_element = self.browser.find_element(input_selector)
            if not input_element:
                logger.error("❌ Could not find input field")
                return False

            # Clear and type message
            input_element.clear()
            input_element.send_keys(message)
            time.sleep(1)

            # Find and click send button
            send_button = self.browser.find_element(send_selector)
            if not send_button:
                logger.error("❌ Could not find send button")
                return False

            send_button.click()
            self.last_action_time = time.time()

            logger.info("✅ Message sent successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send message: {e}")
            return False

    def wait_for_response_ready(
        self, timeout: float = 30.0, input_selector: str = "textarea"
    ) -> bool:
        """Wait for response to be ready."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self._is_input_available(input_selector):
                return True
            time.sleep(1.0)
        return False

    def _is_input_available(self, input_selector: str) -> bool:
        """Check if input field is available."""
        try:
            input_element = self.browser.find_element(input_selector)
            if input_element and input_element.is_enabled():
                return True
        except:
            pass
        return False

    def _verify_page_loaded(self) -> bool:
        """Verify that the page loaded correctly."""
        try:
            title = self.browser.get_title()
            if any(keyword in title.lower() for keyword in ["chat", "conversation", "thea"]):
                return True
            return False
        except Exception:
            return False

    def get_page_status(self, input_selector: str = "textarea") -> dict[str, Any]:
        """Get current page status."""
        try:
            return {
                "url": self.browser.get_current_url(),
                "title": self.browser.get_title(),
                "input_available": self._is_input_available(input_selector),
                "last_action": self.last_action_time,
                "ready_for_input": self.wait_for_response_ready(5.0, input_selector),
            }
        except Exception as e:
            return {
                "error": str(e),
                "url": "unknown",
                "title": "unknown",
                "input_available": False,
                "ready_for_input": False,
            }


class UnifiedBrowserService:
    """Main unified browser service interface."""

    def __init__(
        self, browser_config: BrowserConfig | None = None, thea_config: TheaConfig | None = None
    ):
        """Initialize unified browser service."""
        self.browser_config = browser_config or BrowserConfig()
        self.thea_config = thea_config or TheaConfig()

        # Initialize components
        self.browser_adapter = ChromeBrowserAdapter()
        self.cookie_manager = CookieManager(
            cookie_file=self.thea_config.cookie_file, auto_save=self.thea_config.auto_save_cookies
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

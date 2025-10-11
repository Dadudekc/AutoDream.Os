"""
Browser Adapter - Unified Browser Service
==========================================

Abstract browser adapter and Chrome implementation.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist) - Refactored from Agent-3
License: MIT
"""

import logging
from abc import ABC, abstractmethod
from typing import Any

from .browser_models import BrowserConfig

logger = logging.getLogger(__name__)


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

    @abstractmethod
    def get_cookies(self) -> list[dict]:
        """Get cookies from browser."""
        pass

    @abstractmethod
    def add_cookies(self, cookies: list[dict]) -> None:
        """Add cookies to browser."""
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

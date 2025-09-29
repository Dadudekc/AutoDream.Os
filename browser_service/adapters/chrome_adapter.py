#!/usr/bin/env python3
"""
Chrome Browser Adapter
======================

Chrome-specific browser adapter implementation.
"""

import logging
import time
from abc import ABC, abstractmethod
from typing import Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from ..config.browser_config import BrowserConfig

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
        """Navigate to a URL."""
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
        """Find element by selector."""
        pass

    @abstractmethod
    def find_elements(self, selector: str) -> list[Any]:
        """Find elements by selector."""
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
        self.driver: webdriver.Chrome | None = None
        self.config: BrowserConfig | None = None

    def start(self, config: BrowserConfig) -> bool:
        """Start Chrome browser."""
        try:
            self.config = config

            chrome_options = Options()
            if config.headless:
                chrome_options.add_argument("--headless")

            if config.user_data_dir:
                chrome_options.add_argument(f"--user-data-dir={config.user_data_dir}")

            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument(
                f"--window-size={config.window_size[0]},{config.window_size[1]}"
            )

            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(config.implicit_wait)
            self.driver.set_page_load_timeout(config.page_load_timeout)

            logger.info("Chrome browser started successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to start Chrome browser: {e}")
            return False

    def stop(self) -> None:
        """Stop Chrome browser."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Chrome browser stopped")
            except Exception as e:
                logger.error(f"Error stopping Chrome browser: {e}")
            finally:
                self.driver = None

    def navigate(self, url: str) -> bool:
        """Navigate to URL."""
        if not self.driver:
            return False

        try:
            self.driver.get(url)
            time.sleep(2)  # Allow page to load
            return True
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            return False

    def get_current_url(self) -> str:
        """Get current URL."""
        return self.driver.current_url if self.driver else ""

    def get_title(self) -> str:
        """Get page title."""
        return self.driver.title if self.driver else ""

    def find_element(self, selector: str) -> Any:
        """Find element by selector."""
        if not self.driver:
            return None

        try:
            return self.driver.find_element(By.CSS_SELECTOR, selector)
        except Exception as e:
            logger.error(f"Failed to find element {selector}: {e}")
            return None

    def find_elements(self, selector: str) -> list[Any]:
        """Find elements by selector."""
        if not self.driver:
            return []

        try:
            return self.driver.find_elements(By.CSS_SELECTOR, selector)
        except Exception as e:
            logger.error(f"Failed to find elements {selector}: {e}")
            return []

    def execute_script(self, script: str, *args) -> Any:
        """Execute JavaScript."""
        if not self.driver:
            return None

        try:
            return self.driver.execute_script(script, *args)
        except Exception as e:
            logger.error(f"Failed to execute script: {e}")
            return None

    def is_running(self) -> bool:
        """Check if browser is running."""
        return self.driver is not None

    def get_cookies(self) -> list[dict]:
        """Get browser cookies."""
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

        try:
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        except Exception as e:
            logger.error(f"Failed to add cookies: {e}")

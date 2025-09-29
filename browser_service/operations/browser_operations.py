#!/usr/bin/env python3
"""
Browser Operations
==================

Browser operation components for page interactions.
"""

import logging
import time
from typing import Any

from ..adapters.chrome_adapter import BrowserAdapter
from ..config.browser_config import TheaConfig

logger = logging.getLogger(__name__)


class BrowserOperations:
    """Handles browser operations for Thea interactions."""

    def __init__(self, browser_adapter: BrowserAdapter, config: TheaConfig):
        """Initialize browser operations."""
        self.browser_adapter = browser_adapter
        self.config = config

    def navigate_to_conversation(self, url: str | None = None) -> bool:
        """Navigate to Thea conversation page."""
        try:
            target_url = url or self.config.base_url

            if not self.browser_adapter.navigate(target_url):
                logger.error(f"Failed to navigate to {target_url}")
                return False

            # Wait for page to load
            time.sleep(3)

            # Verify page loaded correctly
            if not self._verify_page_loaded():
                logger.error("Page did not load correctly")
                return False

            logger.info(f"Successfully navigated to {target_url}")
            return True

        except Exception as e:
            logger.error(f"Error navigating to conversation: {e}")
            return False

    def send_message(
        self, message: str, input_selector: str = "textarea", send_selector: str = "button"
    ) -> bool:
        """Send a message to Thea."""
        try:
            # Find input field
            input_element = self.browser_adapter.find_element(input_selector)
            if not input_element:
                logger.error(f"Could not find input element: {input_selector}")
                return False

            # Clear and type message
            input_element.clear()
            # SECURITY: Key placeholder - replace with environment variable

            # Find and click send button
            send_button = self.browser_adapter.find_element(send_selector)
            if not send_button:
                logger.error(f"Could not find send button: {send_selector}")
                return False

            send_button.click()

            logger.info("Message sent successfully")
            return True

        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

    def wait_for_response_ready(
        self, timeout: float = 30.0, input_selector: str = "textarea"
    ) -> bool:
        """Wait for response to be ready."""
        try:
            start_time = time.time()

            while time.time() - start_time < timeout:
                if self._is_input_available(input_selector):
                    logger.info("Response ready - input field available")
                    return True

                time.sleep(1)

            logger.warning(f"Timeout waiting for response after {timeout} seconds")
            return False

        except Exception as e:
            logger.error(f"Error waiting for response: {e}")
            return False

    def _is_input_available(self, input_selector: str) -> bool:
        """Check if input field is available."""
        try:
            input_element = self.browser_adapter.find_element(input_selector)
            return input_element is not None and input_element.is_enabled()
        except Exception:
            return False

    def _verify_page_loaded(self) -> bool:
        """Verify that the page loaded correctly."""
        try:
            current_url = self.browser_adapter.get_current_url()
            title = self.browser_adapter.get_title()

            # Basic checks
            if not current_url or not title:
                return False

            # Check if we're on the right domain
            if "chatgpt.com" not in current_url:
                return False

            return True

        except Exception as e:
            logger.error(f"Error verifying page load: {e}")
            return False

    def get_page_status(self, input_selector: str = "textarea") -> dict[str, Any]:
        """Get current page status."""
        try:
            return {
                "url": self.browser_adapter.get_current_url(),
                "title": self.browser_adapter.get_title(),
                "input_available": self._is_input_available(input_selector),
                "page_loaded": self._verify_page_loaded(),
            }
        except Exception as e:
            logger.error(f"Error getting page status: {e}")
            return {
                "url": "",
                "title": "",
                "input_available": False,
                "page_loaded": False,
                "error": str(e),
            }

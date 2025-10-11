"""
Browser Operations - Unified Browser Service
=============================================

Handles browser operations and interactions.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist) - Refactored from Agent-3
License: MIT
"""

import logging
import time
from typing import Any

from .browser_adapter import BrowserAdapter
from .browser_models import TheaConfig

logger = logging.getLogger(__name__)


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

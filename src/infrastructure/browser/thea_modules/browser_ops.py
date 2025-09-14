"""
Thea Browser Operations Module - V2 Compliance
=============================================

Handles basic browser operations for Thea Manager interactions.
Provides input, clicking, and navigation functionality.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


class TheaBrowserOperations:
    """Handles basic browser operations for Thea Manager."""

    def __init__(self, driver: Any, config_manager: Any):
        pass
EXAMPLE USAGE:
==============

# Basic usage example
from src.infrastructure.browser.thea_modules.browser_ops import Browser_Ops

# Initialize and use
instance = Browser_Ops()
result = instance.execute()
print(f"Execution result: {result}")

# Advanced configuration
config = {
    "option1": "value1",
    "option2": True
}

instance = Browser_Ops(config)
advanced_result = instance.execute_advanced()
print(f"Advanced result: {advanced_result}")

        """Initialize browser operations with driver and configuration."""
        self.driver = driver
        self.config_manager = config_manager
        self._last_action_time = None

    def navigate_to_conversation(self) -> bool:
        """
        Navigate to the Thea Manager conversation.

        Returns:
            True if navigation successful, False otherwise
        """
        try:
            config = self.config_manager.get_config()
            self.driver.get(config.conversation_url)
            time.sleep(3)  # Allow page to load

            # Verify we're on the right page
            if self._verify_page_loaded():
                logger.info("✅ Successfully navigated to Thea Manager conversation")
                return True
            else:
                logger.error("❌ Failed to verify Thea Manager page loaded")
                return False

        except Exception as e:
            logger.error(f"❌ Navigation failed: {e}")
            return False

    def send_message(self, message: str) -> bool:
        """
        Send a message to Thea Manager.

        Args:
            message: Message to send

        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            # Find input field
            input_element = self._find_input_element()
            if not input_element:
                logger.error("❌ Could not find input field")
                return False

            # Clear and type message
            input_element.clear()
            input_element.send_keys(message)
            time.sleep(1)

            # Find and click send button
            send_button = self._find_send_button()
            if not send_button:
                logger.error("❌ Could not find send button")
                return False

            send_button.click()
            self._last_action_time = time.time()

            logger.info("✅ Message sent successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send message: {e}")
            return False

    def wait_for_response_ready(self, timeout: float = 30.0) -> bool:
        """
        Wait for response to be ready.

        Args:
            timeout: Maximum time to wait

        Returns:
            True if response ready, False otherwise
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self._is_input_available():
                return True
            time.sleep(1.0)
        return False

    def _find_input_element(self) -> Any | None:
        """Find the input element using primary and fallback selectors."""
        selectors = self.config_manager.get_selectors()
        fallback_selectors = self.config_manager.get_fallback_selectors()

        # Try primary selector first
        try:
            element = self.driver.find_element_by_css_selector(selectors["input"])
            if element and element.is_displayed():
                return element
        except:
            pass

        # Try fallback selectors
        for selector in fallback_selectors["input"]:
            try:
                element = self.driver.find_element_by_css_selector(selector)
                if element and element.is_displayed():
                    return element
            except:
                continue

        return None

    def _find_send_button(self) -> Any | None:
        """Find the send button using primary and fallback selectors."""
        selectors = self.config_manager.get_selectors()
        fallback_selectors = self.config_manager.get_fallback_selectors()

        # Try primary selector first
        try:
            element = self.driver.find_element_by_css_selector(selectors["send_button"])
            if element and element.is_displayed():
                return element
        except:
            pass

        # Try fallback selectors
        for selector in fallback_selectors["send"]:
            try:
                element = self.driver.find_element_by_css_selector(selector)
                if element and element.is_displayed():
                    return element
            except:
                continue

        return None

    def _is_input_available(self) -> bool:
        """Check if input field is available for new messages."""
        try:
            input_element = self._find_input_element()
            if input_element and input_element.is_enabled():
                return True
        except:
            pass
        return False

    def _verify_page_loaded(self) -> bool:
        """Verify that the Thea Manager page loaded correctly."""
        try:
            # Check for presence of key elements
            title = self.driver.title
            if "Thea Manager" in title or "ChatGPT" in title:
                return True

            # Check for conversation elements
            conversation_elements = self.driver.find_elements_by_css_selector(
                "[data-testid='conversation-turn']"
            )
            if conversation_elements:
                return True

            return False

        except Exception:
            return False

    def get_page_status(self) -> dict[str, Any]:
        """Get current page status information."""
        try:
            return {
                "url": self.driver.current_url,
                "title": self.driver.title,
                "input_available": self._is_input_available(),
                "last_action": self._last_action_time,
                "ready_for_input": self.wait_for_response_ready(5.0),
            }
        except Exception as e:
            return {
                "error": str(e),
                "url": "unknown",
                "title": "unknown",
                "input_available": False,
                "ready_for_input": False,
            }


class TheaElementFinder:
    """Utility class for finding elements with retry logic."""

    def __init__(self, driver: Any, max_retries: int = 3):
        """Initialize element finder."""
        self.driver = driver
        self.max_retries = max_retries

    def find_element_with_retry(self, selector: str, timeout: float = 10.0) -> Any | None:
        """
        Find element with retry logic.

        Args:
            selector: CSS selector to find
            timeout: Timeout per attempt

        Returns:
            Element if found, None otherwise
        """
        for attempt in range(self.max_retries):
            try:
                element = self.driver.find_element_by_css_selector(selector)
                if element and element.is_displayed():
                    return element
            except:
                if attempt < self.max_retries - 1:
                    time.sleep(1.0)
                continue

        return None

    def find_elements_with_retry(self, selector: str, timeout: float = 10.0) -> list[Any]:
        """
        Find elements with retry logic.

        Args:
            selector: CSS selector to find
            timeout: Timeout per attempt

        Returns:
            List of elements found
        """
        for attempt in range(self.max_retries):
            try:
                elements = self.driver.find_elements_by_css_selector(selector)
                if elements:
                    return elements
            except:
                if attempt < self.max_retries - 1:
                    time.sleep(1.0)
                continue

        return []

    def wait_for_element(self, selector: str, timeout: float = 30.0) -> Any | None:
        """
        Wait for element to appear.

        Args:
            selector: CSS selector to wait for
            timeout: Maximum time to wait

        Returns:
            Element if found within timeout, None otherwise
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            element = self.find_element_with_retry(selector, 5.0)
            if element:
                return element
            time.sleep(0.5)

        return None

#!/usr/bin/env python3
"""
Browser Operations for Browser Service
======================================

Handles browser operations and page interactions.
V2 Compliant: ≤400 lines, focused browser operations.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import time
import logging
from typing import Dict, List, Optional, Any

from .browser_adapter import BrowserAdapter
from .browser_service_models import TheaConfig

logger = logging.getLogger(__name__)


class BrowserOperations:
    """Handles browser operations and page interactions."""

    def __init__(self, browser_adapter: BrowserAdapter, thea_config: TheaConfig):
        """Initialize browser operations."""
        self.browser_adapter = browser_adapter
        self.thea_config = thea_config

    def navigate_to_conversation(self, url: Optional[str] = None) -> bool:
        """Navigate to conversation page."""
        try:
            target_url = url or self.thea_config.conversation_url
            return self.browser_adapter.navigate(target_url)
        except Exception as e:
            logger.error(f"❌ Failed to navigate to conversation: {e}")
            return False

    def send_message(self, message: str) -> bool:
        """Send a message to the conversation."""
        try:
            # Find the message input field
            input_selector = "textarea[placeholder*='Message']"
            input_element = self.browser_adapter.find_element(input_selector)
            
            if not input_element:
                logger.error("❌ Message input field not found")
                return False

            # Clear and type the message
            input_element.clear()
            input_element.send_keys(message)
            
            # Find and click send button
            send_selector = "button[data-testid='send-button']"
            send_button = self.browser_adapter.find_element(send_selector)
            
            if not send_button:
                logger.error("❌ Send button not found")
                return False

            send_button.click()
            logger.info(f"✅ Message sent: {message[:50]}...")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send message: {e}")
            return False

    def wait_for_response_ready(self, timeout: float = 30.0) -> bool:
        """Wait for response to be ready."""
        try:
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                # Check for response indicators
                if self._is_response_ready():
                    logger.info("✅ Response is ready")
                    return True
                
                time.sleep(1)
            
            logger.warning(f"⚠️ Response timeout after {timeout}s")
            return False

        except Exception as e:
            logger.error(f"❌ Error waiting for response: {e}")
            return False

    def get_page_status(self) -> Dict[str, Any]:
        """Get current page status."""
        try:
            status = {
                "url": self.browser_adapter.get_current_url(),
                "title": self.browser_adapter.get_title(),
                "is_logged_in": self._check_login_status(),
                "has_message_input": self._has_message_input(),
                "has_send_button": self._has_send_button(),
                "response_ready": self._is_response_ready()
            }
            return status

        except Exception as e:
            logger.error(f"❌ Failed to get page status: {e}")
            return {"error": str(e)}

    def _is_response_ready(self) -> bool:
        """Check if response is ready."""
        try:
            # Look for response indicators
            response_selectors = [
                "[data-testid='conversation-turn-2']",
                ".markdown",
                "[data-message-author-role='assistant']"
            ]
            
            for selector in response_selectors:
                elements = self.browser_adapter.find_elements(selector)
                if elements:
                    return True
            
            return False

        except Exception:
            return False

    def _check_login_status(self) -> bool:
        """Check if user is logged in."""
        try:
            # Look for login indicators
            login_selectors = [
                "button[data-testid='login-button']",
                "a[href*='login']",
                ".login-button"
            ]
            
            for selector in login_selectors:
                elements = self.browser_adapter.find_elements(selector)
                if elements:
                    return False  # Login button found = not logged in
            
            return True  # No login button found = likely logged in

        except Exception:
            return False

    def _has_message_input(self) -> bool:
        """Check if message input is available."""
        try:
            input_selector = "textarea[placeholder*='Message']"
            element = self.browser_adapter.find_element(input_selector)
            return element is not None
        except Exception:
            return False

    def _has_send_button(self) -> bool:
        """Check if send button is available."""
        try:
            send_selector = "button[data-testid='send-button']"
            element = self.browser_adapter.find_element(send_selector)
            return element is not None
        except Exception:
            return False

    def get_response_text(self) -> Optional[str]:
        """Get the latest response text."""
        try:
            response_selectors = [
                "[data-testid='conversation-turn-2'] .markdown",
                "[data-message-author-role='assistant'] .markdown",
                ".conversation-turn-2 .markdown"
            ]
            
            for selector in response_selectors:
                element = self.browser_adapter.find_element(selector)
                if element:
                    return element.text
            
            return None

        except Exception as e:
            logger.error(f"❌ Failed to get response text: {e}")
            return None

    def scroll_to_bottom(self) -> bool:
        """Scroll to bottom of page."""
        try:
            script = "window.scrollTo(0, document.body.scrollHeight);"
            self.browser_adapter.execute_script(script)
            return True
        except Exception as e:
            logger.error(f"❌ Failed to scroll to bottom: {e}")
            return False


def create_browser_operations(browser_adapter: BrowserAdapter, thea_config: TheaConfig) -> BrowserOperations:
    """Create browser operations with adapter and config."""
    return BrowserOperations(browser_adapter, thea_config)


"""
Message Parser - ChatGPT Conversation Extraction
================================================

Handles message extraction and parsing from ChatGPT pages.
Extracted from extractor.py for V2 compliance and preventive optimization.

Author: Agent-1 - Browser Automation Specialist
Created: 2025-10-11 (Preventive Optimization)
License: MIT
"""

import logging
import time
from typing import Any

# Optional dependencies
try:
    from playwright.async_api import Page

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logging.warning("Playwright not available - Message parsing disabled")


class MessageParser:
    """Handles extraction and parsing of ChatGPT messages."""

    def __init__(
        self,
        message_selector: str = "[data-message-author-role]",
        text_selector: str = "[data-message-text]",
        timestamp_selector: str = "time",
        max_messages: int = 1000,
        logger: logging.Logger | None = None,
    ):
        """
        Initialize message parser.

        Args:
            message_selector: CSS selector for message elements
            text_selector: CSS selector for message text
            timestamp_selector: CSS selector for timestamps
            max_messages: Maximum messages to extract
            logger: Logger instance
        """
        self.message_selector = message_selector
        self.text_selector = text_selector
        self.timestamp_selector = timestamp_selector
        self.max_messages = max_messages
        self.logger = logger or logging.getLogger(__name__)

    async def extract_messages(self, page: Page) -> list[dict[str, Any]]:
        """
        Extract messages from ChatGPT conversation page.

        Args:
            page: Playwright page object

        Returns:
            List of message dictionaries
        """
        if not PLAYWRIGHT_AVAILABLE:
            self.logger.error("Cannot extract messages - Playwright not available")
            return []

        try:
            messages = []

            # Wait for messages to load
            await page.wait_for_selector(self.message_selector, timeout=10000)

            # Find all message elements
            message_elements = await page.query_selector_all(self.message_selector)

            self.logger.info(f"Found {len(message_elements)} message elements")

            for i, element in enumerate(message_elements):
                try:
                    # Extract message data
                    message_data = await self._extract_message_data(element, i)
                    if message_data:
                        messages.append(message_data)

                except Exception as e:
                    self.logger.warning(f"Failed to extract message {i}: {e}")
                    continue

            # Limit message count
            if len(messages) > self.max_messages:
                messages = messages[-self.max_messages :]
                self.logger.info(f"Limited to {self.max_messages} most recent messages")

            self.logger.info(f"Extracted {len(messages)} messages")
            return messages

        except Exception as e:
            self.logger.error(f"Message extraction failed: {e}")
            return []

    async def _extract_message_data(self, element, index: int) -> dict[str, Any] | None:
        """
        Extract data from a single message element.

        Args:
            element: Playwright element handle
            index: Message index

        Returns:
            Message data dictionary or None
        """
        try:
            # Get message role (user/assistant)
            role = await element.get_attribute("data-message-author-role")
            if not role:
                role = "unknown"

            # Get message text
            text_element = await element.query_selector(self.text_selector)
            if text_element:
                text = await text_element.inner_text()
            else:
                text = await element.inner_text()

            # Get timestamp
            timestamp_element = await element.query_selector(self.timestamp_selector)
            timestamp = None
            if timestamp_element:
                timestamp_attr = await timestamp_element.get_attribute("datetime")
                if timestamp_attr:
                    timestamp = timestamp_attr
                else:
                    timestamp_text = await timestamp_element.inner_text()
                    timestamp = timestamp_text

            # Create message data
            message_data = {
                "index": index,
                "role": role,
                "text": text.strip(),
                "timestamp": timestamp or time.time(),
                "extraction_time": time.time(),
                "message_id": f"msg_{int(time.time())}_{index}",
            }

            return message_data

        except Exception as e:
            self.logger.warning(f"Failed to extract message data: {e}")
            return None

    async def extract_conversation(
        self, page: Page, conversation_id: str | None = None
    ) -> dict[str, Any]:
        """
        Extract complete conversation from ChatGPT page.

        Args:
            page: Playwright page object
            conversation_id: Optional conversation identifier

        Returns:
            Dictionary with conversation data
        """
        try:
            # Generate conversation ID if not provided
            if not conversation_id:
                conversation_id = f"conv_{int(time.time())}"

            # Get current URL
            current_url = page.url

            # Extract messages
            messages = await self.extract_messages(page)

            # Create conversation data
            conversation = {
                "conversation_id": conversation_id,
                "url": current_url,
                "extraction_time": time.time(),
                "message_count": len(messages),
                "messages": messages,
                "metadata": {
                    "extractor_version": "2.0.0",
                    "max_messages_limit": self.max_messages,
                    "selector_used": self.message_selector,
                },
            }

            self.logger.info(
                f"Extracted conversation {conversation_id} with {len(messages)} messages"
            )
            return conversation

        except Exception as e:
            self.logger.error(f"Conversation extraction failed: {e}")
            return {
                "conversation_id": conversation_id or f"conv_{int(time.time())}",
                "error": str(e),
                "extraction_time": time.time(),
                "messages": [],
            }

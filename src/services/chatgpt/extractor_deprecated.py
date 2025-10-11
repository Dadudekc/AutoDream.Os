"""
Conversation Extractor - V2 Compliant
====================================

Conversation extraction and management for ChatGPT interactions.
Provides structured extraction and storage of ChatGPT conversations.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Browser Automation Specialist
License: MIT
"""

import json
import logging
import time
from pathlib import Path
from typing import Any

# Optional dependencies
try:
    from playwright.async_api import Page

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logging.warning("Playwright not available - ChatGPT extraction disabled")

# V2 Integration imports
try:
    from ...core.unified_config import get_unified_config
    from ...core.unified_logging_system import get_logger
except ImportError as e:
    logging.warning(f"V2 integration imports failed: {e}")

    # Fallback implementations
    def get_unified_config():
        return type("MockConfig", (), {"get_env": lambda x, y=None: y})()

    def get_logger(name):
        return logging.getLogger(name)


class ConversationExtractor:
    """
    ChatGPT conversation extraction and management.

    Provides capabilities for:
    - Extracting conversation history
    - Parsing message structure
    - Saving conversations to files
    - Managing conversation metadata
    """

    def __init__(self, config: dict | None = None):
        """
        Initialize conversation extractor.

        Args:
            config: Configuration dictionary (uses config/chatgpt.yml if None)
        """
        self.config = config or {}
        self.logger = get_logger(__name__)

        # V2 Integration
        self.unified_config = get_unified_config()

        # Extraction settings
        extraction_config = self.config.get("extraction", {})
        self.message_selector = extraction_config.get(
            "message_selector", "[data-message-author-role]"
        )
        self.text_selector = extraction_config.get("text_selector", "[data-message-text]")
        self.timestamp_selector = extraction_config.get("timestamp_selector", "time")
        self.max_messages = extraction_config.get("max_messages", 1000)
        self.save_format = extraction_config.get("save_format", "json")

        # Storage settings
        self.conversations_dir = Path("runtime/conversations")
        self.conversations_dir.mkdir(parents=True, exist_ok=True)

        if not PLAYWRIGHT_AVAILABLE:
            self.logger.warning("Conversation extraction disabled - Playwright not available")

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
        """Extract data from a single message element."""
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

    def save_conversation(
        self, conversation: dict[str, Any], filename: str | None = None
    ) -> str | None:
        """
        Save conversation to file.

        Args:
            conversation: Conversation data to save
            filename: Output filename (generates if None)

        Returns:
            Path to saved file, or None if failed
        """
        try:
            # Generate filename if not provided
            if not filename:
                conv_id = conversation.get("conversation_id", f"conv_{int(time.time())}")
                timestamp = int(conversation.get("extraction_time", time.time()))
                filename = f"{conv_id}_{timestamp}.{self.save_format}"

            filepath = self.conversations_dir / filename

            # Save based on format
            if self.save_format == "json":
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(conversation, f, indent=2, ensure_ascii=False)
            else:
                # Default to JSON for other formats
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(conversation, f, indent=2, ensure_ascii=False)

            self.logger.info(f"Conversation saved to {filepath}")
            return str(filepath)

        except Exception as e:
            self.logger.error(f"Failed to save conversation: {e}")
            return None

    def load_conversation(self, filename: str) -> dict[str, Any] | None:
        """
        Load conversation from file.

        Args:
            filename: Filename to load

        Returns:
            Conversation data, or None if failed
        """
        try:
            filepath = self.conversations_dir / filename

            if not filepath.exists():
                self.logger.error(f"Conversation file not found: {filepath}")
                return None

            with open(filepath, encoding="utf-8") as f:
                conversation = json.load(f)

            self.logger.info(f"Conversation loaded from {filepath}")
            return conversation

        except Exception as e:
            self.logger.error(f"Failed to load conversation: {e}")
            return None

    def list_conversations(self) -> list[dict[str, Any]]:
        """
        List all saved conversations.

        Returns:
            List of conversation metadata
        """
        try:
            conversations = []

            for filepath in self.conversations_dir.glob(f"*.{self.save_format}"):
                try:
                    # Load conversation metadata
                    with open(filepath, encoding="utf-8") as f:
                        conversation = json.load(f)

                    # Extract metadata
                    metadata = {
                        "filename": filepath.name,
                        "conversation_id": conversation.get("conversation_id"),
                        "message_count": conversation.get("message_count", 0),
                        "extraction_time": conversation.get("extraction_time"),
                        "file_size": filepath.stat().st_size,
                        "modified_time": filepath.stat().st_mtime,
                    }

                    conversations.append(metadata)

                except Exception as e:
                    self.logger.warning(f"Failed to read conversation {filepath}: {e}")
                    continue

            # Sort by extraction time (newest first)
            conversations.sort(key=lambda x: x.get("extraction_time", 0), reverse=True)

            self.logger.info(f"Found {len(conversations)} conversations")
            return conversations

        except Exception as e:
            self.logger.error(f"Failed to list conversations: {e}")
            return []

    def cleanup_old_conversations(self, max_age_days: int = 30) -> int:
        """
        Clean up old conversation files.

        Args:
            max_age_days: Maximum age of files to keep

        Returns:
            Number of files cleaned up
        """
        try:
            current_time = time.time()
            max_age_seconds = max_age_days * 24 * 60 * 60
            cleaned_count = 0

            for filepath in self.conversations_dir.glob(f"*.{self.save_format}"):
                if filepath.stat().st_mtime < current_time - max_age_seconds:
                    filepath.unlink()
                    cleaned_count += 1

            self.logger.info(f"Cleaned up {cleaned_count} old conversation files")
            return cleaned_count

        except Exception as e:
            self.logger.error(f"Failed to cleanup old conversations: {e}")
            return 0

    def get_extraction_info(self) -> dict[str, Any]:
        """Get information about extraction capabilities."""
        return {
            "playwright_available": PLAYWRIGHT_AVAILABLE,
            "message_selector": self.message_selector,
            "text_selector": self.text_selector,
            "timestamp_selector": self.timestamp_selector,
            "max_messages": self.max_messages,
            "save_format": self.save_format,
            "conversations_dir": str(self.conversations_dir),
            "conversations_count": len(list(self.conversations_dir.glob(f"*.{self.save_format}"))),
        }

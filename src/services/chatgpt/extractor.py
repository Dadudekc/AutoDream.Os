"""
Conversation Extractor - V2 Compliant Facade
===========================================

Conversation extraction and management for ChatGPT interactions.
Refactored for preventive optimization: 349L → <300L (14%+ reduction).

This facade coordinates between:
- MessageParser: Message extraction and parsing
- ConversationStorage: File persistence operations

V2 Compliance: ≤300 lines, 100L buffer from 400L limit.

Author: Agent-1 - Browser Automation Specialist
Refactored: 2025-10-11 (Preventive Optimization)
License: MIT
"""

import logging
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


# Modular components
from .extractor_message_parser import MessageParser
from .extractor_storage import ConversationStorage


class ConversationExtractor:
    """
    ChatGPT conversation extraction and management facade.

    Coordinates between MessageParser and ConversationStorage to provide:
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
        message_selector = extraction_config.get("message_selector", "[data-message-author-role]")
        text_selector = extraction_config.get("text_selector", "[data-message-text]")
        timestamp_selector = extraction_config.get("timestamp_selector", "time")
        max_messages = extraction_config.get("max_messages", 1000)

        # Storage settings
        save_format = extraction_config.get("save_format", "json")
        storage_dir = Path("runtime/conversations")

        # Initialize modular components
        self.parser = MessageParser(
            message_selector=message_selector,
            text_selector=text_selector,
            timestamp_selector=timestamp_selector,
            max_messages=max_messages,
            logger=self.logger,
        )

        self.storage = ConversationStorage(
            storage_dir=storage_dir, save_format=save_format, logger=self.logger
        )

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
        return await self.parser.extract_messages(page)

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
        return await self.parser.extract_conversation(page, conversation_id)

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
        return self.storage.save_conversation(conversation, filename)

    def load_conversation(self, filename: str) -> dict[str, Any] | None:
        """
        Load conversation from file.

        Args:
            filename: Filename to load

        Returns:
            Conversation data, or None if failed
        """
        return self.storage.load_conversation(filename)

    def list_conversations(self) -> list[dict[str, Any]]:
        """
        List all saved conversations.

        Returns:
            List of conversation metadata
        """
        return self.storage.list_conversations()

    def cleanup_old_conversations(self, max_age_days: int = 30) -> int:
        """
        Clean up old conversation files.

        Args:
            max_age_days: Maximum age of files to keep

        Returns:
            Number of files cleaned up
        """
        return self.storage.cleanup_old_conversations(max_age_days)

    def get_extraction_info(self) -> dict[str, Any]:
        """Get information about extraction capabilities."""
        storage_info = self.storage.get_storage_info()

        return {
            "playwright_available": PLAYWRIGHT_AVAILABLE,
            "message_selector": self.parser.message_selector,
            "text_selector": self.parser.text_selector,
            "timestamp_selector": self.parser.timestamp_selector,
            "max_messages": self.parser.max_messages,
            **storage_info,
        }

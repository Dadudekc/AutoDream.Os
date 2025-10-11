"""
Storage Manager - ChatGPT Conversation Persistence
==================================================

Handles saving, loading, listing, and cleanup of conversation files.
Extracted from extractor.py for V2 compliance and preventive optimization.

Author: Agent-1 - Browser Automation Specialist
Created: 2025-10-11 (Preventive Optimization)
License: MIT
"""

import json
import logging
import time
from pathlib import Path
from typing import Any


class ConversationStorage:
    """Handles persistence operations for ChatGPT conversations."""

    def __init__(
        self,
        storage_dir: Path = None,
        save_format: str = "json",
        logger: logging.Logger | None = None,
    ):
        """
        Initialize conversation storage.

        Args:
            storage_dir: Directory for storing conversations
            save_format: File format (json, etc.)
            logger: Logger instance
        """
        self.conversations_dir = storage_dir or Path("runtime/conversations")
        self.conversations_dir.mkdir(parents=True, exist_ok=True)
        self.save_format = save_format
        self.logger = logger or logging.getLogger(__name__)

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

    def get_storage_info(self) -> dict[str, Any]:
        """Get information about storage status."""
        return {
            "storage_dir": str(self.conversations_dir),
            "save_format": self.save_format,
            "conversations_count": len(list(self.conversations_dir.glob(f"*.{self.save_format}"))),
            "storage_exists": self.conversations_dir.exists(),
        }

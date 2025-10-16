"""
Message Repository - Data Access Layer
======================================

Handles all message-related data operations following the repository pattern.
This repository provides data access abstraction for message storage, history,
and retrieval operations.

Author: Agent-7 (Quarantine Mission Phase 3)
Date: 2025-10-16
Points: 300
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class MessageRepository:
    """
    Repository for message data operations.

    Provides data access layer for message persistence, history tracking,
    and retrieval. No business logic - pure data operations.

    Attributes:
        message_history_file: Path to message history JSON file
        inbox_root: Root directory for agent inboxes
    """

    def __init__(
        self,
        message_history_file: str = "data/message_history.json",
        inbox_root: str = "agent_workspaces",
    ):
        """
        Initialize message repository.

        Args:
            message_history_file: Path to message history storage
            inbox_root: Root directory for agent workspaces
        """
        self.message_history_file = Path(message_history_file)
        self.inbox_root = Path(inbox_root)
        self._ensure_history_file()

    def _ensure_history_file(self) -> None:
        """Ensure message history file exists with proper structure."""
        if not self.message_history_file.exists():
            self.message_history_file.parent.mkdir(parents=True, exist_ok=True)
            self._save_history(
                {
                    "messages": [],
                    "metadata": {"version": "1.0", "created_at": datetime.now().isoformat()},
                }
            )

    def _load_history(self) -> dict[str, Any]:
        """
        Load message history from file.

        Returns:
            Message history data dictionary
        """
        try:
            with open(self.message_history_file, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return {"messages": [], "metadata": {"version": "1.0"}}

    def _save_history(self, data: dict[str, Any]) -> bool:
        """
        Save message history to file.

        Args:
            data: Message history data dictionary

        Returns:
            True if save successful, False otherwise
        """
        try:
            with open(self.message_history_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except OSError:
            return False

    def save_message(self, message: dict[str, Any]) -> bool:
        """
        Save message to storage.

        Args:
            message: Message data dictionary

        Returns:
            True if save successful, False otherwise
        """
        data = self._load_history()
        messages = data.get("messages", [])

        # Add timestamp if not present
        if "timestamp" not in message:
            message["timestamp"] = datetime.now().isoformat()

        # Add message ID if not present
        if "message_id" not in message:
            message["message_id"] = f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        messages.append(message)
        data["messages"] = messages

        return self._save_history(data)

    def get_message_history(
        self, agent_id: str | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get message history, optionally filtered by agent.

        Args:
            agent_id: Optional agent ID to filter messages
            limit: Optional maximum number of messages to return

        Returns:
            List of message data dictionaries
        """
        data = self._load_history()
        messages = data.get("messages", [])

        # Filter by agent if specified
        if agent_id:
            messages = [m for m in messages if m.get("to") == agent_id or m.get("from") == agent_id]

        # Sort by timestamp (newest first)
        messages.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        # Apply limit if specified
        if limit:
            messages = messages[:limit]

        return messages

    def get_recent_messages(self, limit: int = 10) -> list[dict[str, Any]]:
        """
        Get recent messages across all agents.

        Args:
            limit: Maximum number of messages to return (default: 10)

        Returns:
            List of recent message data dictionaries
        """
        return self.get_message_history(limit=limit)

    def get_messages_by_sender(self, sender_id: str) -> list[dict[str, Any]]:
        """
        Get all messages from specific sender.

        Args:
            sender_id: Sender identifier

        Returns:
            List of message data dictionaries
        """
        data = self._load_history()
        messages = data.get("messages", [])

        sender_messages = [m for m in messages if m.get("from") == sender_id]

        sender_messages.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        return sender_messages

    def get_messages_by_recipient(self, recipient_id: str) -> list[dict[str, Any]]:
        """
        Get all messages to specific recipient.

        Args:
            recipient_id: Recipient identifier

        Returns:
            List of message data dictionaries
        """
        data = self._load_history()
        messages = data.get("messages", [])

        recipient_messages = [m for m in messages if m.get("to") == recipient_id]

        recipient_messages.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        return recipient_messages

    def get_inbox_messages(self, agent_id: str) -> list[dict[str, Any]]:
        """
        Get inbox messages for specific agent from file system.

        Args:
            agent_id: Agent identifier

        Returns:
            List of inbox message file metadata
        """
        inbox_dir = self.inbox_root / agent_id / "inbox"

        if not inbox_dir.exists():
            return []

        messages = []
        for msg_file in inbox_dir.glob("*.md"):
            messages.append(
                {
                    "filename": msg_file.name,
                    "path": str(msg_file),
                    "modified": datetime.fromtimestamp(msg_file.stat().st_mtime).isoformat(),
                    "size": msg_file.stat().st_size,
                    "agent_id": agent_id,
                }
            )

        messages.sort(key=lambda x: x["modified"], reverse=True)
        return messages

    def get_message_count(self, agent_id: str | None = None) -> int:
        """
        Get message count, optionally filtered by agent.

        Args:
            agent_id: Optional agent ID to filter messages

        Returns:
            Count of messages
        """
        messages = self.get_message_history(agent_id=agent_id)
        return len(messages)

    def clear_old_messages(self, days: int = 30) -> int:
        """
        Clear messages older than specified days.

        Args:
            days: Number of days to retain (default: 30)

        Returns:
            Number of messages removed
        """
        data = self._load_history()
        messages = data.get("messages", [])

        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        original_count = len(messages)

        # Keep messages newer than cutoff
        filtered_messages = []
        for msg in messages:
            timestamp_str = msg.get("timestamp", "")
            try:
                msg_time = datetime.fromisoformat(timestamp_str).timestamp()
                if msg_time >= cutoff:
                    filtered_messages.append(msg)
            except (ValueError, AttributeError):
                # Keep messages with invalid timestamps
                filtered_messages.append(msg)

        data["messages"] = filtered_messages
        self._save_history(data)

        return original_count - len(filtered_messages)

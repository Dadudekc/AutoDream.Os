#!/usr/bin/env python3
"""Messaging utilities for listing agents and message history."""
from typing import Any, Dict, List

from src.utils.logger import get_logger
from .models.messaging_models import UnifiedMessage
from .utils.agent_registry import list_agents


class MessagingUtils:
    """Utility methods for messaging service."""

    def __init__(self, messages: List[UnifiedMessage]):
        """Initialize utility service with message history."""
        self.agents: Dict[str, Dict[str, Any]] = list_agents()
        self.inbox_paths = {
            agent_id: info.get("inbox", "")
            for agent_id, info in self.agents.items()
        }
        self.messages = messages

    def list_agents(self) -> None:
        """List all available agents."""
        get_logger(__name__).info("📋 AVAILABLE AGENTS:")
        get_logger(__name__).info("=" * 50)
        for agent_id, info in self.agents.items():
            get_logger(__name__).info(f"🤖 {agent_id}: {info['description']}")
            coords = info.get("coords", {})
            get_logger(__name__).info(f"   📍 Coordinates: {coords}")
            inbox = self.inbox_paths.get(agent_id, "N/A")
            get_logger(__name__).info(f"   📬 Inbox: {inbox}")
            get_logger(__name__).info("")

    def show_coordinates(self) -> None:
        """Show agent coordinates."""
        get_logger(__name__).info("📍 AGENT COORDINATES:")
        get_logger(__name__).info("=" * 30)
        for agent_id, info in self.agents.items():
            coords = info.get("coords", {})
            get_logger(__name__).info(f"🤖 {agent_id}: {coords}")
        get_logger(__name__).info("")

    def show_message_history(self) -> None:
        """Show message history."""
        get_logger(__name__).info("📜 MESSAGE HISTORY:")
        get_logger(__name__).info("=" * 30)
        for i, message in enumerate(self.messages, 1):
            get_logger(__name__).info(f"{i}. {message.sender} → {message.recipient}")
            get_logger(__name__).info(f"   Type: {message.message_type.value}")
            get_logger(__name__).info(f"   Priority: {message.priority.value}")
            get_logger(__name__).info(f"   ID: {message.message_id}")
            get_logger(__name__).info("")

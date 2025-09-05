#!/usr/bin/env python3
"""Messaging utilities for agent interactions."""

from typing import List

from .models.messaging_models import UnifiedMessage
from .utils.agent_registry import AGENTS, list_agents
from src.utils.logger import get_logger


class MessagingUtils:
    """Utility methods for messaging service."""

    def __init__(self, messages: List[UnifiedMessage]):
        """Initialize utility service."""
        self.messages = messages

    def list_agents(self) -> None:
        """List all available agents."""
        get_logger(__name__).info("📋 AVAILABLE AGENTS:")
        get_logger(__name__).info("=" * 50)
        for agent_id in list_agents():
            info = AGENTS[agent_id]
            get_logger(__name__).info(f"🤖 {agent_id}: {info['description']}")
            get_logger(__name__).info(f"   📍 Coordinates: {info['coords']}")
            get_logger(__name__).info(f"   📬 Inbox: {info['inbox']}")
            get_logger(__name__).info()

    def show_coordinates(self) -> None:
        """Show agent coordinates."""
        get_logger(__name__).info("📍 AGENT COORDINATES:")
        get_logger(__name__).info("=" * 30)
        for agent_id in list_agents():
            info = AGENTS[agent_id]
            get_logger(__name__).info(f"🤖 {agent_id}: {info['coords']}")
        get_logger(__name__).info()

    def show_message_history(self) -> None:
        """Show message history."""
        get_logger(__name__).info("📜 MESSAGE HISTORY:")
        get_logger(__name__).info("=" * 30)
        for i, message in enumerate(self.messages, 1):
            get_logger(__name__).info(
                f"{i}. {message.sender} → {message.recipient}"
            )
            get_logger(__name__).info(f"   Type: {message.message_type.value}")
            get_logger(__name__).info(f"   Priority: {message.priority.value}")
            get_logger(__name__).info(f"   ID: {message.message_id}")
            get_logger(__name__).info()

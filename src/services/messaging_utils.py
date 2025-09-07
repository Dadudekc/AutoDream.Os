#!/usr/bin/env python3
"""
Messaging Utils Module - Agent Cellphone V2
==========================================

Utility methods for the messaging service.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import List

from src.utils.logger import get_logger
from .models.messaging_models import UnifiedMessage
from .utils.agent_registry import AGENTS, list_agents as registry_list_agents


class MessagingUtils:
    """Utility methods for messaging service."""

    def __init__(self, messages: List[UnifiedMessage]):
        """Initialize utility service."""
        self.messages = messages
        self.logger = get_logger(__name__)

    def list_agents(self) -> None:
        """List all available agents."""
        self.logger.info("📋 AVAILABLE AGENTS:")
        self.logger.info("=" * 50)
        for agent_id in registry_list_agents():
            info = AGENTS[agent_id]
            self.logger.info(f"🤖 {agent_id}: {info['description']}")
            self.logger.info(f"   📍 Coordinates: {info['coords']}")
            self.logger.info(f"   📬 Inbox: {info['inbox']}")
            self.logger.info("")

    def show_coordinates(self) -> None:
        """Show agent coordinates."""
        self.logger.info("📍 AGENT COORDINATES:")
        self.logger.info("=" * 30)
        for agent_id in registry_list_agents():
            info = AGENTS[agent_id]
            self.logger.info(f"🤖 {agent_id}: {info['coords']}")
        self.logger.info("")

    def show_message_history(self) -> None:
        """Show message history."""
        self.logger.info("📜 MESSAGE HISTORY:")
        self.logger.info("=" * 30)
        for i, message in enumerate(self.messages, 1):
            self.logger.info(f"{i}. {message.sender} → {message.recipient}")
            self.logger.info(f"   Type: {message.message_type.value}")
            self.logger.info(f"   Priority: {message.priority.value}")
            self.logger.info(f"   ID: {message.message_id}")
            self.logger.info("")

#!/usr/bin/env python3
"""
Messaging Utils Module - Agent Cellphone V2
==========================================

Utility methods for the messaging service.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import Any, Dict, List, Optional

from src.utils.logger import get_logger

from .models.messaging_models import UnifiedMessage
from .utils.agent_registry import AGENTS, list_agents as registry_list_agents


class MessagingUtils:
    """Utility methods for messaging service."""

    def __init__(
        self,
        agents: Optional[Dict[str, Dict[str, Any]]] = None,
        inbox_paths: Optional[Dict[str, str]] = None,
        messages: Optional[List[UnifiedMessage]] = None,
    ):
        """Initialize utility service."""
        self.agents = agents or AGENTS
        self.inbox_paths = inbox_paths or {}
        self.messages = messages or []

    def list_agents(self):
        """List all available agents."""
        get_logger(__name__).info("📋 AVAILABLE AGENTS:")
        get_logger(__name__).info("=" * 50)
        for agent_id in registry_list_agents():
            info = self.agents.get(agent_id, {})
            get_logger(__name__).info(f"🤖 {agent_id}: {info.get('description')}")
            get_logger(__name__).info(f"   📍 Coordinates: {info.get('coords')}")
            get_logger(__name__).info(
                f"   📬 Inbox: {self.inbox_paths.get(agent_id, 'N/A')}"
            )
            get_logger(__name__).info()

    def show_coordinates(self):
        """Show agent coordinates."""
        get_logger(__name__).info("📍 AGENT COORDINATES:")
        get_logger(__name__).info("=" * 30)
        for agent_id in registry_list_agents():
            info = self.agents.get(agent_id, {})
            get_logger(__name__).info(f"🤖 {agent_id}: {info.get('coords')}")
        get_logger(__name__).info()

    def show_message_history(self):
        """Show message history."""
        get_logger(__name__).info("📜 MESSAGE HISTORY:")
        get_logger(__name__).info("=" * 30)
        for i, message in enumerate(self.messages, 1):
            get_logger(__name__).info(f"{i}. {message.sender} → {message.recipient}")
            get_logger(__name__).info(f"   Type: {message.message_type.value}")
            get_logger(__name__).info(f"   Priority: {message.priority.value}")
            get_logger(__name__).info(f"   ID: {message.message_id}")
            get_logger(__name__).info()

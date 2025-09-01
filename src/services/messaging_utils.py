#!/usr/bin/env python3
"""
Messaging Utils Module - Agent Cellphone V2
==========================================

Utility methods for the messaging service.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import Dict, Any, List

from .models.messaging_models import UnifiedMessage


class MessagingUtils:
    """Utility methods for messaging service."""

    def __init__(self, agents: Dict[str, Dict[str, Any]], inbox_paths: Dict[str, str], messages: List[UnifiedMessage]):
        """Initialize utility service."""
        self.agents = agents
        self.inbox_paths = inbox_paths
        self.messages = messages

    def list_agents(self):
        """List all available agents."""
        print("📋 AVAILABLE AGENTS:")
        print("=" * 50)
        for agent_id, info in self.agents.items():
            print(f"🤖 {agent_id}: {info['description']}")
            print(f"   📍 Coordinates: {info['coords']}")
            print(f"   📬 Inbox: {self.inbox_paths.get(agent_id, 'N/A')}")
            print()

    def show_coordinates(self):
        """Show agent coordinates."""
        print("📍 AGENT COORDINATES:")
        print("=" * 30)
        for agent_id, info in self.agents.items():
            print(f"🤖 {agent_id}: {info['coords']}")
        print()

    def show_message_history(self):
        """Show message history."""
        print("📜 MESSAGE HISTORY:")
        print("=" * 30)
        for i, message in enumerate(self.messages, 1):
            print(f"{i}. {message.sender} → {message.recipient}")
            print(f"   Type: {message.message_type.value}")
            print(f"   Priority: {message.priority.value}")
            print(f"   ID: {message.message_id}")
            print()

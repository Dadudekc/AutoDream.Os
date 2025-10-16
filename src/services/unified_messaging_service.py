#!/usr/bin/env python3
"""
Unified Messaging Service
=========================

Unified wrapper for all messaging operations.
Provides single interface for messaging functionality.

Author: Agent-8 (SSOT & System Integration Specialist)
Created: 2025-10-16 (Quarantine Phase 2 fix)
Mission: Fix missing service - 300 pts
License: MIT
"""

from .messaging_service import MessagingService
from ..core.messaging_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority


class UnifiedMessagingService:
    """Unified messaging service wrapper."""

    def __init__(self):
        """Initialize unified messaging service."""
        self.messaging = MessagingService()

    def send_message(
        self,
        recipient: str,
        message: str,
        priority: str = "normal",
        message_type: str = "text",
        **kwargs
    ) -> dict:
        """
        Send message to recipient.

        Args:
            recipient: Agent ID or "broadcast"
            message: Message content
            priority: "normal" or "urgent"
            message_type: "text", "broadcast", "onboarding"
            **kwargs: Additional options

        Returns:
            dict with send result
        """
        return self.messaging.send(
            recipient=recipient,
            content=message,
            priority=priority,
            msg_type=message_type,
            **kwargs
        )

    def broadcast(self, message: str, priority: str = "normal", **kwargs) -> dict:
        """Broadcast message to all agents."""
        return self.send_message(
            recipient="broadcast",
            message=message,
            priority=priority,
            message_type="broadcast",
            **kwargs
        )

    def send_to_captain(self, message: str, priority: str = "normal", **kwargs) -> dict:
        """Send message to Captain Agent-4."""
        return self.send_message(
            recipient="Agent-4",
            message=message,
            priority=priority,
            **kwargs
        )


__all__ = ["UnifiedMessagingService"]


#!/usr/bin/env python3
"""
Messaging Protocol Models - V2 Compliance Module
================================================

Protocol interfaces for messaging system dependency injection.
Extracted from messaging_core.py for better separation of concerns.

V2 Compliance: Interface Segregation Principle (ISP)
SOLID Principles: Dependency Inversion Principle (DIP)

Author: Agent-2 (Architecture & Design Specialist) - ROI 19.57 Task
Created: 2025-10-13
License: MIT
"""

from __future__ import annotations

from typing import Protocol

from .messaging_models_core import UnifiedMessage


class IMessageDelivery(Protocol):
    """
    Interface for message delivery mechanisms.

    Defines the contract for any message delivery service.
    Supports dependency injection and testability.
    """

    def send_message(self, message: UnifiedMessage) -> bool:
        """
        Send a message using the delivery mechanism.

        Args:
            message: UnifiedMessage object to deliver

        Returns:
            bool: True if delivery successful, False otherwise
        """
        ...


class IOnboardingService(Protocol):
    """
    Interface for onboarding operations.

    Defines the contract for agent onboarding services.
    Supports customizable onboarding styles and content.
    """

    def generate_onboarding_message(self, agent_id: str, style: str) -> str:
        """
        Generate onboarding message for an agent.

        Args:
            agent_id: Target agent identifier
            style: Onboarding message style (e.g., "friendly", "professional")

        Returns:
            str: Formatted onboarding message content
        """
        ...


class IMessageFormatter(Protocol):
    """
    Interface for message formatting operations.

    Defines the contract for message formatting services.
    Supports template-based message formatting.
    """

    def format_message(self, message: UnifiedMessage, template: str) -> str:
        """
        Format a message using the specified template.

        Args:
            message: UnifiedMessage object to format
            template: Template name to use for formatting

        Returns:
            str: Formatted message content
        """
        ...


class IInboxManager(Protocol):
    """
    Interface for inbox management operations.

    Defines the contract for inbox rotation and management.
    Supports automated inbox cleanup and archival.
    """

    def check_and_rotate(self, filepath: str) -> bool:
        """
        Check if inbox rotation is needed and perform it.

        Args:
            filepath: Path to inbox file to check

        Returns:
            bool: True if rotation performed, False otherwise
        """
        ...


__all__ = [
    "IMessageDelivery",
    "IOnboardingService",
    "IMessageFormatter",
    "IInboxManager",
]

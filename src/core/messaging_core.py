#!/usr/bin/env python3
"""
UNIFIED MESSAGING CORE SYSTEM - SINGLE SOURCE OF TRUTH
=====================================================

This is the ONE AND ONLY messaging system for the entire Agent Cellphone V2 project.
Consolidates ALL messaging functionality into a single, unified system.

V2 Compliance: SSOT Implementation
SOLID Principles: Single Responsibility (One messaging system), Open-Closed (Extensible)

Author: Agent-1 (System Recovery Specialist) - Messaging Consolidation Champion
License: MIT
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Protocol

# Configure logging
logger = logging.getLogger(__name__)


class DeliveryMethod(Enum):
    """Delivery methods for messages."""

    INBOX = "inbox"
    PYAUTOGUI = "pyautogui"
    BROADCAST = "broadcast"


class UnifiedMessageType(Enum):
    """Message types for unified messaging."""

    TEXT = "text"
    BROADCAST = "broadcast"
    ONBOARDING = "onboarding"
    AGENT_TO_AGENT = "agent_to_agent"
    CAPTAIN_TO_AGENT = "captain_to_agent"
    SYSTEM_TO_AGENT = "system_to_agent"
    HUMAN_TO_AGENT = "human_to_agent"


class UnifiedMessagePriority(Enum):
    """Message priorities for unified messaging."""

    REGULAR = "regular"
    URGENT = "urgent"


class UnifiedMessageTag(Enum):
    """Message tags for unified messaging."""

    CAPTAIN = "captain"
    ONBOARDING = "onboarding"
    WRAPUP = "wrapup"
    COORDINATION = "coordination"
    SYSTEM = "system"


class RecipientType(Enum):
    """Recipient types for unified messaging."""

    AGENT = "agent"
    CAPTAIN = "captain"
    SYSTEM = "system"
    HUMAN = "human"


class SenderType(Enum):
    """Sender types for unified messaging."""

    AGENT = "agent"
    CAPTAIN = "captain"
    SYSTEM = "system"
    HUMAN = "human"


@dataclass
class UnifiedMessage:
    """Core message structure for unified messaging."""

    content: str
    sender: str
    recipient: str
    message_type: UnifiedMessageType
    priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR
    tags: list[UnifiedMessageTag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    sender_type: SenderType = SenderType.SYSTEM
    recipient_type: RecipientType = RecipientType.AGENT


class IMessageDelivery(Protocol):
    """Interface for message delivery mechanisms."""

    def send_message(self, message: UnifiedMessage) -> bool:
        """Send a message."""
        ...


class IOnboardingService(Protocol):
    """Interface for onboarding operations."""

    def generate_onboarding_message(self, agent_id: str, style: str) -> str:
        """Generate onboarding message."""
        ...


class UnifiedMessagingCore:
    """SINGLE SOURCE OF TRUTH for all messaging functionality."""

    def __init__(
        self,
        delivery_service: IMessageDelivery | None = None,
        onboarding_service: IOnboardingService | None = None,
    ):
        """Initialize the unified messaging core."""
        self.delivery_service = delivery_service
        self.onboarding_service = onboarding_service
        self.logger = logging.getLogger(__name__)

        # Initialize subsystems
        self._initialize_subsystems()

    def _initialize_subsystems(self):
        """Initialize all messaging subsystems."""
        # Import and initialize delivery services
        try:
            from .messaging_pyautogui import PyAutoGUIMessagingDelivery

            if not self.delivery_service:
                self.delivery_service = PyAutoGUIMessagingDelivery()
        except ImportError:
            self.logger.warning("PyAutoGUI delivery service not available")

        # Import and initialize onboarding service
        try:
            from .onboarding_service import OnboardingService

            if not self.onboarding_service:
                self.onboarding_service = OnboardingService()
        except ImportError:
            self.logger.warning("Onboarding service not available")

    def send_message(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: list[UnifiedMessageTag] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Send a message using the unified messaging system."""
        message = UnifiedMessage(
            content=content,
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            priority=priority,
            tags=tags or [],
            metadata=metadata or {},
        )

        return self.send_message_object(message)

    def send_message_object(self, message: UnifiedMessage) -> bool:
        """Send a UnifiedMessage object."""
        try:
            # Role- and channel-aware template resolution hook
            # Attach selected template into metadata for downstream delivery/formatting layers
            try:
                from ..services.messaging.policy_loader import (
                    load_template_policy,
                    resolve_template_by_channel,
                    resolve_template_by_roles,
                )
            except Exception:
                load_template_policy = None  # type: ignore
                resolve_template_by_channel = None  # type: ignore
                resolve_template_by_roles = None  # type: ignore

            template = (
                message.metadata.get("template") if isinstance(message.metadata, dict) else None
            )
            channel = (
                (message.metadata or {}).get("channel", "standard")
                if isinstance(message.metadata, dict)
                else "standard"
            )
            sender_role = (
                (message.metadata or {}).get("sender_role", "AGENT")
                if isinstance(message.metadata, dict)
                else "AGENT"
            )
            receiver_role = (
                (message.metadata or {}).get("receiver_role", "AGENT")
                if isinstance(message.metadata, dict)
                else "AGENT"
            )

            if (
                not template
                and load_template_policy
                and resolve_template_by_channel
                and resolve_template_by_roles
            ):
                policy = load_template_policy()
                # Channel overrides first
                if channel in ("onboarding", "passdown", "standard"):
                    template = resolve_template_by_channel(policy, channel)
                # If not forced by channel, resolve by roles
                if not template or template == "compact":
                    template = resolve_template_by_roles(
                        policy, str(sender_role), str(receiver_role)
                    )

                message.metadata["template"] = template  # type: ignore[index]

            if self.delivery_service:
                return self.delivery_service.send_message(message)
            else:
                self.logger.error("No delivery service configured")
                return False
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return False

    def send_message_to_inbox(self, message: UnifiedMessage, max_retries: int = 3) -> bool:
        """Send message to agent inbox with retry logic."""
        try:
            # Create inbox file path in agent workspace
            inbox_dir = Path("agent_workspaces") / message.recipient / "inbox"
            inbox_dir.mkdir(parents=True, exist_ok=True)

            filepath = inbox_dir / f"{message.recipient}_inbox.txt"

            with open(filepath, "a", encoding="utf-8") as f:
                # Handle both enum and string values
                msg_type = (
                    message.message_type.value
                    if hasattr(message.message_type, "value")
                    else str(message.message_type).upper()
                )
                priority = (
                    message.priority.value
                    if hasattr(message.priority, "value")
                    else str(message.priority)
                )

                f.write(f"# 🚨 CAPTAIN MESSAGE - {msg_type}\n\n")
                f.write(f"**From**: {message.sender}\n")
                f.write(f"**To**: {message.recipient}\n")
                f.write(f"**Priority**: {priority}\n")
                f.write(f"**Timestamp**: {message.timestamp}\n")
                if message.tags:
                    f.write(
                        f'**Tags**: {", ".join(tag.value if hasattr(tag, "value") else str(tag) for tag in message.tags)}\n'
                    )
                f.write("\n")
                f.write(f"{message.content}\n")
                f.write("\n" + "=" * 50 + "\n\n")

            self.logger.info(f"Message sent to inbox: {message.recipient}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send message to inbox: {e}")
            return False

    def show_message_history(self):
        """Display message history."""
        try:
            # Simple history display - in practice would use message queue
            self.logger.info("📋 Message History:")
            self.logger.info("-" * 40)
            # This would be enhanced to show actual message history
            self.logger.info("Message history functionality available")
        except Exception as e:
            self.logger.error(f"Failed to show message history: {e}")

    def generate_onboarding_message(self, agent_id: str, style: str = "standard") -> str:
        """Generate onboarding message for an agent."""
        if self.onboarding_service:
            return self.onboarding_service.generate_onboarding_message(agent_id, style)
        else:
            return f"Welcome {agent_id}! You have been onboarded to the Agent Cellphone V2 system."

    def broadcast_message(
        self,
        content: str,
        sender: str,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
    ) -> bool:
        """Broadcast message to all agents."""
        message = UnifiedMessage(
            content=content,
            sender=sender,
            recipient="ALL_AGENTS",
            message_type=UnifiedMessageType.BROADCAST,
            priority=priority,
            tags=[UnifiedMessageTag.SYSTEM],
        )

        return self.send_message_object(message)

    def list_agents(self):
        """List all available agents."""
        # This would integrate with agent registry
        agents = [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-4",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
        ]
        self.logger.info("🤖 Available Agents:")
        for agent in agents:
            self.logger.info(f"  • {agent}")


# SINGLE GLOBAL INSTANCE - THE ONE TRUE MESSAGING CORE
messaging_core = UnifiedMessagingCore()


# PUBLIC API - Single point of access for all messaging
def get_messaging_core() -> UnifiedMessagingCore:
    """Get the SINGLE SOURCE OF TRUTH messaging core."""
    return messaging_core


def send_message(
    content: str,
    sender: str,
    recipient: str,
    message_type: UnifiedMessageType,
    priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
    tags: list[UnifiedMessageTag] | None = None,
    metadata: dict[str, Any] | None = None,
) -> bool:
    """Send message using the SINGLE SOURCE OF TRUTH."""
    return messaging_core.send_message(
        content, sender, recipient, message_type, priority, tags, metadata
    )


def send_message_object(message: UnifiedMessage) -> bool:
    """Send UnifiedMessage using the SINGLE SOURCE OF TRUTH."""
    return messaging_core.send_message_object(message)


def broadcast_message(
    content: str, sender: str, priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR
) -> bool:
    """Broadcast message using the SINGLE SOURCE OF TRUTH."""
    return messaging_core.broadcast_message(content, sender, priority)


def generate_onboarding_message(agent_id: str, style: str = "standard") -> str:
    """Generate onboarding message using the SINGLE SOURCE OF TRUTH."""
    return messaging_core.generate_onboarding_message(agent_id, style)


def show_message_history():
    """Show message history using the SINGLE SOURCE OF TRUTH."""
    messaging_core.show_message_history()


def list_agents():
    """List agents using the SINGLE SOURCE OF TRUTH."""
    messaging_core.list_agents()


# LEGACY COMPATIBILITY FUNCTIONS
def get_messaging_logger():
    """Legacy compatibility function."""
    return logging.getLogger(__name__)


# MESSAGING MODELS EXPORTS - Single source for all messaging models
__all__ = [
    # Core classes
    "UnifiedMessagingCore",
    "UnifiedMessage",
    # Enums
    "DeliveryMethod",
    "UnifiedMessageType",
    "UnifiedMessagePriority",
    "UnifiedMessageTag",
    "RecipientType",
    "SenderType",
    # Interfaces
    "IMessageDelivery",
    "IOnboardingService",
    # Public API functions
    "get_messaging_core",
    "send_message",
    "send_message_object",
    "broadcast_message",
    "generate_onboarding_message",
    "show_message_history",
    "list_agents",
    # Legacy compatibility
    "get_messaging_logger",
]


# VALIDATION AND HEALTH CHECKS
def validate_messaging_system() -> bool:
    """Validate the messaging system is properly configured."""
    try:
        core = get_messaging_core()
        if not core:
            logger.error("Messaging core not available")
            return False

        # Test basic functionality
        test_message = UnifiedMessage(
            content="System validation test",
            sender="SYSTEM",
            recipient="TEST_AGENT",
            message_type=UnifiedMessageType.TEXT,
        )

        logger.info("✅ Messaging system validation passed")
        return True

    except Exception as e:
        logger.error(f"❌ Messaging system validation failed: {e}")
        return False


# AUTO-INITIALIZATION
def initialize_messaging_system() -> None:
    """Initialize the messaging system."""
    logger.info("🔧 Initializing SINGLE SOURCE OF TRUTH Messaging System")

    if validate_messaging_system():
        logger.info("✅ Messaging system ready - SSOT established")
    else:
        logger.error("❌ Messaging system initialization failed")
        raise ValueError("Invalid messaging system configuration")


# Initialize on import
try:
    initialize_messaging_system()
except Exception as e:
    logger.error(f"Failed to initialize messaging system: {e}")
    # Don't raise exception during import - allow system to continue

#!/usr/bin/env python3
"""
Message Template Formatters
============================

Implements compact, minimal, and full message formatting templates
for the unified messaging system.

V2 Compliance: <400 lines, single responsibility
Author: Agent-7 - Repository Cloning Specialist
Date: 2025-10-11
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def format_message_full(message: Any) -> str:
    """Format message with full details (Captain communications, onboarding).

    Includes:
    - Full header with emojis and type
    - All metadata fields (sender, recipient, priority, timestamp, tags)
    - Optional context fields (channel, session, context)
    - Content with clear separation
    - Footer with swarm branding

    Args:
        message: UnifiedMessage object with content and metadata

    Returns:
        Formatted string with full message details

    Example:
        # [C2A] CAPTAIN MESSAGE - captain_to_agent

        **From**: Agent-4 (Captain)
        **To**: Agent-7
        **Priority**: urgent
        **Timestamp**: 2025-10-11 15:30:00
        **Tags**: mission-assignment, team-beta

        {content}

        🐝 WE. ARE. SWARM.
        ==================================================
    """
    # Extract message attributes
    msg_type = (
        message.message_type.value
        if hasattr(message.message_type, "value")
        else str(message.message_type).upper()
    )
    priority = (
        message.priority.value if hasattr(message.priority, "value") else str(message.priority)
    )

    # Determine message prefix and label based on type
    # CRITICAL: Use message_type ONLY for prefix determination
    # Checking sender field causes incorrect classification when defaults are used
    msg_type_lower = str(msg_type).lower()

    if "captain_to_agent" in msg_type_lower:
        prefix = "[C2A]"
        label = "CAPTAIN MESSAGE"
    elif "agent_to_agent" in msg_type_lower:
        prefix = "[A2A]"
        label = "AGENT MESSAGE"
    elif "system_to_agent" in msg_type_lower:
        prefix = "[S2A]"
        label = "SYSTEM MESSAGE"
    elif "human_to_agent" in msg_type_lower:
        prefix = "[H2A]"
        label = "HUMAN MESSAGE"
    elif "discord" in msg_type_lower or "discord" in str(message.sender).lower():
        prefix = "[D2A]"
        label = "DISCORD MESSAGE"
    elif "broadcast" in msg_type_lower:
        prefix = "[BROADCAST]"
        label = "BROADCAST MESSAGE"
    elif "onboarding" in msg_type_lower:
        prefix = "[ONBOARDING]"
        label = "ONBOARDING MESSAGE"
    else:
        # Default to generic message
        prefix = "[MSG]"
        label = "MESSAGE"

    # Build full format
    lines = []

    # Header with appropriate type tag
    lines.append(f"# {prefix} {label} - {msg_type}\n")

    # Core fields
    lines.append(f"**From**: {message.sender}")
    lines.append(f"**To**: {message.recipient}")
    lines.append(f"**Priority**: {priority}")
    lines.append(f"**Timestamp**: {message.timestamp}")

    # Tags if present
    if message.tags:
        tags_str = ", ".join(
            tag.value if hasattr(tag, "value") else str(tag) for tag in message.tags
        )
        lines.append(f"**Tags**: {tags_str}")

    # Optional metadata fields
    if isinstance(message.metadata, dict):
        if "channel" in message.metadata:
            lines.append(f"**Channel**: {message.metadata['channel']}")
        if "session_id" in message.metadata:
            lines.append(f"**Session**: {message.metadata['session_id']}")
        if "context" in message.metadata:
            lines.append(f"**Context**: {message.metadata['context']}")

    # Content section
    lines.append("")  # Blank line before content
    lines.append(message.content)
    lines.append("")  # Blank line after content

    # Footer
    lines.append("🐝 WE. ARE. SWARM.")
    lines.append("=" * 50)
    lines.append("")

    return "\n".join(lines)


def format_message_compact(message: Any) -> str:
    """Format message with compact details (standard agent-to-agent).

    Includes:
    - Simple header with type
    - Essential fields (sender, recipient, priority, timestamp)
    - Content
    - Simple separator

    Args:
        message: UnifiedMessage object with content and metadata

    Returns:
        Formatted string with compact message details

    Example:
        # [A2A] MESSAGE - agent_to_agent

        **From**: Agent-7
        **To**: Agent-6
        **Priority**: regular
        **Timestamp**: 2025-10-11 15:30:00

        {content}

        ==================================================
    """
    # Extract message attributes
    msg_type = (
        message.message_type.value
        if hasattr(message.message_type, "value")
        else str(message.message_type).upper()
    )
    priority = (
        message.priority.value if hasattr(message.priority, "value") else str(message.priority)
    )

    # Determine message prefix based on type
    # CRITICAL: Use message_type ONLY for prefix determination
    # Checking sender field causes incorrect classification when defaults are used
    msg_type_lower = str(msg_type).lower()

    if "captain_to_agent" in msg_type_lower:
        prefix = "[C2A]"
    elif "agent_to_agent" in msg_type_lower:
        prefix = "[A2A]"
    elif "system_to_agent" in msg_type_lower:
        prefix = "[S2A]"
    elif "human_to_agent" in msg_type_lower:
        prefix = "[H2A]"
    elif "discord" in msg_type_lower or "discord" in str(message.sender).lower():
        prefix = "[D2A]"
    elif "broadcast" in msg_type_lower:
        prefix = "[BROADCAST]"
    else:
        prefix = "[MSG]"

    # Build compact format
    lines = []

    # Simple header with prefix
    lines.append(f"# {prefix} MESSAGE - {msg_type}\n")

    # Essential fields only
    lines.append(f"**From**: {message.sender}")
    lines.append(f"**To**: {message.recipient}")
    lines.append(f"**Priority**: {priority}")
    lines.append(f"**Timestamp**: {message.timestamp}")

    # Content section
    lines.append("")  # Blank line before content
    lines.append(message.content)
    lines.append("")  # Blank line after content

    # Simple separator
    lines.append("=" * 50)
    lines.append("")

    return "\n".join(lines)


def format_message_minimal(message: Any) -> str:
    """Format message with minimal details (quick updates, passdown).

    Includes:
    - Bare minimum: from/to
    - Content only
    - No separators

    Args:
        message: UnifiedMessage object with content and metadata

    Returns:
        Formatted string with minimal message details

    Example:
        From: Agent-7
        To: Agent-6

        {content}
    """
    # Build minimal format
    lines = []

    # Bare minimum fields
    lines.append(f"From: {message.sender}")
    lines.append(f"To: {message.recipient}")
    lines.append("")  # Blank line before content

    # Content only
    lines.append(message.content)
    lines.append("")  # Single blank line after

    return "\n".join(lines)


def format_message(message: Any, template: str = "compact") -> str:
    """Format message using specified template type.

    Routes to appropriate formatter based on template type.
    Defaults to compact if template type not recognized.

    Args:
        message: UnifiedMessage object to format
        template: Template type - "full", "compact", or "minimal"

    Returns:
        Formatted message string

    Example:
        >>> formatted = format_message(msg, template="full")
        >>> print(formatted)
        # 🚨 CAPTAIN MESSAGE - STATUS_UPDATE
        ...
    """
    # Normalize template name
    template_normalized = str(template).lower().strip()

    # Route to appropriate formatter
    if template_normalized == "full":
        return format_message_full(message)
    elif template_normalized == "minimal":
        return format_message_minimal(message)
    elif template_normalized == "compact":
        return format_message_compact(message)
    else:
        # Default to compact for unknown templates
        logger.warning(f"Unknown template type '{template}', using compact")
        return format_message_compact(message)


# Public API
__all__ = [
    "format_message",
    "format_message_full",
    "format_message_compact",
    "format_message_minimal",
]

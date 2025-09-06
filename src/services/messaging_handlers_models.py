#!/usr/bin/env python3
"""
Messaging CLI Handlers Models - V2 Compliant
============================================

Data models for messaging CLI handlers system.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactoring)
Created: 2025-01-27
Purpose: Modular data models for messaging CLI handlers
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from enum import Enum


class RecipientType(Enum):
    """Recipient type enumeration."""

    AGENT = "agent"
    SYSTEM = "system"


class SenderType(Enum):
    """Sender type enumeration."""

    AGENT = "agent"
    SYSTEM = "system"


class UnifiedMessagePriority(Enum):
    """Message priority enumeration."""

    REGULAR = "regular"
    URGENT = "urgent"


class UnifiedMessageTag(Enum):
    """Message tag enumeration."""

    CAPTAIN = "captain"
    ONBOARDING = "onboarding"
    WRAPUP = "wrapup"


class UnifiedMessageType(Enum):
    """Message type enumeration."""

    TEXT = "text"
    BROADCAST = "broadcast"
    ONBOARDING = "onboarding"


@dataclass
class CoordinateConfig:
    """Coordinate configuration data structure."""

    agent_id: str
    x: int
    y: int
    description: str = ""


@dataclass
class CLICommand:
    """CLI command data structure."""

    command: str
    args: Dict[str, Any]
    agent: Optional[str] = None
    message: Optional[str] = None
    sender: Optional[str] = None
    priority: str = "regular"
    message_type: str = "text"


@dataclass
class CommandResult:
    """Command execution result."""

    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

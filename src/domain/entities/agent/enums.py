#!/usr/bin/env python3
"""
Agent Enums - Clean OOP Design
==============================

Agent-related enumerations following clean object-oriented principles.
Single responsibility: Define agent-related constants and types.

Author: Agent-1 (Integration Specialist)
License: MIT
"""

from enum import Enum


class AgentStatus(Enum):
    """Agent status enumeration."""
    INACTIVE = "inactive"
    ACTIVE = "active"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


class AgentType(Enum):
    """Agent type enumeration."""
    CORE = "core"
    SERVICE = "service"
    INTEGRATION = "integration"
    UTILITY = "utility"


class AgentCapability(Enum):
    """Agent capability enumeration."""
    MESSAGING = "messaging"
    COMMAND_EXECUTION = "command_execution"
    DATA_PROCESSING = "data_processing"
    COORDINATION = "coordination"
    USER_INTERFACE = "user_interface"
    SECURITY = "security"
    SYSTEM_INTEGRATION = "system_integration"
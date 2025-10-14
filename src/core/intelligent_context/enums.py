#!/usr/bin/env python3
"""
Intelligent Context Enumerations
=================================

Enum types for intelligent context operations.

Author: Agent-7 - Knowledge & OSS Contribution Specialist
Refactored from intelligent_context_models.py for V2 compliance
License: MIT
"""

from enum import Enum


class MissionPhase(Enum):
    """Mission phases."""

    PLANNING = "planning"
    EXECUTION = "execution"
    MONITORING = "monitoring"
    COMPLETION = "completion"
    EMERGENCY = "emergency"


class AgentStatus(Enum):
    """Agent availability status."""

    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


class RiskLevel(Enum):
    """Risk levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

#!/usr/bin/env python3
"""
Intelligent Context Enums - V2 Compliance
==========================================

Enumerations for intelligent context system.

Extracted from intelligent_context_models.py for V2 compliance.
Part of 13→≤5 class consolidation (ROI 90.00).

Author: Agent-7 (Repository Cloning Specialist) - V2 Compliance Refactor
Original: Captain Agent-4 - Strategic Oversight
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


__all__ = ["MissionPhase", "AgentStatus", "RiskLevel"]

#!/usr/bin/env python3
"""
Directive Models - V2 Compliant
===============================

Data models and enumerations for Captain Directive Manager.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

from datetime import datetime
from enum import Enum


class DirectiveType(Enum):
    """Directive type enumeration."""

    STRATEGIC = "strategic"
    TACTICAL = "tactical"
    OPERATIONAL = "operational"
    EMERGENCY = "emergency"


class DirectiveStatus(Enum):
    """Directive status enumeration."""

    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class InitiativeStatus(Enum):
    """Initiative status enumeration."""

    CONCEPTION = "conception"
    PLANNING = "planning"
    EXECUTION = "execution"
    MONITORING = "monitoring"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Directive:
    """Directive data class."""

    def __init__(
        self,
        name: str,
        directive_type: DirectiveType,
        description: str,
        priority: int,
        timeline: str,
    ):
        """Initialize directive."""
        self.name = name
        self.type = directive_type
        self.description = description
        self.priority = priority
        self.timeline = timeline
        self.status = DirectiveStatus.PLANNING
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.progress = 0
        self.assigned_agents = []
        self.milestones = []
        self.notes = []


class Initiative:
    """Initiative data class."""

    def __init__(self, name: str, description: str, category: str, priority: int, timeline: str):
        """Initialize initiative."""
        self.name = name
        self.description = description
        self.category = category
        self.priority = priority
        self.timeline = timeline
        self.status = InitiativeStatus.CONCEPTION
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.progress = 0
        self.assigned_agents = []
        self.resources = []
        self.milestones = []
        self.notes = []

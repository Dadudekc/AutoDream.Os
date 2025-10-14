#!/usr/bin/env python3
"""
Intelligent Context Emergency Models
=====================================

Data models for emergency context and intervention protocols.

Author: Agent-7 - Knowledge & OSS Contribution Specialist
Refactored from intelligent_context_models.py for V2 compliance
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class EmergencyContext:
    """Emergency context structure."""

    emergency_id: str
    mission_id: str
    emergency_type: str
    severity_level: str
    affected_agents: list[str] = field(default_factory=list)
    intervention_protocols: list[str] = field(default_factory=list)
    estimated_resolution_time: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class InterventionProtocol:
    """Intervention protocol structure."""

    protocol_id: str
    protocol_name: str
    trigger_conditions: list[str] = field(default_factory=list)
    intervention_steps: list[str] = field(default_factory=list)
    success_criteria: list[str] = field(default_factory=list)
    estimated_duration: float = 0.0
    required_agents: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

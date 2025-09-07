#!/usr/bin/env python3
"""
Emergency Types Module - Extracted from emergency_response_system.py
Agent-3: Monolithic File Modularization Contract

This module contains all emergency-related data structures and enums.
"""

from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional


class EmergencyLevel(Enum):
    """Emergency severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    CODE_BLACK = "code_black"


class EmergencyType(Enum):
    """Types of emergency situations"""
    SYSTEM_FAILURE = "system_failure"
    WORKFLOW_STALL = "workflow_stall"
    CONTRACT_SYSTEM_DOWN = "contract_system_down"
    AGENT_COORDINATION_BREAKDOWN = "agent_coordination_breakdown"
    SECURITY_BREACH = "security_breach"
    DATA_CORRUPTION = "data_corruption"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    COMMUNICATION_FAILURE = "communication_failure"


@dataclass
class EmergencyEvent:
    """Emergency event data structure"""
    id: str
    type: EmergencyType
    level: EmergencyLevel
    description: str
    timestamp: datetime
    source: str
    affected_components: List[str] = field(default_factory=list)
    impact_assessment: Dict[str, Any] = field(default_factory=dict)
    response_actions: List[Dict[str, Any]] = field(default_factory=list)
    status: str = "active"
    resolution_time: Optional[datetime] = None
    lessons_learned: List[str] = field(default_factory=list)


@dataclass
class EmergencyProtocol:
    """Emergency response protocol definition"""
    name: str
    description: str
    activation_conditions: List[str]
    response_actions: List[Dict[str, Any]]
    escalation_procedures: List[Dict[str, Any]]
    recovery_procedures: List[Dict[str, Any]]
    validation_criteria: List[str]
    documentation_requirements: List[str]


@dataclass
class EmergencyAction:
    """Emergency action definition"""
    name: str
    description: str
    action_type: str
    parameters: Dict[str, Any]
    timeout: int
    retry_count: int = 0
    max_retries: int = 3
    status: str = "pending"


@dataclass
class EmergencyResponse:
    """Emergency response result"""
    emergency_id: str
    response_time: datetime
    actions_taken: List[str]
    success: bool
    error_message: Optional[str] = None
    resolution_time: Optional[datetime] = None

#!/usr/bin/env python3
"""
Intelligent Context Models Extended - V2 Compliance Module
=========================================================

Extended data models for intelligent context operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum
from .models_core import ContextType, Priority, Status


class MissionPhase(Enum):
    """Mission phases."""
    PLANNING = "planning"
    EXECUTION = "execution"
    MONITORING = "monitoring"
    COMPLETION = "completion"
    EMERGENCY = "emergency"


class AgentStatus(Enum):
    """Agent status types."""
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"
    ERROR = "error"


class RiskLevel(Enum):
    """Risk levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class EmergencyContext:
    """Emergency context data."""
    emergency_id: str
    emergency_type: str
    severity: str
    description: str
    affected_agents: List[str]
    reported_at: datetime
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.affected_agents is None:
            self.affected_agents = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class InterventionProtocol:
    """Intervention protocol data."""
    protocol_id: str
    protocol_name: str
    emergency_type: str
    severity_level: str
    actions: List[str]
    priority: Priority
    estimated_duration: int
    success_rate: float
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.actions is None:
            self.actions = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class InterventionResult:
    """Intervention result data."""
    intervention_id: str
    emergency_id: str
    action: str
    success: bool
    message: str
    executed_at: datetime
    duration: float = 0.0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.metadata is None:
            self.metadata = {}


@dataclass
class EmergencyPattern:
    """Emergency pattern data."""
    pattern_id: str
    pattern_name: str
    emergency_type: str
    frequency: int
    severity_distribution: Dict[str, int]
    common_factors: List[str]
    prevention_strategies: List[str]
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.common_factors is None:
            self.common_factors = []
        if self.prevention_strategies is None:
            self.prevention_strategies = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class EmergencyMetrics:
    """Emergency metrics data."""
    total_emergencies: int = 0
    resolved_emergencies: int = 0
    active_emergencies: int = 0
    total_interventions: int = 0
    successful_interventions: int = 0
    failed_interventions: int = 0
    average_response_time: float = 0.0
    average_resolution_time: float = 0.0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.metadata is None:
            self.metadata = {}


@dataclass
class InterventionAction:
    """Intervention action data."""
    action_id: str
    action_type: str
    description: str
    priority: Priority
    estimated_duration: int
    required_skills: List[str]
    success_rate: float
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.required_skills is None:
            self.required_skills = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class EmergencyResponse:
    """Emergency response data."""
    emergency_id: str
    response_type: str
    message: str
    success: bool
    recommended_actions: List[str] = None
    timestamp: datetime = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.recommended_actions is None:
            self.recommended_actions = []
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}


@dataclass
class EmergencyHistory:
    """Emergency history data."""
    history_id: str
    emergency_id: str
    event_type: str
    description: str
    timestamp: datetime
    agent_id: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.metadata is None:
            self.metadata = {}

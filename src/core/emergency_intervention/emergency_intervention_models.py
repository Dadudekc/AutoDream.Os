#!/usr/bin/env python3
"""
Emergency Intervention Models - V2 Compliance Module
===================================================

Data models and enums for emergency intervention operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime


class EmergencySeverity(Enum):
    """Emergency severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EmergencyType(Enum):
    """Types of emergencies that can occur."""
    AGENT_FAILURE = "agent_failure"
    MISSION_BLOCKED = "mission_blocked"
    RESOURCE_SHORTAGE = "resource_shortage"
    DEADLINE_PRESSURE = "deadline_pressure"
    COMMUNICATION_BREAKDOWN = "communication_breakdown"
    QUALITY_DEGRADATION = "quality_degradation"
    SYSTEM_OVERLOAD = "system_overload"
    SECURITY_INCIDENT = "security_incident"


class EmergencyStatus(Enum):
    """Emergency status enumeration."""
    DETECTED = "detected"
    ANALYZING = "analyzing"
    RESPONDING = "responding"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    MONITORING = "monitoring"


@dataclass
class Emergency:
    """Emergency incident structure."""
    
    emergency_id: str
    emergency_type: EmergencyType
    severity: EmergencySeverity
    description: str
    detected_at: datetime = field(default_factory=datetime.now)
    status: EmergencyStatus = EmergencyStatus.DETECTED
    affected_agents: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "emergency_id": self.emergency_id,
            "emergency_type": self.emergity_type.value,
            "severity": self.severity.value,
            "description": self.description,
            "detected_at": self.detected_at.isoformat(),
            "status": self.status.value,
            "affected_agents": self.affected_agents,
            "context": self.context,
            "metadata": self.metadata
        }


@dataclass
class InterventionProtocol:
    """Intervention protocol structure."""
    
    protocol_id: str
    emergency_type: EmergencyType
    severity_threshold: EmergencySeverity
    actions: List[str] = field(default_factory=list)
    priority: int = 1
    estimated_duration: float = 0.0
    success_rate: float = 0.0
    last_used: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "protocol_id": self.protocol_id,
            "emergency_type": self.emergency_type.value,
            "severity_threshold": self.severity_threshold.value,
            "actions": self.actions,
            "priority": self.priority,
            "estimated_duration": self.estimated_duration,
            "success_rate": self.success_rate,
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "metadata": self.metadata
        }


@dataclass
class InterventionResult:
    """Intervention result structure."""
    
    result_id: str
    emergency_id: str
    protocol_id: str
    success: bool
    duration: float
    actions_taken: List[str] = field(default_factory=list)
    outcome: str = ""
    effectiveness_score: float = 0.0
    completed_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "result_id": self.result_id,
            "emergency_id": self.emergency_id,
            "protocol_id": self.protocol_id,
            "success": self.success,
            "duration": self.duration,
            "actions_taken": self.actions_taken,
            "outcome": self.outcome,
            "effectiveness_score": self.effectiveness_score,
            "completed_at": self.completed_at.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class EmergencyPattern:
    """Emergency pattern analysis structure."""
    
    pattern_id: str
    emergency_type: EmergencyType
    frequency: int
    common_triggers: List[str] = field(default_factory=list)
    resolution_patterns: List[str] = field(default_factory=list)
    prevention_strategies: List[str] = field(default_factory=list)
    last_occurrence: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "pattern_id": self.pattern_id,
            "emergency_type": self.emergency_type.value,
            "frequency": self.frequency,
            "common_triggers": self.common_triggers,
            "resolution_patterns": self.resolution_patterns,
            "prevention_strategies": self.prevention_strategies,
            "last_occurrence": self.last_occurrence.isoformat() if self.last_occurrence else None,
            "metadata": self.metadata
        }


@dataclass
class EmergencyMetrics:
    """Emergency metrics structure."""
    
    total_emergencies: int = 0
    resolved_emergencies: int = 0
    active_emergencies: int = 0
    average_resolution_time: float = 0.0
    success_rate: float = 0.0
    emergency_types: Dict[str, int] = field(default_factory=dict)
    severity_distribution: Dict[str, int] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_emergencies": self.total_emergencies,
            "resolved_emergencies": self.resolved_emergencies,
            "active_emergencies": self.active_emergencies,
            "average_resolution_time": self.average_resolution_time,
            "success_rate": self.success_rate,
            "emergency_types": self.emergency_types,
            "severity_distribution": self.severity_distribution,
            "last_updated": self.last_updated.isoformat()
        }


@dataclass
class InterventionAction:
    """Intervention action structure."""
    
    action_id: str
    action_type: str
    description: str
    priority: int
    estimated_duration: float
    required_resources: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "action_id": self.action_id,
            "action_type": self.action_type,
            "description": self.description,
            "priority": self.priority,
            "estimated_duration": self.estimated_duration,
            "required_resources": self.required_resources,
            "success_criteria": self.success_criteria,
            "metadata": self.metadata
        }


@dataclass
class EmergencyContext:
    """Emergency context information."""
    
    context_id: str
    emergency_id: str
    system_state: Dict[str, Any] = field(default_factory=dict)
    agent_status: Dict[str, Any] = field(default_factory=dict)
    resource_availability: Dict[str, Any] = field(default_factory=dict)
    environmental_factors: Dict[str, Any] = field(default_factory=dict)
    historical_data: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "context_id": self.context_id,
            "emergency_id": self.emergency_id,
            "system_state": self.system_state,
            "agent_status": self.agent_status,
            "resource_availability": self.resource_availability,
            "environmental_factors": self.environmental_factors,
            "historical_data": self.historical_data,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class EmergencyResponse:
    """Emergency response structure."""
    
    response_id: str
    emergency_id: str
    protocol_id: str
    actions: List[InterventionAction] = field(default_factory=list)
    status: EmergencyStatus = EmergencyStatus.RESPONDING
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    effectiveness_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "response_id": self.response_id,
            "emergency_id": self.emergency_id,
            "protocol_id": self.protocol_id,
            "actions": [action.to_dict() for action in self.actions],
            "status": self.status.value,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "effectiveness_score": self.effectiveness_score,
            "metadata": self.metadata
        }


@dataclass
class EmergencyHistory:
    """Emergency history structure."""
    
    history_id: str
    emergency_id: str
    event_type: str
    description: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "history_id": self.history_id,
            "emergency_id": self.emergency_id,
            "event_type": self.event_type,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }

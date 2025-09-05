"""
Emergency Intervention Metrics - V2 Compliance Module
====================================================

Metrics and analytics models for emergency intervention operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
from .emergency_intervention_enums import EmergencySeverity, EmergencyType, EmergencyStatus


@dataclass
class EmergencyMetrics:
    """Emergency response metrics."""
    metrics_id: str
    time_period: str
    total_emergencies: int = 0
    resolved_emergencies: int = 0
    escalated_emergencies: int = 0
    average_response_time: float = 0.0
    average_resolution_time: float = 0.0
    success_rate: float = 0.0
    severity_distribution: Dict[str, int] = field(default_factory=dict)
    type_distribution: Dict[str, int] = field(default_factory=dict)
    agent_performance: Dict[str, float] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class InterventionAction:
    """Individual intervention action."""
    action_id: str
    emergency_id: str
    action_type: str
    description: str
    executed_by: str
    executed_at: datetime
    duration: float = 0.0
    success: bool = False
    resources_consumed: List[str] = field(default_factory=list)
    outcome: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmergencyContext:
    """Context information for emergency analysis."""
    context_id: str
    emergency_id: str
    system_state: Dict[str, Any] = field(default_factory=dict)
    agent_states: Dict[str, Any] = field(default_factory=dict)
    mission_states: Dict[str, Any] = field(default_factory=dict)
    resource_availability: Dict[str, Any] = field(default_factory=dict)
    communication_status: Dict[str, Any] = field(default_factory=dict)
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    environmental_factors: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmergencyResponse:
    """Emergency response coordination."""
    response_id: str
    emergency_id: str
    coordinator: str
    response_team: List[str] = field(default_factory=list)
    status: EmergencyStatus = EmergencyStatus.DETECTED
    priority: str = "medium"
    estimated_resolution: Optional[datetime] = None
    actual_resolution: Optional[datetime] = None
    communication_log: List[str] = field(default_factory=list)
    resource_allocations: List[str] = field(default_factory=list)
    escalation_history: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

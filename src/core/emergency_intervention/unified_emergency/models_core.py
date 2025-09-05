"""
Emergency Intervention Unified Models Core - KISS Simplified
===========================================================

Core data models for emergency intervention operations.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined emergency models.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid
from .models_enums import (
    EmergencySeverity, EmergencyType, EmergencyStatus,
    InterventionAction, InterventionPriority, AlertLevel
)


@dataclass
class EmergencyEvent:
    """Emergency event data structure."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    emergency_type: EmergencyType = EmergencyType.SYSTEM_FAILURE
    severity: EmergencySeverity = EmergencySeverity.MEDIUM
    status: EmergencyStatus = EmergencyStatus.DETECTED
    title: str = ""
    description: str = ""
    detected_at: datetime = field(default_factory=datetime.now)
    detected_by: str = "system"
    affected_components: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class InterventionPlan:
    """Intervention plan data structure."""
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    emergency_id: str = ""
    plan_name: str = ""
    description: str = ""
    actions: List[InterventionAction] = field(default_factory=list)
    priority: InterventionPriority = InterventionPriority.MEDIUM
    estimated_duration: int = 0
    required_resources: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = "system"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class InterventionResult:
    """Intervention result data structure."""
    result_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    emergency_id: str = ""
    plan_id: str = ""
    status: EmergencyStatus = EmergencyStatus.DETECTED
    success: bool = False
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    actions_executed: List[InterventionAction] = field(default_factory=list)
    resources_used: List[str] = field(default_factory=list)
    outcome: str = ""
    lessons_learned: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

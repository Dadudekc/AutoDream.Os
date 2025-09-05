"""
Emergency Intervention Models - KISS Simplified
==============================================

Simplified data models for emergency intervention operations.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined emergency models.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import uuid


class EmergencySeverity(Enum):
    """Emergency severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EmergencyType(Enum):
    """Types of emergencies."""
    SYSTEM_FAILURE = "system_failure"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    SECURITY_BREACH = "security_breach"
    DATA_CORRUPTION = "data_corruption"
    NETWORK_OUTAGE = "network_outage"
    RESOURCE_EXHAUSTION = "resource_exhaustion"


class EmergencyStatus(Enum):
    """Emergency status states."""
    DETECTED = "detected"
    ANALYZING = "analyzing"
    INTERVENING = "intervening"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    FAILED = "failed"


class InterventionAction(Enum):
    """Types of intervention actions."""
    RESTART_SERVICE = "restart_service"
    SCALE_RESOURCES = "scale_resources"
    ISOLATE_COMPONENT = "isolate_component"
    ROLLBACK_CHANGES = "rollback_changes"
    NOTIFY_ADMIN = "notify_admin"
    EXECUTE_SCRIPT = "execute_script"


@dataclass
class EmergencyEvent:
    """Simplified emergency event model."""
    event_id: str
    emergency_type: EmergencyType
    severity: EmergencySeverity
    description: str
    detected_at: datetime
    status: EmergencyStatus = EmergencyStatus.DETECTED
    affected_components: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.affected_components is None:
            self.affected_components = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class InterventionPlan:
    """Simplified intervention plan model."""
    plan_id: str
    emergency_id: str
    actions: List[InterventionAction]
    priority: int = 1
    created_at: datetime = None
    status: str = "pending"
    estimated_duration: int = 300  # seconds
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class InterventionResult:
    """Simplified intervention result model."""
    result_id: str
    plan_id: str
    action: InterventionAction
    success: bool
    executed_at: datetime
    duration: float = 0.0
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class EmergencyMetrics:
    """Simplified emergency metrics model."""
    total_emergencies: int = 0
    resolved_emergencies: int = 0
    avg_resolution_time: float = 0.0
    critical_emergencies: int = 0
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()


@dataclass
class EmergencyConfig:
    """Simplified emergency configuration model."""
    auto_intervention_enabled: bool = True
    escalation_threshold: int = 5
    max_intervention_time: int = 1800  # 30 minutes
    notification_recipients: List[str] = None
    monitoring_interval: int = 60  # seconds
    
    def __post_init__(self):
        if self.notification_recipients is None:
            self.notification_recipients = []


@dataclass
class EmergencyAlert:
    """Simplified emergency alert model."""
    alert_id: str
    emergency_id: str
    message: str
    severity: EmergencySeverity
    created_at: datetime
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None


@dataclass
class EmergencyLog:
    """Simplified emergency log model."""
    log_id: str
    emergency_id: str
    action: str
    details: str
    timestamp: datetime
    user_id: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class EmergencyReport:
    """Simplified emergency report model."""
    report_id: str
    emergency_id: str
    title: str
    summary: str
    created_at: datetime
    status: str = "draft"
    findings: List[str] = None
    recommendations: List[str] = None
    
    def __post_init__(self):
        if self.findings is None:
            self.findings = []
        if self.recommendations is None:
            self.recommendations = []


@dataclass
class EmergencyTemplate:
    """Simplified emergency template model."""
    template_id: str
    name: str
    emergency_type: EmergencyType
    severity: EmergencySeverity
    actions: List[InterventionAction]
    description: str = ""
    is_active: bool = True
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class EmergencyEscalation:
    """Simplified emergency escalation model."""
    escalation_id: str
    emergency_id: str
    escalated_to: str
    reason: str
    escalated_at: datetime
    status: str = "pending"
    resolved_at: Optional[datetime] = None


@dataclass
class EmergencyRecovery:
    """Simplified emergency recovery model."""
    recovery_id: str
    emergency_id: str
    recovery_plan: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: str = "in_progress"
    success: bool = False
    notes: str = ""


@dataclass
class EmergencyAudit:
    """Simplified emergency audit model."""
    audit_id: str
    emergency_id: str
    audit_type: str
    performed_by: str
    performed_at: datetime
    findings: List[str] = None
    recommendations: List[str] = None
    status: str = "completed"
    
    def __post_init__(self):
        if self.findings is None:
            self.findings = []
        if self.recommendations is None:
            self.recommendations = []


@dataclass
class EmergencyNotification:
    """Simplified emergency notification model."""
    notification_id: str
    emergency_id: str
    recipient: str
    message: str
    sent_at: datetime
    delivery_status: str = "sent"
    delivery_method: str = "email"
    retry_count: int = 0


@dataclass
class EmergencyWorkflow:
    """Simplified emergency workflow model."""
    workflow_id: str
    name: str
    emergency_type: EmergencyType
    steps: List[str]
    is_active: bool = True
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


@dataclass
class EmergencyDashboard:
    """Simplified emergency dashboard model."""
    dashboard_id: str
    name: str
    widgets: List[str]
    is_public: bool = False
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
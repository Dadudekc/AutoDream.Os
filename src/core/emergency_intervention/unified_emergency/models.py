"""
Emergency Intervention Models
============================

Data models for emergency intervention operations.
V2 Compliance: < 300 lines, single responsibility, data modeling.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
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
    ISOLATE_SYSTEM = "isolate_system"
    ROLLBACK_CHANGES = "rollback_changes"
    NOTIFY_ADMIN = "notify_admin"
    EXECUTE_SCRIPT = "execute_script"


@dataclass
class Emergency:
    """Emergency incident data."""
    emergency_id: str
    emergency_type: EmergencyType
    severity: EmergencySeverity
    status: EmergencyStatus
    description: str
    detected_at: datetime
    resolved_at: Optional[datetime] = None
    context: Dict[str, Any] = None
    metrics: Dict[str, Any] = None


@dataclass
class InterventionProtocol:
    """Emergency intervention protocol."""
    protocol_id: str
    emergency_type: EmergencyType
    severity_threshold: EmergencySeverity
    actions: List[InterventionAction]
    priority: int
    timeout_seconds: int
    auto_execute: bool = False


@dataclass
class InterventionResult:
    """Result of intervention action."""
    action: InterventionAction
    success: bool
    execution_time: float
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = None


@dataclass
class EmergencyResponse:
    """Emergency response data."""
    emergency_id: str
    response_time: float
    interventions: List[InterventionResult]
    resolution_time: Optional[float] = None
    escalated: bool = False


@dataclass
class EmergencyContext:
    """Context data for emergency."""
    system_metrics: Dict[str, Any]
    recent_events: List[Dict[str, Any]]
    user_impact: Dict[str, Any]
    resource_usage: Dict[str, Any]


@dataclass
class EmergencyPattern:
    """Pattern for emergency detection."""
    pattern_id: str
    name: str
    conditions: Dict[str, Any]
    severity: EmergencySeverity
    confidence: float


@dataclass
class EmergencyMetrics:
    """Emergency system metrics."""
    total_emergencies: int = 0
    resolved_emergencies: int = 0
    active_emergencies: int = 0
    average_response_time: float = 0.0
    average_resolution_time: float = 0.0
    escalation_rate: float = 0.0
    last_updated: datetime = None


@dataclass
class EmergencyHistory:
    """Historical emergency data."""
    emergency_id: str
    events: List[Dict[str, Any]]
    timeline: List[datetime]
    resolution_notes: Optional[str] = None


class EmergencyInterventionModels:
    """Emergency intervention models and validation."""
    
    @staticmethod
    def create_emergency(
        emergency_type: EmergencyType,
        severity: EmergencySeverity,
        description: str,
        context: Dict[str, Any] = None,
        metrics: Dict[str, Any] = None
    ) -> Emergency:
        """Create emergency incident."""
        return Emergency(
            emergency_id=str(uuid.uuid4()),
            emergency_type=emergency_type,
            severity=severity,
            status=EmergencyStatus.DETECTED,
            description=description,
            detected_at=datetime.now(),
            context=context or {},
            metrics=metrics or {}
        )
    
    @staticmethod
    def create_intervention_protocol(
        emergency_type: EmergencyType,
        severity_threshold: EmergencySeverity,
        actions: List[InterventionAction],
        priority: int = 1,
        timeout_seconds: int = 300,
        auto_execute: bool = False
    ) -> InterventionProtocol:
        """Create intervention protocol."""
        return InterventionProtocol(
            protocol_id=str(uuid.uuid4()),
            emergency_type=emergency_type,
            severity_threshold=severity_threshold,
            actions=actions,
            priority=priority,
            timeout_seconds=timeout_seconds,
            auto_execute=auto_execute
        )
    
    @staticmethod
    def create_intervention_result(
        action: InterventionAction,
        success: bool,
        execution_time: float,
        error_message: str = None,
        metadata: Dict[str, Any] = None
    ) -> InterventionResult:
        """Create intervention result."""
        return InterventionResult(
            action=action,
            success=success,
            execution_time=execution_time,
            error_message=error_message,
            metadata=metadata or {}
        )
    
    @staticmethod
    def create_emergency_response(
        emergency_id: str,
        response_time: float,
        interventions: List[InterventionResult],
        resolution_time: float = None,
        escalated: bool = False
    ) -> EmergencyResponse:
        """Create emergency response."""
        return EmergencyResponse(
            emergency_id=emergency_id,
            response_time=response_time,
            interventions=interventions,
            resolution_time=resolution_time,
            escalated=escalated
        )
    
    @staticmethod
    def create_emergency_context(
        system_metrics: Dict[str, Any] = None,
        recent_events: List[Dict[str, Any]] = None,
        user_impact: Dict[str, Any] = None,
        resource_usage: Dict[str, Any] = None
    ) -> EmergencyContext:
        """Create emergency context."""
        return EmergencyContext(
            system_metrics=system_metrics or {},
            recent_events=recent_events or [],
            user_impact=user_impact or {},
            resource_usage=resource_usage or {}
        )
    
    @staticmethod
    def create_emergency_pattern(
        name: str,
        conditions: Dict[str, Any],
        severity: EmergencySeverity,
        confidence: float
    ) -> EmergencyPattern:
        """Create emergency pattern."""
        return EmergencyPattern(
            pattern_id=str(uuid.uuid4()),
            name=name,
            conditions=conditions,
            severity=severity,
            confidence=confidence
        )
    
    @staticmethod
    def create_emergency_metrics() -> EmergencyMetrics:
        """Create emergency metrics."""
        return EmergencyMetrics(
            total_emergencies=0,
            resolved_emergencies=0,
            active_emergencies=0,
            average_response_time=0.0,
            average_resolution_time=0.0,
            escalation_rate=0.0,
            last_updated=datetime.now()
        )
    
    @staticmethod
    def create_emergency_history(emergency_id: str) -> EmergencyHistory:
        """Create emergency history."""
        return EmergencyHistory(
            emergency_id=emergency_id,
            events=[],
            timeline=[],
            resolution_notes=None
        )
    
    @staticmethod
    def update_emergency_metrics(
        metrics: EmergencyMetrics,
        emergency: Emergency,
        response: EmergencyResponse
    ) -> EmergencyMetrics:
        """Update emergency metrics."""
        metrics.total_emergencies += 1
        
        if emergency.status == EmergencyStatus.RESOLVED:
            metrics.resolved_emergencies += 1
            if response.resolution_time:
                total_time = metrics.average_resolution_time * (metrics.resolved_emergencies - 1)
                metrics.average_resolution_time = (total_time + response.resolution_time) / metrics.resolved_emergencies
        else:
            metrics.active_emergencies += 1
        
        # Update response time
        total_response_time = metrics.average_response_time * (metrics.total_emergencies - 1)
        metrics.average_response_time = (total_response_time + response.response_time) / metrics.total_emergencies
        
        # Update escalation rate
        if response.escalated:
            escalated_count = metrics.escalation_rate * metrics.total_emergencies
            metrics.escalation_rate = (escalated_count + 1) / metrics.total_emergencies
        
        metrics.last_updated = datetime.now()
        return metrics

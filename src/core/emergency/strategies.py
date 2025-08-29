"""Strategy definitions for emergency protocols."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any

from .logging import get_logger

logger = get_logger(__name__)


class ProtocolStatus(Enum):
    """Protocol activation status"""

    INACTIVE = "inactive"
    ACTIVE = "active"
    ESCALATED = "escalated"
    COMPLETED = "completed"
    FAILED = "failed"


class ProtocolPriority(Enum):
    """Protocol priority levels"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ResponseAction:
    """Emergency response action definition"""

    action: str
    description: str
    priority: ProtocolPriority
    timeout: int  # seconds
    required: bool = True
    completed: bool = False
    completion_time: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None


@dataclass
class EscalationProcedure:
    """Protocol escalation procedure"""

    level: ProtocolPriority
    action: str
    timeout: int  # seconds
    description: str
    triggered: bool = False
    trigger_time: Optional[datetime] = None


@dataclass
class RecoveryProcedure:
    """Protocol recovery procedure"""

    action: str
    description: str
    validation_criteria: List[str]
    required: bool = True
    completed: bool = False
    completion_time: Optional[datetime] = None
    validation_results: Optional[Dict[str, bool]] = None


@dataclass
class EmergencyProtocol:
    """Emergency response protocol definition"""

    name: str
    description: str
    activation_conditions: List[str]
    response_actions: List[ResponseAction]
    escalation_procedures: List[EscalationProcedure]
    recovery_procedures: List[RecoveryProcedure]
    validation_criteria: List[str]
    documentation_requirements: List[str]
    status: ProtocolStatus = ProtocolStatus.INACTIVE
    activated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    activation_source: Optional[str] = None


def create_protocol_from_data(
    protocol_data: Dict[str, Any]
) -> Optional[EmergencyProtocol]:
    """Create EmergencyProtocol from configuration data"""
    try:
        response_actions = []
        for action_data in protocol_data.get("response_actions", []):
            action = ResponseAction(
                action=action_data["action"],
                description=action_data["description"],
                priority=ProtocolPriority(action_data["priority"]),
                timeout=action_data["timeout"],
                required=action_data.get("required", True),
            )
            response_actions.append(action)

        escalation_procedures = []
        for escalation_data in protocol_data.get("escalation_procedures", []):
            escalation = EscalationProcedure(
                level=ProtocolPriority(escalation_data["level"]),
                action=escalation_data["action"],
                timeout=escalation_data["timeout"],
                description=escalation_data.get("description", ""),
            )
            escalation_procedures.append(escalation)

        recovery_procedures = []
        for recovery_data in protocol_data.get("recovery_procedures", []):
            recovery = RecoveryProcedure(
                action=recovery_data["action"],
                description=recovery_data["description"],
                validation_criteria=recovery_data["validation_criteria"],
            )
            recovery_procedures.append(recovery)

        protocol = EmergencyProtocol(
            name=protocol_data["name"],
            description=protocol_data["description"],
            activation_conditions=protocol_data["activation_conditions"],
            response_actions=response_actions,
            escalation_procedures=escalation_procedures,
            recovery_procedures=recovery_procedures,
            validation_criteria=protocol_data["validation_criteria"],
            documentation_requirements=protocol_data["documentation_requirements"],
        )
        return protocol
    except Exception as e:
        logger.error(f"Failed to create protocol from data: {e}")
        return None


def load_default_protocols() -> Dict[str, EmergencyProtocol]:
    """Return default emergency protocol definitions."""
    # Emergency Workflow Restoration Protocol
    workflow_restoration = EmergencyProtocol(
        name="Emergency Workflow Restoration",
        description="Critical intervention system for restoring stalled workflows and momentum",
        activation_conditions=[
            "Workflow stall detected in any agent mission",
            "Sprint acceleration momentum loss",
            "Contract claiming system failures",
            "Agent coordination breakdowns",
        ],
        response_actions=[
            ResponseAction(
                action="generate_emergency_contracts",
                description="Generate 10+ emergency contracts worth 4,375+ points",
                priority=ProtocolPriority.CRITICAL,
                timeout=300,
            ),
            ResponseAction(
                action="activate_agent_mobilization",
                description="Send emergency directives to all agents",
                priority=ProtocolPriority.HIGH,
                timeout=60,
            ),
            ResponseAction(
                action="validate_system_health",
                description="Perform comprehensive system health audit",
                priority=ProtocolPriority.HIGH,
                timeout=600,
            ),
        ],
        escalation_procedures=[
            EscalationProcedure(
                level=ProtocolPriority.HIGH,
                action="notify_captain_coordinator",
                timeout=120,
                description="Notify captain coordinator of critical situation",
            ),
            EscalationProcedure(
                level=ProtocolPriority.CRITICAL,
                action="activate_code_black_protocol",
                timeout=60,
                description="Activate highest level emergency protocol",
            ),
        ],
        recovery_procedures=[
            RecoveryProcedure(
                action="restore_contract_system",
                description="Fix contract claiming system and synchronization",
                validation_criteria=["Contract availability > 40"],
            ),
            RecoveryProcedure(
                action="resolve_task_conflicts",
                description="Resolve task assignment conflicts",
                validation_criteria=["No task assignment conflicts"],
            ),
            RecoveryProcedure(
                action="optimize_agent_priority",
                description="Optimize agent priority system",
                validation_criteria=["Agent priority system aligned"],
            ),
        ],
        validation_criteria=[
            "All agents can claim emergency contracts",
            "Perpetual motion system resumes operation",
            "Contract system corruption resolved",
            "System returns to 40+ available contracts",
            "Workflow momentum restored",
        ],
        documentation_requirements=[
            "Emergency event log",
            "Response action timeline",
            "Recovery validation results",
            "Lessons learned documentation",
        ],
    )

    # Crisis Management Protocol
    crisis_management = EmergencyProtocol(
        name="Crisis Management",
        description="Real-time crisis management and system health monitoring",
        activation_conditions=[
            "Contract completion rate < 40%",
            "Agent idle time > 15 minutes",
            "Workflow synchronization errors",
            "Task assignment conflicts",
        ],
        response_actions=[
            ResponseAction(
                action="deploy_emergency_contracts",
                description="Generate and deploy emergency contracts within 5 minutes",
                priority=ProtocolPriority.CRITICAL,
                timeout=300,
            ),
            ResponseAction(
                action="implement_bulk_messaging",
                description="Send system-wide emergency announcements",
                priority=ProtocolPriority.HIGH,
                timeout=120,
            ),
            ResponseAction(
                action="activate_health_monitoring",
                description="Enable continuous system health assessment",
                priority=ProtocolPriority.HIGH,
                timeout=60,
            ),
        ],
        escalation_procedures=[
            EscalationProcedure(
                level=ProtocolPriority.MEDIUM,
                action="increase_monitoring_frequency",
                timeout=300,
                description="Increase monitoring frequency for crisis situation",
            ),
            EscalationProcedure(
                level=ProtocolPriority.HIGH,
                action="activate_emergency_coordination",
                timeout=180,
                description="Activate emergency coordination protocols",
            ),
        ],
        recovery_procedures=[
            RecoveryProcedure(
                action="restore_workflow_momentum",
                description="Restore workflow momentum and agent engagement",
                validation_criteria=["Agent engagement > 90%"],
            ),
            RecoveryProcedure(
                action="validate_system_synchronization",
                description="Ensure system component synchronization",
                validation_criteria=["All systems synchronized"],
            ),
        ],
        validation_criteria=[
            "Workflow momentum restored",
            "Agent engagement levels normalized",
            "System synchronization validated",
            "Performance metrics within thresholds",
        ],
        documentation_requirements=[
            "Crisis timeline documentation",
            "Response effectiveness analysis",
            "System recovery validation",
            "Prevention strategy documentation",
        ],
    )

    return {
        "workflow_restoration": workflow_restoration,
        "crisis_management": crisis_management,
    }


__all__ = [
    "ProtocolStatus",
    "ProtocolPriority",
    "ResponseAction",
    "EscalationProcedure",
    "RecoveryProcedure",
    "EmergencyProtocol",
    "create_protocol_from_data",
    "load_default_protocols",
]

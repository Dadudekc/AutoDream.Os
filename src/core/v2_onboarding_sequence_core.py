import logging
import uuid
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum

from .communication_compatibility_layer import (
    AgentCommunicationProtocol,
    MessageType,
    MessagePriority,
    InboxManager,
)
from .fsm_core_v2 import FSMCoreV2

logger = logging.getLogger(__name__)


class OnboardingStatus(Enum):
    """Onboarding status values."""

    PENDING = "pending"
    INITIALIZING = "initializing"
    TRAINING = "training"
    VALIDATION = "validation"
    COMPLETED = "completed"
    FAILED = "failed"


class OnboardingPhase(Enum):
    """Onboarding phases."""

    SYSTEM_OVERVIEW = "system_overview"
    ROLE_ASSIGNMENT = "role_assignment"
    CAPTAIN_COORDINATION = "captain_coordination"
    CAPABILITY_TRAINING = "capability_training"
    INTEGRATION_TESTING = "integration_testing"
    PERFORMANCE_VALIDATION = "performance_validation"
    READINESS_CONFIRMATION = "readiness_confirmation"


@dataclass
class OnboardingSession:
    """Onboarding session tracking."""

    session_id: str
    agent_id: str
    status: OnboardingStatus
    current_phase: OnboardingPhase
    completed_phases: List[OnboardingPhase]
    start_time: datetime
    completion_time: Optional[datetime] = None
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    validation_results: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OnboardingMessage:
    """Structured onboarding message."""

    message_id: str
    phase: OnboardingPhase
    content: str
    role_specific: bool
    requires_response: bool
    validation_criteria: Dict[str, Any] = field(default_factory=dict)


class V2OnboardingSequenceCore:
    """Core functionality for the V2 onboarding sequence."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        from .v2_onboarding_sequence_config import (
            DEFAULT_PHASE_TIMEOUT,
            DEFAULT_VALIDATION_RETRIES,
            DEFAULT_PERFORMANCE_THRESHOLDS,
            ROLE_DEFINITIONS,
            create_default_message_templates,
        )

        self.config = config or {}

        # Core components
        self.communication_protocol: Optional[AgentCommunicationProtocol] = None
        self.fsm_core: Optional[FSMCoreV2] = None
        self.inbox_manager: Optional[InboxManager] = None

        # Onboarding state
        self.active_sessions: Dict[str, OnboardingSession] = {}
        self.onboarding_templates: Dict[str, OnboardingMessage] = create_default_message_templates()
        self.role_definitions: Dict[str, Dict[str, Any]] = ROLE_DEFINITIONS.copy()

        # Configuration
        self.phase_timeout = self.config.get("phase_timeout", DEFAULT_PHASE_TIMEOUT)
        self.validation_retries = self.config.get("validation_retries", DEFAULT_VALIDATION_RETRIES)
        self.performance_thresholds = self.config.get(
            "performance_thresholds", DEFAULT_PERFORMANCE_THRESHOLDS
        )

        logger.info("V2OnboardingSequenceCore initialized")

    # ------------------------------------------------------------------
    # Messaging helpers
    # ------------------------------------------------------------------
    def _get_phase_message(self, phase: OnboardingPhase, agent_id: str) -> OnboardingMessage:
        """Get the message for a specific phase."""
        if phase == OnboardingPhase.SYSTEM_OVERVIEW:
            return self.onboarding_templates["system_overview"]

        if phase == OnboardingPhase.ROLE_ASSIGNMENT:
            role_info = self.role_definitions[agent_id]
            return OnboardingMessage(
                message_id=str(uuid.uuid4()),
                phase=phase,
                content=(
                    f"🎯 Role Assignment: You are {role_info['role']}. "
                    f"Your capabilities include: {', '.join(role_info['capabilities'])}. "
                    "Are you ready to accept this role?"
                ),
                role_specific=True,
                requires_response=True,
                validation_criteria={
                    "role_acceptance": True,
                    "capability_confirmation": True,
                },
            )

        if phase == OnboardingPhase.CAPTAIN_COORDINATION:
            return OnboardingMessage(
                message_id=str(uuid.uuid4()),
                phase=phase,
                content=(
                    "🤝 Captain Agent Coordination Training: You will now learn how to work "
                    "effectively in a coordinated swarm. This includes FSM integration, "
                    "agent collaboration, and conflict resolution. The captain agent serves "
                    "as an orchestrator, not a commander. Are you ready to learn coordination?"
                ),
                role_specific=False,
                requires_response=True,
                validation_criteria={
                    "coordination_understanding": True,
                    "fsm_integration_skills": True,
                    "collaboration_workflow": True,
                },
            )

        if phase == OnboardingPhase.CAPABILITY_TRAINING:
            role_info = self.role_definitions[agent_id]
            return OnboardingMessage(
                message_id=str(uuid.uuid4()),
                phase=phase,
                content=(
                    f"🔧 Capability Training: You will now receive specialized training for your role as {role_info['role']}. "
                    "This includes V2 development standards, FSM integration, and performance optimization."
                ),
                role_specific=True,
                requires_response=True,
                validation_criteria={
                    "training_completion": True,
                    "skill_assessment": True,
                },
            )

        if phase == OnboardingPhase.INTEGRATION_TESTING:
            return self.onboarding_templates["integration_testing"]

        return self.onboarding_templates["system_overview"]

    # ------------------------------------------------------------------
    # Status helpers
    # ------------------------------------------------------------------
    def get_onboarding_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of an onboarding session."""
        session = self.active_sessions.get(session_id)
        if not session:
            return None

        return {
            "session_id": session.session_id,
            "agent_id": session.agent_id,
            "status": session.status.value,
            "current_phase": session.current_phase.value,
            "completed_phases": [p.value for p in session.completed_phases],
            "start_time": session.start_time.isoformat(),
            "completion_time": session.completion_time.isoformat()
            if session.completion_time
            else None,
            "performance_metrics": session.performance_metrics,
            "validation_results": session.validation_results,
        }

    def get_all_onboarding_status(self) -> Dict[str, Any]:
        """Get status of all onboarding sessions."""
        return {sid: self.get_onboarding_status(sid) for sid in self.active_sessions}

    def cleanup_completed_sessions(self) -> None:
        """Clean up completed onboarding sessions."""
        completed = [
            sid
            for sid, session in self.active_sessions.items()
            if session.status in (OnboardingStatus.COMPLETED, OnboardingStatus.FAILED)
        ]
        for sid in completed:
            del self.active_sessions[sid]
        if completed:
            logger.info(f"Cleaned up {len(completed)} completed sessions")

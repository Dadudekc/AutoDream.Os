import logging
import threading
import time
from datetime import datetime
from typing import Optional

from .v2_onboarding_sequence_core import (
    OnboardingSession,
    OnboardingStatus,
    OnboardingPhase,
    OnboardingMessage,
    MessageType,
    MessagePriority,
)

logger = logging.getLogger(__name__)


class V2OnboardingSequenceCoordinator:
    """Coordination logic for executing the onboarding sequence."""

    def start_onboarding(
        self,
        agent_id: str,
        communication_protocol,
        fsm_core,
        inbox_manager: Optional[object] = None,
    ) -> str:
        """Start the onboarding process for an agent."""
        if agent_id not in self.role_definitions:
            raise ValueError(f"Unknown agent ID: {agent_id}")

        self.communication_protocol = communication_protocol
        self.fsm_core = fsm_core
        self.inbox_manager = inbox_manager

        session_id = f"onboard_{agent_id}_{int(time.time())}"
        session = OnboardingSession(
            session_id=session_id,
            agent_id=agent_id,
            status=OnboardingStatus.INITIALIZING,
            current_phase=OnboardingPhase.SYSTEM_OVERVIEW,
            completed_phases=[],
            start_time=datetime.now(),
        )
        self.active_sessions[session_id] = session

        threading.Thread(
            target=self._execute_onboarding_sequence,
            args=(session_id,),
            daemon=True,
        ).start()
        logger.info(f"Started onboarding session {session_id} for agent {agent_id}")
        return session_id

    def _execute_onboarding_sequence(self, session_id: str) -> None:
        """Execute the complete onboarding sequence for an agent."""
        session = self.active_sessions[session_id]
        agent_id = session.agent_id

        if self._execute_phase(session, OnboardingPhase.SYSTEM_OVERVIEW):
            session.completed_phases.append(OnboardingPhase.SYSTEM_OVERVIEW)
            if self._execute_phase(session, OnboardingPhase.ROLE_ASSIGNMENT):
                session.completed_phases.append(OnboardingPhase.ROLE_ASSIGNMENT)
                if self._execute_phase(session, OnboardingPhase.CAPABILITY_TRAINING):
                    session.completed_phases.append(OnboardingPhase.CAPABILITY_TRAINING)
                    if self._execute_phase(session, OnboardingPhase.INTEGRATION_TESTING):
                        session.completed_phases.append(OnboardingPhase.INTEGRATION_TESTING)
                        if self._validate_onboarding_completion(session):
                            session.status = OnboardingStatus.COMPLETED
                            session.completion_time = datetime.now()
                            logger.info(
                                f"Onboarding completed successfully for {agent_id}"
                            )
                            return
        session.status = OnboardingStatus.FAILED
        logger.error(f"Onboarding failed for {agent_id}")

    def _execute_phase(
        self, session: OnboardingSession, phase: OnboardingPhase
    ) -> bool:
        """Execute a specific onboarding phase."""
        session.current_phase = phase
        agent_id = session.agent_id
        message = self._get_phase_message(phase, agent_id)

        if self.communication_protocol:
            message_id = self.communication_protocol.send_message(
                sender_id="SYSTEM",
                recipient_id=agent_id,
                message_type=MessageType.COORDINATION,
                payload={
                    "phase": phase.value,
                    "content": message.content,
                    "requires_response": message.requires_response,
                    "validation_criteria": message.validation_criteria,
                },
                priority=MessagePriority.HIGH,
            )
            if message.requires_response:
                return self._wait_for_phase_response(session, phase, message_id)
            return True
        return False

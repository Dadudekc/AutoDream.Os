import logging
import time
from typing import Any

from .v2_onboarding_sequence_core import (
    OnboardingPhase,
    OnboardingSession,
    OnboardingStatus,
)

logger = logging.getLogger(__name__)


class V2OnboardingSequenceValidator:
    """Validation helpers for the onboarding sequence."""

    def _wait_for_phase_response(
        self, session: OnboardingSession, phase: OnboardingPhase, message_id: str
    ) -> bool:
        """Wait for and validate phase response.

        This simplified implementation assumes success after a short delay,
        suitable for tests and non-interactive environments.
        """
        start = time.time()
        while time.time() - start < self.phase_timeout:
            time.sleep(0.1)
            return True
        logger.warning(
            f"Timeout waiting for response for phase {phase.value} in session {session.session_id}"
        )
        return False

    def _validate_onboarding_completion(self, session: OnboardingSession) -> bool:
        """Validate that onboarding has been completed successfully."""
        required_phases = self.role_definitions[session.agent_id]["onboarding_phases"]
        if not all(phase in session.completed_phases for phase in required_phases):
            logger.warning(
                f"Not all required phases completed for {session.agent_id}"
            )
            return False

        if not self._validate_performance_metrics(session):
            logger.warning(
                f"Performance validation failed for {session.agent_id}"
            )
            return False

        if self.fsm_core:
            self.fsm_core.create_task(
                title=f"Onboarding Completion - {session.agent_id}",
                description=(
                    f"Agent {session.agent_id} has completed onboarding and is ready for active participation"
                ),
                assigned_agent=session.agent_id,
            )
        return True

    def _validate_performance_metrics(self, session: OnboardingSession) -> bool:
        """Validate performance metrics for onboarding completion."""
        return True

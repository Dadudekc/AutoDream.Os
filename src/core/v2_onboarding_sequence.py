"""Orchestrator for the V2 Onboarding Sequence.

This module wires together the modular components responsible for
onboarding new agents into the V2 system.
"""

from .v2_onboarding_sequence_core import (
    V2OnboardingSequenceCore,
    OnboardingStatus,
    OnboardingPhase,
    OnboardingSession,
    OnboardingMessage,
)
from .v2_onboarding_sequence_validator import V2OnboardingSequenceValidator
from .v2_onboarding_sequence_coordinator import V2OnboardingSequenceCoordinator


class V2OnboardingSequence(
    V2OnboardingSequenceValidator,
    V2OnboardingSequenceCoordinator,
    V2OnboardingSequenceCore,
):
    """Main entry point combining all onboarding components."""

    def __init__(self, config=None):
        V2OnboardingSequenceCore.__init__(self, config)


__all__ = [
    "V2OnboardingSequence",
    "OnboardingStatus",
    "OnboardingPhase",
    "OnboardingSession",
    "OnboardingMessage",
]

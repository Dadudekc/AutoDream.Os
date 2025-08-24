import uuid
from typing import Dict, Any

from .v2_onboarding_sequence_core import OnboardingPhase, OnboardingMessage

# Default configuration values
DEFAULT_PHASE_TIMEOUT = 300  # 5 minutes
DEFAULT_VALIDATION_RETRIES = 3
DEFAULT_PERFORMANCE_THRESHOLDS: Dict[str, Any] = {}

# Role definitions for the V2 system
ROLE_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "Agent-1": {
        "role": "System Coordinator & Project Manager",
        "capabilities": [
            "FSM coordination",
            "Multi-repository oversight",
            "Performance monitoring",
        ],
        "onboarding_phases": [
            OnboardingPhase.SYSTEM_OVERVIEW,
            OnboardingPhase.ROLE_ASSIGNMENT,
            OnboardingPhase.CAPABILITY_TRAINING,
            OnboardingPhase.INTEGRATION_TESTING,
        ],
    },
    "Agent-2": {
        "role": "Frontend Development Specialist",
        "capabilities": [
            "Modern web development",
            "UI/UX design",
            "Performance optimization",
        ],
        "onboarding_phases": [
            OnboardingPhase.SYSTEM_OVERVIEW,
            OnboardingPhase.ROLE_ASSIGNMENT,
            OnboardingPhase.CAPABILITY_TRAINING,
            OnboardingPhase.INTEGRATION_TESTING,
        ],
    },
    "Agent-3": {
        "role": "Backend Development Specialist",
        "capabilities": [
            "API development",
            "Database design",
            "Security implementation",
        ],
        "onboarding_phases": [
            OnboardingPhase.SYSTEM_OVERVIEW,
            OnboardingPhase.ROLE_ASSIGNMENT,
            OnboardingPhase.CAPABILITY_TRAINING,
            OnboardingPhase.INTEGRATION_TESTING,
        ],
    },
    "Agent-4": {
        "role": "DevOps & Infrastructure Specialist",
        "capabilities": [
            "Cloud infrastructure",
            "CI/CD pipelines",
            "Monitoring systems",
        ],
        "onboarding_phases": [
            OnboardingPhase.SYSTEM_OVERVIEW,
            OnboardingPhase.ROLE_ASSIGNMENT,
            OnboardingPhase.CAPABILITY_TRAINING,
            OnboardingPhase.INTEGRATION_TESTING,
        ],
    },
    "Agent-5": {
        "role": "Gaming & Entertainment Specialist",
        "capabilities": [
            "Game development",
            "Entertainment systems",
            "Performance optimization",
        ],
        "onboarding_phases": [
            OnboardingPhase.SYSTEM_OVERVIEW,
            OnboardingPhase.ROLE_ASSIGNMENT,
            OnboardingPhase.CAPABILITY_TRAINING,
            OnboardingPhase.INTEGRATION_TESTING,
        ],
    },
    "Agent-6": {
        "role": "AI/ML & Research Specialist",
        "capabilities": [
            "Machine learning",
            "AI system integration",
            "Research initiatives",
        ],
        "onboarding_phases": [
            OnboardingPhase.SYSTEM_OVERVIEW,
            OnboardingPhase.ROLE_ASSIGNMENT,
            OnboardingPhase.CAPABILITY_TRAINING,
            OnboardingPhase.INTEGRATION_TESTING,
        ],
    },
    "Agent-7": {
        "role": "Web & UI Framework Specialist",
        "capabilities": [
            "Framework development",
            "Component systems",
            "Performance optimization",
        ],
        "onboarding_phases": [
            OnboardingPhase.SYSTEM_OVERVIEW,
            OnboardingPhase.ROLE_ASSIGNMENT,
            OnboardingPhase.CAPABILITY_TRAINING,
            OnboardingPhase.INTEGRATION_TESTING,
        ],
    },
    "Agent-8": {
        "role": "Mobile & Cross-Platform Specialist",
        "capabilities": [
            "Mobile development",
            "Cross-platform compatibility",
            "Performance optimization",
        ],
        "onboarding_phases": [
            OnboardingPhase.SYSTEM_OVERVIEW,
            OnboardingPhase.ROLE_ASSIGNMENT,
            OnboardingPhase.CAPABILITY_TRAINING,
            OnboardingPhase.INTEGRATION_TESTING,
        ],
    },
}


def create_default_message_templates() -> Dict[str, OnboardingMessage]:
    """Create default onboarding message templates."""
    templates: Dict[str, OnboardingMessage] = {
        "system_overview": OnboardingMessage(
            message_id=str(uuid.uuid4()),
            phase=OnboardingPhase.SYSTEM_OVERVIEW,
            content=(
                "🚀 Welcome to Agent Cellphone V2! You are now part of the most advanced autonomous agent coordination platform ever created."
            ),
            role_specific=False,
            requires_response=True,
            validation_criteria={"response_time": 30, "comprehension": True},
        ),
        "role_assignment": OnboardingMessage(
            message_id=str(uuid.uuid4()),
            phase=OnboardingPhase.ROLE_ASSIGNMENT,
            content=(
                "🎯 Role Assignment: You have been assigned a specialized role in the V2 system."
            ),
            role_specific=True,
            requires_response=True,
            validation_criteria={"role_acceptance": True, "capability_confirmation": True},
        ),
        "capability_training": OnboardingMessage(
            message_id=str(uuid.uuid4()),
            phase=OnboardingPhase.CAPABILITY_TRAINING,
            content=(
                "🔧 Capability Training: You will now receive specialized training for your role."
            ),
            role_specific=True,
            requires_response=True,
            validation_criteria={"training_completion": True, "skill_assessment": True},
        ),
        "integration_testing": OnboardingMessage(
            message_id=str(uuid.uuid4()),
            phase=OnboardingPhase.INTEGRATION_TESTING,
            content=(
                "🧪 Integration Testing: You will now participate in integration testing to validate coordination with other agents and the FSM system."
            ),
            role_specific=False,
            requires_response=True,
            validation_criteria={
                "integration_success": True,
                "coordination_effectiveness": True,
            },
        ),
    }
    return templates

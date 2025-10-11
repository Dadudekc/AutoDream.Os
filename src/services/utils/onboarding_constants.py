"""
Onboarding Constants and Configuration
======================================
Phase 2 status tracking and default configurations for onboarding service.
Extracted for V2 compliance.

Author: Agent-5 (extracted from Agent-1's unified_onboarding_service.py)
License: MIT
"""

# Phase 2 Status Tracking
PHASE_2_STATUS: dict[str, bool] = {
    "wrap_up_completed": True,
    "agent_8_prepared": True,
    "swarm_coordination_activated": True,
    "cycle_1_foundation_audit_initiated": True,
    "discord_devlog_reminder_system_updated": True,
    "comprehensive_reminder_system_enhanced": True,
}

AGENT_ASSIGNMENTS: dict[str, str] = {
    "Agent-8": "Support & Monitoring Specialist (Position: 1611, 941)",
    "Agent-3": "Infrastructure Audit (Cycle 1, Days 1-3)",
    "Agent-7": "JavaScript Audit (Cycle 1, Days 1-3)",
    "Agent-4": "QA Captain & Coordination",
}

TARGETS: dict[str, str] = {
    "file_reduction": "15-20% initial file reduction",
    "timeline": "3-day cycles with daily check-ins",
    "coordination": "Real-time PyAutoGUI messaging active",
    "documentation": "Comprehensive reminder system (identity, devlog, inbox, status)",
}

# Default Agent Roles
DEFAULT_AGENT_ROLES: dict[str, str] = {
    "Agent-1": "Integration & Core Systems Specialist",
    "Agent-2": "Architecture & Design Specialist",
    "Agent-3": "Infrastructure & DevOps Lead",
    "Agent-4": "Quality Assurance & Captain",
    "Agent-5": "Business Intelligence & Analytics",
    "Agent-6": "Testing & Validation Specialist",
    "Agent-7": "Web Development Specialist",
    "Agent-8": "Documentation & Knowledge Management",
}


def get_phase_2_status() -> dict[str, bool]:
    """Get current Phase 2 consolidation execution status."""
    return PHASE_2_STATUS.copy()


def get_agent_assignments() -> dict[str, str]:
    """Get current agent assignments."""
    return AGENT_ASSIGNMENTS.copy()


def get_targets() -> dict[str, str]:
    """Get current execution targets."""
    return TARGETS.copy()


def is_phase_2_active() -> bool:
    """Check if Phase 2 consolidation execution is active."""
    return all(PHASE_2_STATUS.values())

#!/usr/bin/env python3
"""
Unified Onboarding System - Agent Cellphone V2
==============================================

Consolidated onboarding system that eliminates duplication and provides
a single source of truth for agent onboarding.

Follows V2 standards: 400 LOC, OOP design, SRP.
"""

import logging
import uuid
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import json

from .fsm_core_v2 import FSMCoreV2
from .communication_compatibility_layer import InboxManager

logger = logging.getLogger(__name__)


class OnboardingStatus(Enum):
    """Onboarding status values."""
    PENDING = "pending"
    INITIALIZING = "initializing"
    ORIENTATION = "orientation"
    CAPTAIN_COORDINATION = "captain_coordination"
    ROLE_TRAINING = "role_training"
    SSOT_TRAINING = "ssot_training"
    INTEGRATION = "integration"
    VALIDATION = "validation"
    COMPLETED = "completed"
    FAILED = "failed"


class OnboardingPhase(Enum):
    """Onboarding phases."""
    SYSTEM_OVERVIEW = "system_overview"
    ROLE_ASSIGNMENT = "role_assignment"
    CAPTAIN_COORDINATION = "captain_coordination"
    CAPABILITY_TRAINING = "capability_training"
    UNIVERSAL_WORKFLOW = "universal_workflow"
    COMMUNICATION_PROTOCOL = "communication_protocol"
    DEVLOG_TRAINING = "devlog_training"
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


class UnifiedOnboardingSystem:
    """
    Unified Onboarding System - Single responsibility: Agent onboarding management.
    
    Consolidates all onboarding functionality into one system to eliminate duplication.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the unified onboarding system."""
        self.config = config or {}
        
        # Core components
        self.fsm_core: Optional[FSMCoreV2] = None
        self.inbox_manager: Optional[InboxManager] = None
        
        # Onboarding state
        self.active_sessions: Dict[str, OnboardingSession] = {}
        self.onboarding_templates: Dict[str, OnboardingMessage] = self._create_default_templates()
        self.role_definitions: Dict[str, Dict[str, Any]] = self._load_role_definitions()
        
        # Configuration
        self.phase_timeout = self.config.get("phase_timeout", 30)  # minutes
        self.validation_retries = self.config.get("validation_retries", 3)
        
        logger.info("UnifiedOnboardingSystem initialized")

    def _create_default_templates(self) -> Dict[str, OnboardingMessage]:
        """Create default onboarding message templates."""
        templates = {}
        
        # System overview template
        templates["system_overview"] = OnboardingMessage(
            message_id=str(uuid.uuid4()),
            phase=OnboardingPhase.SYSTEM_OVERVIEW,
            content=(
                "🎯 Welcome to Agent Cellphone V2! You are now part of a coordinated swarm. "
                "This system uses FSM-driven development with contract management. "
                "Are you ready to begin orientation?"
            ),
            role_specific=False,
            requires_response=True,
            validation_criteria={"orientation_ready": True}
        )
        
        # Captain coordination template
        templates["captain_coordination"] = OnboardingMessage(
            message_id=str(uuid.uuid4()),
            phase=OnboardingPhase.CAPTAIN_COORDINATION,
            content=(
                "🤝 Captain Agent Coordination Training: You will now learn how to work "
                "effectively in a coordinated swarm. The captain agent serves as an "
                "orchestrator, not a commander. Are you ready to learn coordination?"
            ),
            role_specific=False,
            requires_response=True,
            validation_criteria={
                "coordination_understanding": True,
                "fsm_integration_skills": True,
                "collaboration_workflow": True
            }
        )
        
        # Integration testing template
        templates["integration_testing"] = OnboardingMessage(
            message_id=str(uuid.uuid4()),
            phase=OnboardingPhase.INTEGRATION_TESTING,
            content=(
                "🔧 Integration Testing: You will now test your integration with the FSM system "
                "and verify your ability to create and update tasks. Ready to test?"
            ),
            role_specific=False,
            requires_response=True,
            validation_criteria={"integration_verified": True}
        )
        
        # Devlog training template
        templates["devlog_training"] = OnboardingMessage(
            message_id=str(uuid.uuid4()),
            phase=OnboardingPhase.DEVLOG_TRAINING,
            content=(
                "📝 Devlog System Training: You will now learn about the SINGLE SOURCE OF TRUTH "
                "for posting project updates - the Devlog CLI system. This is how you communicate "
                "progress, issues, and milestones to the team via Discord. Ready to learn?"
            ),
            role_specific=False,
            requires_response=True,
            validation_criteria={"devlog_understanding": True}
        )
        
        return templates

    def _load_role_definitions(self) -> Dict[str, Dict[str, Any]]:
        """Load role definitions from configuration."""
        return {
            "default": {
                "role": "General Agent",
                "capabilities": ["task_execution", "fsm_integration", "collaboration"],
                "training_modules": ["basic_workflow", "fsm_usage", "coordination"]
            },
            "developer": {
                "role": "Development Agent",
                "capabilities": ["code_development", "refactoring", "testing"],
                "training_modules": ["coding_standards", "modularization", "testing"]
            },
            "coordinator": {
                "role": "Coordination Agent",
                "capabilities": ["task_assignment", "progress_tracking", "conflict_resolution"],
                "training_modules": ["coordination_workflow", "fsm_management", "conflict_resolution"]
            }
        }

    def start_onboarding(self, agent_id: str, role: str = "default") -> str:
        """Start onboarding for a new agent."""
        try:
            session_id = str(uuid.uuid4())
            now = datetime.now()
            
            session = OnboardingSession(
                session_id=session_id,
                agent_id=agent_id,
                status=OnboardingStatus.INITIALIZING,
                current_phase=OnboardingPhase.SYSTEM_OVERVIEW,
                completed_phases=[],
                start_time=now
            )
            
            self.active_sessions[session_id] = session
            
            # Create FSM task for onboarding
            if self.fsm_core:
                task_id = self.fsm_core.create_task(
                    title=f"Onboard Agent {agent_id}",
                    description=f"Complete onboarding process for {agent_id} as {role}",
                    assigned_agent=agent_id,
                    priority="HIGH"
                )
                logger.info(f"Created FSM task {task_id} for onboarding {agent_id}")
            
            logger.info(f"Started onboarding session {session_id} for agent {agent_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to start onboarding for {agent_id}: {e}")
            return ""

    def get_phase_message(self, phase: OnboardingPhase, agent_id: str) -> OnboardingMessage:
        """Get the message for a specific phase."""
        if phase == OnboardingPhase.SYSTEM_OVERVIEW:
            return self.onboarding_templates["system_overview"]
            
        if phase == OnboardingPhase.ROLE_ASSIGNMENT:
            role_info = self.role_definitions.get("default", {})
            return OnboardingMessage(
                message_id=str(uuid.uuid4()),
                phase=phase,
                content=(
                    f"🎯 Role Assignment: You are {role_info.get('role', 'General Agent')}. "
                    f"Your capabilities include: {', '.join(role_info.get('capabilities', []))}. "
                    "Are you ready to accept this role?"
                ),
                role_specific=True,
                requires_response=True,
                validation_criteria={
                    "role_acceptance": True,
                    "capability_confirmation": True
                }
            )
            
        if phase == OnboardingPhase.CAPTAIN_COORDINATION:
            return self.onboarding_templates["captain_coordination"]
            
        if phase == OnboardingPhase.CAPABILITY_TRAINING:
            role_info = self.role_definitions.get("default", {})
            return OnboardingMessage(
                message_id=str(uuid.uuid4()),
                phase=phase,
                content=(
                    f"🔧 Capability Training: You will now receive specialized training for your role. "
                    "This includes V2 development standards, FSM integration, and performance optimization. "
                    "Ready to begin training?"
                ),
                role_specific=True,
                requires_response=True,
                validation_criteria={
                    "training_completion": True,
                    "skill_assessment": True
                }
            )
            
        if phase == OnboardingPhase.DEVLOG_TRAINING:
            return OnboardingMessage(
                message_id=str(uuid.uuid4()),
                phase=phase,
                content=(
                    "📝 **DEVLOG SYSTEM - YOUR SINGLE SOURCE OF TRUTH**\n\n"
                    "🎯 **Purpose**: Post project updates, milestones, and progress to Discord\n"
                    "🔧 **Tool**: Devlog CLI system (python -m src.core.devlog_cli)\n"
                    "📱 **Output**: Automatically posts to Discord devlog channel\n\n"
                    "**Key Commands**:\n"
                    "• Create: python -m src.core.devlog_cli create --title 'Title' --content 'Content' --agent 'your-id'\n"
                    "• Search: python -m src.core.devlog_cli search --query 'search term'\n"
                    "• Recent: python -m src.core.devlog_cli recent --limit 5\n"
                    "• Status: python -m src.core.devlog_cli status\n\n"
                    "**This is how you communicate with the team!** Ready to learn more?"
                ),
                role_specific=False,
                requires_response=True,
                validation_criteria={
                    "devlog_understanding": True,
                    "command_familiarity": True
                }
            )
            
        if phase == OnboardingPhase.INTEGRATION_TESTING:
            return self.onboarding_templates["integration_testing"]
            
        return self.onboarding_templates["system_overview"]

    def advance_phase(self, session_id: str, new_phase: OnboardingPhase) -> bool:
        """Advance an onboarding session to the next phase."""
        try:
            session = self.active_sessions.get(session_id)
            if not session:
                logger.error(f"Session {session_id} not found")
                return False
            
            # Mark current phase as completed
            if session.current_phase not in session.completed_phases:
                session.completed_phases.append(session.current_phase)
            
            # Update to new phase
            session.current_phase = new_phase
            session.status = OnboardingStatus(new_phase.value)
            
            # Update FSM task if available
            if self.fsm_core:
                # Find the onboarding task for this agent
                # This would need to be implemented based on FSM task structure
                pass
            
            logger.info(f"Advanced session {session_id} to phase {new_phase.value}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to advance phase for session {session_id}: {e}")
            return False

    def complete_onboarding(self, session_id: str) -> bool:
        """Mark onboarding as completed."""
        try:
            session = self.active_sessions.get(session_id)
            if not session:
                logger.error(f"Session {session_id} not found")
                return False
            
            session.status = OnboardingStatus.COMPLETED
            session.completion_time = datetime.now()
            
            # Update FSM task if available
            if self.fsm_core:
                # Mark the onboarding task as completed
                pass
            
            logger.info(f"Completed onboarding session {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to complete onboarding for session {session_id}: {e}")
            return False

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
            "completion_time": session.completion_time.isoformat() if session.completion_time else None,
            "performance_metrics": session.performance_metrics,
            "validation_results": session.validation_results
        }

    def get_all_onboarding_status(self) -> Dict[str, Any]:
        """Get status of all onboarding sessions."""
        return {sid: self.get_onboarding_status(sid) for sid in self.active_sessions}

    def cleanup_completed_sessions(self) -> None:
        """Clean up completed onboarding sessions."""
        completed = [
            sid for sid, session in self.active_sessions.items()
            if session.status in (OnboardingStatus.COMPLETED, OnboardingStatus.FAILED)
        ]
        
        for sid in completed:
            del self.active_sessions[sid]
            
        if completed:
            logger.info(f"Cleaned up {len(completed)} completed sessions")

    def set_fsm_core(self, fsm_core: FSMCoreV2) -> None:
        """Set the FSM core for task tracking."""
        self.fsm_core = fsm_core
        logger.info("FSM core connected to onboarding system")

    def set_inbox_manager(self, inbox_manager: InboxManager) -> None:
        """Set the inbox manager for communication."""
        self.inbox_manager = inbox_manager
        logger.info("Inbox manager connected to onboarding system")


# Main entry point for the unified system
def create_onboarding_system(config: Optional[Dict[str, Any]] = None) -> UnifiedOnboardingSystem:
    """Factory function to create a new onboarding system instance."""
    return UnifiedOnboardingSystem(config)

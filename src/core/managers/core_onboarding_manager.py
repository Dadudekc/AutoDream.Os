"""Specialized manager handling agent onboarding operations."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from src.core.constants.manager import COMPLETION_SIGNAL
from .contracts import Manager, ManagerContext, ManagerResult


@dataclass
class OnboardingSession:
    """Represents a single onboarding session."""

    agent_id: str
    agent_name: str
    role: str
    template: str
    status: str = "pending"
    start_time: datetime | None = None
    end_time: datetime | None = None
    notes: str | None = None


class CoreOnboardingManager(Manager):
    """Focuses solely on onboarding related operations."""

    def __init__(self) -> None:
        self._templates = ["default", "advanced"]
        self._sessions: Dict[str, OnboardingSession] = {}

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize onboarding manager."""
        context.logger("CoreOnboardingManager initialized")
        return True

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute onboarding operation."""
        handlers = {
            "onboard_agent": self.onboard_agent,
            "start_onboarding": self.start_onboarding,
            "complete_onboarding": self.complete_onboarding,
            "get_onboarding_status": self.get_onboarding_status,
        }
        handler = handlers.get(operation)
        if not handler:
            return ManagerResult(
                False, {}, {}, f"Unknown operation: {operation}"
            )
        return handler(context, payload)

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup resources."""
        self._sessions.clear()
        context.logger("CoreOnboardingManager cleaned up")
        return True

    def get_status(self) -> Dict[str, Any]:
        """Return manager status."""
        return {
            "templates": self._templates,
            "total_sessions": len(self._sessions),
        }

    # Handlers ---------------------------------------------------------------
    def onboard_agent(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        agent_id = payload["agent_id"]
        session_id = str(uuid.uuid4())
        session = OnboardingSession(
            agent_id=agent_id,
            agent_name=payload.get("agent_name", agent_id),
            role=payload.get("role", "unknown"),
            template=payload.get("template", "default"),
        )
        self._sessions[session_id] = session
        context.logger(f"Onboarding session created: {session_id}")
        return ManagerResult(
            True, {"session_id": session_id, "agent_id": agent_id}, {}
        )

    def start_onboarding(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        session = self._sessions.get(payload["session_id"])
        if not session:
            return ManagerResult(False, {}, {}, "Session not found")
        session.status = "in_progress"
        session.start_time = datetime.utcnow()
        context.logger(f"Onboarding session started: {payload['session_id']}")
        return ManagerResult(True, {"session_id": payload["session_id"]}, {})

    def complete_onboarding(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        session = self._sessions.get(payload["session_id"])
        if not session:
            return ManagerResult(False, {}, {}, "Session not found")
        session.status = (
            "completed" if payload.get("success", True) else "failed"
        )
        session.end_time = datetime.utcnow()
        session.notes = payload.get("notes")
        context.logger(
            f"Onboarding session completed: {payload['session_id']} "
            f"{COMPLETION_SIGNAL}"
        )
        return ManagerResult(
            True,
            {"session_id": payload["session_id"], "status": session.status},
            {},
        )

    def get_onboarding_status(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        session = self._sessions.get(payload["session_id"])
        if not session:
            return ManagerResult(False, {}, {}, "Session not found")
        data = {
            "session_id": payload["session_id"],
            "status": session.status,
            "start_time": session.start_time,
            "end_time": session.end_time,
            "notes": session.notes,
        }
        return ManagerResult(True, data, {})

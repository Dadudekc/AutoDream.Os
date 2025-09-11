#!/usr/bin/env python3
"""
Debate Engine - Intent-Oriented Subsystem
=========================================

Decomposed from SwarmOrchestrator to handle debate coordination logic.
Provides plug-and-play, testable debate management with clear separation of concerns.

Author: Swarm Representative (Following Commander Thea directives)
Mission: Orchestration Layer Decomposition - Intent Subsystem Creation
License: MIT
"""

from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, Union
from pathlib import Path

from ..contracts import OrchestrationContext, OrchestrationResult, Step
from ..registry import StepRegistry


class DebateStatus(Enum):
    """Debate status enumeration."""
    PENDING = "pending"
    ACTIVE = "active"
    VOTING = "voting"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class DebatePhase(Enum):
    """Debate phase enumeration."""
    INITIALIZATION = "initialization"
    ARGUMENT_COLLECTION = "argument_collection"
    ANALYSIS = "analysis"
    VOTING = "voting"
    CONSENSUS = "consensus"
    RESOLUTION = "resolution"


@dataclass
class DebateArgument:
    """Debate argument structure."""
    id: str
    author_agent: str
    content: str
    supports_option: str
    confidence: float
    technical_feasibility: float
    business_value: float
    timestamp: datetime
    votes: Dict[str, int] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DebateSession:
    """Debate session container."""
    session_id: str
    topic: str
    status: DebateStatus = DebateStatus.PENDING
    current_phase: DebatePhase = DebatePhase.INITIALIZATION
    participants: List[str] = field(default_factory=list)
    arguments: List[DebateArgument] = field(default_factory=list)
    options: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    deadline: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class DebateStrategy(Protocol):
    """Strategy pattern for debate management."""

    def initialize_debate(self, topic: str, options: List[str], participants: List[str]) -> DebateSession: ...

    def collect_arguments(self, session: DebateSession, arguments: List[DebateArgument]) -> DebateSession: ...

    def analyze_arguments(self, session: DebateSession) -> Dict[str, Any]: ...

    def conduct_voting(self, session: DebateSession) -> Dict[str, Any]: ...

    def reach_consensus(self, session: DebateSession, analysis: Dict[str, Any]) -> str: ...


class SwarmDebateStrategy:
    """Swarm-optimized debate strategy."""

    def initialize_debate(self, topic: str, options: List[str], participants: List[str]) -> DebateSession:
        """Initialize a new debate session."""
        session_id = f"debate_{int(time.time())}_{len(participants)}agents"

        session = DebateSession(
            session_id=session_id,
            topic=topic,
            participants=participants,
            options=options,
            deadline=datetime.now() + timedelta(hours=24)  # 24-hour default
        )

        return session

    def collect_arguments(self, session: DebateSession, arguments: List[DebateArgument]) -> DebateSession:
        """Collect and validate arguments."""
        # Filter arguments by participants
        valid_arguments = [
            arg for arg in arguments
            if arg.author_agent in session.participants
        ]

        session.arguments = valid_arguments
        session.current_phase = DebatePhase.ARGUMENT_COLLECTION

        return session

    def analyze_arguments(self, session: DebateSession) -> Dict[str, Any]:
        """Analyze collected arguments."""
        analysis = {
            "total_arguments": len(session.arguments),
            "arguments_by_option": {},
            "average_quality_by_option": {},
            "top_contributors": [],
            "consensus_indicators": {}
        }

        # Group arguments by option
        option_counts = {}
        option_quality = {}

        for arg in session.arguments:
            option = arg.supports_option
            if option not in option_counts:
                option_counts[option] = 0
                option_quality[option] = []

            option_counts[option] += 1
            quality_score = (arg.confidence + arg.technical_feasibility + arg.business_value) / 3
            option_quality[option].append(quality_score)

        analysis["arguments_by_option"] = option_counts

        # Calculate average quality
        avg_quality = {}
        for option, scores in option_quality.items():
            avg_quality[option] = sum(scores) / len(scores) if scores else 0

        analysis["average_quality_by_option"] = avg_quality

        # Find top contributors
        contributor_counts = {}
        for arg in session.arguments:
            contributor_counts[arg.author_agent] = contributor_counts.get(arg.author_agent, 0) + 1

        top_contributors = sorted(contributor_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        analysis["top_contributors"] = top_contributors

        return analysis

    def conduct_voting(self, session: DebateSession) -> Dict[str, Any]:
        """Conduct voting on arguments."""
        voting_results = {
            "votes_cast": 0,
            "argument_votes": {},
            "participant_votes": {}
        }

        # Simple majority voting simulation
        for arg in session.arguments:
            votes = len(arg.votes)
            voting_results["votes_cast"] += votes
            voting_results["argument_votes"][arg.id] = votes

        return voting_results

    def reach_consensus(self, session: DebateSession, analysis: Dict[str, Any]) -> str:
        """Reach consensus based on analysis."""
        # Find option with highest average quality
        avg_quality = analysis.get("average_quality_by_option", {})

        if not avg_quality:
            return "No consensus - insufficient data"

        best_option = max(avg_quality.items(), key=lambda x: x[1])
        return f"Consensus: {best_option[0]} (Quality Score: {best_option[1]:.2f})"


class DebateEngine:
    """Debate Engine - Intent-Oriented Subsystem for debate coordination."""

    def __init__(self, strategy: Optional[DebateStrategy] = None):
        self.logger = logging.getLogger(__name__)
        self.strategy = strategy or SwarmDebateStrategy()
        self.active_sessions: Dict[str, DebateSession] = {}
        self.completed_sessions: Dict[str, DebateSession] = {}
        self.debate_history: List[DebateSession] = []

    def create_debate(self, topic: str, options: List[str], participants: List[str]) -> str:
        """Create a new debate session."""
        session = self.strategy.initialize_debate(topic, options, participants)
        self.active_sessions[session.session_id] = session

        self.logger.info(f"Created debate session: {session.session_id} - {topic}")
        return session.session_id

    def submit_argument(self, session_id: str, argument: DebateArgument) -> bool:
        """Submit an argument to a debate session."""
        if session_id not in self.active_sessions:
            self.logger.error(f"Debate session not found: {session_id}")
            return False

        session = self.active_sessions[session_id]
        if argument.author_agent not in session.participants:
            self.logger.error(f"Agent not authorized: {argument.author_agent}")
            return False

        session.arguments.append(argument)
        self.logger.info(f"Argument submitted to {session_id} by {argument.author_agent}")
        return True

    def analyze_debate(self, session_id: str) -> Dict[str, Any]:
        """Analyze a debate session."""
        if session_id not in self.active_sessions:
            self.logger.error(f"Debate session not found: {session_id}")
            return {"error": "Session not found"}

        session = self.active_sessions[session_id]
        analysis = self.strategy.analyze_arguments(session)

        self.logger.info(f"Debate analysis completed for {session_id}")
        return analysis

    def conduct_voting(self, session_id: str) -> Dict[str, Any]:
        """Conduct voting for a debate session."""
        if session_id not in self.active_sessions:
            self.logger.error(f"Debate session not found: {session_id}")
            return {"error": "Session not found"}

        session = self.active_sessions[session_id]
        voting_results = self.strategy.conduct_voting(session)

        self.logger.info(f"Voting completed for {session_id}")
        return voting_results

    def resolve_debate(self, session_id: str) -> str:
        """Resolve a debate and reach consensus."""
        if session_id not in self.active_sessions:
            self.logger.error(f"Debate session not found: {session_id}")
            return "Error: Session not found"

        session = self.active_sessions[session_id]

        # Conduct analysis
        analysis = self.strategy.analyze_arguments(session)

        # Reach consensus
        consensus = self.strategy.reach_consensus(session, analysis)

        # Move to completed
        session.status = DebateStatus.COMPLETED
        session.current_phase = DebatePhase.RESOLUTION
        self.completed_sessions[session_id] = session
        del self.active_sessions[session_id]
        self.debate_history.append(session)

        self.logger.info(f"Debate resolved: {session_id} - {consensus}")
        return consensus

    def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a debate session."""
        session = (self.active_sessions.get(session_id) or
                  self.completed_sessions.get(session_id))

        if not session:
            return None

        return {
            "session_id": session.session_id,
            "topic": session.topic,
            "status": session.status.value,
            "phase": session.current_phase.value,
            "participants": session.participants,
            "arguments_count": len(session.arguments),
            "options": session.options,
            "created_at": session.created_at.isoformat(),
            "deadline": session.deadline.isoformat() if session.deadline else None
        }

    def list_active_sessions(self) -> List[Dict[str, Any]]:
        """List all active debate sessions."""
        return [
            self.get_session_status(session_id)
            for session_id in self.active_sessions.keys()
        ]

    def get_debate_history(self) -> List[Dict[str, Any]]:
        """Get debate history."""
        return [
            {
                "session_id": session.session_id,
                "topic": session.topic,
                "status": session.status.value,
                "created_at": session.created_at.isoformat(),
                "arguments_count": len(session.arguments),
                "consensus": getattr(session, 'consensus', 'Unknown')
            }
            for session in self.debate_history[-10:]  # Last 10 debates
        ]


class DebateOrchestrationStep(Step):
    """Orchestration step for debate operations."""

    def __init__(self, debate_engine: DebateEngine, operation: str, **params):
        self.debate_engine = debate_engine
        self.operation = operation
        self.params = params

    def name(self) -> str:
        return f"debate_{self.operation}"

    def run(self, ctx: OrchestrationContext, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute debate operation."""
        try:
            if self.operation == "create":
                session_id = self.debate_engine.create_debate(
                    topic=self.params.get("topic", "Strategic Debate"),
                    options=self.params.get("options", []),
                    participants=self.params.get("participants", [])
                )
                payload["debate_session_id"] = session_id

            elif self.operation == "analyze":
                session_id = payload.get("debate_session_id")
                if session_id:
                    analysis = self.debate_engine.analyze_debate(session_id)
                    payload["debate_analysis"] = analysis

            elif self.operation == "resolve":
                session_id = payload.get("debate_session_id")
                if session_id:
                    consensus = self.debate_engine.resolve_debate(session_id)
                    payload["debate_consensus"] = consensus

            ctx.logger(f"Debate operation completed: {self.operation}")
            return payload

        except Exception as e:
            ctx.logger(f"Debate operation failed: {e}")
            payload["debate_error"] = str(e)
            return payload


# Factory function for creating DebateEngine instances
def create_debate_engine(strategy: Optional[DebateStrategy] = None) -> DebateEngine:
    """Factory function for DebateEngine creation."""
    return DebateEngine(strategy=strategy)


__all__ = [
    "DebateEngine",
    "DebateSession",
    "DebateArgument",
    "DebateStatus",
    "DebatePhase",
    "DebateStrategy",
    "SwarmDebateStrategy",
    "DebateOrchestrationStep",
    "create_debate_engine"
]

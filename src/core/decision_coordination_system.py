#!/usr/bin/env python3
"""Decision Coordination System - trimmed engine."""

import json
import time
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from src.utils.stability_improvements import stability_manager, safe_import
from .decision import DecisionManager as DecisionMakingEngine, DecisionType, DecisionRequest
from .coordination_status import CoordinationMode, CoordinationStatus
from .coordination_results import (
    gather_agent_inputs,
    deliberate_decision,
    build_consensus,
    finalize_decision,
    handle_no_consensus,
)
from .coordination_scheduler import CoordinationScheduler


@dataclass
class CoordinationSession:
    """Decision coordination session data."""

    session_id: str
    decision_id: str
    mode: CoordinationMode
    participants: List[str]
    start_time: float
    end_time: Optional[float]
    status: str
    consensus_reached: bool
    final_decision: Optional[Any]


class DecisionCoordinationSystem:
    """Coordinates collaborative decision-making across agent swarm."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"{__name__}.DecisionCoordinationSystem")
        self.workspace_path = Path("agent_workspaces")
        self.decision_engine = DecisionMakingEngine()
        self.active_sessions: Dict[str, CoordinationSession] = {}
        self.session_history: List[CoordinationSession] = []
        self.coordination_protocols: Dict[CoordinationMode, Dict] = {}
        self.scheduler = CoordinationScheduler(
            gather_agent_inputs,
            deliberate_decision,
            build_consensus,
            finalize_decision,
            handle_no_consensus,
        )
        self.workspace_path.mkdir(exist_ok=True)
        self._initialize_coordination_protocols()

    def _initialize_coordination_protocols(self) -> None:
        """Initialize coordination protocols for different modes."""
        self.coordination_protocols = {
            CoordinationMode.CONSENSUS: {
                "description": "All participants must agree",
                "threshold": 1.0,
                "timeout": 300,
                "retry_attempts": 3,
            },
            CoordinationMode.MAJORITY: {
                "description": "Majority vote decides",
                "threshold": 0.51,
                "timeout": 180,
                "retry_attempts": 2,
            },
            CoordinationMode.EXPERT_OPINION: {
                "description": "Expert agent makes final decision",
                "threshold": 0.8,
                "timeout": 120,
                "retry_attempts": 1,
            },
            CoordinationMode.HIERARCHICAL: {
                "description": "Hierarchical decision structure",
                "threshold": 0.7,
                "timeout": 240,
                "retry_attempts": 2,
            },
            CoordinationMode.COLLABORATIVE: {
                "description": "Full collaborative decision-making",
                "threshold": 0.6,
                "timeout": 360,
                "retry_attempts": 3,
            },
        }

    def initiate_coordination_session(
        self,
        decision_id: str,
        mode: CoordinationMode,
        participants: Optional[List[str]] = None,
    ) -> str:
        """Initiate a new decision coordination session."""
        session_id = f"session_{mode.value}_{decision_id}_{int(time.time())}"
        if not participants:
            participants = self._discover_available_agents()
        session = CoordinationSession(
            session_id=session_id,
            decision_id=decision_id,
            mode=mode,
            participants=participants,
            start_time=time.time(),
            end_time=None,
            status=CoordinationStatus.ACTIVE.value,
            consensus_reached=False,
            final_decision=None,
        )
        self.active_sessions[session_id] = session
        self._notify_session_participants(session)
        protocol = self.coordination_protocols[mode]
        self.scheduler.start(self, session, protocol)
        self.logger.info(
            f"Coordination session initiated: {session_id} with {len(participants)} participants"
        )
        return session_id

    def _discover_available_agents(self) -> List[str]:
        """Discover available agents for coordination."""
        agents: List[str] = []
        if self.workspace_path.exists():
            for agent_dir in self.workspace_path.iterdir():
                if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                    agents.append(agent_dir.name)
        return agents

    def _notify_session_participants(self, session: CoordinationSession) -> None:
        """Notify all participants about coordination session."""
        for participant in session.participants:
            self._send_session_notification(session, participant)

    def _send_session_notification(self, session: CoordinationSession, participant: str) -> None:
        """Send session notification to participant."""
        message = {
            "type": "coordination_session",
            "from": "DecisionCoordinationSystem",
            "to": participant,
            "timestamp": time.time(),
            "session_id": session.session_id,
            "decision_id": session.decision_id,
            "mode": session.mode.value,
            "action": "join_coordination_session",
        }
        agent_inbox = self.workspace_path / participant / "inbox"
        agent_inbox.mkdir(exist_ok=True)
        message_file = agent_inbox / f"coordination_session_{session.session_id}.json"
        with open(message_file, "w") as f:
            json.dump(message, f, indent=2)

    def _send_input_request(self, session: CoordinationSession, participant: str) -> None:
        """Send input request to participant."""
        message = {
            "type": "input_request",
            "from": "DecisionCoordinationSystem",
            "to": participant,
            "timestamp": time.time(),
            "session_id": session.session_id,
            "decision_id": session.decision_id,
            "action": "provide_decision_input",
            "deadline": time.time() + 60,
        }
        agent_inbox = self.workspace_path / participant / "inbox"
        agent_inbox.mkdir(exist_ok=True)
        message_file = agent_inbox / f"input_request_{session.session_id}.json"
        with open(message_file, "w") as f:
            json.dump(message, f, indent=2)

    def _all_inputs_received(self, session: CoordinationSession) -> bool:
        """Check if all inputs have been received."""
        for participant in session.participants:
            input_file = (
                self.workspace_path
                / participant
                / "inbox"
                / f"input_response_{session.session_id}.json"
            )
            if not input_file.exists():
                return False
        return True

    def _notify_final_decision(self, session: CoordinationSession, result) -> None:
        """Notify all participants of final decision."""
        for participant in session.participants:
            message = {
                "type": "final_decision",
                "from": "DecisionCoordinationSystem",
                "to": participant,
                "timestamp": time.time(),
                "session_id": session.session_id,
                "decision_id": session.decision_id,
                "decision": session.final_decision,
                "status": "completed",
            }
            agent_inbox = self.workspace_path / participant / "inbox"
            agent_inbox.mkdir(exist_ok=True)
            message_file = agent_inbox / f"final_decision_{session.session_id}.json"
            with open(message_file, "w") as f:
                json.dump(message, f, indent=2)

    def get_coordination_status(self) -> Dict[str, Any]:
        """Get current coordination system status."""
        return {
            "active_sessions": len(self.active_sessions),
            "completed_sessions": len(self.session_history),
            "total_participants": sum(
                len(s.participants) for s in self.active_sessions.values()
            ),
            "coordination_modes": [mode.value for mode in CoordinationMode],
            "status": "DECISION_COORDINATION_ACTIVE",
        }

    def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific coordination session."""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            return {
                "session_id": session.session_id,
                "status": session.status,
                "mode": session.mode.value,
                "participants": session.participants,
                "consensus_reached": session.consensus_reached,
                "duration": time.time() - session.start_time,
            }
        return None


def main() -> None:
    """CLI interface for Decision Coordination System."""
    import argparse

    parser = argparse.ArgumentParser(description="Decision Coordination System CLI")
    parser.add_argument("--initiate", "-i", help="Initiate coordination session for decision ID")
    parser.add_argument("--mode", "-m", default="collaborative", help="Coordination mode")
    parser.add_argument("--status", "-s", help="Get session status by ID")
    parser.add_argument("--system-status", action="store_true", help="Show system status")

    args = parser.parse_args()
    system = DecisionCoordinationSystem()

    if args.initiate:
        try:
            mode = CoordinationMode(args.mode)
            session_id = system.initiate_coordination_session(args.initiate, mode)
            print(f"✅ Coordination session initiated: {session_id}")
            print(f"📋 Mode: {mode.value}")
        except ValueError as e:
            print(f"❌ Error: {e}")
    elif args.status:
        status = system.get_session_status(args.status)
        if status:
            print(f"📊 Session Status: {status['status']}")
            print(f"  Mode: {status['mode']}")
            print(f"  Participants: {status['participants']}")
            print(f"  Consensus: {status['consensus_reached']}")
            print(f"  Duration: {status['duration']:.1f}s")
        else:
            print(f"❌ Session {args.status} not found")
    elif args.system_status:
        status = system.get_coordination_status()
        print("📊 Decision Coordination System Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
    else:
        print("Decision Coordination System - Use --help for options")


if __name__ == "__main__":
    main()

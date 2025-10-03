#!/usr/bin/env python3
"""
Swarm Intelligence Coordination Core - Core Logic Module
=======================================================

Core logic for swarm intelligence coordination with real-time communication.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
Refactored By: Agent-6 (Quality Assurance Specialist)
Original: swarm_intelligence_coordination.py (410 lines) - Core module
"""

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class DecisionType(Enum):
    """Types of decisions in swarm coordination"""

    TASK_ASSIGNMENT = "task_assignment"
    CONFLICT_RESOLUTION = "conflict_resolution"
    ARCHITECTURE_CHANGE = "architecture_change"
    EMERGENCY_RESPONSE = "emergency_response"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"


class AgentRole(Enum):
    """Agent roles in swarm coordination"""

    CAPTAIN = "captain"
    SPECIALIST = "specialist"
    COORDINATOR = "coordinator"
    ANALYST = "analyst"
    EXECUTOR = "executor"


@dataclass
class SwarmDecision:
    """Swarm decision structure"""

    decision_id: str
    decision_type: DecisionType
    title: str
    description: str
    proposed_by: str
    created_at: str
    status: str  # pending, voting, resolved, rejected
    votes: dict[str, str]  # agent_id -> vote (yes/no/abstain)
    resolution: str | None = None
    resolved_at: str | None = None


@dataclass
class AgentStatus:
    """Agent status in swarm coordination"""

    agent_id: str
    role: AgentRole
    status: str  # active, busy, idle, offline
    current_task: str | None = None
    last_activity: str | None = None
    capabilities: list[str] | None = None


class SwarmCoordinationCore:
    """Core swarm coordination logic"""

    def __init__(self, data_dir: str = "data/swarm"):
        """Initialize swarm coordination core"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.decisions_file = self.data_dir / "decisions.json"
        self.status_file = self.data_dir / "agent_status.json"
        self.active_decisions: dict[str, SwarmDecision] = {}
        self.agent_statuses: dict[str, AgentStatus] = {}
        self._manage_data_operations("load")

    def create_decision(
        self, decision_type: DecisionType, title: str, description: str, proposed_by: str
    ) -> SwarmDecision:
        """Create a new swarm decision"""
        decision_id = f"decision_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        decision = SwarmDecision(
            decision_id=decision_id,
            decision_type=decision_type,
            title=title,
            description=description,
            proposed_by=proposed_by,
            created_at=datetime.now().isoformat(),
            status="pending",
            votes={},
        )

        self.active_decisions[decision_id] = decision
        self._manage_data_operations("save", "decisions")

        logger.info(f"Created decision {decision_id}: {title}")
        return decision

    def vote_on_decision(self, decision_id: str, agent_id: str, vote: str) -> bool:
        """Vote on a swarm decision"""
        if decision_id not in self.active_decisions:
            return False

        decision = self.active_decisions[decision_id]

        if vote not in ["yes", "no", "abstain"]:
            return False

        decision.votes[agent_id] = vote
        decision.status = "voting"

        # Check if we have enough votes to resolve
        if len(decision.votes) >= 5:  # Majority of 8 agents
            self._resolve_decision(decision)

        self._manage_data_operations("save", "decisions")
        logger.info(f"Agent {agent_id} voted {vote} on decision {decision_id}")
        return True

    def manage_agent_operations(
        self, action: str, agent_id: str, status: str = None, current_task: str = None
    ) -> Any:
        """Consolidated agent operations"""
        if action == "get_status":
            return self.agent_statuses.get(agent_id)
        elif action == "update_status":
            if agent_id in self.agent_statuses:
                agent = self.agent_statuses[agent_id]
                agent.status = status
                agent.current_task = current_task
                agent.last_activity = datetime.now().isoformat()
            else:
                agent = AgentStatus(
                    agent_id=agent_id,
                    role=AgentRole.SPECIALIST,
                    status=status,
                    current_task=current_task,
                    last_activity=datetime.now().isoformat(),
                    capabilities=[],
                )
                self.agent_statuses[agent_id] = agent

            self._manage_data_operations("save", "statuses")
            logger.info(f"Updated agent {agent_id} status to {status}")
            return True
        return None

    def manage_decisions(self, action: str, decision_id: str = None) -> Any:
        """Consolidated decision management"""
        if action == "get_active":
            return list(self.active_decisions.values())
        elif action == "get":
            return self.active_decisions.get(decision_id)
        return None

    def _resolve_decision(self, decision: SwarmDecision) -> None:
        """Resolve a decision based on votes"""
        yes_votes = sum(1 for vote in decision.votes.values() if vote == "yes")
        no_votes = sum(1 for vote in decision.votes.values() if vote == "no")

        if yes_votes > no_votes:
            decision.status = "resolved"
            decision.resolution = "approved"
        elif no_votes > yes_votes:
            decision.status = "resolved"
            decision.resolution = "rejected"
        else:
            decision.status = "resolved"
            decision.resolution = "tied"

        decision.resolved_at = datetime.now().isoformat()
        logger.info(f"Decision {decision.decision_id} resolved as {decision.resolution}")

    def _manage_data_operations(self, operation: str, data_type: str = None) -> None:
        """Consolidated data operations"""
        if operation == "load":
            self._load_data_files("decisions")
            self._load_data_files("statuses")
        elif operation == "save":
            if data_type == "decisions":
                self._save_decisions()
            elif data_type == "statuses":
                self._save_agent_statuses()
            else:
                self._save_decisions()
                self._save_agent_statuses()
        elif operation == "load_decisions":
            self._load_data_files("decisions")
        elif operation == "load_statuses":
            self._load_data_files("statuses")

    def _save_decisions(self) -> None:
        """Save decisions to file"""
        try:
            data = {
                decision_id: asdict(decision)
                for decision_id, decision in self.active_decisions.items()
            }
            with open(self.decisions_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving decisions: {e}")

    def _save_agent_statuses(self) -> None:
        """Save agent statuses to file"""
        try:
            data = {agent_id: asdict(agent) for agent_id, agent in self.agent_statuses.items()}
            with open(self.status_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving agent statuses: {e}")

    def _load_data_files(self, data_type: str) -> None:
        """Consolidated data loading"""
        try:
            if data_type == "decisions":
                if self.decisions_file.exists():
                    with open(self.decisions_file) as f:
                        data = json.load(f)

                    for decision_id, decision_data in data.items():
                        decision = SwarmDecision(**decision_data)
                        decision.decision_type = DecisionType(decision.decision_type)
                        self.active_decisions[decision_id] = decision
            elif data_type == "statuses":
                if self.status_file.exists():
                    with open(self.status_file) as f:
                        data = json.load(f)

                    for agent_id, agent_data in data.items():
                        agent = AgentStatus(**agent_data)
                        agent.role = AgentRole(agent.role)
                        self.agent_statuses[agent_id] = agent
        except Exception as e:
            logger.error(f"Error loading {data_type}: {e}")

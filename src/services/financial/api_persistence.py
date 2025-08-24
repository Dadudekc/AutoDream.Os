"""Persistence utilities for UnifiedFinancialAPI."""

import json
import logging
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from .models import AgentRegistration, CrossAgentRequest

logger = logging.getLogger(__name__)


class PersistenceManager:
    """Handles saving and loading API state to disk."""

    def __init__(self, agents_file: Path, requests_file: Path, performance_file: Path) -> None:
        self.agents_file = agents_file
        self.requests_file = requests_file
        self.performance_file = performance_file

    def save(
        self,
        registered_agents: Dict[str, AgentRegistration],
        request_history: List[CrossAgentRequest],
        performance_metrics: Dict[str, Dict[str, Any]],
    ) -> None:
        """Persist agents, requests, and performance metrics."""
        try:
            agents_data = {aid: asdict(agent) for aid, agent in registered_agents.items()}
            with open(self.agents_file, "w") as f:
                json.dump(agents_data, f, indent=2, default=str)

            requests_data = [asdict(req) for req in request_history]
            with open(self.requests_file, "w") as f:
                json.dump(requests_data, f, indent=2, default=str)

            with open(self.performance_file, "w") as f:
                json.dump(performance_metrics, f, indent=2, default=str)
            logger.info("Unified Financial API data saved successfully")
        except Exception as exc:  # pragma: no cover - disk failures
            logger.error("Error saving Unified Financial API data: %s", exc)

    def load(
        self,
        registered_agents: Dict[str, AgentRegistration],
        request_history: List[CrossAgentRequest],
        performance_metrics: Dict[str, Dict[str, Any]],
    ) -> None:
        """Load persisted data into provided containers."""
        try:
            if self.agents_file.exists():
                with open(self.agents_file, "r") as f:
                    agents_data = json.load(f)
                for agent_id, agent_dict in agents_data.items():
                    if "registration_time" in agent_dict:
                        agent_dict["registration_time"] = datetime.fromisoformat(
                            agent_dict["registration_time"]
                        )
                    if "last_heartbeat" in agent_dict:
                        agent_dict["last_heartbeat"] = datetime.fromisoformat(
                            agent_dict["last_heartbeat"]
                        )
                    registered_agents[agent_id] = AgentRegistration(**agent_dict)
                logger.info("Loaded %d registered agents", len(agents_data))

            if self.requests_file.exists():
                with open(self.requests_file, "r") as f:
                    requests_data = json.load(f)
                for request_dict in requests_data:
                    if "timestamp" in request_dict:
                        request_dict["timestamp"] = datetime.fromisoformat(
                            request_dict["timestamp"]
                        )
                    request_history.append(CrossAgentRequest(**request_dict))
                logger.info("Loaded %d request history items", len(requests_data))

            if self.performance_file.exists():
                with open(self.performance_file, "r") as f:
                    data = json.load(f)
                performance_metrics.update(data)
                logger.info(
                    "Loaded performance metrics for %d agents", len(performance_metrics)
                )
        except Exception as exc:  # pragma: no cover - disk failures
            logger.error("Error loading Unified Financial API data: %s", exc)

#!/usr/bin/env python3
"""
Core Coordinator Service - Agent Cellphone V2
============================================

Core coordination logic and agent management service.
Follows V2 standards: ≤ 200 LOC, SRP, OOP design, CLI interface.
"""

import json
import logging
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import argparse


@dataclass
class AgentStatus:
    """Agent status data structure."""

    agent_id: str
    status: str
    last_activity: Optional[datetime]
    coordination_count: int
    errors: List[str]
    captain_terms: int
    campaign_success: int
    voting_record: Dict[str, Any]


@dataclass
class CoordinationConfig:
    """Coordination configuration data structure."""

    election_mode: bool
    round_robin: bool
    campaign_duration: int
    voting_duration: int
    term_duration: int


class CoreCoordinatorService:
    """
    Core Coordinator Service - Single responsibility: Core coordination logic and agent management.

    This service manages:
    - Agent status tracking and management
    - Coordination cycle management
    - Service orchestration and integration
    - Configuration management
    """

    def __init__(self, config_path: str = "config"):
        """Initialize Core Coordinator Service."""
        self.config_path = Path(config_path)
        self.logger = self._setup_logging()
        self.agent_status: Dict[str, AgentStatus] = {}
        self.coordination_cycle = 0
        self.config = self._load_configuration()

        # Initialize agent status
        self._initialize_agent_status()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the service."""
        logger = logging.getLogger("CoreCoordinatorService")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _load_configuration(self) -> CoordinationConfig:
        """Load coordination configuration."""
        try:
            config_file = self.config_path / "coordination_config.json"
            if config_file.exists():
                with open(config_file, "r") as f:
                    config_data = json.load(f)
                    return CoordinationConfig(**config_data)
            else:
                # Default configuration
                return CoordinationConfig(
                    election_mode=False,
                    round_robin=False,
                    campaign_duration=300,
                    voting_duration=120,
                    term_duration=1800,
                )
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            return CoordinationConfig(
                election_mode=False,
                round_robin=False,
                campaign_duration=300,
                voting_duration=120,
                term_duration=1800,
            )

    def _initialize_agent_status(self):
        """Initialize agent status for all agents."""
        agent_roles = {
            "Agent-1": "Strategic Coordination & Knowledge Management",
            "Agent-2": "Task Breakdown & Resource Allocation",
            "Agent-3": "Data Analysis & Technical Implementation",
            "Agent-4": "Communication Protocols & Security",
            "Agent-5": "CAPTAIN Coordination & PyAutoGUI Leadership",
        }

        for agent_id in agent_roles.keys():
            self.agent_status[agent_id] = AgentStatus(
                agent_id=agent_id,
                status="standby",
                last_activity=None,
                coordination_count=0,
                errors=[],
                captain_terms=0,
                campaign_success=0,
                voting_record={},
            )

    def get_agent_status(self, agent_id: str) -> Optional[AgentStatus]:
        """Get status for a specific agent."""
        return self.agent_status.get(agent_id)

    def update_agent_status(
        self, agent_id: str, status: str, error: Optional[str] = None
    ):
        """Update agent status and activity."""
        if agent_id in self.agent_status:
            agent = self.agent_status[agent_id]
            agent.status = status
            agent.last_activity = datetime.now()
            agent.coordination_count += 1

            if error:
                agent.errors.append(error)

            self.logger.info(f"Updated {agent_id} status: {status}")

    def get_coordination_summary(self) -> Dict[str, Any]:
        """Get coordination system summary."""
        active_agents = sum(
            1 for agent in self.agent_status.values() if agent.status == "active"
        )
        total_errors = sum(len(agent.errors) for agent in self.agent_status.values())

        return {
            "total_agents": len(self.agent_status),
            "active_agents": active_agents,
            "standby_agents": len(self.agent_status) - active_agents,
            "total_errors": total_errors,
            "coordination_cycle": self.coordination_cycle,
            "election_mode": self.config.election_mode,
            "round_robin": self.config.round_robin,
        }

    def increment_coordination_cycle(self):
        """Increment coordination cycle counter."""
        self.coordination_cycle += 1
        self.logger.info(f"Coordination cycle incremented: {self.coordination_cycle}")

    def reset_agent_errors(self, agent_id: str):
        """Reset errors for a specific agent."""
        if agent_id in self.agent_status:
            self.agent_status[agent_id].errors.clear()
            self.logger.info(f"Reset errors for {agent_id}")

    def get_agent_performance_metrics(self, agent_id: str) -> Dict[str, Any]:
        """Get performance metrics for a specific agent."""
        agent = self.agent_status.get(agent_id)
        if not agent:
            return {}

        return {
            "agent_id": agent_id,
            "status": agent.status,
            "coordination_count": agent.coordination_count,
            "error_count": len(agent.errors),
            "captain_terms": agent.captain_terms,
            "campaign_success": agent.campaign_success,
            "last_activity": agent.last_activity.isoformat()
            if agent.last_activity
            else None,
        }


def main():
    """CLI interface for Core Coordinator Service."""
    parser = argparse.ArgumentParser(description="Core Coordinator Service CLI")
    parser.add_argument(
        "--status", action="store_true", help="Show coordination status"
    )
    parser.add_argument("--agent", type=str, help="Get status for specific agent")
    parser.add_argument(
        "--reset-errors", type=str, help="Reset errors for specific agent"
    )
    parser.add_argument(
        "--metrics", type=str, help="Get performance metrics for specific agent"
    )

    args = parser.parse_args()

    # Initialize service
    coordinator = CoreCoordinatorService()

    if args.status:
        summary = coordinator.get_coordination_summary()
        print("📊 Coordination Status Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")

    elif args.agent:
        status = coordinator.get_agent_status(args.agent)
        if status:
            print(f"🤖 Agent {args.agent} Status:")
            print(f"  Status: {status.status}")
            print(f"  Coordination Count: {status.coordination_count}")
            print(f"  Errors: {len(status.errors)}")
            print(f"  Last Activity: {status.last_activity}")
        else:
            print(f"❌ Agent {args.agent} not found")

    elif args.reset_errors:
        coordinator.reset_agent_errors(args.reset_errors)
        print(f"✅ Reset errors for {args.reset_errors}")

    elif args.metrics:
        metrics = coordinator.get_agent_performance_metrics(args.metrics)
        if metrics:
            print(f"📈 Performance Metrics for {args.metrics}:")
            for key, value in metrics.items():
                print(f"  {key}: {value}")
        else:
            print(f"❌ Agent {args.metrics} not found")

    else:
        print("🎖️ Core Coordinator Service - Use --help for available commands")


if __name__ == "__main__":
    main()

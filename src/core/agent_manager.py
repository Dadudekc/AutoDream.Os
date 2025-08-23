#!/usr/bin/env python3
"""
Agent Manager - V2 Core Agent Management System

This module manages agent lifecycle, status tracking, and capabilities.
Follows Single Responsibility Principle - only agent management.
Architecture: Single Responsibility Principle - agent management only
LOC: Target 200 lines (under 200 limit)
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Set
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import threading
import time

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent status states"""

    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    IDLE = "idle"
    MAINTENANCE = "maintenance"
    ERROR = "error"


class AgentCapability(Enum):
    """Agent capability types"""

    REFACTORING = "refactoring"
    TESTING = "testing"
    INTEGRATION = "integration"
    DOCUMENTATION = "documentation"
    COORDINATION = "coordination"
    SECURITY = "security"
    PERFORMANCE = "performance"


@dataclass
class AgentInfo:
    """Information about an agent"""

    agent_id: str
    name: str
    status: AgentStatus
    capabilities: List[AgentCapability]
    current_contract: Optional[str]
    last_heartbeat: str
    performance_score: float
    contracts_completed: int
    total_uptime: float
    resource_usage: Dict[str, Any]


@dataclass
class AgentMetrics:
    """Agent performance metrics"""

    contracts_completed: int
    average_completion_time: float
    success_rate: float
    last_activity: str
    total_uptime: float


class AgentManager:
    """
    Manages agent lifecycle, status tracking, and capabilities

    Responsibilities:
    - Agent registration and lifecycle management
    - Status tracking and monitoring
    - Capability management and assignment
    - Performance metrics and analytics
    """

    def __init__(self, agents_dir: str = "agent_workspaces"):
        self.agents_dir = Path(agents_dir)
        self.agents: Dict[str, AgentInfo] = {}
        self.capabilities: Dict[AgentCapability, Set[str]] = {
            cap: set() for cap in AgentCapability
        }
        self.performance_metrics: Dict[str, AgentMetrics] = {}
        self.logger = logging.getLogger(f"{__name__}.AgentManager")
        self.heartbeat_interval = 30  # seconds
        self.heartbeat_thread = None
        self.running = False

        # Ensure agents directory exists
        self.agents_dir.mkdir(exist_ok=True)

        # Load existing agents
        self._discover_existing_agents()

        # Start heartbeat monitoring
        self._start_heartbeat_monitoring()

    def _discover_existing_agents(self):
        """Discover existing agents in the agents directory"""
        try:
            for agent_dir in self.agents_dir.iterdir():
                if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                    agent_id = agent_dir.name
                    self._load_agent_info(agent_id, agent_dir)
        except Exception as e:
            self.logger.error(f"Failed to discover existing agents: {e}")

    def _load_agent_info(self, agent_id: str, agent_dir: Path):
        """Load information about an existing agent"""
        try:
            # Load agent config if it exists
            config_file = agent_dir / "agent_config.json"
            if config_file.exists():
                with open(config_file, "r") as f:
                    config_data = json.load(f)

                agent_info = AgentInfo(
                    agent_id=agent_id,
                    name=config_data.get("name", agent_id),
                    status=AgentStatus(config_data.get("status", "offline")),
                    capabilities=[
                        AgentCapability(cap)
                        for cap in config_data.get("capabilities", [])
                    ],
                    current_contract=config_data.get("current_contract"),
                    last_heartbeat=config_data.get(
                        "last_heartbeat", self._get_current_timestamp()
                    ),
                    performance_score=config_data.get("performance_score", 0.0),
                    contracts_completed=config_data.get("contracts_completed", 0),
                    total_uptime=config_data.get("total_uptime", 0.0),
                    resource_usage=config_data.get("resource_usage", {}),
                )

                self.agents[agent_id] = agent_info
                self._update_capability_index(agent_id, agent_info.capabilities)
                self.logger.info(f"Loaded existing agent: {agent_id}")

        except Exception as e:
            self.logger.error(f"Failed to load agent info for {agent_id}: {e}")

    def _update_capability_index(
        self, agent_id: str, capabilities: List[AgentCapability]
    ):
        """Update the capability index for an agent"""
        for capability in capabilities:
            self.capabilities[capability].add(agent_id)

    def register_agent(
        self, agent_id: str, name: str, capabilities: List[AgentCapability]
    ) -> bool:
        """Register a new agent"""
        try:
            if agent_id in self.agents:
                self.logger.warning(f"Agent {agent_id} already registered")
                return False

            # Create agent info
            agent_info = AgentInfo(
                agent_id=agent_id,
                name=name,
                status=AgentStatus.ONLINE,
                capabilities=capabilities,
                current_contract=None,
                last_heartbeat=self._get_current_timestamp(),
                performance_score=0.0,
                contracts_completed=0,
                total_uptime=0.0,
                resource_usage={},
            )

            # Add to tracking
            self.agents[agent_id] = agent_info
            self._update_capability_index(agent_id, capabilities)

            # Save agent config
            self._save_agent_config(agent_id, agent_info)

            self.logger.info(f"Registered agent: {agent_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to register agent {agent_id}: {e}")
            return False

    def update_agent_status(self, agent_id: str, status: AgentStatus) -> bool:
        """Update agent status"""
        try:
            if agent_id in self.agents:
                self.agents[agent_id].status = status
                self.agents[agent_id].last_heartbeat = self._get_current_timestamp()
                self._save_agent_config(agent_id, self.agents[agent_id])
                self.logger.info(f"Updated agent {agent_id} status to {status.value}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to update agent status: {e}")
            return False

    def get_agents_by_capability(self, capability: AgentCapability) -> List[AgentInfo]:
        """Get all agents with a specific capability"""
        agent_ids = self.capabilities.get(capability, set())
        return [
            self.agents[agent_id] for agent_id in agent_ids if agent_id in self.agents
        ]

    def get_available_agents(self) -> List[AgentInfo]:
        """Get all available (online/idle) agents"""
        return [
            agent
            for agent in self.agents.values()
            if agent.status in [AgentStatus.ONLINE, AgentStatus.IDLE]
        ]

    def assign_contract(self, agent_id: str, contract_id: str) -> bool:
        """Assign a contract to an agent"""
        try:
            if agent_id in self.agents:
                self.agents[agent_id].current_contract = contract_id
                self.agents[agent_id].status = AgentStatus.BUSY
                self.agents[agent_id].last_heartbeat = self._get_current_timestamp()
                self._save_agent_config(agent_id, self.agents[agent_id])
                self.logger.info(f"Assigned contract {contract_id} to agent {agent_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to assign contract: {e}")
            return False

    def complete_contract(
        self, agent_id: str, contract_id: str, success: bool = True
    ) -> bool:
        """Mark a contract as completed for an agent"""
        try:
            if (
                agent_id in self.agents
                and self.agents[agent_id].current_contract == contract_id
            ):
                agent = self.agents[agent_id]
                agent.current_contract = None
                agent.status = AgentStatus.IDLE
                agent.contracts_completed += 1
                agent.last_heartbeat = self._get_current_timestamp()

                # Update performance score
                if success:
                    agent.performance_score = min(100.0, agent.performance_score + 1.0)
                else:
                    agent.performance_score = max(0.0, agent.performance_score - 0.5)

                self._save_agent_config(agent_id, agent)
                self.logger.info(
                    f"Completed contract {contract_id} for agent {agent_id}"
                )
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to complete contract: {e}")
            return False

    def _start_heartbeat_monitoring(self):
        """Start heartbeat monitoring thread"""
        self.running = True
        self.heartbeat_thread = threading.Thread(
            target=self._heartbeat_monitoring_loop, daemon=True
        )
        self.heartbeat_thread.start()

    def _heartbeat_monitoring_loop(self):
        """Monitor agent heartbeats"""
        while self.running:
            try:
                current_time = datetime.now()
                for agent_id, agent in self.agents.items():
                    last_heartbeat = datetime.fromisoformat(agent.last_heartbeat)
                    if current_time - last_heartbeat > timedelta(
                        seconds=self.heartbeat_interval * 2
                    ):
                        # Agent is offline
                        if agent.status != AgentStatus.OFFLINE:
                            agent.status = AgentStatus.OFFLINE
                            self._save_agent_config(agent_id, agent)
                            self.logger.warning(f"Agent {agent_id} marked as offline")

                time.sleep(self.heartbeat_interval)
            except Exception as e:
                self.logger.error(f"Heartbeat monitoring error: {e}")
                time.sleep(self.heartbeat_interval)

    def _save_agent_config(self, agent_id: str, agent_info: AgentInfo):
        """Save agent configuration to file"""
        try:
            agent_dir = self.agents_dir / agent_id
            agent_dir.mkdir(exist_ok=True)

            config_file = agent_dir / "agent_config.json"
            config_data = asdict(agent_info)
            config_data["status"] = agent_info.status.value
            config_data["capabilities"] = [cap.value for cap in agent_info.capabilities]

            with open(config_file, "w") as f:
                json.dump(config_data, f, indent=2, default=str)

        except Exception as e:
            self.logger.error(f"Failed to save agent config for {agent_id}: {e}")

    def _get_current_timestamp(self) -> str:
        """Get current timestamp string"""
        return datetime.now().isoformat()

    def get_agent_summary(self) -> Dict[str, Any]:
        """Get summary of all agents"""
        try:
            total_agents = len(self.agents)
            online_agents = len(
                [a for a in self.agents.values() if a.status == AgentStatus.ONLINE]
            )
            busy_agents = len(
                [a for a in self.agents.values() if a.status == AgentStatus.BUSY]
            )

            return {
                "total_agents": total_agents,
                "online_agents": online_agents,
                "busy_agents": busy_agents,
                "agent_statuses": {
                    status.value: len(
                        [a for a in self.agents.values() if a.status == status]
                    )
                    for status in AgentStatus
                },
                "capability_distribution": {
                    cap.value: len(agent_ids)
                    for cap, agent_ids in self.capabilities.items()
                },
            }
        except Exception as e:
            self.logger.error(f"Failed to get agent summary: {e}")
            return {"error": str(e)}

    def run_smoke_test(self) -> bool:
        """Run basic functionality test for this instance"""
        try:
            # Test agent registration
            test_agent_id = "smoke_test_agent"
            success = self.register_agent(
                test_agent_id, "Smoke Test Agent", [AgentCapability.TESTING]
            )
            if not success:
                return False

            # Test status update
            success = self.update_agent_status(test_agent_id, AgentStatus.BUSY)
            if not success:
                return False

            # Test contract assignment
            success = self.assign_contract(test_agent_id, "test_contract")
            if not success:
                return False

            # Test contract completion
            success = self.complete_contract(test_agent_id, "test_contract", True)
            if not success:
                return False

            # Test capability search
            agents_with_testing = self.get_agents_by_capability(AgentCapability.TESTING)
            if len(agents_with_testing) == 0:
                return False

            # Test agent summary
            summary = self.get_agent_summary()
            if "total_agents" not in summary:
                return False

            # Cleanup test agent
            if test_agent_id in self.agents:
                del self.agents[test_agent_id]
                # Remove from capability index
                for cap in AgentCapability:
                    if test_agent_id in self.capabilities[cap]:
                        self.capabilities[cap].remove(test_agent_id)

            return True

        except Exception as e:
            self.logger.error(f"Smoke test failed: {e}")
            return False

    def shutdown(self):
        """Shutdown the agent manager"""
        self.running = False
        if self.heartbeat_thread:
            self.heartbeat_thread.join(timeout=5)


def run_smoke_test():
    """Run basic functionality test for AgentManager"""
    print("🧪 Running AgentManager Smoke Test...")

    try:
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            manager = AgentManager(temp_dir)

            # Test agent registration
            success = manager.register_agent(
                "test_agent", "Test Agent", [AgentCapability.TESTING]
            )
            assert success

            # Test status update
            success = manager.update_agent_status("test_agent", AgentStatus.BUSY)
            assert success

            # Test contract assignment
            success = manager.assign_contract("test_agent", "test_contract")
            assert success

            # Test contract completion
            success = manager.complete_contract("test_agent", "test_contract", True)
            assert success

            # Test capability search
            agents_with_testing = manager.get_agents_by_capability(
                AgentCapability.TESTING
            )
            assert len(agents_with_testing) == 1

            # Test agent summary
            summary = manager.get_agent_summary()
            assert "total_agents" in summary

            manager.shutdown()

        print("✅ AgentManager Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ AgentManager Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for AgentManager testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Agent Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument(
        "--register",
        nargs=3,
        metavar=("ID", "NAME", "CAPABILITIES"),
        help="Register agent",
    )
    parser.add_argument(
        "--status", nargs=2, metavar=("ID", "STATUS"), help="Update agent status"
    )
    parser.add_argument(
        "--assign", nargs=2, metavar=("ID", "CONTRACT"), help="Assign contract"
    )
    parser.add_argument(
        "--complete",
        nargs=3,
        metavar=("ID", "CONTRACT", "SUCCESS"),
        help="Complete contract",
    )
    parser.add_argument("--capability", help="Find agents by capability")
    parser.add_argument("--summary", action="store_true", help="Show agent summary")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    manager = AgentManager()

    if args.register:
        agent_id, name, capabilities_str = args.register
        capabilities = [
            AgentCapability(cap.strip()) for cap in capabilities_str.split(",")
        ]
        success = manager.register_agent(agent_id, name, capabilities)
        print(f"Agent registration: {'✅ Success' if success else '❌ Failed'}")
    elif args.status:
        agent_id, status = args.status
        try:
            agent_status = AgentStatus(status)
            success = manager.update_agent_status(agent_id, agent_status)
            print(f"Status update: {'✅ Success' if success else '❌ Failed'}")
        except ValueError:
            print(f"❌ Invalid status: {status}")
            print(f"Valid statuses: {[s.value for s in AgentStatus]}")
    elif args.assign:
        agent_id, contract = args.assign
        success = manager.assign_contract(agent_id, contract)
        print(f"Contract assignment: {'✅ Success' if success else '❌ Failed'}")
    elif args.complete:
        agent_id, contract, success_str = args.complete
        success = manager.complete_contract(
            agent_id, contract, success_str.lower() == "true"
        )
        print(f"Contract completion: {'✅ Success' if success else '❌ Failed'}")
    elif args.capability:
        try:
            capability = AgentCapability(args.capability)
            agents = manager.get_agents_by_capability(capability)
            print(f"Agents with capability {capability.value}:")
            for agent in agents:
                print(f"  {agent.agent_id}: {agent.status.value}")
        except ValueError:
            print(f"❌ Invalid capability: {args.capability}")
            print(f"Valid capabilities: {[c.value for c in AgentCapability]}")
    elif args.summary:
        summary = manager.get_agent_summary()
        print("Agent Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    else:
        parser.print_help()

    manager.shutdown()


if __name__ == "__main__":
    main()

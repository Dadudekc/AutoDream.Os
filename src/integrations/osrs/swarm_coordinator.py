#!/usr/bin/env python3
"""OSRS Swarm Coordinator - Manages coordination between 8 OSRS agents

V2 COMPLIANT: Refactored to ≤400 lines by extracting:
- Strategic planning → swarm_strategic_planner.py
"""

import json
import logging
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from ..agents.osrs_agent_core import AgentRole, AgentStatus, OSRS_Agent_Core
from .swarm_strategic_planner import OSRSStrategicPlanner


@dataclass
class SwarmMessage:
    """Message structure for swarm communication."""

    message_id: str
    from_agent: str
    to_agent: str | None  # None for broadcast
    message_type: str
    content: dict[str, Any]
    timestamp: datetime
    priority: str = "normal"  # normal, high, urgent


@dataclass
class SwarmActivity:
    """Coordinated swarm activity."""

    activity_id: str
    activity_type: str
    description: str
    participating_agents: list[str]
    start_time: datetime
    end_time: datetime | None
    status: str  # planned, active, completed, cancelled
    requirements: dict[str, Any]


class OSRS_Swarm_Coordinator:
    """OSRS Swarm Coordinator - Manages coordination between 8 OSRS agents"""

    def __init__(self):
        """Initialize the swarm coordinator."""
        self.agents: dict[str, OSRS_Agent_Core] = {}
        self.message_queues: dict[str, list[SwarmMessage]] = {}
        self.coordination_activities: dict[str, SwarmActivity] = {}
        self.is_running = False

        # Logging
        self.logger = logging.getLogger("OSRS_Swarm_Coordinator")
        self.setup_logging()

        # Data persistence
        self.data_dir = Path("data/coordination")
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info("OSRS Swarm Coordinator initialized")

    def setup_logging(self):
        """Setup coordinator logging."""
        log_file = self.data_dir / "swarm_coordinator.log"
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def register_agent(self, agent: OSRS_Agent_Core):
        """Register an agent with the swarm coordinator."""
        agent_id = agent.agent_id
        self.agents[agent_id] = agent
        self.message_queues[agent_id] = []
        self.logger.info(f"Registered agent: {agent_id} with role {agent.role.value}")

    def start_coordination(self):
        """Start the swarm coordination system."""
        self.logger.info("Starting OSRS swarm coordination")
        self.is_running = True
        coordination_thread = threading.Thread(target=self.coordination_loop, daemon=True)
        coordination_thread.start()
        for agent in self.agents.values():
            agent_thread = threading.Thread(target=agent.start_autonomous_operation, daemon=True)
            agent_thread.start()
        self.logger.info("OSRS swarm coordination started")

    def coordination_loop(self):
        """Main coordination loop."""
        while self.is_running:
            try:
                self.process_coordination_activities()
                self.manage_resource_sharing()
                self.coordinate_strategic_activities()
                self.monitor_agent_health()
                self.update_coordination_status()
                time.sleep(5)
            except Exception as e:
                self.logger.error(f"Error in coordination loop: {e}")
                time.sleep(10)

    def process_coordination_activities(self):
        """Process active coordination activities."""
        for activity_id, activity in self.coordination_activities.items():
            if activity.status == "active":
                self.execute_coordination_activity(activity)
            elif activity.status == "planned":
                self.check_activity_readiness(activity)

    def execute_coordination_activity(self, activity: SwarmActivity):
        """Execute a coordination activity."""
        try:
            self.logger.info(f"Executing coordination activity: {activity.activity_type}")
            for agent_id in activity.participating_agents:
                if agent_id in self.agents:
                    message = SwarmMessage(
                        message_id=f"activity_{activity.activity_id}_{agent_id}",
                        from_agent="Swarm_Coordinator",
                        to_agent=agent_id,
                        message_type="activity_instruction",
                        content={
                            "activity_id": activity.activity_id,
                            "activity_type": activity.activity_type,
                            "description": activity.description,
                            "requirements": activity.requirements,
                        },
                        timestamp=datetime.now(),
                        priority="high",
                    )
                    self.send_message(message)
        except Exception as e:
            self.logger.error(f"Error executing coordination activity: {e}")

    def check_activity_readiness(self, activity: SwarmActivity):
        """Check if an activity is ready to start."""
        try:
            ready_agents = []
            for agent_id in activity.participating_agents:
                if agent_id in self.agents:
                    agent = self.agents[agent_id]
                    if agent.status == AgentStatus.ACTIVE:
                        ready_agents.append(agent_id)
            if len(ready_agents) == len(activity.participating_agents):
                activity.status = "active"
                activity.start_time = datetime.now()
                self.logger.info(f"Starting coordination activity: {activity.activity_type}")
        except Exception as e:
            self.logger.error(f"Error checking activity readiness: {e}")

    def manage_resource_sharing(self):
        """Manage resource sharing between agents."""
        try:
            # Collect resource requests from all agents
            resource_requests = []
            for agent_id, agent in self.agents.items():
                # Check agent's message queue for resource requests
                messages = self.message_queues.get(agent_id, [])
                for message in messages:
                    if message.message_type == "resource_request":
                        resource_requests.append(
                            {
                                "requesting_agent": agent_id,
                                "requested_item": message.content.get("item"),
                                "priority": message.priority,
                            }
                        )

            # Process resource requests
            for request in resource_requests:
                self.process_resource_request(request)

        except Exception as e:
            self.logger.error(f"Error managing resource sharing: {e}")

    def process_resource_request(self, request: dict[str, Any]):
        """Process a resource request."""
        try:
            requesting_agent = request["requesting_agent"]
            requested_item = request["requested_item"]

            # Find agents that might have the requested resource
            potential_suppliers = []
            for agent_id, agent in self.agents.items():
                if agent_id != requesting_agent and agent.status == AgentStatus.ACTIVE:
                    # Check if agent has the requested resource
                    if agent.game_state and requested_item in agent.game_state.inventory_items:
                        potential_suppliers.append(agent_id)

            # Send resource request to potential suppliers
            for supplier_id in potential_suppliers:
                message = SwarmMessage(
                    message_id=f"resource_request_{requesting_agent}_{supplier_id}",
                    from_agent="Swarm_Coordinator",
                    to_agent=supplier_id,
                    message_type="resource_request",
                    content={
                        "requesting_agent": requesting_agent,
                        "requested_item": requested_item,
                        "priority": request["priority"],
                    },
                    timestamp=datetime.now(),
                    priority=request["priority"],
                )
                self.send_message(message)

        except Exception as e:
            self.logger.error(f"Error processing resource request: {e}")

    def coordinate_strategic_activities(self):
        """Coordinate strategic activities across the swarm."""
        try:
            strategic_activities = OSRSStrategicPlanner.plan_strategic_activities(self)

            for activity in strategic_activities:
                if activity.activity_id not in self.coordination_activities:
                    self.coordination_activities[activity.activity_id] = activity
                    self.logger.info(f"Planned strategic activity: {activity.activity_type}")

        except Exception as e:
            self.logger.error(f"Error coordinating strategic activities: {e}")

    def monitor_agent_health(self):
        """Monitor the health and status of all agents."""
        try:
            for agent_id, agent in self.agents.items():
                # Check if agent is responding
                if agent.status == AgentStatus.ERROR:
                    self.logger.warning(f"Agent {agent_id} is in error state")
                    # Attempt to restart the agent
                    self.restart_agent(agent_id)
                elif agent.status == AgentStatus.SHUTDOWN:
                    self.logger.warning(f"Agent {agent_id} has shutdown")
                    # Remove from active agents
                    if agent_id in self.agents:
                        del self.agents[agent_id]

        except Exception as e:
            self.logger.error(f"Error monitoring agent health: {e}")

    def restart_agent(self, agent_id: str):
        """Restart a failed agent."""
        try:
            self.logger.info(f"Attempting to restart agent {agent_id}")

            # In a real implementation, this would restart the agent process
            # For now, we'll just log the attempt
            self.logger.info(f"Agent {agent_id} restart attempted")

        except Exception as e:
            self.logger.error(f"Error restarting agent {agent_id}: {e}")

    def send_message(self, message: SwarmMessage):
        """
        @brief Send a message to an agent or broadcast to all agents.

        @param message Message to send
        """
        try:
            if message.to_agent:
                # Send to specific agent
                if message.to_agent in self.message_queues:
                    self.message_queues[message.to_agent].append(message)
                    self.logger.debug(f"Sent message to {message.to_agent}: {message.message_type}")
            else:
                # Broadcast to all agents
                for agent_id in self.message_queues:
                    self.message_queues[agent_id].append(message)
                self.logger.debug(f"Broadcast message: {message.message_type}")

        except Exception as e:
            self.logger.error(f"Error sending message: {e}")

    def update_coordination_status(self):
        """Update coordination status and save to persistent storage."""
        try:
            status_data = {
                "coordinator_status": "active" if self.is_running else "inactive",
                "active_agents": len(self.agents),
                "coordination_activities": len(self.coordination_activities),
                "active_activities": len(
                    [a for a in self.coordination_activities.values() if a.status == "active"]
                ),
                "last_update": datetime.now().isoformat(),
                "agents": {
                    agent_id: {
                        "role": agent.role.value,
                        "status": agent.status.value,
                        "current_activity": agent.current_activity,
                    }
                    for agent_id, agent in self.agents.items()
                },
            }

            status_file = self.data_dir / "coordination_status.json"
            with open(status_file, "w") as f:
                json.dump(status_data, f, indent=2, default=str)

        except Exception as e:
            self.logger.error(f"Error updating coordination status: {e}")

    def shutdown(self):
        """Shutdown the swarm coordinator gracefully."""
        self.logger.info("Shutting down OSRS swarm coordinator")
        self.is_running = False

        # Shutdown all agents
        for agent in self.agents.values():
            agent.shutdown()

        # Save final status
        self.update_coordination_status()

        self.logger.info("OSRS swarm coordinator shutdown complete")


def create_swarm_coordinator() -> OSRS_Swarm_Coordinator:
    """
    @brief Factory function for creating swarm coordinator.

    @return Initialized swarm coordinator
    """
    return OSRS_Swarm_Coordinator()


if __name__ == "__main__":
    # Example usage
    coordinator = create_swarm_coordinator()

    try:
        coordinator.start_coordination()

        # Keep running until interrupted
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        coordinator.shutdown()

#!/usr/bin/env python3
"""Swarm Agent Management System"""

import logging
from datetime import datetime

from .swarm_communication_enums import SwarmAgent, SwarmAgentStatus, SwarmCommunicationMetrics

logger = logging.getLogger(__name__)


class SwarmAgentManager:
    """Manages swarm agents and their states"""

    def __init__(self):
        self.agents: dict[str, SwarmAgent] = {}
        self.metrics = SwarmCommunicationMetrics()
        logger.info("Swarm Agent Manager initialized")

    def initialize_swarm_agents(self) -> None:
        """Initialize all swarm agents with their specialties"""
        swarm_agents = [
            ("Agent-1", "Integration & Core Systems Specialist"),
            ("Agent-2", "Architecture & Design Specialist"),
            ("Agent-3", "Infrastructure & DevOps Specialist"),
            ("Agent-4", "Quality Assurance Specialist (CAPTAIN)"),
            ("Agent-5", "Business Intelligence Specialist"),
            ("Agent-6", "Communication Specialist"),
            ("Agent-7", "Web Development Specialist"),
            ("Agent-8", "Operations Specialist"),
            ("Captain Agent-4", "Strategic Oversight & Final Approval"),
        ]

        for agent_id, specialty in swarm_agents:
            capabilities = self._get_agent_capabilities(agent_id, specialty)
            self.agents[agent_id] = SwarmAgent(
                agent_id=agent_id,
                specialty=specialty,
                status=SwarmAgentStatus.ACTIVE,
                capabilities=capabilities,
            )

        self.metrics.active_agents = len(self.agents)
        logger.info(f"Initialized {len(self.agents)} swarm agents")

    def _get_agent_capabilities(self, agent_id: str, specialty: str) -> set[str]:
        """Get capabilities for a specific agent based on their specialty"""
        base_capabilities = {"communication", "coordination", "reporting"}

        specialty_capabilities = {
            "Integration & Core Systems Specialist": {
                "integration",
                "core_systems",
                "system_architecture",
            },
            "Architecture & Design Specialist": {
                "architecture",
                "design_patterns",
                "system_design",
            },
            "Infrastructure & DevOps Specialist": {
                "infrastructure",
                "devops",
                "deployment",
                "monitoring",
            },
            "Quality Assurance Specialist (CAPTAIN)": {
                "quality_assurance",
                "testing",
                "validation",
                "oversight",
            },
            "Business Intelligence Specialist": {
                "analytics",
                "data_processing",
                "reporting",
                "metrics",
            },
            "Communication Specialist": {"communication", "messaging", "coordination", "routing"},
            "Web Development Specialist": {"web_development", "ui_ux", "frontend", "backend"},
            "Operations Specialist": {"operations", "coordination", "monitoring", "management"},
            "Strategic Oversight & Final Approval": {
                "strategic_oversight",
                "final_approval",
                "decision_making",
            },
        }

        capabilities = base_capabilities.copy()
        capabilities.update(specialty_capabilities.get(specialty, set()))
        return capabilities

    def get_agent(self, agent_id: str) -> SwarmAgent | None:
        """Get an agent by ID"""
        return self.agents.get(agent_id)

    def get_agents_by_status(self, status: SwarmAgentStatus) -> list[SwarmAgent]:
        """Get all agents with a specific status"""
        return [agent for agent in self.agents.values() if agent.status == status]

    def get_active_agents(self) -> list[SwarmAgent]:
        """Get all active agents"""
        return self.get_agents_by_status(SwarmAgentStatus.ACTIVE)

    def update_agent_status(self, agent_id: str, status: SwarmAgentStatus) -> bool:
        """Update an agent's status"""
        if agent_id in self.agents:
            self.agents[agent_id].status = status
            self.agents[agent_id].last_activity = datetime.now()
            logger.info(f"Updated agent {agent_id} status to {status.value}")
            return True
        return False

    def assign_mission(self, agent_id: str, mission: str) -> bool:
        """Assign a mission to an agent"""
        if agent_id in self.agents:
            self.agents[agent_id].current_mission = mission
            self.agents[agent_id].last_activity = datetime.now()
            logger.info(f"Assigned mission '{mission}' to agent {agent_id}")
            return True
        return False

    def update_performance_metrics(self, agent_id: str, metrics: dict[str, any]) -> bool:
        """Update performance metrics for an agent"""
        if agent_id in self.agents:
            self.agents[agent_id].performance_metrics.update(metrics)
            self.agents[agent_id].last_activity = datetime.now()
            logger.info(f"Updated performance metrics for agent {agent_id}")
            return True
        return False

    def get_agent_summary(self) -> dict[str, any]:
        """Get a summary of all agents"""
        return {
            "total_agents": len(self.agents),
            "active_agents": len(self.get_active_agents()),
            "agents_by_status": {
                status.value: len(self.get_agents_by_status(status)) for status in SwarmAgentStatus
            },
            "agents_with_missions": len(
                [agent for agent in self.agents.values() if agent.current_mission is not None]
            ),
        }

    def get_metrics(self) -> SwarmCommunicationMetrics:
        """Get current metrics"""
        self.metrics.active_agents = len(self.get_active_agents())
        self.metrics.last_updated = datetime.now()
        return self.metrics


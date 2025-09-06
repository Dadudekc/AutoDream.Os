"""
Strategic Oversight Engine Core Metrics - KISS Simplified
========================================================

Metrics management functionality for strategic oversight operations.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined metrics operations.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

import logging
from typing import Dict, List, Optional
from .models import AgentPerformanceMetrics, SwarmCoordinationStatus


class StrategicOversightEngineCoreMetrics:
    """Metrics management for strategic oversight engine."""

    def __init__(
        self,
        agent_metrics: Dict[str, AgentPerformanceMetrics],
        coordination_status: Dict[str, SwarmCoordinationStatus],
        logger: logging.Logger,
    ):
        """Initialize metrics management."""
        self.agent_metrics = agent_metrics
        self.coordination_status = coordination_status
        self.logger = logger

    def add_agent_metrics(self, metrics: AgentPerformanceMetrics) -> bool:
        """Add agent performance metrics - simplified."""
        try:
            self.agent_metrics[metrics.agent_id] = metrics
            self.logger.info(f"Added agent performance metrics: {metrics.agent_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add agent performance metrics: {e}")
            return False

    def get_agent_metrics(self, agent_id: str) -> Optional[AgentPerformanceMetrics]:
        """Get agent performance metrics by agent ID - simplified."""
        try:
            return self.agent_metrics.get(agent_id)
        except Exception as e:
            self.logger.error(f"Failed to get agent performance metrics: {e}")
            return None

    def get_all_agent_metrics(self) -> List[AgentPerformanceMetrics]:
        """Get all agent performance metrics - simplified."""
        try:
            return list(self.agent_metrics.values())
        except Exception as e:
            self.logger.error(f"Failed to get all agent performance metrics: {e}")
            return []

    def add_coordination_status(self, status: SwarmCoordinationStatus) -> bool:
        """Add swarm coordination status - simplified."""
        try:
            self.coordination_status[status.status_id] = status
            self.logger.info(f"Added swarm coordination status: {status.status_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add swarm coordination status: {e}")
            return False

    def get_coordination_status(
        self, status_id: str
    ) -> Optional[SwarmCoordinationStatus]:
        """Get swarm coordination status by ID - simplified."""
        try:
            return self.coordination_status.get(status_id)
        except Exception as e:
            self.logger.error(f"Failed to get swarm coordination status: {e}")
            return None

    def get_latest_coordination_status(self) -> Optional[SwarmCoordinationStatus]:
        """Get latest swarm coordination status - simplified."""
        try:
            if not self.coordination_status:
                return None

            # Get the most recent status by creation time
            latest_status = max(
                self.coordination_status.values(), key=lambda x: x.created_at
            )
            return latest_status
        except Exception as e:
            self.logger.error(f"Failed to get latest coordination status: {e}")
            return None

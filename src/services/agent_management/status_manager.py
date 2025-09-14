"""
Agent Status Manager
====================

Manages agent status tracking and monitoring.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class AgentStatus:
    """Represents the status of an agent."""
    agent_id: str
    status: str = "unknown"
    last_updated: datetime = field(default_factory=datetime.now)
    current_mission: Optional[str] = None
    performance_metrics: Dict[str, float] = field(default_factory=dict)


class AgentStatusManager:
    """Manages agent status tracking and monitoring."""
    
    def __init__(self):
        """Initialize the status manager."""
        self.logger = logging.getLogger(__name__)
        self.agent_statuses: Dict[str, AgentStatus] = {}
    
    def update_status(self, agent_id: str, status: str, mission: Optional[str] = None) -> bool:
        """Update agent status."""
        try:
            if agent_id not in self.agent_statuses:
                self.agent_statuses[agent_id] = AgentStatus(agent_id=agent_id)
            
            self.agent_statuses[agent_id].status = status
            self.agent_statuses[agent_id].last_updated = datetime.now()
            if mission:
                self.agent_statuses[agent_id].current_mission = mission
            
            self.logger.info(f"Updated status for agent {agent_id}: {status}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update status for agent {agent_id}: {e}")
            return False
    
    def get_status(self, agent_id: str) -> Optional[AgentStatus]:
        """Get current status of an agent."""
        return self.agent_statuses.get(agent_id)
    
    def get_all_statuses(self) -> Dict[str, AgentStatus]:
        """Get statuses of all agents."""
        return self.agent_statuses.copy()
    
    def update_metrics(self, agent_id: str, metrics: Dict[str, float]) -> bool:
        """Update performance metrics for an agent."""
        try:
            if agent_id not in self.agent_statuses:
                self.agent_statuses[agent_id] = AgentStatus(agent_id=agent_id)
            
            self.agent_statuses[agent_id].performance_metrics.update(metrics)
            self.agent_statuses[agent_id].last_updated = datetime.now()
            
            self.logger.info(f"Updated metrics for agent {agent_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update metrics for agent {agent_id}: {e}")
            return False
    
    def get_agents_by_status(self, status: str) -> List[str]:
        """Get all agents with a specific status."""
        return [
            agent_id for agent_id, agent_status in self.agent_statuses.items()
            if agent_status.status == status
        ]

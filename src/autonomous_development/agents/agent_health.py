#!/usr/bin/env python3
"""
Agent Health Monitoring - Agent Cellphone V2
============================================

Handles agent health monitoring and status tracking.
Follows V2 standards: SRP, clean separation of concerns.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List

from .agent_models import AgentInfo


class AgentHealthMonitor:
    """Handles agent health monitoring and status tracking"""
    
    def __init__(self):
        """Initialize health monitor"""
        self.logger = logging.getLogger(__name__)
        self.agent_heartbeats: Dict[str, datetime] = {}
        self.agent_workloads: Dict[str, int] = {}
        self.health_threshold = timedelta(minutes=5)  # 5 minute timeout
    
    def update_heartbeat(self, agent_id: str) -> None:
        """Update agent heartbeat timestamp"""
        self.agent_heartbeats[agent_id] = datetime.now()
        self.logger.debug(f"Updated heartbeat for agent {agent_id}")
    
    def update_workload(self, agent_id: str, task_count: int) -> None:
        """Update agent workload count"""
        self.agent_workloads[agent_id] = task_count
        self.logger.debug(f"Updated workload for agent {agent_id}: {task_count} tasks")
    
    def check_agent_health(self, agents: Dict[str, AgentInfo]) -> Dict[str, bool]:
        """Check health status of all agents
        
        Returns:
            Dict mapping agent_id to health status (True = healthy, False = unhealthy)
        """
        health_status = {}
        current_time = datetime.now()
        
        for agent_id, agent in agents.items():
            if not agent.is_active:
                health_status[agent_id] = True  # Inactive agents are considered healthy
                continue
                
            last_heartbeat = self.agent_heartbeats.get(agent_id)
            if not last_heartbeat:
                health_status[agent_id] = False
                self.logger.warning(f"Agent {agent_id} has no heartbeat record")
                continue
                
            time_since_heartbeat = current_time - last_heartbeat
            is_healthy = time_since_heartbeat <= self.health_threshold
            
            if not is_healthy:
                self.logger.warning(f"Agent {agent_id} heartbeat expired: {time_since_heartbeat}")
            
            health_status[agent_id] = is_healthy
        
        return health_status
    
    def get_agent_workloads(self) -> Dict[str, int]:
        """Get current workload for all agents"""
        return self.agent_workloads.copy()
    
    def get_heartbeat_times(self) -> Dict[str, datetime]:
        """Get last heartbeat times for all agents"""
        return self.agent_heartbeats.copy()
    
    def clear_agent_data(self, agent_id: str) -> None:
        """Clear health data for a specific agent"""
        self.agent_heartbeats.pop(agent_id, None)
        self.agent_workloads.pop(agent_id, None)
        self.logger.debug(f"Cleared health data for agent {agent_id}")
    
    def clear_all_data(self) -> None:
        """Clear all health monitoring data"""
        self.agent_heartbeats.clear()
        self.agent_workloads.clear()
        self.logger.debug("Cleared all health monitoring data")

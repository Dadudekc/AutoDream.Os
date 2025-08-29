#!/usr/bin/env python3
"""
Agent Task Management - Agent Cellphone V2
==========================================

Handles agent task assignment and workload management.
Follows V2 standards: SRP, clean separation of concerns.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

from .agent_models import AgentInfo
from .agent_health import AgentHealthMonitor


class AgentTaskManager:
    """Handles agent task assignment and workload management"""
    
    def __init__(self, health_monitor: AgentHealthMonitor):
        """Initialize task manager
        
        Args:
            health_monitor: Health monitor instance for tracking agent status
        """
        self.health_monitor = health_monitor
        self.logger = logging.getLogger(__name__)
    
    def assign_task_to_agent(self, task_id: str, agent_id: str, agents: Dict[str, AgentInfo]) -> bool:
        """Assign a task to a specific agent
        
        Args:
            task_id: ID of the task to assign
            agent_id: ID of the agent to assign the task to
            agents: Dictionary of available agents
            
        Returns:
            bool: True if assignment was successful, False otherwise
        """
        if agent_id not in agents:
            self.logger.error(f"Agent {agent_id} not found")
            return False
            
        agent = agents[agent_id]
        if not agent.is_active:
            self.logger.error(f"Agent {agent_id} is not active")
            return False
            
        current_workload = len(agent.current_tasks)
        if current_workload >= agent.max_concurrent_tasks:
            self.logger.error(f"Agent {agent_id} at max capacity: {current_workload}/{agent.max_concurrent_tasks}")
            return False
            
        # Add task to agent
        agent.current_tasks.append(task_id)
        
        # Update health monitor
        self.health_monitor.update_workload(agent_id, len(agent.current_tasks))
        
        self.logger.info(f"Assigned task {task_id} to agent {agent_id}")
        return True
    
    def remove_task_from_agent(self, task_id: str, agent_id: str, agents: Dict[str, AgentInfo]) -> bool:
        """Remove a task from a specific agent
        
        Args:
            task_id: ID of the task to remove
            agent_id: ID of the agent to remove the task from
            agents: Dictionary of available agents
            
        Returns:
            bool: True if removal was successful, False otherwise
        """
        if agent_id not in agents:
            self.logger.error(f"Agent {agent_id} not found")
            return False
            
        agent = agents[agent_id]
        if task_id in agent.current_tasks:
            agent.current_tasks.remove(task_id)
            
            # Update health monitor
            self.health_monitor.update_workload(agent_id, len(agent.current_tasks))
            
            self.logger.info(f"Removed task {task_id} from agent {agent_id}")
            return True
        else:
            self.logger.warning(f"Task {task_id} not found in agent {agent_id}")
            return False
    
    def get_agent_workload(self, agent_id: str, agents: Dict[str, AgentInfo]) -> int:
        """Get current workload for a specific agent"""
        if agent_id in agents:
            return len(agents[agent_id].current_tasks)
        return 0
    
    def get_available_agents(self, agents: Dict[str, AgentInfo]) -> List[str]:
        """Get list of agents that can accept new tasks"""
        available = []
        for agent_id, agent in agents.items():
            if (agent.is_active and 
                len(agent.current_tasks) < agent.max_concurrent_tasks):
                available.append(agent_id)
        return available
    
    def get_overloaded_agents(self, agents: Dict[str, AgentInfo]) -> List[str]:
        """Get list of agents that are at or over capacity"""
        overloaded = []
        for agent_id, agent in agents.items():
            if len(agent.current_tasks) >= agent.max_concurrent_tasks:
                overloaded.append(agent_id)
        return overloaded

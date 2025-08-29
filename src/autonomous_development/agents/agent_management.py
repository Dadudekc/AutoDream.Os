#!/usr/bin/env python3
"""
Agent Management - Agent Cellphone V2
====================================

Main agent management orchestrator.
Follows V2 standards: SRP, OOP principles, BaseManager inheritance.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Callable

from src.core.enums import AgentRole
from src.core.base_manager import BaseManager
from .agent_models import AgentInfo, AgentStats
from .agent_health import AgentHealthMonitor
from .agent_persistence import AgentPersistenceHandler
from .agent_tasks import AgentTaskManager


class AgentManager(BaseManager):
    """
    Main agent management orchestrator
    
    Coordinates agent registration, health monitoring, task management,
    and persistence through specialized modules.
    """
    
    def __init__(self, data_handler: Optional[Callable[[str], None]] = None):
        """Initialize agent manager with modular components

        Args:
            data_handler: Optional callable or object with a ``write`` method
                used to persist serialized agent data. If ``None`` persistence
                will be skipped.
        """
        super().__init__(
            manager_id="agent_manager",
            name="Agent Manager",
            description="Manages agent registration, unregistration, and basic operations"
        )
        
        # Initialize modular components
        self.health_monitor = AgentHealthMonitor()
        self.persistence_handler = AgentPersistenceHandler(data_handler)
        self.task_manager = AgentTaskManager(self.health_monitor)
        
        # Agent storage
        self.agents: Dict[str, AgentInfo] = {}
        
        # Management tracking
        self.management_stats = AgentStats()
        
        # Initialize with sample agents
        self._initialize_sample_agents()
        
        self.logger.info("Agent Manager initialized with modular architecture")
    
    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize agent management system"""
        try:
            self.logger.info("Starting Agent Manager...")
            
            # Clear agent data
            self.agents.clear()
            self.health_monitor.clear_all_data()
            
            # Reset stats
            self.management_stats = AgentStats()
            
            # Initialize sample agents
            self._initialize_sample_agents()
            
            self.logger.info("Agent Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Agent Manager: {e}")
            return False
    
    def _on_stop(self) -> bool:
        """Cleanup agent management system"""
        try:
            self.logger.info("Stopping Agent Manager...")
            
            # Save final agent data
            self._save_agent_data()
            
            # Clear all data
            self.agents.clear()
            self.health_monitor.clear_all_data()
            
            self.logger.info("Agent Manager stopped successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop Agent Manager: {e}")
            return False
    
    def _on_health_check(self) -> bool:
        """Perform health check on agent management system"""
        try:
            # Check agent health
            health_status = self.health_monitor.check_agent_health(self.agents)
            
            # Update active agent count
            active_count = sum(1 for status in health_status.values() if status)
            self.management_stats.active_agents = active_count
            
            # Log health status
            unhealthy_count = len(health_status) - active_count
            if unhealthy_count > 0:
                self.logger.warning(f"Found {unhealthy_count} unhealthy agents")
            
            return active_count > 0  # Consider healthy if at least one agent is active
            
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
    
    # ============================================================================
    # Public Agent Management Methods
    # ============================================================================
    
    def register_agent(self, agent_id: str, name: str, role: AgentRole, 
                      skills: List[str], max_concurrent_tasks: int = 3) -> bool:
        """Register a new agent"""
        try:
            if agent_id in self.agents:
                self.logger.warning(f"Agent {agent_id} already registered")
                return False
            
            agent = AgentInfo(
                agent_id=agent_id,
                name=name,
                role=role,
                skills=skills,
                max_concurrent_tasks=max_concurrent_tasks
            )
            
            self.agents[agent_id] = agent
            self.health_monitor.update_heartbeat(agent_id)
            self.health_monitor.update_workload(agent_id, 0)
            
            self.management_stats.total_agents_registered += 1
            self.management_stats.active_agents += 1
            
            self.logger.info(f"Registered agent {agent_id} ({name})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register agent {agent_id}: {e}")
            return False
    
    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an existing agent"""
        try:
            if agent_id not in self.agents:
                self.logger.warning(f"Agent {agent_id} not found")
                return False
            
            agent = self.agents[agent_id]
            if agent.is_active:
                self.management_stats.active_agents -= 1
            
            # Clear health data
            self.health_monitor.clear_agent_data(agent_id)
            
            # Remove agent
            del self.agents[agent_id]
            
            self.logger.info(f"Unregistered agent {agent_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unregister agent {agent_id}: {e}")
            return False
    
    def update_agent_heartbeat(self, agent_id: str) -> bool:
        """Update agent heartbeat"""
        try:
            if agent_id not in self.agents:
                self.logger.warning(f"Agent {agent_id} not found")
                return False
            
            self.health_monitor.update_heartbeat(agent_id)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update heartbeat for agent {agent_id}: {e}")
            return False
    
    def assign_task_to_agent(self, task_id: str, agent_id: str) -> bool:
        """Assign a task to an agent"""
        return self.task_manager.assign_task_to_agent(task_id, agent_id, self.agents)
    
    def remove_task_from_agent(self, task_id: str, agent_id: str) -> bool:
        """Remove a task from an agent"""
        return self.task_manager.remove_task_from_agent(task_id, agent_id, self.agents)
    
    def get_agent_info(self, agent_id: str) -> Optional[AgentInfo]:
        """Get information about a specific agent"""
        return self.agents.get(agent_id)
    
    def get_all_agents(self) -> Dict[str, AgentInfo]:
        """Get all registered agents"""
        return self.agents.copy()
    
    def get_agent_workload(self, agent_id: str) -> int:
        """Get current workload for a specific agent"""
        return self.task_manager.get_agent_workload(agent_id, self.agents)
    
    def get_available_agents(self) -> List[str]:
        """Get list of agents that can accept new tasks"""
        return self.task_manager.get_available_agents(self.agents)
    
    def get_management_stats(self) -> AgentStats:
        """Get current management statistics"""
        return self.management_stats
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _initialize_sample_agents(self) -> None:
        """Initialize with sample agents for testing"""
        sample_agents = [
            ("coordinator", "System Coordinator", AgentRole.COORDINATOR, ["coordination", "planning"], 5),
            ("developer", "Code Developer", AgentRole.DEVELOPER, ["coding", "testing"], 3),
            ("analyst", "Data Analyst", AgentRole.ANALYST, ["analysis", "reporting"], 2),
        ]
        
        for agent_id, name, role, skills, max_tasks in sample_agents:
            self.register_agent(agent_id, name, role, skills, max_tasks)
    
    def _save_agent_data(self) -> None:
        """Save agent data using persistence handler"""
        self.persistence_handler.save_agent_data(self.agents)

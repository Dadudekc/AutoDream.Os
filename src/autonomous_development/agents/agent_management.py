#!/usr/bin/env python3
"""
Agent Management - Agent Cellphone V2
====================================

Handles agent registration, unregistration, and basic agent operations.
Follows V2 standards: SRP, OOP principles, BaseManager inheritance.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from src.core.enums import AgentRole
from src.core.models import DevelopmentTask
from src.core.base_manager import BaseManager, ManagerStatus, ManagerPriority


@dataclass
class AgentInfo:
    """Agent information and capabilities"""
    agent_id: str
    name: str
    role: AgentRole
    skills: List[str]
    max_concurrent_tasks: int
    is_active: bool = True
    last_heartbeat: datetime = None
    current_tasks: List[str] = None
    
    def __post_init__(self):
        if self.current_tasks is None:
            self.current_tasks = []
        if self.last_heartbeat is None:
            self.last_heartbeat = datetime.now()


class AgentManager(BaseManager):
    """
    Manages agent registration, unregistration, and basic operations
    
    Now inherits from BaseManager for unified functionality
    """
    
    def __init__(self):
        """Initialize agent manager with BaseManager"""
        super().__init__(
            manager_id="agent_manager",
            name="Agent Manager",
            description="Manages agent registration, unregistration, and basic operations"
        )
        
        # Agent storage
        self.agents: Dict[str, AgentInfo] = {}
        
        # Management tracking
        self.management_stats = {
            "total_agents_registered": 0,
            "active_agents": 0,
        }
        
        # Agent monitoring
        self.agent_heartbeats: Dict[str, datetime] = {}
        self.agent_workloads: Dict[str, int] = {}
        
        # Initialize with sample agents
        self._initialize_sample_agents()
        
        self.logger.info("Agent Manager initialized")
    
    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize agent management system"""
        try:
            self.logger.info("Starting Agent Manager...")
            
            # Clear agent data
            self.agents.clear()
            self.agent_heartbeats.clear()
            self.agent_workloads.clear()
            
            # Reset stats
            self.management_stats["total_agents_registered"] = 0
            self.management_stats["active_agents"] = 0
            
            # Initialize sample agents
            self._initialize_sample_agents()
            
            self.logger.info("Agent Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Agent Manager: {e}")
            return False
    
    def _on_stop(self):
        """Cleanup agent management system"""
        try:
            self.logger.info("Stopping Agent Manager...")
            
            # Save agent data
            self._save_agent_data()
            
            # Clear data
            self.agents.clear()
            self.agent_heartbeats.clear()
            self.agent_workloads.clear()
            
            self.logger.info("Agent Manager stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to stop Agent Manager: {e}")
    
    def _on_heartbeat(self):
        """Agent manager heartbeat"""
        try:
            # Check agent health
            self._check_agent_health()
            
            # Cleanup inactive agents
            self.cleanup_inactive_agents()
            
            # Update metrics
            self.record_operation("heartbeat", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)
    
    def _on_initialize_resources(self) -> bool:
        """Initialize agent manager resources"""
        try:
            # Initialize data structures
            self.agents = {}
            self.agent_heartbeats = {}
            self.agent_workloads = {}
            self.management_stats = {
                "total_agents_registered": 0,
                "active_agents": 0,
            }
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Cleanup agent manager resources"""
        try:
            # Clear data
            self.agents.clear()
            self.agent_heartbeats.clear()
            self.agent_workloads.clear()
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
    
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors"""
        try:
            self.logger.info(f"Attempting recovery for {context}")
            
            # Reset agent state
            self.agents.clear()
            self.agent_heartbeats.clear()
            self.agent_workloads.clear()
            
            # Reinitialize sample agents
            self._initialize_sample_agents()
            
            self.logger.info("Recovery successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False
    
    # ============================================================================
    # Agent Management Methods
    # ============================================================================
    
    def _initialize_sample_agents(self):
        """Initialize with sample development agents - ALL can take command"""
        try:
            sample_agents = [
                {
                    "agent_id": "agent_1",
                    "name": "Agent-1 (Swarm Captain)",
                    "role": AgentRole.COORDINATOR,
                    "skills": ["coordination", "planning", "monitoring", "swarm_command"],
                    "max_concurrent_tasks": 1
                },
                {
                    "agent_id": "agent_2",
                    "name": "Agent-2 (Swarm Commander)",
                    "role": AgentRole.COORDINATOR,
                    "skills": ["git", "code_analysis", "optimization", "testing", "swarm_command"],
                    "max_concurrent_tasks": 3
                },
                {
                    "agent_id": "agent_3",
                    "name": "Agent-3 (Swarm Leader)",
                    "role": AgentRole.COORDINATOR,
                    "skills": ["documentation", "markdown", "api_design", "security", "swarm_command"],
                    "max_concurrent_tasks": 2
                },
                {
                    "agent_id": "agent_4",
                    "name": "Agent-4 (Swarm Director)",
                    "role": AgentRole.COORDINATOR,
                    "skills": ["monitoring", "reporting", "quality_assurance", "swarm_command"],
                    "max_concurrent_tasks": 1
                },
                {
                    "agent_id": "agent_5",
                    "name": "Agent-5 (Swarm Validator)",
                    "role": AgentRole.VALIDATOR,
                    "skills": ["code_review", "testing", "validation", "swarm_command"],
                    "max_concurrent_tasks": 2
                }
            ]
            
            for agent_data in sample_agents:
                self.register_agent(**agent_data)
                
        except Exception as e:
            self.logger.error(f"Failed to initialize sample agents: {e}")
    
    def register_agent(self, agent_id: str, name: str, role: AgentRole,
                      skills: List[str], max_concurrent_tasks: int) -> bool:
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
            self.management_stats["total_agents_registered"] += 1
            self.management_stats["active_agents"] += 1
            
            # Initialize tracking
            self.agent_heartbeats[agent_id] = datetime.now()
            self.agent_workloads[agent_id] = 0
            
            # Record operation
            self.record_operation("register_agent", True, 0.0)
            
            self.logger.info(f"Registered agent {agent_id}: {name} ({role.value})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register agent {agent_id}: {e}")
            self.record_operation("register_agent", False, 0.0)
            return False
    
    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent"""
        try:
            if agent_id not in self.agents:
                return False
            
            agent = self.agents[agent_id]
            if agent.is_active:
                self.management_stats["active_agents"] -= 1
            
            # Remove tracking
            if agent_id in self.agent_heartbeats:
                del self.agent_heartbeats[agent_id]
            if agent_id in self.agent_workloads:
                del self.agent_workloads[agent_id]
            
            del self.agents[agent_id]
            
            # Record operation
            self.record_operation("unregister_agent", True, 0.0)
            
            self.logger.info(f"Unregistered agent {agent_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unregister agent {agent_id}: {e}")
            self.record_operation("unregister_agent", False, 0.0)
            return False
    
    def update_agent_heartbeat(self, agent_id: str) -> bool:
        """Update agent heartbeat"""
        try:
            if agent_id not in self.agents:
                return False
            
            agent = self.agents[agent_id]
            agent.last_heartbeat = datetime.now()
            
            # Update tracking
            self.agent_heartbeats[agent_id] = datetime.now()
            
            # Reactivate if was inactive
            if not agent.is_active:
                agent.is_active = True
                self.management_stats["active_agents"] += 1
                self.logger.info(f"Agent {agent_id} reactivated")
            
            # Record operation
            self.record_operation("update_agent_heartbeat", True, 0.0)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update agent heartbeat {agent_id}: {e}")
            self.record_operation("update_agent_heartbeat", False, 0.0)
            return False
    
    def deactivate_agent(self, agent_id: str) -> bool:
        """Deactivate an agent"""
        try:
            if agent_id not in self.agents:
                return False
            
            agent = self.agents[agent_id]
            if agent.is_active:
                agent.is_active = False
                self.management_stats["active_agents"] -= 1
                
                # Record operation
                self.record_operation("deactivate_agent", True, 0.0)
                
                self.logger.info(f"Agent {agent_id} deactivated")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to deactivate agent {agent_id}: {e}")
            self.record_operation("deactivate_agent", False, 0.0)
            return False
    
    def get_agent(self, agent_id: str) -> Optional[AgentInfo]:
        """Get agent information"""
        try:
            agent = self.agents.get(agent_id)
            
            # Record operation
            self.record_operation("get_agent", True, 0.0)
            
            return agent
            
        except Exception as e:
            self.logger.error(f"Failed to get agent {agent_id}: {e}")
            self.record_operation("get_agent", False, 0.0)
            return None
    
    def get_active_agents(self) -> List[AgentInfo]:
        """Get all active agents"""
        try:
            active_agents = [agent for agent in self.agents.values() if agent.is_active]
            
            # Record operation
            self.record_operation("get_active_agents", True, 0.0)
            
            return active_agents
            
        except Exception as e:
            self.logger.error(f"Failed to get active agents: {e}")
            self.record_operation("get_active_agents", False, 0.0)
            return []
    
    def get_agents_by_role(self, role: AgentRole) -> List[AgentInfo]:
        """Get agents by role"""
        try:
            agents = [agent for agent in self.agents.values() if agent.role == role]
            
            # Record operation
            self.record_operation("get_agents_by_role", True, 0.0)
            
            return agents
            
        except Exception as e:
            self.logger.error(f"Failed to get agents by role {role}: {e}")
            self.record_operation("get_agents_by_role", False, 0.0)
            return []
    
    def get_agents_with_skill(self, skill: str) -> List[AgentInfo]:
        """Get agents with a specific skill"""
        try:
            agents = [agent for agent in self.agents.values() if skill in agent.skills]
            
            # Record operation
            self.record_operation("get_agents_with_skill", True, 0.0)
            
            return agents
            
        except Exception as e:
            self.logger.error(f"Failed to get agents with skill {skill}: {e}")
            self.record_operation("get_agents_with_skill", False, 0.0)
            return []
    
    def get_available_agents(self) -> List[AgentInfo]:
        """Get agents available for new tasks"""
        try:
            available_agents = [
                agent for agent in self.agents.values()
                if (agent.is_active and 
                    len(agent.current_tasks) < agent.max_concurrent_tasks)
            ]
            
            # Record operation
            self.record_operation("get_available_agents", True, 0.0)
            
            return available_agents
            
        except Exception as e:
            self.logger.error(f"Failed to get available agents: {e}")
            self.record_operation("get_available_agents", False, 0.0)
            return []
    
    def get_all_agents(self) -> List[AgentInfo]:
        """Get all registered agents."""
        try:
            agents = list(self.agents.values())
            
            # Record operation
            self.record_operation("get_all_agents", True, 0.0)
            
            return agents
            
        except Exception as e:
            self.logger.error(f"Failed to get all agents: {e}")
            self.record_operation("get_all_agents", False, 0.0)
            return []
    
    def cleanup_inactive_agents(self, max_inactive_time: int = 3600) -> int:
        """Remove agents that haven't sent heartbeat for specified time"""
        try:
            timeout = timedelta(minutes=max_inactive_time)
            cutoff_time = datetime.now() - timeout
            removed_count = 0
            
            agent_ids_to_remove = []
            for agent_id, agent in self.agents.items():
                if (agent.last_heartbeat and 
                    agent.last_heartbeat < cutoff_time and
                    agent.role != AgentRole.COORDINATOR):  # Don't remove coordinator
                    agent_ids_to_remove.append(agent_id)
            
            for agent_id in agent_ids_to_remove:
                self.unregister_agent(agent_id)
                removed_count += 1
            
            # Record operation
            self.record_operation("cleanup_inactive_agents", True, 0.0)
            
            self.logger.info(f"Removed {removed_count} inactive agents")
            return removed_count
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup inactive agents: {e}")
            self.record_operation("cleanup_inactive_agents", False, 0.0)
            return 0
    
    def get_agent_statistics(self) -> Dict[str, Any]:
        """Get comprehensive agent statistics."""
        try:
            active_agents = [agent for agent in self.agents.values() if agent.is_active]
            inactive_agents = [agent for agent in self.agents.values() if not agent.is_active]
            
            stats = {
                "total_agents": len(self.agents),
                "active_agents": len(active_agents),
                "inactive_agents": len(inactive_agents),
                "total_skills": sum(len(agent.skills) for agent in self.agents.values()),
                "avg_skills_per_agent": sum(len(agent.skills) for agent in self.agents.values()) / len(self.agents) if self.agents else 0,
                "total_tasks_assigned": sum(len(agent.current_tasks) for agent in self.agents.values()),
                "avg_tasks_per_agent": sum(len(agent.current_tasks) for agent in self.agents.values()) / len(self.agents) if self.agents else 0
            }
            
            # Record operation
            self.record_operation("get_agent_statistics", True, 0.0)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to get agent statistics: {e}")
            self.record_operation("get_agent_statistics", False, 0.0)
            return {}
    
    def get_agent_workload_summary(self) -> Dict[str, Any]:
        """Get summary of agent workloads"""
        try:
            workload_summary = {}
            
            for agent_id, agent in self.agents.items():
                workload_summary[agent_id] = {
                    "name": agent.name,
                    "role": agent.role.value,
                    "current_tasks": len(agent.current_tasks),
                    "max_tasks": agent.max_concurrent_tasks,
                    "workload_percentage": (len(agent.current_tasks) / agent.max_concurrent_tasks) * 100,
                    "is_active": agent.is_active,
                    "last_heartbeat": agent.last_heartbeat.isoformat() if agent.last_heartbeat else None
                }
            
            # Record operation
            self.record_operation("get_agent_workload_summary", True, 0.0)
            
            return workload_summary
            
        except Exception as e:
            self.logger.error(f"Failed to get agent workload summary: {e}")
            self.record_operation("get_agent_workload_summary", False, 0.0)
            return {}
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _save_agent_data(self):
        """Save agent data (placeholder for future persistence)"""
        try:
            # TODO: Implement persistence to database/file
            self.logger.debug("Agent data saved")
            
        except Exception as e:
            self.logger.error(f"Failed to save agent data: {e}")
    
    def _check_agent_health(self):
        """Check agent health status"""
        try:
            current_time = datetime.now()
            
            for agent_id, agent in self.agents.items():
                if agent.last_heartbeat:
                    time_since_heartbeat = (current_time - agent.last_heartbeat).total_seconds()
                    
                    # Check if agent is responsive
                    if time_since_heartbeat > 300:  # 5 minutes
                        self.logger.warning(f"Agent {agent_id} heartbeat is stale ({time_since_heartbeat}s old)")
                    
                    # Check workload
                    workload_percentage = (len(agent.current_tasks) / agent.max_concurrent_tasks) * 100
                    if workload_percentage > 90:
                        self.logger.warning(f"Agent {agent_id} is at {workload_percentage:.1f}% capacity")
                        
        except Exception as e:
            self.logger.error(f"Failed to check agent health: {e}")
    
    def get_agent_manager_stats(self) -> Dict[str, Any]:
        """Get agent manager statistics"""
        try:
            stats = {
                "total_agents_registered": self.management_stats["total_agents_registered"],
                "active_agents": self.management_stats["active_agents"],
                "agent_heartbeats_count": len(self.agent_heartbeats),
                "agent_workloads_count": len(self.agent_workloads),
                "manager_status": self.status.value,
                "manager_uptime": self.metrics.uptime_seconds
            }
            
            # Record operation
            self.record_operation("get_agent_manager_stats", True, 0.0)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to get agent manager stats: {e}")
            self.record_operation("get_agent_manager_stats", False, 0.0)
            return {"error": str(e)}

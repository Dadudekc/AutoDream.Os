#!/usr/bin/env python3
"""
Agent Manager - Clean OOP Design
================================

Agent Manager following clean object-oriented principles.
Single responsibility: Manage multiple agents and their lifecycle.

Author: Agent-1 (Integration Specialist)
License: MIT
"""

import logging
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta

from .core import Agent
from .enums import AgentStatus, AgentType, AgentCapability
from .configuration import AgentConfiguration

logger = logging.getLogger(__name__)


class AgentManager:
    """Manages multiple agents with clean separation of concerns."""
    
    def __init__(self):
        """Initialize agent manager."""
        self._agents: Dict[str, Agent] = {}
        self._agent_types: Dict[AgentType, Set[str]] = {
            agent_type: set() for agent_type in AgentType
        }
        self._capability_index: Dict[AgentCapability, Set[str]] = {
            capability: set() for capability in AgentCapability
        }
    
    # Agent registration with clean indexing
    def register_agent(self, agent: Agent) -> bool:
        """Register a new agent."""
        if agent.id in self._agents:
            logger.warning(f"Agent {agent.name} already registered")
            return False
        
        self._agents[agent.id] = agent
        self._agent_types[agent.agent_type].add(agent.id)
        
        for capability in agent.capabilities:
            self._capability_index[capability].add(agent.id)
        
        logger.info(f"Registered agent {agent.name} ({agent.id})")
        return True
    
    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent."""
        if agent_id not in self._agents:
            logger.warning(f"Agent {agent_id} not found")
            return False
        
        agent = self._agents[agent_id]
        
        # Remove from indexes
        self._agent_types[agent.agent_type].discard(agent_id)
        for capability in agent.capabilities:
            self._capability_index[capability].discard(agent_id)
        
        del self._agents[agent_id]
        logger.info(f"Unregistered agent {agent.name} ({agent_id})")
        return True
    
    # Agent retrieval with clean querying
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID."""
        return self._agents.get(agent_id)
    
    def get_agent_by_name(self, name: str) -> Optional[Agent]:
        """Get agent by name."""
        for agent in self._agents.values():
            if agent.name == name:
                return agent
        return None
    
    def get_agents_by_type(self, agent_type: AgentType) -> List[Agent]:
        """Get all agents of a specific type."""
        agent_ids = self._agent_types[agent_type]
        return [self._agents[agent_id] for agent_id in agent_ids if agent_id in self._agents]
    
    def get_agents_by_capability(self, capability: AgentCapability) -> List[Agent]:
        """Get all agents with a specific capability."""
        agent_ids = self._capability_index[capability]
        return [self._agents[agent_id] for agent_id in agent_ids if agent_id in self._agents]
    
    def get_all_agents(self) -> List[Agent]:
        """Get all registered agents."""
        return list(self._agents.values())
    
    def get_active_agents(self) -> List[Agent]:
        """Get all active agents."""
        return [agent for agent in self._agents.values() if agent.status == AgentStatus.ACTIVE]
    
    def get_healthy_agents(self) -> List[Agent]:
        """Get all healthy agents."""
        return [agent for agent in self._agents.values() if agent.is_healthy()]
    
    # Agent lifecycle management with clean state handling
    def activate_agent(self, agent_id: str) -> bool:
        """Activate an agent."""
        agent = self.get_agent(agent_id)
        if not agent:
            logger.warning(f"Cannot activate agent {agent_id}: not found")
            return False
        
        agent.activate()
        return True
    
    def deactivate_agent(self, agent_id: str) -> bool:
        """Deactivate an agent."""
        agent = self.get_agent(agent_id)
        if not agent:
            logger.warning(f"Cannot deactivate agent {agent_id}: not found")
            return False
        
        agent.deactivate()
        return True
    
    def activate_all_agents(self):
        """Activate all registered agents."""
        for agent in self._agents.values():
            agent.activate()
        logger.info("Activated all agents")
    
    def deactivate_all_agents(self):
        """Deactivate all registered agents."""
        for agent in self._agents.values():
            agent.deactivate()
        logger.info("Deactivated all agents")
    
    # Agent monitoring with clean health checks
    def get_agent_count(self) -> int:
        """Get total number of registered agents."""
        return len(self._agents)
    
    def get_agent_count_by_type(self) -> Dict[str, int]:
        """Get agent count by type."""
        counts = {}
        for agent_type, agent_ids in self._agent_types.items():
            counts[agent_type.value] = len(agent_ids)
        return counts
    
    def get_agent_count_by_capability(self) -> Dict[str, int]:
        """Get agent count by capability."""
        counts = {}
        for capability, agent_ids in self._capability_index.items():
            counts[capability.value] = len(agent_ids)
        return counts
    
    def get_health_summary(self) -> Dict[str, any]:
        """Get overall health summary."""
        total_agents = len(self._agents)
        active_agents = len(self.get_active_agents())
        healthy_agents = len(self.get_healthy_agents())
        
        return {
            'total_agents': total_agents,
            'active_agents': active_agents,
            'healthy_agents': healthy_agents,
            'health_percentage': (healthy_agents / total_agents * 100) if total_agents > 0 else 0,
            'agent_types': self.get_agent_count_by_type(),
            'capabilities': self.get_agent_count_by_capability()
        }
    
    # Agent discovery with clean capability matching
    def find_agent_for_task(self, required_capabilities: List[AgentCapability]) -> Optional[Agent]:
        """Find an agent that can handle a task with required capabilities."""
        available_agents = []
        
        for agent in self.get_active_agents():
            if all(agent.has_capability(cap) for cap in required_capabilities):
                available_agents.append(agent)
        
        if not available_agents:
            return None
        
        # Return agent with best success rate
        return max(available_agents, key=lambda a: a.metrics.get_success_rate())
    
    def find_agents_for_task(self, required_capabilities: List[AgentCapability]) -> List[Agent]:
        """Find all agents that can handle a task with required capabilities."""
        available_agents = []
        
        for agent in self.get_active_agents():
            if all(agent.has_capability(cap) for cap in required_capabilities):
                available_agents.append(agent)
        
        # Sort by success rate (best first)
        return sorted(available_agents, key=lambda a: a.metrics.get_success_rate(), reverse=True)
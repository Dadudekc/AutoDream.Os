#!/usr/bin/env python3
"""
Agent Persistence - Agent Cellphone V2
======================================

Handles agent data persistence and serialization.
Follows V2 standards: SRP, clean separation of concerns.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import logging
from typing import Dict, Callable, Optional
from datetime import datetime

from src.core.enums import AgentRole
from .agent_models import AgentInfo


class AgentPersistenceHandler:
    """Handles agent data persistence operations"""
    
    def __init__(self, data_handler: Optional[Callable[[str], None]] = None):
        """Initialize persistence handler
        
        Args:
            data_handler: Optional callable or object with a ``write`` method
                used to persist serialized agent data. If ``None`` persistence
                will be skipped.
        """
        self.data_handler = data_handler
        self.logger = logging.getLogger(__name__)
    
    def save_agent_data(self, agents: Dict[str, AgentInfo]) -> bool:
        """Serialize agent data and persist using the injected handler
        
        Args:
            agents: Dictionary of agent_id to AgentInfo mappings
            
        Returns:
            bool: True if save was successful, False otherwise
        """
        if not self.data_handler:
            self.logger.debug("No data handler configured; skipping save")
            return False
            
        try:
            data = {}
            for agent_id, agent in agents.items():
                info = self._serialize_agent(agent)
                data[agent_id] = info
                
            serialized = json.dumps(data)
            self._write_data(serialized)
            self.logger.debug("Agent data saved")
            return True
            
        except Exception as e:
            context = {"agents": len(agents)}
            self.logger.error(f"Failed to save agent data: {e} | context: {context}")
            return False
    
    def _serialize_agent(self, agent: AgentInfo) -> Dict:
        """Serialize a single agent to dictionary format"""
        info = {
            "agent_id": agent.agent_id,
            "name": agent.name,
            "skills": agent.skills,
            "max_concurrent_tasks": agent.max_concurrent_tasks,
            "is_active": agent.is_active,
            "current_tasks": agent.current_tasks
        }
        
        # Handle role serialization
        if isinstance(agent.role, AgentRole):
            info["role"] = agent.role.value
        else:
            info["role"] = agent.role
            
        # Handle datetime serialization
        if agent.last_heartbeat:
            info["last_heartbeat"] = agent.last_heartbeat.isoformat()
        else:
            info["last_heartbeat"] = None
            
        return info
    
    def _write_data(self, data: str) -> None:
        """Write data using the configured handler"""
        if hasattr(self.data_handler, "write"):
            self.data_handler.write(data)
        elif callable(self.data_handler):
            self.data_handler(data)
        else:
            raise TypeError("data_handler must be callable or have write() method")

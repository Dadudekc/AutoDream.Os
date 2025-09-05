#!/usr/bin/env python3
"""
Agent Context Engine - KISS Compliant
=====================================

Simple agent context operations.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class AgentContextEngine:
    """Simple agent context engine."""
    
    def __init__(self):
        """Initialize agent context engine."""
        self.agent_contexts: Dict[str, Dict[str, Any]] = {}
        self.metrics = {
            'total_agents': 0,
            'total_recommendations': 0,
            'last_updated': datetime.now().isoformat()
        }
        self.logger = logger
    
    def get_agent_context(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent context by ID."""
        try:
            return self.agent_contexts.get(agent_id)
        except Exception as e:
            self.logger.error(f"Error getting agent context: {e}")
            return None
    
    def update_agent_context(self, agent_id: str, context: Dict[str, Any]) -> bool:
        """Update agent context."""
        try:
            self.agent_contexts[agent_id] = {
                **context,
                'last_updated': datetime.now().isoformat()
            }
            self.metrics['total_agents'] = len(self.agent_contexts)
            self.metrics['last_updated'] = datetime.now().isoformat()
            self.logger.info(f"Updated context for agent {agent_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating agent context: {e}")
            return False
    
    def get_all_agents(self) -> List[str]:
        """Get all agent IDs."""
        try:
            return list(self.agent_contexts.keys())
        except Exception as e:
            self.logger.error(f"Error getting all agents: {e}")
            return []
    
    def delete_agent_context(self, agent_id: str) -> bool:
        """Delete agent context."""
        try:
            if agent_id in self.agent_contexts:
                del self.agent_contexts[agent_id]
                self.metrics['total_agents'] = len(self.agent_contexts)
                self.metrics['last_updated'] = datetime.now().isoformat()
                self.logger.info(f"Deleted context for agent {agent_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error deleting agent context: {e}")
            return False
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get engine metrics."""
        return self.metrics.copy()
    
    def reset_metrics(self) -> None:
        """Reset engine metrics."""
        self.metrics = {
            'total_agents': len(self.agent_contexts),
            'total_recommendations': 0,
            'last_updated': datetime.now().isoformat()
        }
        self.logger.info("Metrics reset")
    
    def get_status(self) -> Dict[str, Any]:
        """Get engine status."""
        return {
            "active": True,
            "total_agents": len(self.agent_contexts),
            "metrics": self.get_metrics(),
            "timestamp": datetime.now().isoformat()
        }

# Simple factory function
def create_agent_context_engine() -> AgentContextEngine:
    """Create agent context engine."""
    return AgentContextEngine()

__all__ = ["AgentContextEngine", "create_agent_context_engine"]
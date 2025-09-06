#!/usr/bin/env python3
"""
Agent Context Orchestrator - KISS Compliant
===========================================

Simple agent context orchestration.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from .agent_context_models import (
    AgentContext,
    Recommendation,
    ContextMetrics,
    AgentProfile,
    RecommendationType,
    ConfidenceLevel,
    create_agent_profile,
    create_recommendation,
    create_agent_context,
)
from .agent_context_engine import AgentContextEngine

logger = logging.getLogger(__name__)


class AgentContextSystem:
    """Simple agent context system."""

    def __init__(self, agent_id: str, vector_db=None):
        """Initialize agent context system."""
        self.agent_id = agent_id
        self.vector_db = vector_db
        self.engine = AgentContextEngine()
        self.logger = logger

    def get_agent_context(self, agent_id: str = None) -> Optional[Dict[str, Any]]:
        """Get agent context."""
        target_id = agent_id or self.agent_id
        return self.engine.get_agent_context(target_id)

    def update_agent_context(self, agent_id: str, context: Dict[str, Any]) -> bool:
        """Update agent context."""
        return self.engine.update_agent_context(agent_id, context)

    def create_agent_profile(
        self, agent_id: str, name: str, role: str, **kwargs
    ) -> bool:
        """Create agent profile."""
        profile_data = {"name": name, "role": role, **kwargs}
        return self.engine.update_agent_context(agent_id, profile_data)

    def get_all_agents(self) -> List[str]:
        """Get all agent IDs."""
        return self.engine.get_all_agents()

    def delete_agent_context(self, agent_id: str) -> bool:
        """Delete agent context."""
        return self.engine.delete_agent_context(agent_id)

    def get_metrics(self) -> Dict[str, Any]:
        """Get system metrics."""
        return self.engine.get_metrics()

    def get_status(self) -> Dict[str, Any]:
        """Get system status."""
        return self.engine.get_status()

    def reset_metrics(self) -> None:
        """Reset system metrics."""
        self.engine.reset_metrics()


# Simple factory function
def create_agent_context_system(agent_id: str, vector_db=None) -> AgentContextSystem:
    """Create agent context system."""
    return AgentContextSystem(agent_id, vector_db)


__all__ = ["AgentContextSystem", "create_agent_context_system"]

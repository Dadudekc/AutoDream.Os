#!/usr/bin/env python3
"""
Agent Vector Integration Refactored - V2 Compliance Module
==========================================================

Main refactored entry point for agent vector integration.

Author: Agent-2 (Architecture & Design Specialist) - V2 Refactoring
License: MIT
"""

from .agent_vector_integration_core import AgentVectorIntegrationCore
from .agent_vector_integration_operations import AgentVectorIntegrationOperations


class AgentVectorIntegration(AgentVectorIntegrationCore, AgentVectorIntegrationOperations):
    """Unified agent vector integration with core and operations functionality."""
    
    def __init__(self, agent_id: str, config_path: Optional[str] = None):
        """Initialize unified agent vector integration."""
        AgentVectorIntegrationCore.__init__(self, agent_id, config_path)
        AgentVectorIntegrationOperations.__init__(self, agent_id, config_path)

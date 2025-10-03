#!/usr/bin/env python3
"""
Agent Entity - Clean Entry Point
===============================

Clean entry point for Agent entities following clean object-oriented principles.
All functionality has been refactored into focused modules.

Author: Agent-1 (Integration Specialist)
License: MIT
"""

# Import all agent functionality from clean modules
from .agent import (
    AgentStatus,
    AgentType,
    AgentCapability,
    AgentMetrics,
    AgentConfiguration,
    Agent,
    AgentManager
)

# Re-export for backward compatibility
__all__ = [
    'AgentStatus',
    'AgentType',
    'AgentCapability', 
    'AgentMetrics',
    'AgentConfiguration',
    'Agent',
    'AgentManager'
]
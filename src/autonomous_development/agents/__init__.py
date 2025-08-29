#!/usr/bin/env python3
"""
Agent Management Package - Agent Cellphone V2
=============================================

Comprehensive agent management system with modular architecture.
Follows V2 standards: SRP, OOP principles, clean separation of concerns.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .agent_models import AgentInfo, AgentStats
from .agent_health import AgentHealthMonitor
from .agent_persistence import AgentPersistenceHandler
from .agent_tasks import AgentTaskManager
from .agent_management import AgentManager

__all__ = [
    'AgentInfo',
    'AgentStats', 
    'AgentHealthMonitor',
    'AgentPersistenceHandler',
    'AgentTaskManager',
    'AgentManager'
]

"""
Coordination Repositories
=========================

Repositories for the coordination system using Repository pattern.

Author: Agent-2 (Architecture & Design Specialist)
Mission: Large File Modularization and V2 Compliance
Contract: CONTRACT_Agent-2_1757826687
License: MIT
"""

from .agent_status_repository import AgentStatusRepository
from .coordination_state_repository import CoordinationStateRepository

__all__ = ['AgentStatusRepository', 'CoordinationStateRepository']


"""
Repository Layer - Data Access Pattern
=======================================

This package provides the repository pattern implementation for the agent system.
Repositories handle all data access operations, providing a clean abstraction
over the underlying data storage mechanisms.

Author: Agent-7 - Repository Cloning Specialist
Mission: Quarantine Fix Phase 3 (Repository Pattern)
Date: 2025-10-16
Points: 900 pts (3 repositories × 300 pts each)

Architecture:
- AgentRepository: Agent data operations
- ContractRepository: Contract data operations  
- MessageRepository: Message data operations

Usage:
    from src.repositories import AgentRepository, ContractRepository, MessageRepository
    
    agent_repo = AgentRepository()
    agent = agent_repo.get_agent("Agent-7")
"""

from .agent_repository import AgentRepository
from .contract_repository import ContractRepository
from .message_repository import MessageRepository

__all__ = [
    'AgentRepository',
    'ContractRepository',
    'MessageRepository',
]


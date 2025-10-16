"""
Repository Layer - Data Access Pattern
======================================

This package provides data access repositories following the repository pattern.
All repositories handle data operations without business logic.

Available Repositories:
- AgentRepository: Agent data operations
- ContractRepository: Contract data operations
- MessageRepository: Message data operations

Usage:
    from src.repositories import AgentRepository, ContractRepository, MessageRepository
    
    agent_repo = AgentRepository()
    agents = agent_repo.get_all_agents()
"""

from .agent_repository import AgentRepository
from .contract_repository import ContractRepository
from .message_repository import MessageRepository

__all__ = [
    'AgentRepository',
    'ContractRepository',
    'MessageRepository',
]

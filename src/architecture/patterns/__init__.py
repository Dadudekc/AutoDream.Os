#!/usr/bin/env python3
"""
Design Patterns Package - V2 Compliant
======================================

Design patterns package for the Agent Cellphone V2 project.
Provides essential design patterns with V2 compliance.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from .command_repository import (
    Command,
    CommandInvoker,
    Entity,
    FileRepository,
    InMemoryRepository,
    MessageCommand,
    Repository,
)
from .observer_strategy import (
    AgentValidationStrategy,
    EmailValidationStrategy,
    Event,
    EventBus,
    MessageValidationStrategy,
    Observer,
    StrategyFactory,
    Subject,
    ValidationContext,
    ValidationStrategy,
)

# Import pattern modules
from .singleton_factory import ServiceFactory, ServiceLocator, SingletonBase, SingletonMeta

# Export all patterns
__all__ = [
    # Singleton and Factory
    "SingletonMeta",
    "SingletonBase",
    "ServiceFactory",
    "ServiceLocator",
    # Observer and Strategy
    "Event",
    "Observer",
    "Subject",
    "ValidationStrategy",
    "MessageValidationStrategy",
    "AgentValidationStrategy",
    "EmailValidationStrategy",
    "ValidationContext",
    "EventBus",
    "StrategyFactory",
    # Command and Repository
    "Command",
    "MessageCommand",
    "CommandInvoker",
    "Repository",
    "Entity",
    "InMemoryRepository",
    "FileRepository",
]

#!/usr/bin/env python3
"""
Design Patterns V2 - Scalable Architecture
==========================================

Essential design patterns for the growing Agent Cellphone V2 project.
Implements key patterns while maintaining V2 compliance and KISS principles.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import threading
from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Generic, TypeVar

from ..core.shared_logging import get_module_logger

logger = get_module_logger(__name__)

T = TypeVar("T")


class PatternType(Enum):
    """Design pattern type enumeration."""

    SINGLETON = "singleton"
    FACTORY = "factory"
    OBSERVER = "observer"
    STRATEGY = "strategy"
    COMMAND = "command"
    REPOSITORY = "repository"
    SERVICE_LOCATOR = "service_locator"


# ============================================================================
# SINGLETON PATTERN
# ============================================================================


class SingletonMeta(type):
    """Thread-safe singleton metaclass."""

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonBase(metaclass=SingletonMeta):
    """Base class for singleton pattern."""

    pass


# ============================================================================
# FACTORY PATTERN
# ============================================================================


class ServiceFactory:
    """Factory for creating service instances."""

    _services: dict[str, Any] = {}
    _lock = threading.Lock()

    @classmethod
    def create_service(cls, service_type: str, *args, **kwargs) -> Any:
        """Create or get service instance."""
        with cls._lock:
            if service_type not in cls._services:
                cls._services[service_type] = cls._create_instance(service_type, *args, **kwargs)
            return cls._services[service_type]

    @classmethod
    def _create_instance(cls, service_type: str, *args, **kwargs) -> Any:
        """Create service instance based on type."""
        service_map = {
            "messaging": "src.services.consolidated_messaging_service.ConsolidatedMessagingService",
            "discord": "src.services.discord_bot.core.discord_bot.EnhancedDiscordAgentBot",
            "thea": "src.services.thea.thea_communication_interface.TheaCommunicationInterface",
            "vector_db": "src.services.vector_database.vector_database_integration.VectorDatabaseIntegration",
        }

        if service_type not in service_map:
            raise ValueError(f"Unknown service type: {service_type}")

        # Dynamic import and instantiation
        module_path, class_name = service_map[service_type].rsplit(".", 1)
        module = __import__(module_path, fromlist=[class_name])
        service_class = getattr(module, class_name)
        return service_class(*args, **kwargs)


# ============================================================================
# OBSERVER PATTERN
# ============================================================================


@dataclass
class Event:
    """Base event class."""

    event_type: str
    source: str
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: __import__("time").time())


class Observer(ABC):
    """Observer interface."""

    @abstractmethod
    def update(self, event: Event) -> None:
        """Handle event update."""
        pass


class Subject:
    """Subject for observer pattern."""

    def __init__(self):
        self._observers: list[Observer] = []
        self._lock = threading.Lock()

    def attach(self, observer: Observer) -> None:
        """Attach observer."""
        with self._lock:
            if observer not in self._observers:
                self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Detach observer."""
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)

    def notify(self, event: Event) -> None:
        """Notify all observers."""
        with self._lock:
            for observer in self._observers:
                try:
                    observer.update(event)
                except Exception as e:
                    logger.error(f"Observer notification failed: {e}")


# ============================================================================
# STRATEGY PATTERN
# ============================================================================


class ValidationStrategy(ABC):
    """Validation strategy interface."""

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate data."""
        pass


class MessageValidationStrategy(ValidationStrategy):
    """Message validation strategy."""

    def validate(self, data: Any) -> bool:
        """Validate message data."""
        return isinstance(data, str) and len(data.strip()) > 0


class AgentValidationStrategy(ValidationStrategy):
    """Agent validation strategy."""

    def validate(self, data: Any) -> bool:
        """Validate agent data."""
        return isinstance(data, str) and data.startswith("Agent-")


class ValidationContext:
    """Validation context using strategy pattern."""

    def __init__(self, strategy: ValidationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ValidationStrategy) -> None:
        """Set validation strategy."""
        self._strategy = strategy

    def validate(self, data: Any) -> bool:
        """Validate using current strategy."""
        return self._strategy.validate(data)


# ============================================================================
# COMMAND PATTERN
# ============================================================================


class Command(ABC):
    """Command interface."""

    @abstractmethod
    def execute(self) -> Any:
        """Execute command."""
        pass

    @abstractmethod
    def undo(self) -> Any:
        """Undo command."""
        pass


@dataclass
class MessageCommand(Command):
    """Message sending command."""

    messaging_service: Any
    agent_id: str
    message: str
    from_agent: str = "Agent-2"
    priority: str = "NORMAL"

    def execute(self) -> bool:
        """Execute message sending."""
        return self.messaging_service.send_message(
            self.agent_id, self.message, self.from_agent, self.priority
        )

    def undo(self) -> bool:
        """Undo message sending (not applicable)."""
        logger.warning("Cannot undo message sending")
        return False


class CommandInvoker:
    """Command invoker with history."""

    def __init__(self):
        self._history: list[Command] = []
        self._max_history = 100

    def execute_command(self, command: Command) -> Any:
        """Execute command and add to history."""
        result = command.execute()
        self._history.append(command)

        # Limit history size
        if len(self._history) > self._max_history:
            self._history.pop(0)

        return result

    def undo_last(self) -> Any:
        """Undo last command."""
        if not self._history:
            return None

        command = self._history.pop()
        return command.undo()


# ============================================================================
# REPOSITORY PATTERN
# ============================================================================


class Repository(ABC, Generic[T]):
    """Repository interface."""

    @abstractmethod
    def save(self, entity: T) -> T:
        """Save entity."""
        pass

    @abstractmethod
    def find_by_id(self, entity_id: str) -> T | None:
        """Find entity by ID."""
        pass

    @abstractmethod
    def find_all(self) -> list[T]:
        """Find all entities."""
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Delete entity."""
        pass


class InMemoryRepository(Repository[T]):
    """In-memory repository implementation."""

    def __init__(self):
        self._entities: dict[str, T] = {}
        self._lock = threading.Lock()

    def save(self, entity: T) -> T:
        """Save entity."""
        with self._lock:
            entity_id = getattr(entity, "id", str(id(entity)))
            self._entities[entity_id] = entity
            return entity

    def find_by_id(self, entity_id: str) -> T | None:
        """Find entity by ID."""
        with self._lock:
            return self._entities.get(entity_id)

    def find_all(self) -> list[T]:
        """Find all entities."""
        with self._lock:
            return list(self._entities.values())

    def delete(self, entity_id: str) -> bool:
        """Delete entity."""
        with self._lock:
            if entity_id in self._entities:
                del self._entities[entity_id]
                return True
            return False


# ============================================================================
# SERVICE LOCATOR PATTERN
# ============================================================================


class ServiceLocator:
    """Service locator for dependency injection."""

    _services: dict[str, Any] = {}
    _lock = threading.Lock()

    @classmethod
    def register(cls, service_name: str, service_instance: Any) -> None:
        """Register service."""
        with cls._lock:
            cls._services[service_name] = service_instance

    @classmethod
    def get(cls, service_name: str) -> Any:
        """Get service."""
        with cls._lock:
            if service_name not in cls._services:
                raise ValueError(f"Service not found: {service_name}")
            return cls._services[service_name]

    @classmethod
    def is_registered(cls, service_name: str) -> bool:
        """Check if service is registered."""
        with cls._lock:
            return service_name in cls._services


# ============================================================================
# CONTEXT MANAGER FOR RESOURCE MANAGEMENT
# ============================================================================


@contextmanager
def service_context(service_name: str, service_instance: Any):
    """Context manager for service lifecycle."""
    try:
        ServiceLocator.register(service_name, service_instance)
        yield service_instance
    finally:
        # Cleanup if needed
        pass


# ============================================================================
# PATTERN REGISTRY
# ============================================================================


class PatternRegistry:
    """Registry for design patterns."""

    _patterns: dict[PatternType, Any] = {}

    @classmethod
    def register_pattern(cls, pattern_type: PatternType, pattern_instance: Any) -> None:
        """Register pattern instance."""
        cls._patterns[pattern_type] = pattern_instance

    @classmethod
    def get_pattern(cls, pattern_type: PatternType) -> Any:
        """Get pattern instance."""
        return cls._patterns.get(pattern_type)

    @classmethod
    def list_patterns(cls) -> list[PatternType]:
        """List registered patterns."""
        return list(cls._patterns.keys())

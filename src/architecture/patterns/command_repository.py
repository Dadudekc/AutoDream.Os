#!/usr/bin/env python3
"""
Command and Repository Patterns - V2 Compliant
==============================================

Command and Repository pattern implementations for the Agent Cellphone V2 project.
Maintains V2 compliance with focused responsibility.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import json
import threading
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, TypeVar

from ...core.shared_logging import get_module_logger

logger = get_module_logger(__name__)

T = TypeVar("T")


class Command:
    """Command interface."""

    def execute(self) -> Any:
        """Execute command."""
        pass

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
        try:
            return self.messaging_service.send_message(
                self.agent_id, self.message, self.from_agent, self.priority
            )
        except Exception as e:
            logger.error(f"Message command execution failed: {e}")
            return False

    def undo(self) -> bool:
        """Undo message sending (not applicable)."""
        logger.warning("Cannot undo message sending")
        return False


class CommandInvoker:
    """Command invoker with history."""

    def __init__(self, max_history: int = 100):
        self._history: list[Command] = []
        self._max_history = max_history
        self._lock = threading.Lock()

    def execute_command(self, command: Command) -> Any:
        """Execute command and add to history."""
        result = command.execute()

        with self._lock:
            self._history.append(command)

            # Limit history size
            if len(self._history) > self._max_history:
                self._history.pop(0)

        return result

    def undo_last(self) -> Any:
        """Undo last command."""
        with self._lock:
            if not self._history:
                return None

            command = self._history.pop()
            return command.undo()

    def get_history_size(self) -> int:
        """Get history size."""
        with self._lock:
            return len(self._history)

    def clear_history(self) -> None:
        """Clear command history."""
        with self._lock:
            self._history.clear()


class Repository:
    """Repository interface."""

    def save(self, entity: T) -> T:
        """Save entity."""
        pass

    def find_by_id(self, entity_id: str) -> T | None:
        """Find entity by ID."""
        pass

    def find_all(self) -> list[T]:
        """Find all entities."""
        pass

    def delete(self, entity_id: str) -> bool:
        """Delete entity."""
        pass


@dataclass
class Entity:
    """Base entity class."""

    id: str
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


class InMemoryRepository(Repository[T]):
    """In-memory repository implementation."""

    def __init__(self):
        self._entities: dict[str, T] = {}
        self._lock = threading.Lock()

    def save(self, entity: T) -> T:
        """Save entity."""
        with self._lock:
            entity_id = getattr(entity, "id", str(id(entity)))
            entity.updated_at = datetime.now()
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

    def count(self) -> int:
        """Get entity count."""
        with self._lock:
            return len(self._entities)

    def clear(self) -> None:
        """Clear all entities."""
        with self._lock:
            self._entities.clear()


class FileRepository(Repository[T]):
    """File-based repository implementation."""

    def __init__(self, file_path: Path, entity_type: type[T]):
        self.file_path = file_path
        self.entity_type = entity_type
        self._entities: dict[str, T] = {}
        self._lock = threading.Lock()
        self._load_from_file()

    def _load_from_file(self) -> None:
        """Load entities from file."""
        try:
            if self.file_path.exists():
                with open(self.file_path, encoding="utf-8") as f:
                    data = json.load(f)
                    for entity_data in data:
                        entity = self._dict_to_entity(entity_data)
                        self._entities[entity.id] = entity
                logger.info(f"Loaded {len(self._entities)} entities from {self.file_path}")
        except Exception as e:
            logger.error(f"Failed to load entities from file: {e}")

    def _save_to_file(self) -> None:
        """Save entities to file."""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as f:
                data = [self._entity_to_dict(entity) for entity in self._entities.values()]
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save entities to file: {e}")

    def _entity_to_dict(self, entity: T) -> dict[str, Any]:
        """Convert entity to dictionary."""
        return asdict(entity)

    def _dict_to_entity(self, data: dict[str, Any]) -> T:
        """Convert dictionary to entity."""
        # Handle datetime fields
        for field in ["created_at", "updated_at"]:
            if field in data and data[field]:
                data[field] = datetime.fromisoformat(data[field])

        return self.entity_type(**data)

    def save(self, entity: T) -> T:
        """Save entity."""
        with self._lock:
            entity.updated_at = datetime.now()
            self._entities[entity.id] = entity
            self._save_to_file()
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
                self._save_to_file()
                return True
            return False

    def count(self) -> int:
        """Get entity count."""
        with self._lock:
            return len(self._entities)

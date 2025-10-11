"""
Base Repository - Unified Persistence Service
==============================================

Abstract base class for repositories.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist) - Refactored from Agent-3
License: MIT
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Generic, TypeVar

from .database_connection import DatabaseConnection

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Abstract base class for repositories."""

    def __init__(self, db_connection: DatabaseConnection):
        """Initialize repository with database connection."""
        self.db = db_connection

    @abstractmethod
    def get(self, entity_id: str) -> T | None:
        """Get entity by ID."""
        pass

    @abstractmethod
    def save(self, entity: T) -> None:
        """Save entity (create or update)."""
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Delete entity by ID."""
        pass

    @abstractmethod
    def list_all(self, limit: int = 1000) -> Iterable[T]:
        """List all entities."""
        pass

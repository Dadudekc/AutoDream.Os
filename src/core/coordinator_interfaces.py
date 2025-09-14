"""
Coordinator Interfaces - V2 Compliance Module
=============================================

Abstract interfaces for coordinator system following SOLID principles.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Any, Protocol


class ICoordinatorLogger(Protocol):
    """Interface for coordinator logging operations."""

    def info(self, message: str) -> None: ...

    def warning(self, message: str) -> None: ...

    def error(self, message: str) -> None: ...


class ICoordinator(Protocol):
    """Interface for coordinator instances."""

    @property
    def name(self) -> str: ...

    def get_status(self) -> dict[str, Any]: ...

    def shutdown(self) -> None: ...


class ICoordinatorRegistry(ABC):
    """Abstract interface for coordinator registry operations."""

    @abstractmethod
    def register_coordinator(self, coordinator: Any) -> bool:
        """Register a coordinator instance."""
        pass

    @abstractmethod
    def get_coordinator(self, name: str) -> Any | None:
        """Get coordinator by name."""
        pass

    @abstractmethod
    def get_all_coordinators(self) -> dict[str, Any]:
        """Get all registered coordinators."""
        pass

    @abstractmethod
    def unregister_coordinator(self, name: str) -> bool:
        """Unregister a coordinator."""
        pass

    @abstractmethod
    def get_coordinator_statuses(self) -> dict[str, dict[str, Any]]:
        """Get status of all coordinators."""
        pass

    @abstractmethod
    def shutdown_all_coordinators(self) -> None:
        """Shutdown all registered coordinators."""
        pass

    @abstractmethod
    def get_coordinator_count(self) -> int:
        """Get total number of registered coordinators."""
        pass


class ICoordinatorStatusParser(Protocol):
    """Interface for parsing coordinator status."""

    def parse_status(self, coordinator: Any) -> dict[str, Any]: ...

    def can_parse_status(self, coordinator: Any) -> bool: ...

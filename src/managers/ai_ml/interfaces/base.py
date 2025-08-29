"""Legacy base interface for AI/ML managers."""

from abc import ABC, abstractmethod


class BaseManager(ABC):
    """Simple abstract base class used by AI/ML manager components."""

    def __init__(self, name: str):
        self.name = name
        self.status = "initialized"

    @abstractmethod
    def initialize(self) -> None:
        """Initialize manager resources."""

    @abstractmethod
    def execute(self, operation: str) -> None:
        """Execute a manager operation."""

    def get_status(self) -> dict:
        """Return current manager status."""
        return {"name": self.name, "status": self.status}

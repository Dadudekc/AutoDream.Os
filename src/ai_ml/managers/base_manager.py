"""Base Manager Interface

Provides a minimal manager contract that reuses shared mixins.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from src.utils.serializable import SerializableMixin


@dataclass
class BaseManager(SerializableMixin, ABC):
    """Abstract base manager using common mixins."""

    name: str
    status: str = field(default="initialized")

    @abstractmethod
    def initialize(self) -> None:
        """Initialize manager."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, operation: Any) -> Any:
        """Execute manager operation."""
        raise NotImplementedError

    def get_status(self) -> dict:
        """Get manager status."""
        return {"name": self.name, "status": self.status}

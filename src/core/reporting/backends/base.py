from __future__ import annotations

"""Abstract interface for report storage backends."""

from abc import ABC, abstractmethod
from pathlib import Path


class ReportBackend(ABC):
    """Defines the interface for report storage backends."""

    @abstractmethod
    def save(self, path: Path, content: str) -> str:
        """Persist content to the given path and return the path."""
        raise NotImplementedError

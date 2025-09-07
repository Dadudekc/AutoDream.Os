from pathlib import Path

from __future__ import annotations
from abc import ABC, abstractmethod


"""Abstract interface for report storage backends."""



class ReportBackend(ABC):
    """Defines the interface for report storage backends."""

    @abstractmethod
    def save(self, path: Path, content: str) -> str:
        """Persist content to the given path and return the path."""
        raise NotImplementedError

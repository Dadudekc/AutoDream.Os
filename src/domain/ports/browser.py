"""
Browser Port Interface
=====================

Defines the browser interface contract for the domain layer.
"""

from abc import ABC, abstractmethod
from typing import Optional, Any
from dataclasses import dataclass


@dataclass
class PageReply:
    """Standardized response from browser interactions."""
    id: str
    text: str


class Browser(ABC):
    """Abstract browser interface for domain layer."""

    @abstractmethod
    def open(self, profile: str | None = None) -> None:
        """Open browser with optional profile."""
        pass

    @abstractmethod
    def goto(self, url: str) -> None:
        """Navigate to URL."""
        pass

    @abstractmethod
    def send_and_wait(self, prompt: str, timeout_s: float = 120.0) -> PageReply:
        """Send prompt and wait for response."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the browser."""
        pass

    @abstractmethod
    def is_ready(self) -> bool:
        """Check if browser is ready for interactions."""
        pass
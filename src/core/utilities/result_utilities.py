"""
Result Utilities - Result Manager
==================================

Manages results for operations with generic type support.
Part of shared_utilities.py modular refactoring.

Author: Agent-1 (Integration & Core Systems Specialist) - V2 Refactor
Original: Agent-6 (Coordination & Communication Specialist)
License: MIT
"""

from typing import Generic, TypeVar

from .base_utilities import BaseUtility

T = TypeVar("T")


class ResultManager(BaseUtility, Generic[T]):
    """Manages results for operations."""

    def __init__(self):
        super().__init__()
        self.results = []
        self.last_result = None

    def initialize(self) -> bool:
        """Initialize result manager."""
        self.logger.info("ResultManager initialized")
        return True

    def cleanup(self) -> bool:
        """Clean up result resources."""
        self.results.clear()
        self.last_result = None
        return True

    def add_result(self, result: T) -> None:
        """Add a result."""
        self.results.append(result)
        self.last_result = result

    def get_results(self) -> list[T]:
        """Get all results."""
        return self.results.copy()

    def get_last_result(self) -> T | None:
        """Get last result."""
        return self.last_result

    def clear_results(self) -> None:
        """Clear all results."""
        self.results.clear()
        self.last_result = None


def create_result_manager() -> ResultManager:
    """Create a new result manager instance."""
    return ResultManager()


__all__ = ["ResultManager", "create_result_manager"]

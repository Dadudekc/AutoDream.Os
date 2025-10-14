"""
Status Utilities - Status Manager
==================================

Manages status tracking for manager components.
Part of shared_utilities.py modular refactoring.

Author: Agent-1 (Integration & Core Systems Specialist) - V2 Refactor
Original: Agent-6 (Coordination & Communication Specialist)
License: MIT
"""

from datetime import datetime

from .base_utilities import BaseUtility


class StatusManager(BaseUtility):
    """Manages status for managers."""

    def __init__(self):
        super().__init__()
        self.status = "initialized"
        self.status_history = []

    def initialize(self) -> bool:
        """Initialize status manager."""
        self.set_status("initialized")
        self.logger.info("StatusManager initialized")
        return True

    def cleanup(self) -> bool:
        """Clean up status resources."""
        self.status_history.clear()
        return True

    def set_status(self, status: str) -> None:
        """Set current status."""
        old_status = self.status
        self.status = status
        timestamp = datetime.now()

        self.status_history.append(
            {"timestamp": timestamp, "old_status": old_status, "new_status": status}
        )

        self.logger.info(f"Status changed: {old_status} -> {status}")

    def get_status(self) -> str:
        """Get current status."""
        return self.status

    def get_status_history(self) -> list:
        """Get status history."""
        return self.status_history.copy()


def create_status_manager() -> StatusManager:
    """Create a new status manager instance."""
    return StatusManager()


__all__ = ["StatusManager", "create_status_manager"]

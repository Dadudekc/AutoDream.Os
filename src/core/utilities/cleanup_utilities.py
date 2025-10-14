"""
Cleanup Utilities - Cleanup Manager
====================================

Manages cleanup operations for manager components.
Part of shared_utilities.py modular refactoring.

Author: Agent-1 (Integration & Core Systems Specialist) - V2 Refactor
Original: Agent-6 (Coordination & Communication Specialist)
License: MIT
"""

from .base_utilities import BaseUtility


class CleanupManager(BaseUtility):
    """Manages cleanup operations for managers."""

    def __init__(self):
        super().__init__()
        self.cleanup_handlers = []

    def initialize(self) -> bool:
        """Initialize cleanup manager."""
        self.logger.info("CleanupManager initialized")
        return True

    def cleanup(self) -> bool:
        """Execute all registered cleanup handlers."""
        success = True
        for handler in reversed(self.cleanup_handlers):
            try:
                handler()
            except Exception as e:
                self.logger.error(f"Cleanup handler failed: {e}")
                success = False
        self.cleanup_handlers.clear()
        return success

    def register_handler(self, handler: callable) -> None:
        """Register a cleanup handler."""
        self.cleanup_handlers.append(handler)


def create_cleanup_manager() -> CleanupManager:
    """Create a new cleanup manager instance."""
    return CleanupManager()


__all__ = ["CleanupManager", "create_cleanup_manager"]

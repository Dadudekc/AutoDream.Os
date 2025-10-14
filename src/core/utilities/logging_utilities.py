"""
Logging Utilities - Logging Manager
====================================

Manages logging for manager components.
Part of shared_utilities.py modular refactoring.

Author: Agent-1 (Integration & Core Systems Specialist) - V2 Refactor
Original: Agent-6 (Coordination & Communication Specialist)
License: MIT
"""

import logging

from .base_utilities import BaseUtility


class LoggingManager(BaseUtility):
    """Manages logging for managers."""

    def __init__(self):
        super().__init__()
        self.log_level = logging.INFO

    def initialize(self) -> bool:
        """Initialize logging manager."""
        logging.basicConfig(level=self.log_level)
        self.logger.info("LoggingManager initialized")
        return True

    def cleanup(self) -> bool:
        """Clean up logging resources."""
        return True

    def set_log_level(self, level: int) -> None:
        """Set logging level."""
        self.log_level = level
        logging.getLogger().setLevel(level)

    def log_info(self, message: str) -> None:
        """Log info message."""
        self.logger.info(message)

    def log_error(self, message: str) -> None:
        """Log error message."""
        self.logger.error(message)


def create_logging_manager() -> LoggingManager:
    """Create a new logging manager instance."""
    return LoggingManager()


__all__ = ["LoggingManager", "create_logging_manager"]

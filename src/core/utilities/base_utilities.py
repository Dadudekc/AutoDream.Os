"""
Base Utilities - Abstract Base Class
=====================================

Abstract base class for all shared utility components.
Part of shared_utilities.py modular refactoring.

Author: Agent-1 (Integration & Core Systems Specialist) - V2 Refactor
Original: Agent-6 (Coordination & Communication Specialist)
License: MIT
"""

import logging
from abc import ABC, abstractmethod


class BaseUtility(ABC):
    """Base class for all shared utilities."""

    def __init__(self, name: str = None):
        self.name = name or self.__class__.__name__
        self.logger = logging.getLogger(self.name)

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the utility."""
        pass

    @abstractmethod
    def cleanup(self) -> bool:
        """Clean up resources."""
        pass


__all__ = ["BaseUtility"]

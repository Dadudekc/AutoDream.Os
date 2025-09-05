#!/usr/bin/env python3
"""
Coordinator Interfaces - KISS Compliant
======================================

Simple interfaces for coordinator system.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class ICoordinator(ABC):
    """Simple coordinator interface."""
    
    @abstractmethod
    def start(self) -> bool:
        """Start coordinator."""
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        """Stop coordinator."""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get coordinator status."""
        pass

class ICoordinatorLogger(ABC):
    """Simple logger interface."""
    
    @abstractmethod
    def info(self, message: str) -> None:
        """Log info message."""
        pass
    
    @abstractmethod
    def error(self, message: str) -> None:
        """Log error message."""
        pass
    
    @abstractmethod
    def warning(self, message: str) -> None:
        """Log warning message."""
        pass

__all__ = ["ICoordinator", "ICoordinatorLogger"]

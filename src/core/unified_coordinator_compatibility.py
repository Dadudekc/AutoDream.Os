#!/usr/bin/env python3
"""
Unified Coordinator Compatibility Layer
======================================

Backward compatibility layer for the refactored coordinator system.

Author: Agent-2 - Architecture & Design Specialist
Created: 2025-01-27
Purpose: Ensure backward compatibility with existing code
"""

from typing import Any, Dict, List, Optional, Callable
from datetime import datetime

# Import the refactored components
from .unified_coordinator_refactored import UnifiedCoordinator
from .coordinator_models import CoordinationTarget, CoordinationResult, CoordinatorStatus
from .coordinator_registry import (
    CoordinatorRegistry,
    get_global_registry,
    register_coordinator,
    get_coordinator,
    get_all_coordinators,
    get_all_coordinator_statuses,
    shutdown_all_coordinators
)

# Re-export for backward compatibility
__all__ = [
    'UnifiedCoordinatorBase',
    'CoordinationTarget', 
    'CoordinationResult',
    'CoordinatorStatus',
    'CoordinatorRegistry',
    'get_coordinator_registry',
    'register_coordinator',
    'get_coordinator',
    'get_all_coordinators',
    'get_all_coordinator_statuses'
]

# Backward compatibility aliases
UnifiedCoordinatorBase = UnifiedCoordinator

# Global registry instance for backward compatibility
_coordinator_registry = None


def get_coordinator_registry() -> CoordinatorRegistry:
    """Get global coordinator registry instance (backward compatibility)."""
    global _coordinator_registry
    if _coordinator_registry is None:
        import logging
        logger = logging.getLogger("CoordinatorRegistry")
        _coordinator_registry = CoordinatorRegistry(logger)
    return _coordinator_registry


# Backward compatibility functions
def register_coordinator(coordinator: UnifiedCoordinatorBase) -> bool:
    """Register a coordinator with the global registry (backward compatibility)."""
    import logging
    logger = logging.getLogger("CoordinatorRegistry")
    return register_coordinator(coordinator, logger)


def get_coordinator(name: str) -> Optional[UnifiedCoordinatorBase]:
    """Get a coordinator by name from the global registry (backward compatibility)."""
    import logging
    logger = logging.getLogger("CoordinatorRegistry")
    return get_coordinator(name, logger)


def get_all_coordinators() -> Dict[str, UnifiedCoordinatorBase]:
    """Get all coordinators from the global registry (backward compatibility)."""
    import logging
    logger = logging.getLogger("CoordinatorRegistry")
    return get_all_coordinators(logger)


def get_all_coordinator_statuses() -> Dict[str, Dict[str, Any]]:
    """Get status of all coordinators from the global registry (backward compatibility)."""
    import logging
    logger = logging.getLogger("CoordinatorRegistry")
    return get_all_coordinator_statuses(logger)

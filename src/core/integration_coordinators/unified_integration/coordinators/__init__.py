"""
Unified Integration Coordinators - V2 Compliant Modular Architecture
===================================================================

Modular coordinator system for integration operations.
Each module handles a specific aspect of coordination.

V2 Compliance: < 300 lines per module, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from .coordinator import UnifiedIntegrationCoordinator
from .task_manager import TaskManager
from .health_monitor import HealthMonitor
from .config_manager import ConfigManager

__all__ = [
    'UnifiedIntegrationCoordinator',
    'TaskManager',
    'HealthMonitor',
    'ConfigManager'
]

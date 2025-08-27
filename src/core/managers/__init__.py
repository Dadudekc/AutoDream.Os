#!/usr/bin/env python3
"""
Base Manager Package - Agent Cellphone V2
========================================

Package containing refactored base manager components.
Follows Single Responsibility Principle for better maintainability.

**Author:** Agent-3 (Integration & Testing)
**Created:** Current Sprint
**Status:** ACTIVE - REFACTORING IN PROGRESS
"""

from .base_manager_types import (
    ManagerStatus, ManagerPriority, ManagerMetrics, ManagerConfig
)
from .base_manager_interface import BaseManagerInterface
from .base_manager_lifecycle import BaseManagerLifecycle
from .base_manager_monitoring import BaseManagerMonitoring
from .base_manager_config import BaseManagerConfiguration
from .base_manager_utils import BaseManagerUtils

__all__ = [
    "ManagerStatus",
    "ManagerPriority", 
    "ManagerMetrics",
    "ManagerConfig",
    "BaseManagerInterface",
    "BaseManagerLifecycle",
    "BaseManagerMonitoring",
    "BaseManagerConfiguration",
    "BaseManagerUtils"
]

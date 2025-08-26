#!/usr/bin/env python3
"""
Managers Package - V2 Core Manager Consolidation System
======================================================

Specialized managers inheriting from BaseManager.
Eliminates 80% duplication across 42 manager files.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .system_manager import SystemManager
from .config_manager import ConfigManager
from .status_manager import StatusManager
from .task_manager import TaskManager
from .data_manager import DataManager
from .communication_manager import CommunicationManager
from .health_manager import HealthManager
from .unified_manager_system import UnifiedManagerSystem

# Performance manager will be created as part of TASK 3B
# from .performance_manager import PerformanceManager

__all__ = [
    'SystemManager',
    'ConfigManager', 
    'StatusManager',
    'TaskManager',
    'DataManager',
    'CommunicationManager',
    'HealthManager',
    'UnifiedManagerSystem',
    # 'PerformanceManager'  # Will be added when TASK 3B is complete
]

# Version information
__version__ = "2.0.0"
__author__ = "V2 SWARM CAPTAIN"
__description__ = "Consolidated manager system eliminating 80% duplication"

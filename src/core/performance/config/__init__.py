
# MIGRATED: This file has been migrated to the centralized configuration system
#!/usr/bin/env python3
"""
Performance Configuration Package - V2 Modular Architecture
==========================================================

Modular configuration system for performance management.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .validation_config import ValidationThreshold, ValidationConfig
from .benchmark_config import BenchmarkConfig, BenchmarkExecutionConfig
from .system_config import SystemConfig, PerformanceTargets
from .alert_config import AlertConfig, AlertChannel
from .config_manager import PerformanceConfigManager

__all__ = [
    "ValidationThreshold",
    "ValidationConfig", 
    "BenchmarkConfig",
    "BenchmarkExecutionConfig",
    "SystemConfig",
    "PerformanceTargets",
    "AlertConfig",
    "AlertChannel",
    "PerformanceConfigManager"
]

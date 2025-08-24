#!/usr/bin/env python3
"""
Health Core Package - Agent Cellphone V2
========================================

Core health monitoring functionality extracted into modular components.
Follows V2 standards: ≤200 LOC per module, SRP, OOP principles.
"""

from .monitor import HealthMonitor
from .checker import HealthChecker, AlertLevel
from .reporter import HealthReporter

__all__ = [
    "HealthMonitor",
    "HealthChecker", 
    "AlertLevel",
    "HealthReporter"
]

__version__ = "2.0.0"
__author__ = "Agent-3 (Integration & Testing Specialist)"
__status__ = "Production Ready"

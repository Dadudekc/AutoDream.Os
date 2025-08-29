#!/usr/bin/env python3
"""
Monitor Package - Agent Cellphone V2
===================================

Refactored agent status monitoring system.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

from .monitor_types import AgentStatus, AgentCapability, AgentInfo, MonitorConfig

from .monitor_core import AgentStatusMonitor
from ..health.monitoring.health_core import AgentHealthCoreMonitor as HealthMonitor
from .monitor_reporting import MonitorReporter

# Backward compatibility
__all__ = [
    "AgentStatus",
    "AgentCapability",
    "AgentInfo",
    "MonitorConfig",
    "AgentStatusMonitor",
    "HealthMonitor",
    "MonitorReporter",
]

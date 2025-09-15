#!/usr/bin/env python3
"""
🐝 INFRASTRUCTURE MONITORING INTEGRATION
Phase 2 Batch 2A: Infrastructure Health Dashboard Integration

This module integrates consolidated infrastructure components with the health monitoring system.
Now modularized for V2 compliance (≤400 lines).

For the full implementation, see: src/infrastructure/monitoring/
"""

from __future__ import annotations

from typing import Optional

# Import the modularized implementation
from .monitoring.infrastructure_monitoring_integration import (
    InfrastructureMonitoringIntegration as _InfrastructureMonitoringIntegration
)

# Re-export the main class for backward compatibility
InfrastructureMonitoringIntegration = _InfrastructureMonitoringIntegration

# Also export key components for direct access
from .monitoring.components.monitoring_components import MonitoringComponents
from .monitoring.components.infrastructure_services import InfrastructureServices
from .monitoring.components.performance_metrics import PerformanceMetricsCollector

__all__ = [
    "InfrastructureMonitoringIntegration",
    "MonitoringComponents",
    "InfrastructureServices", 
    "PerformanceMetricsCollector",
]
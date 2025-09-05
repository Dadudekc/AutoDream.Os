#!/usr/bin/env python3
"""
Performance Dashboard - V2 Compliant Redirect
=============================================

V2 compliance redirect to modular performance dashboard system.
Original monolithic implementation refactored into focused modules.

Author: Agent-3 - Infrastructure & DevOps Specialist (V2 Refactoring)
Created: 2025-01-28
Purpose: V2 compliant modular performance dashboard
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .unified_dashboard import (
    PerformanceDashboardOrchestrator,
    DashboardModels,
    DashboardEngine,
    DashboardReporter
)

# Backward compatibility aliases
PerformanceDashboard = PerformanceDashboardOrchestrator

# Factory function for backward compatibility
def get_performance_dashboard():
    """Get performance dashboard instance."""
    return PerformanceDashboardOrchestrator()

# Re-export for backward compatibility
__all__ = [
    'PerformanceDashboardOrchestrator',
    'DashboardModels',
    'DashboardEngine',
    'DashboardReporter',
    'PerformanceDashboard',
    'get_performance_dashboard'
]
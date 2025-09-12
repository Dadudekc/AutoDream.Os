#!/usr/bin/env python3
"""
Advanced Analytics Service - V2 COMPLIANT REDIRECT
=================================================

V2 COMPLIANT: This file now redirects to the modular analytics system.
The original monolithic implementation has been refactored into focused modules:
- metrics_collector.py (metrics collection)
- usage_analytics.py (usage analytics)
- performance_dashboard.py (dashboard generation)
- automated_reporting.py (reporting system)
- consolidated_analytics_service.py (main coordinator)

All modules are V2 compliant (<300 lines, focused responsibilities).

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

# Redirect to the new modular analytics system
from .analytics.consolidated_analytics_service import (
    ConsolidatedAnalyticsService,
    get_analytics_service,
    get_consolidated_analytics_service,
)

# Maintain backward compatibility by importing the main service
AdvancedAnalyticsService = ConsolidatedAnalyticsService

from .analytics.automated_reporting import AnalyticsResult

# Re-export key classes for backward compatibility
from .analytics.metrics_collector import MetricDataPoint

# Global service instance for backward compatibility
_analytics_service = None


def get_advanced_analytics_service():
    """Get the global advanced analytics service instance (backward compatibility)."""
    global _analytics_service
    if _analytics_service is None:
        _analytics_service = ConsolidatedAnalyticsService()
    return _analytics_service


# Export for backward compatibility
__all__ = [
    "AdvancedAnalyticsService",
    "ConsolidatedAnalyticsService",
    "get_analytics_service",
    "get_advanced_analytics_service",
    "get_consolidated_analytics_service",
    "MetricDataPoint",
    "AnalyticsResult",
]

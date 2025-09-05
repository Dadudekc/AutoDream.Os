#!/usr/bin/env python3
"""
Vector Integration Analytics Package - V2 Compliance
===================================================

Modular vector integration analytics system with V2 compliance.
Replaces the monolithic vector_integration_analytics.py.

Package Structure:
- vector_integration_models.py: Data models and configuration
- vector_integration_monitor.py: Real-time monitoring and alerting
- vector_integration_analytics_engine.py: Analytics processing engine
- vector_integration_analytics_orchestrator.py: Main orchestrator

V2 Compliance: Modular design, single responsibility, dependency injection.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

# Import main classes for easy access
from .vector_integration_models import (
    IntegrationConfig,
    PerformanceAlert,
    TrendAnalysis,
    PerformanceForecast,
    OptimizationRecommendation,
    PerformanceMetrics,
    AnalyticsMode,
    AlertLevel,
    create_default_config,
    create_performance_alert,
    create_trend_analysis,
    create_performance_forecast,
    create_optimization_recommendation
)

from .vector_integration_monitor import VectorIntegrationMonitor

from .vector_integration_analytics_engine import VectorIntegrationAnalyticsEngine

from .vector_integration_analytics_orchestrator import (
    VectorIntegrationAnalyticsOrchestrator,
    create_vector_integration_analytics,
    get_vector_integration_analytics,
    VectorIntegrationAnalytics
)

# Package metadata
__version__ = "2.0.0"
__author__ = "Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager"
__description__ = "Modular vector integration analytics system with V2 compliance"

# Export main interface functions
__all__ = [
    # Core classes
    "VectorIntegrationAnalyticsOrchestrator",
    "VectorIntegrationMonitor",
    "VectorIntegrationAnalyticsEngine",
    
    # Data models
    "IntegrationConfig",
    "PerformanceAlert",
    "TrendAnalysis",
    "PerformanceForecast",
    "OptimizationRecommendation",
    "PerformanceMetrics",
    
    # Enums
    "AnalyticsMode",
    "AlertLevel",
    
    # Factory functions
    "create_default_config",
    "create_performance_alert",
    "create_trend_analysis", 
    "create_performance_forecast",
    "create_optimization_recommendation",
    
    # Main interface functions
    "create_vector_integration_analytics",
    "get_vector_integration_analytics",
    
    # Backward compatibility
    "VectorIntegrationAnalytics"
]

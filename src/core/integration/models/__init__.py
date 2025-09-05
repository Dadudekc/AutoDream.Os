"""
Vector Integration Models - V2 Compliant Modular Architecture
============================================================

Modular model system for vector integration analytics.
Each module handles a specific aspect of data modeling.

V2 Compliance: < 300 lines per module, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from .vector_integration_models import (
    AnalyticsMode, AlertLevel, PerformanceAlert, TrendAnalysis,
    PerformanceForecast, OptimizationRecommendation, PerformanceMetrics,
    IntegrationConfig, create_default_config, create_performance_alert,
    create_trend_analysis, create_performance_forecast, create_optimization_recommendation
)
from .enums import AnalyticsMode, AlertLevel
from .data_models import PerformanceAlert, TrendAnalysis, PerformanceForecast, OptimizationRecommendation, PerformanceMetrics
from .config_models import IntegrationConfig

__all__ = [
    'AnalyticsMode', 'AlertLevel', 'PerformanceAlert', 'TrendAnalysis',
    'PerformanceForecast', 'OptimizationRecommendation', 'PerformanceMetrics',
    'IntegrationConfig', 'create_default_config', 'create_performance_alert',
    'create_trend_analysis', 'create_performance_forecast', 'create_optimization_recommendation'
]

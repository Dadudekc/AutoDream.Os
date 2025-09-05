#!/usr/bin/env python3
"""
Trading BI Analytics Package
============================

Modular trading business intelligence analytics system.
V2 COMPLIANT: Clean, focused, modular architecture.

@version 1.0.0 - V2 COMPLIANCE MODULAR PACKAGE
@license MIT
"""

# Import main orchestrator
from .trading_bi_orchestrator import (
    TradingBiAnalyticsOrchestrator,
    create_trading_bi_analytics_orchestrator
)

# Import individual engines
from .risk_analysis_engine import (
    RiskAnalysisEngine,
    create_risk_analysis_engine
)

from .performance_metrics_engine import (
    PerformanceMetricsEngine,
    create_performance_metrics_engine
)

from .market_trend_engine import (
    MarketTrendEngine,
    create_market_trend_engine
)

# Import data models
from .trading_bi_models import (
    RiskLevel,
    PerformanceMetrics,
    RiskMetrics,
    MarketTrend,
    PnLResult,
    TrendAnalysisConfig,
    RiskAssessmentConfig,
    PerformanceConfig
)

# Export all public interfaces
__all__ = [
    # Main orchestrator
    'TradingBiAnalyticsOrchestrator',
    'create_trading_bi_analytics_orchestrator',
    
    # Individual engines
    'RiskAnalysisEngine',
    'create_risk_analysis_engine',
    'PerformanceMetricsEngine', 
    'create_performance_metrics_engine',
    'MarketTrendEngine',
    'create_market_trend_engine',
    
    # Data models
    'RiskLevel',
    'PerformanceMetrics',
    'RiskMetrics',
    'MarketTrend',
    'PnLResult',
    'TrendAnalysisConfig',
    'RiskAssessmentConfig',
    'PerformanceConfig'
]

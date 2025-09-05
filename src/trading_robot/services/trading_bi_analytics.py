#!/usr/bin/env python3
"""
Trading Business Intelligence Analytics Service - V2 Compliant Redirect
======================================================================

V2 COMPLIANT: Modular architecture with clean separation of concerns.
Original monolithic implementation refactored into focused modules.

@version 2.0.0 - V2 COMPLIANCE MODULAR REFACTOR
@license MIT
"""

# Import the new modular orchestrator
from .analytics import (
    TradingBiAnalyticsOrchestrator,
    create_trading_bi_analytics_orchestrator,
    RiskLevel,
    PerformanceMetrics,
    RiskMetrics,
    MarketTrend,
    PnLResult,
    TrendAnalysisConfig,
    RiskAssessmentConfig,
    PerformanceConfig
)

# Re-export for backward compatibility
TradingBiAnalyticsService = TradingBiAnalyticsOrchestrator
create_trading_bi_analytics_service = create_trading_bi_analytics_orchestrator

# Export all public interfaces
__all__ = [
    'TradingBiAnalyticsService',
    'TradingBiAnalyticsOrchestrator', 
    'create_trading_bi_analytics_service',
    'create_trading_bi_analytics_orchestrator',
    'RiskLevel',
    'PerformanceMetrics',
    'RiskMetrics', 
    'MarketTrend',
    'PnLResult',
    'TrendAnalysisConfig',
    'RiskAssessmentConfig',
    'PerformanceConfig'
]

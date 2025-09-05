#!/usr/bin/env python3
"""
Trading Backtest Package
========================

Modular trading backtest system.
V2 COMPLIANT: Clean, focused, modular architecture.

@version 1.0.0 - V2 COMPLIANCE MODULAR PACKAGE
@license MIT
"""

# Import main orchestrator
from .tsla_atr_backtest_orchestrator import (
    TSLAATRBacktestOrchestrator,
    create_tsla_atr_backtest_orchestrator
)

# Import individual engines
from .data_management_engine import (
    DataManagementEngine,
    BacktestConfig,
    create_data_management_engine
)

from .technical_indicators_engine import (
    TechnicalIndicatorsEngine,
    IndicatorConfig,
    create_technical_indicators_engine
)

from .signal_detection_engine import (
    SignalDetectionEngine,
    SignalConfig,
    TradeSide,
    create_signal_detection_engine
)

from .position_management_engine import (
    PositionManagementEngine,
    PositionConfig,
    Trade,
    create_position_management_engine
)

from .performance_analytics_engine import (
    PerformanceAnalyticsEngine,
    AnalyticsConfig,
    create_performance_analytics_engine
)

# Export all public interfaces
__all__ = [
    # Main orchestrator
    'TSLAATRBacktestOrchestrator',
    'create_tsla_atr_backtest_orchestrator',
    
    # Individual engines
    'DataManagementEngine',
    'BacktestConfig',
    'create_data_management_engine',
    'TechnicalIndicatorsEngine',
    'IndicatorConfig',
    'create_technical_indicators_engine',
    'SignalDetectionEngine',
    'SignalConfig',
    'TradeSide',
    'create_signal_detection_engine',
    'PositionManagementEngine',
    'PositionConfig',
    'Trade',
    'create_position_management_engine',
    'PerformanceAnalyticsEngine',
    'AnalyticsConfig',
    'create_performance_analytics_engine'
]

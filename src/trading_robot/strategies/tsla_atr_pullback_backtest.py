#!/usr/bin/env python3
"""
TSLA ATR Pullback Strategy - V2 Compliant Redirect
==================================================

V2 COMPLIANT: Modular architecture with clean separation of concerns.
Original monolithic implementation refactored into focused modules.

@version 2.0.0 - V2 COMPLIANCE MODULAR REFACTOR
@license MIT
"""

# Import the new modular orchestrator
from .backtest import (
    TSLAATRBacktestOrchestrator,
    create_tsla_atr_backtest_orchestrator,
    BacktestConfig,
    TradeSide,
)

# Re-export for backward compatibility
TSLA_ATR_Pullback_Backtest = TSLAATRBacktestOrchestrator

# Export all public interfaces
__all__ = [
    "TSLA_ATR_Pullback_Backtest",
    "TSLAATRBacktestOrchestrator",
    "create_tsla_atr_backtest_orchestrator",
    "BacktestConfig",
    "TradeSide",
]

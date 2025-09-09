#!/usr/bin/env python3
"""
Trading BI Analytics Data Models
===============================

Data models and enums for trading business intelligence analytics.
V2 COMPLIANT: Focused data structures under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR MODELS
@license MIT
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class RiskLevel(Enum):
    """Risk assessment levels for trading positions."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class PerformanceMetrics:
    """Performance metrics data structure for trading analysis."""

    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    total_trades: int
    avg_trade_duration: timedelta
    timestamp: datetime


@dataclass
class RiskMetrics:
    """Risk assessment metrics for portfolio analysis."""

    portfolio_volatility: float
    value_at_risk: float
    expected_shortfall: float
    beta_coefficient: float
    risk_level: RiskLevel
    max_position_size: float
    timestamp: datetime


@dataclass
class MarketTrend:
    """Market trend analysis data structure."""

    direction: str  # 'bullish', 'bearish', 'sideways'
    strength: float  # 0-1 scale
    confidence: float  # 0-1 scale
    predicted_change: float  # percentage
    timeframe: str  # 'short', 'medium', 'long'
    timestamp: datetime


@dataclass
class PnLResult:
    """P&L calculation result structure."""

    symbol: str
    pnl: float
    pnl_percentage: float
    position_value: float
    timestamp: datetime


@dataclass
class TrendAnalysisConfig:
    """Configuration for trend analysis."""

    min_trades_for_analysis: int = 10
    confidence_threshold: float = 0.7
    strength_threshold: float = 0.5
    timeframe_mapping: dict[str, int] = None

    def __post_init__(self):
        if self.timeframe_mapping is None:
            self.timeframe_mapping = {"short": 5, "medium": 20, "long": 50}


@dataclass
class RiskAssessmentConfig:
    """Configuration for risk assessment."""

    var_confidence_level: float = 0.95
    critical_var_threshold: float = 0.05
    critical_volatility_threshold: float = 0.03
    high_var_threshold: float = 0.03
    high_volatility_threshold: float = 0.02
    medium_var_threshold: float = 0.02
    medium_volatility_threshold: float = 0.015


@dataclass
class PerformanceConfig:
    """Configuration for performance metrics calculation."""

    risk_free_rate: float = 0.02  # Annual risk-free rate
    min_trades_for_metrics: int = 5
    drawdown_calculation_method: str = "peak_to_trough"  # or "rolling"


# Export all models
__all__ = [
    "RiskLevel",
    "PerformanceMetrics",
    "RiskMetrics",
    "MarketTrend",
    "PnLResult",
    "TrendAnalysisConfig",
    "RiskAssessmentConfig",
    "PerformanceConfig",
]

"""
Financial Analytics Data Models - V2 Compliant Data Structures

This module contains all financial analytics data models and classes.
Follows V2 standards with ≤200 LOC and single responsibility for data structures.
"""

from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass
import pandas as pd


@dataclass
class BacktestResult:
    """Backtesting result data"""
    
    strategy_name: str
    start_date: datetime
    end_date: datetime
    total_return: float
    annualized_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_win: float
    avg_loss: float
    largest_win: float
    largest_loss: float
    consecutive_wins: int
    consecutive_losses: int
    equity_curve: List[float]
    trade_history: List[Dict[str, Any]]
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class PerformanceMetrics:
    """Comprehensive performance metrics"""
    
    returns: pd.Series
    cumulative_returns: pd.Series
    drawdown: pd.Series
    rolling_sharpe: pd.Series
    rolling_volatility: pd.Series
    rolling_beta: pd.Series
    rolling_alpha: pd.Series
    value_at_risk: float
    conditional_var: float
    calmar_ratio: float
    sortino_ratio: float
    sharpe_ratio: float
    information_ratio: float
    treynor_ratio: float
    jensen_alpha: float
    tracking_error: float
    correlation: float


@dataclass
class RiskAnalysis:
    """Comprehensive risk analysis"""
    
    volatility_analysis: Dict[str, float]
    drawdown_analysis: Dict[str, float]
    var_analysis: Dict[str, float]
    correlation_analysis: Dict[str, float]
    stress_test_results: Dict[str, float]
    scenario_analysis: Dict[str, float]
    risk_decomposition: Dict[str, float]


@dataclass
class BacktestParameters:
    """Backtesting configuration parameters"""
    
    initial_capital: float = 100000
    commission: float = 0.001  # 0.1%
    slippage: float = 0.0005   # 0.05%
    risk_free_rate: float = 0.02  # 2%
    benchmark: str = "SPY"  # S&P 500 ETF
    confidence_level: float = 0.95  # For VaR calculations


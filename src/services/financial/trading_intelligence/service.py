"""Trading Intelligence Service package"""
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any

import numpy as np
import pandas as pd

from src.utils.stability_improvements import stability_manager, safe_import

from .models import (
    StrategyType,
    SignalType,
    SignalStrength,
    TradingSignal,
    StrategyPerformance,
    MarketCondition,
)
from .data_processing import calculate_rsi, analyze_market_conditions
from .strategy_analysis import (
    momentum_strategy,
    mean_reversion_strategy,
    breakout_strategy,
    scalping_strategy,
    pairs_trading_strategy,
    grid_trading_strategy,
)
from .execution import generate_trading_signals, update_signal_performance
from .reporting import get_strategy_recommendations, save_data, load_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TradingIntelligenceService:
    """Advanced trading intelligence and strategy execution service"""

    def __init__(self, market_data_service=None, data_dir: str = "trading_intelligence"):
        self.market_data_service = market_data_service
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        self.strategies: Dict[StrategyType, Callable] = {}
        self.performance_metrics: Dict[StrategyType, StrategyPerformance] = {}
        self.active_signals: List[TradingSignal] = []
        self.market_conditions: Optional[MarketCondition] = None

        self.signals_file = self.data_dir / "trading_signals.json"
        self.performance_file = self.data_dir / "strategy_performance.json"

        self.strategy_params = {
            StrategyType.MOMENTUM: {
                "lookback_period": 20,
                "momentum_threshold": 0.02,
                "volume_threshold": 1.5,
                "strong_momentum": 0.05,
                "strong_volume": 2.0,
                "rsi_upper": 70,
                "rsi_lower": 30,
                "base_confidence": 0.6,
                "strong_confidence": 0.8,
            },
            StrategyType.MEAN_REVERSION: {
                "lookback_period": 50,
                "std_dev_threshold": 2.0,
                "strong_threshold": 3.0,
                "reversion_strength": 0.1,
                "base_confidence": 0.6,
                "strong_confidence": 0.8,
            },
            StrategyType.BREAKOUT: {
                "breakout_period": 20,
                "volume_multiplier": 1.5,
                "breakout_buffer": 0.01,
                "target_multiplier": 0.05,
                "base_confidence": 0.7,
            },
            StrategyType.SCALPING: {
                "sma_short": 5,
                "sma_long": 10,
                "min_spread": 0.001,
                "profit_target": 0.002,
                "volatility_threshold": 0.01,
                "stop_loss_pct": 0.001,
                "base_confidence": 0.6,
            },
            StrategyType.PAIRS_TRADING: {
                "min_history": 50,
                "correlation_threshold": 0.7,
                "z_score_threshold": 2.0,
                "base_confidence": 0.7,
            },
            StrategyType.GRID_TRADING: {
                "grid_levels": 5,
                "price_range_pct": 0.1,
                "min_history": 20,
            },
        }

        self.initialize_strategies()
        self.load_data()

    def initialize_strategies(self):
        """Initialize trading strategies"""
        self.strategies = {
            StrategyType.MOMENTUM: self.momentum_strategy,
            StrategyType.MEAN_REVERSION: self.mean_reversion_strategy,
            StrategyType.BREAKOUT: self.breakout_strategy,
            StrategyType.SCALPING: self.scalping_strategy,
            StrategyType.PAIRS_TRADING: self.pairs_trading_strategy,
            StrategyType.GRID_TRADING: self.grid_trading_strategy,
        }
        for strategy_type in StrategyType:
            self.performance_metrics[strategy_type] = StrategyPerformance(
                strategy_type=strategy_type,
                total_signals=0,
                successful_signals=0,
                win_rate=0.0,
                avg_return=0.0,
                max_drawdown=0.0,
                sharpe_ratio=0.0,
                total_pnl=0.0,
            )

    # Bind methods from modules
    analyze_market_conditions = analyze_market_conditions
    calculate_rsi = staticmethod(calculate_rsi)

    momentum_strategy = momentum_strategy
    mean_reversion_strategy = mean_reversion_strategy
    breakout_strategy = breakout_strategy
    scalping_strategy = scalping_strategy
    pairs_trading_strategy = pairs_trading_strategy
    grid_trading_strategy = grid_trading_strategy

    generate_trading_signals = generate_trading_signals
    update_signal_performance = update_signal_performance

    get_strategy_recommendations = get_strategy_recommendations
    save_data = save_data
    load_data = load_data

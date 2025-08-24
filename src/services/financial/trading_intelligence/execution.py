import logging
from datetime import datetime
from typing import List
import numpy as np

from .models import TradingSignal, StrategyType, SignalType, SignalStrength

logger = logging.getLogger(__name__)


def generate_trading_signals(self, symbols: List[str]) -> List[TradingSignal]:
    """Generate trading signals for multiple symbols"""
    try:
        signals: List[TradingSignal] = []
        hist_data_map = {}
        if self.market_data_service:
            for symbol in symbols:
                historical_data = self.market_data_service.get_historical_data(symbol, period="3mo")
                if not historical_data:
                    continue
                hist_data_map[symbol] = historical_data
                for strategy_type, strategy_func in self.strategies.items():
                    if strategy_type == StrategyType.PAIRS_TRADING:
                        continue
                    signal = strategy_func(symbol, historical_data.data)
                    if signal:
                        if isinstance(signal, list):
                            signals.extend(signal)
                        else:
                            signals.append(signal)
        if len(hist_data_map) >= 2:
            symbols_with_data = list(hist_data_map.keys())
            for i in range(len(symbols_with_data)):
                for j in range(i + 1, len(symbols_with_data)):
                    hist1 = hist_data_map[symbols_with_data[i]]
                    hist2 = hist_data_map[symbols_with_data[j]]
                    pairs_signal = self.pairs_trading_strategy(
                        symbols_with_data[i], symbols_with_data[j], hist1.data, hist2.data
                    )
                    if pairs_signal:
                        if isinstance(pairs_signal, list):
                            signals.extend(pairs_signal)
                        else:
                            signals.append(pairs_signal)
        self.active_signals.extend(signals)
        self.save_data()
        return signals
    except Exception as e:
        logger.error(f"Error generating trading signals: {e}")
        return []


def update_signal_performance(self, signal: TradingSignal, exit_price: float, exit_time: datetime):
    """Update strategy performance metrics"""
    try:
        strategy_type = signal.strategy
        if strategy_type not in self.performance_metrics:
            return
        if signal.signal_type in [SignalType.BUY, SignalType.STRONG_BUY]:
            return_pct = (exit_price - signal.price) / signal.price
        else:
            return_pct = (signal.price - exit_price) / signal.price
        metrics = self.performance_metrics[strategy_type]
        metrics.total_signals += 1
        if return_pct > 0:
            metrics.successful_signals += 1
        metrics.win_rate = metrics.successful_signals / metrics.total_signals
        total_return = metrics.avg_return * (metrics.total_signals - 1) + return_pct
        metrics.avg_return = total_return / metrics.total_signals
        metrics.total_pnl += return_pct
        if return_pct < metrics.max_drawdown:
            metrics.max_drawdown = return_pct
        metrics.returns.append(return_pct)
        if len(metrics.returns) > 1:
            metrics.sharpe_ratio = (
                np.mean(metrics.returns) / np.std(metrics.returns)
                if np.std(metrics.returns) > 0
                else 0
            )
        metrics.last_updated = datetime.now()
        self.save_data()
    except Exception as e:
        logger.error(f"Error updating signal performance: {e}")

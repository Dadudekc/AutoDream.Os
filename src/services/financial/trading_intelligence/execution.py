import logging
from datetime import datetime
from typing import List
import numpy as np

from .models import TradingSignal, StrategyType, SignalType, SignalStrength

logger = logging.getLogger(__name__)


def generate_trading_signals(self, symbols: List[str]) -> List[TradingSignal]:
    """Generate trading signals for multiple symbols"""
    try:
        signals = []
        for symbol in symbols:
            if self.market_data_service:
                historical_data = self.market_data_service.get_historical_data(symbol, period="3mo")
                if not historical_data:
                    continue
                for strategy_type, strategy_func in self.strategies.items():
                    if strategy_type == StrategyType.PAIRS_TRADING:
                        continue
                    signal = strategy_func(symbol, historical_data.data)
                    if signal:
                        signals.append(signal)
        if len(symbols) >= 2 and self.market_data_service:
            for i in range(len(symbols)):
                for j in range(i + 1, len(symbols)):
                    hist1 = self.market_data_service.get_historical_data(symbols[i], period="3mo")
                    hist2 = self.market_data_service.get_historical_data(symbols[j], period="3mo")
                    if hist1 and hist2:
                        pairs_signal = self.pairs_trading_strategy(symbols[i], symbols[j], hist1.data, hist2.data)
                        if pairs_signal:
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
        if metrics.total_signals > 1:
            returns = [return_pct]
            metrics.sharpe_ratio = np.mean(returns) / np.std(returns) if np.std(returns) > 0 else 0
        metrics.last_updated = datetime.now()
        self.save_data()
    except Exception as e:
        logger.error(f"Error updating signal performance: {e}")

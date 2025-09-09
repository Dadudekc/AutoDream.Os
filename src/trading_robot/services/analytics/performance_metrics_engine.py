#!/usr/bin/env python3
"""
Trading BI Performance Metrics Engine
====================================

Performance metrics engine for trading business intelligence analytics.
Handles returns, Sharpe ratio, drawdown, win rate, and profit factor calculations.
V2 COMPLIANT: Focused performance analysis under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR PERFORMANCE ENGINE
@license MIT
"""

import statistics
from datetime import datetime, timedelta

from ...repositories.trading_repository import Trade
from .trading_bi_models import PerformanceConfig, PerformanceMetrics


class PerformanceMetricsEngine:
    """Performance metrics engine for trading portfolio analysis."""

    def __init__(self, config: PerformanceConfig | None = None):
        """Initialize performance metrics engine with configuration."""
        self.config = config or PerformanceConfig()

    def calculate_performance_metrics(self, trades: list[Trade]) -> PerformanceMetrics:
        """Calculate comprehensive performance metrics for trading portfolio."""
        try:
            if not trades or len(trades) < self.config.min_trades_for_metrics:
                return self._create_default_performance_metrics()

            # Calculate all performance metrics
            total_return = self._calculate_total_return(trades)
            sharpe_ratio = self._calculate_sharpe_ratio(trades)
            max_drawdown = self._calculate_max_drawdown(trades)
            win_rate = self._calculate_win_rate(trades)
            profit_factor = self._calculate_profit_factor(trades)
            avg_duration = self._calculate_avg_trade_duration(trades)

            return PerformanceMetrics(
                total_return=total_return,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown,
                win_rate=win_rate,
                profit_factor=profit_factor,
                total_trades=len(trades),
                avg_trade_duration=avg_duration,
                timestamp=datetime.now(),
            )

        except Exception:
            # Return default metrics on error
            return self._create_default_performance_metrics()

    def _calculate_total_return(self, trades: list[Trade]) -> float:
        """Calculate total return from trades."""
        if not trades:
            return 0.0

        # Simplified total return calculation
        total_cost = sum(trade.quantity * trade.price for trade in trades if trade.side == "buy")
        total_revenue = sum(
            trade.quantity * trade.price for trade in trades if trade.side == "sell"
        )

        if total_cost == 0:
            return 0.0

        return ((total_revenue - total_cost) / total_cost) * 100

    def _calculate_sharpe_ratio(self, trades: list[Trade]) -> float:
        """Calculate Sharpe ratio."""
        returns = self._calculate_returns_series(trades)

        if len(returns) < 2:
            return 0.0

        avg_return = statistics.mean(returns)
        volatility = statistics.stdev(returns)

        if volatility == 0:
            return 0.0

        # Use configured risk-free rate
        risk_free_rate = self.config.risk_free_rate / 252  # Daily risk-free rate
        return (avg_return - risk_free_rate) / volatility

    def _calculate_max_drawdown(self, trades: list[Trade]) -> float:
        """Calculate maximum drawdown."""
        if not trades:
            return 0.0

        trades_sorted = sorted(trades, key=lambda x: x.timestamp)

        if self.config.drawdown_calculation_method == "peak_to_trough":
            return self._calculate_peak_to_trough_drawdown(trades_sorted)
        else:
            return self._calculate_rolling_drawdown(trades_sorted)

    def _calculate_peak_to_trough_drawdown(self, trades_sorted: list[Trade]) -> float:
        """Calculate peak-to-trough drawdown."""
        peak = trades_sorted[0].price
        max_drawdown = 0.0

        for trade in trades_sorted:
            if trade.price > peak:
                peak = trade.price
            drawdown = (peak - trade.price) / peak
            max_drawdown = max(max_drawdown, drawdown)

        return max_drawdown * 100

    def _calculate_rolling_drawdown(self, trades_sorted: list[Trade]) -> float:
        """Calculate rolling drawdown (simplified)"""
        # Simplified rolling drawdown calculation
        prices = [trade.price for trade in trades_sorted]
        max_drawdown = 0.0

        for i in range(1, len(prices)):
            peak = max(prices[: i + 1])
            drawdown = (peak - prices[i]) / peak
            max_drawdown = max(max_drawdown, drawdown)

        return max_drawdown * 100

    def _calculate_win_rate(self, trades: list[Trade]) -> float:
        """Calculate win rate percentage."""
        if not trades:
            return 0.0

        # Group trades by symbol for win/loss calculation
        symbol_trades = self._group_trades_by_symbol(trades)

        winning_trades = 0
        total_trades = 0

        for symbol, trade_list in symbol_trades.items():
            if len(trade_list) >= 2:
                buy_trades = [t for t in trade_list if t.side == "buy"]
                sell_trades = [t for t in trade_list if t.side == "sell"]

                if buy_trades and sell_trades:
                    avg_buy_price = statistics.mean(t.price for t in buy_trades)
                    avg_sell_price = statistics.mean(t.price for t in sell_trades)

                    if avg_sell_price > avg_buy_price:
                        winning_trades += 1
                    total_trades += 1

        return (winning_trades / total_trades * 100) if total_trades > 0 else 0.0

    def _calculate_profit_factor(self, trades: list[Trade]) -> float:
        """Calculate profit factor."""
        if not trades:
            return 0.0

        # Group by symbol and calculate P&L
        symbol_trades = self._group_trades_by_symbol(trades)

        profits = []
        losses = []

        for symbol, trade_list in symbol_trades.items():
            if len(trade_list) >= 2:
                buy_trades = [t for t in trade_list if t.side == "buy"]
                sell_trades = [t for t in trade_list if t.side == "sell"]

                if buy_trades and sell_trades:
                    total_buy = sum(t.quantity * t.price for t in buy_trades)
                    total_sell = sum(t.quantity * t.price for t in sell_trades)
                    pnl = total_sell - total_buy

                    if pnl > 0:
                        profits.append(pnl)
                    elif pnl < 0:
                        losses.append(abs(pnl))

        total_profits = sum(profits)
        total_losses = sum(losses)

        return total_profits / total_losses if total_losses > 0 else float("inf")

    def _calculate_avg_trade_duration(self, trades: list[Trade]) -> timedelta:
        """Calculate average trade duration."""
        if not trades:
            return timedelta(0)

        durations = []
        symbol_trades = self._group_trades_by_symbol(trades)

        for symbol, trade_list in symbol_trades.items():
            buy_times = [t.timestamp for t in trade_list if t.side == "buy"]
            sell_times = [t.timestamp for t in trade_list if t.side == "sell"]

            if buy_times and sell_times:
                # Simplified: assume first buy to last sell
                duration = sell_times[-1] - buy_times[0]
                durations.append(duration)

        return statistics.mean(durations) if durations else timedelta(0)

    def _calculate_returns_series(self, trades: list[Trade]) -> list[float]:
        """Calculate returns series from trades."""
        if not trades or len(trades) < 2:
            return []

        symbol_trades = self._group_trades_by_symbol(trades)
        returns = []

        for symbol_trades in symbol_trades.values():
            if len(symbol_trades) > 1:
                symbol_trades.sort(key=lambda x: x.timestamp)
                for i in range(1, len(symbol_trades)):
                    prev_price = symbol_trades[i - 1].price
                    curr_price = symbol_trades[i].price
                    if prev_price > 0:
                        daily_return = (curr_price - prev_price) / prev_price
                        returns.append(daily_return)

        return returns

    def _group_trades_by_symbol(self, trades: list[Trade]) -> dict[str, list[Trade]]:
        """Group trades by symbol."""
        symbol_trades = {}
        for trade in trades:
            if trade.symbol not in symbol_trades:
                symbol_trades[trade.symbol] = []
            symbol_trades[trade.symbol].append(trade)
        return symbol_trades

    def _create_default_performance_metrics(self) -> PerformanceMetrics:
        """Create default performance metrics when calculation fails."""
        return PerformanceMetrics(
            total_return=0.0,
            sharpe_ratio=0.0,
            max_drawdown=0.0,
            win_rate=0.0,
            profit_factor=0.0,
            total_trades=0,
            avg_trade_duration=timedelta(0),
            timestamp=datetime.now(),
        )


# Factory function for dependency injection
def create_performance_metrics_engine(
    config: PerformanceConfig | None = None,
) -> PerformanceMetricsEngine:
    """Factory function to create performance metrics engine with optional
    configuration."""
    return PerformanceMetricsEngine(config)


# Export for DI
__all__ = ["PerformanceMetricsEngine", "create_performance_metrics_engine"]

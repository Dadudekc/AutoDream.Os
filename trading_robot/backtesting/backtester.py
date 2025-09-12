"""
Backtesting System for Trading Strategies
"""
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from core.alpaca_client import AlpacaClient
from loguru import logger
from strategies.base_strategy import BaseStrategy, Signal, StrategyResult


class BacktestResult:
    """Results of a backtest"""

    def __init__(self):
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.win_rate = 0.0
        self.avg_win = 0.0
        self.avg_loss = 0.0
        self.profit_factor = 0.0
        self.max_drawdown = 0.0
        self.sharpe_ratio = 0.0
        self.total_return = 0.0
        self.annual_return = 0.0
        self.volatility = 0.0
        self.trades = []
        self.portfolio_values = []
        self.dates = []

    def calculate_metrics(self):
        """Calculate performance metrics"""
        if not self.trades:
            return

        # Basic metrics
        self.total_trades = len(self.trades)
        self.winning_trades = len([t for t in self.trades if t['pnl'] > 0])
        self.losing_trades = self.total_trades - self.winning_trades
        self.win_rate = self.winning_trades / self.total_trades if self.total_trades > 0 else 0

        # Profit metrics
        winning_pnls = [t['pnl'] for t in self.trades if t['pnl'] > 0]
        losing_pnls = [t['pnl'] for t in self.trades if t['pnl'] < 0]

        self.avg_win = np.mean(winning_pnls) if winning_pnls else 0
        self.avg_loss = np.mean(losing_pnls) if losing_pnls else 0

        total_wins = sum(winning_pnls)
        total_losses = abs(sum(losing_pnls))
        self.profit_factor = total_wins / total_losses if total_losses > 0 else float('inf')

        # Portfolio metrics
        if self.portfolio_values:
            self.total_return = (self.portfolio_values[-1] / self.portfolio_values[0] - 1) * 100

            # Calculate drawdown
            peak = self.portfolio_values[0]
            max_drawdown = 0

            for value in self.portfolio_values:
                if value > peak:
                    peak = value
                drawdown = (peak - value) / peak
                max_drawdown = max(max_drawdown, drawdown)

            self.max_drawdown = max_drawdown * 100

            # Calculate Sharpe ratio (simplified)
            if len(self.portfolio_values) > 1:
                returns = np.diff(np.log(self.portfolio_values))
                if len(returns) > 0:
                    self.sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252)

    def print_summary(self):
        """Print backtest summary"""
        print("\n" + "="*50)
        print("BACKTEST RESULTS SUMMARY")
        print("="*50)
        print(f"Total Trades: {self.total_trades}")
        print(f"Win Rate: {self.win_rate:.1%}")
        print(f"Average Win: ${self.avg_win:.2f}")
        print(f"Average Loss: ${self.avg_loss:.2f}")
        print(f"Profit Factor: {self.profit_factor:.2f}")
        print(f"Total Return: {self.total_return:.2f}%")
        print(f"Max Drawdown: {self.max_drawdown:.2f}%")
        print(f"Sharpe Ratio: {self.sharpe_ratio:.2f}")
        print("="*50)


class Backtester:
    """Backtesting engine for trading strategies"""

    def __init__(self, initial_balance: float = 100000.0):
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.positions = {}
        self.trades = []
        self.portfolio_history = []
        self.commission = 0.001  # 0.1% commission

    def run_backtest(self, strategy: BaseStrategy, data: pd.DataFrame,
                    symbol: str, start_date: datetime | None = None,
                    end_date: datetime | None = None) -> BacktestResult:
        """Run backtest for a strategy on historical data"""

        logger.info(f"🚀 Starting backtest for {strategy.name} on {symbol}")

        # Filter data by date range if specified
        if start_date:
            data = data[data.index >= start_date]
        if end_date:
            data = data[data.index <= end_date]

        if len(data) < 100:
            logger.warning("Insufficient data for backtesting")
            return BacktestResult()

        result = BacktestResult()
        result.portfolio_values.append(self.initial_balance)
        result.dates.append(data.index[0])

        # Reset state
        self.current_balance = self.initial_balance
        self.positions = {}
        self.trades = []
        self.portfolio_history = []

        # Run through each data point
        for i in range(100, len(data)):  # Start after enough data for indicators
            current_date = data.index[i]
            current_data = data.iloc[:i+1]

            try:
                # Get strategy signal
                strategy_result = strategy.analyze(current_data, symbol)

                # Execute trade if signal is strong enough
                if strategy_result.confidence > 0.6:
                    self._execute_trade(strategy_result, data.iloc[i], current_date, result)

                # Update portfolio value
                portfolio_value = self._calculate_portfolio_value(data.iloc[i])
                result.portfolio_values.append(portfolio_value)
                result.dates.append(current_date)

            except Exception as e:
                logger.error(f"Error processing {current_date}: {e}")

        # Close any remaining positions
        self._close_all_positions(data.iloc[-1], data.index[-1], result)

        # Calculate final metrics
        result.calculate_metrics()
        result.trades = self.trades.copy()

        logger.info(f"✅ Backtest completed for {strategy.name} on {symbol}")
        return result

    def _execute_trade(self, strategy_result: StrategyResult, current_bar: pd.Series,
                      current_date: datetime, result: BacktestResult):
        """Execute a trade based on strategy signal"""

        symbol = strategy_result.symbol
        signal = strategy_result.signal
        current_price = current_bar['close']

        # Calculate position size
        position_size = strategy.calculate_position_size(
            self.current_balance, current_price, 0.01  # 1% risk
        )

        if signal == Signal.BUY and symbol not in self.positions:
            # Open long position
            cost = position_size * current_price * (1 + self.commission)
            if cost <= self.current_balance:
                self.positions[symbol] = {
                    'quantity': position_size,
                    'entry_price': current_price,
                    'entry_date': current_date
                }
                self.current_balance -= cost
                logger.debug(f"📈 BUY {position_size} {symbol} @ {current_price}")

        elif signal == Signal.SELL:
            if symbol in self.positions:
                # Close long position
                position = self.positions[symbol]
                exit_value = position['quantity'] * current_price * (1 - self.commission)
                pnl = (current_price - position['entry_price']) * position['quantity']

                trade = {
                    'symbol': symbol,
                    'side': 'SELL',
                    'quantity': position['quantity'],
                    'entry_price': position['entry_price'],
                    'exit_price': current_price,
                    'entry_date': position['entry_date'],
                    'exit_date': current_date,
                    'pnl': pnl,
                    'commission': (position['quantity'] * position['entry_price'] * self.commission +
                                 position['quantity'] * current_price * self.commission)
                }

                self.trades.append(trade)
                self.current_balance += exit_value
                del self.positions[symbol]

                logger.debug(f"📉 SELL {position['quantity']} {symbol} @ {current_price}, PnL: ${pnl:.2f}")

    def _calculate_portfolio_value(self, current_bar: pd.Series) -> float:
        """Calculate current portfolio value"""
        cash = self.current_balance
        positions_value = 0

        for symbol, position in self.positions.items():
            current_price = current_bar['close']  # Assuming same symbol, adjust if needed
            positions_value += position['quantity'] * current_price

        return cash + positions_value

    def _close_all_positions(self, final_bar: pd.Series, final_date: datetime, result: BacktestResult):
        """Close all remaining positions at the end"""
        for symbol, position in list(self.positions.items()):
            current_price = final_bar['close']
            exit_value = position['quantity'] * current_price * (1 - self.commission)
            pnl = (current_price - position['entry_price']) * position['quantity']

            trade = {
                'symbol': symbol,
                'side': 'SELL',
                'quantity': position['quantity'],
                'entry_price': position['entry_price'],
                'exit_price': current_price,
                'entry_date': position['entry_date'],
                'exit_date': final_date,
                'pnl': pnl,
                'commission': (position['quantity'] * position['entry_price'] * self.commission +
                             position['quantity'] * current_price * self.commission)
            }

            self.trades.append(trade)
            self.current_balance += exit_value
            del self.positions[symbol]

    def run_walk_forward_optimization(self, strategy: BaseStrategy, data: pd.DataFrame,
                                    symbol: str, train_window: int = 252, test_window: int = 63) -> list[BacktestResult]:
        """Run walk-forward optimization"""
        results = []
        total_days = len(data)

        for start in range(0, total_days - train_window - test_window, test_window):
            train_end = start + train_window
            test_end = train_end + test_window

            if test_end > total_days:
                break

            # Training period
            train_data = data.iloc[start:train_end]

            # Testing period
            test_data = data.iloc[train_end:test_end]

            # Run backtest on test data
            result = self.run_backtest(strategy, test_data, symbol)
            results.append(result)

        return results


class BacktestVisualizer:
    """Visualization tools for backtest results"""

    @staticmethod
    def plot_portfolio_value(result: BacktestResult, title: str = "Portfolio Value"):
        """Plot portfolio value over time"""
        plt.figure(figsize=(12, 6))
        plt.plot(result.dates, result.portfolio_values)
        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value ($)")
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_drawdown(result: BacktestResult):
        """Plot drawdown chart"""
        portfolio_values = np.array(result.portfolio_values)
        peak = np.maximum.accumulate(portfolio_values)
        drawdown = (portfolio_values - peak) / peak * 100

        plt.figure(figsize=(12, 6))
        plt.fill_between(result.dates, drawdown, 0, alpha=0.3, color='red')
        plt.plot(result.dates, drawdown, color='red')
        plt.title("Portfolio Drawdown")
        plt.xlabel("Date")
        plt.ylabel("Drawdown (%)")
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_trade_distribution(result: BacktestResult):
        """Plot trade P&L distribution"""
        if not result.trades:
            return

        pnls = [trade['pnl'] for trade in result.trades]

        plt.figure(figsize=(10, 6))
        plt.hist(pnls, bins=50, alpha=0.7, edgecolor='black')
        plt.axvline(x=0, color='red', linestyle='--', alpha=0.7)
        plt.title("Trade P&L Distribution")
        plt.xlabel("P&L ($)")
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.show()


# Example usage function
def run_sample_backtest():
    """Example of how to run a backtest"""

    # Initialize Alpaca client
    client = AlpacaClient()
    client.connect()

    # Get historical data
    symbol = "AAPL"
    data = client.get_historical_data(symbol, "1Day", limit=1000)

    if data.empty:
        logger.error("No historical data available")
        return

    # Initialize strategy
    strategy = TrendFollowingStrategy({
        'fast_period': 10,
        'slow_period': 20,
        'rsi_period': 14
    })

    # Run backtest
    backtester = Backtester(initial_balance=100000)
    result = backtester.run_backtest(strategy, data, symbol)

    # Print results
    result.print_summary()

    # Visualize results
    BacktestVisualizer.plot_portfolio_value(result, f"{strategy.name} - {symbol}")
    BacktestVisualizer.plot_drawdown(result)
    BacktestVisualizer.plot_trade_distribution(result)

    return result


if __name__ == "__main__":
    # Run sample backtest
    result = run_sample_backtest()

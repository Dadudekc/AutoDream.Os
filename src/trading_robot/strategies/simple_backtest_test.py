from ..core.unified_entry_point_system import main
"""
Simple backtest test for TSLA ATR Pullback strategy
Test the core logic without external dependencies
"""


# Add the current directory to the Python path
sys.path.append(get_unified_utility().path.dirname(get_unified_utility().path.abspath(__file__)))

def create_test_data():
    """Create synthetic TSLA-like data for testing"""
    get_logger(__name__).info("Creating synthetic TSLA data for testing...")

    # Create date range (2 years of trading days)
    dates = pd.date_range(start="2022-01-01", end="2024-01-01", freq='D')
    dates = dates[dates.weekday < 5]  # Remove weekends

    np.random.seed(42)  # For reproducible results

    # TSLA-like price characteristics (volatile, trending)
    base_price = 250  # Starting around 2022 levels
    n_bars = len(dates)

    # Generate realistic price series with trend and volatility
    # Long-term upward trend with high volatility
    trend = np.linspace(0, 0.8, n_bars)  # Upward trend
    noise = np.random.normal(0, 0.025, n_bars)  # High volatility
    returns = trend * 0.001 + noise  # Combine trend and noise

    prices = base_price * np.exp(np.cumsum(returns))

    # Generate OHLC data
    volatility = np.abs(np.random.normal(0, 0.02, n_bars)) + 0.01
    highs = prices * (1 + volatility)
    lows = prices * (1 - volatility)
    opens = prices * (1 + np.random.normal(0, 0.005, n_bars))

    # Ensure OHLC relationships are correct
    highs = np.maximum(np.maximum(highs, opens), prices)
    lows = np.minimum(np.minimum(lows, opens), prices)

    # Create DataFrame
    df = pd.DataFrame({
        'open': opens,
        'high': highs,
        'low': lows,
        'close': prices,
        'volume': np.random.lognormal(15, 1, n_bars)
    }, index=dates)

    return df

def calculate_indicators(df):
    """Calculate technical indicators"""
    # Moving averages
    df['ma_short'] = df['close'].rolling(20).mean()
    df['ma_long'] = df['close'].rolling(50).mean()

    # RSI
    def calculate_rsi(prices, period=14):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    df['rsi'] = calculate_rsi(df['close'], 14)

    # ATR
    def calculate_atr(high, low, close, period=14):
        tr1 = high - low
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(period).mean()

    df['atr'] = calculate_atr(df['high'], df['low'], df['close'], 14)

    # Trend filters
    df['trend_up'] = (df['ma_short'] > df['ma_long']) & df['ma_short'].notna() & df['ma_long'].notna()
    df['trend_dn'] = (df['ma_short'] < df['ma_long']) & df['ma_short'].notna() & df['ma_long'].notna()

    # Session filter (simplified - just remove some random bars to simulate RTH)
    np.random.seed(123)
    df['in_session'] = np.random.choice([True, False], size=len(df), p=[0.8, 0.2])

    # Volatility filter
    df['vol_ok'] = (df['atr'] / df['close']) >= 0.004

    return df.dropna()

def simple_backtest(df, initial_capital=100000, risk_percent=0.5):
    """Run a simple backtest"""
    capital = initial_capital
    position = 0
    position_price = 0
    trades = []
    equity_curve = [capital]

    get_logger(__name__).info(f"Running backtest with ${initial_capital} capital, {risk_percent}% risk per trade")

    for i, (date, row) in enumerate(df.iterrows()):
        # Check for signals
        long_signal = (
            row['trend_up'] and
            row['close'] > row['ma_short'] and
            row['rsi'] < 70 and
            (row['rsi'] > df.iloc[i-1]['rsi'] if i > 0 else False) and
            row['in_session'] and
            row['vol_ok']
        )

        short_signal = (
            row['trend_dn'] and
            row['close'] < row['ma_short'] and
            row['rsi'] > 30 and
            (row['rsi'] < df.iloc[i-1]['rsi'] if i > 0 else False) and
            row['in_session'] and
            row['vol_ok']
        )

        # Exit logic
        if position != 0:
            entry_price = abs(position_price)
            stop_distance = row['atr'] * 2.0

            if position > 0:  # Long position
                stop_price = entry_price - stop_distance
                target_price = entry_price + stop_distance * 2.0

                if row['close'] <= stop_price or row['close'] >= target_price:
                    # Exit position
                    exit_price = row['close']
                    pnl = (exit_price - entry_price) * abs(position)
                    commission = abs(exit_price * abs(position)) * 0.0002  # 2bps
                    pnl -= commission

                    capital += pnl
                    trades.append({
                        'entry_date': position_price,  # This should be the entry date
                        'exit_date': date,
                        'side': 'LONG',
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'quantity': abs(position),
                        'pnl': pnl,
                        'pnl_pct': pnl / (entry_price * abs(position)) * 100
                    })

                    position = 0
                    position_price = 0

            elif position < 0:  # Short position
                stop_price = entry_price + stop_distance
                target_price = entry_price - stop_distance * 2.0

                if row['close'] >= stop_price or row['close'] <= target_price:
                    # Exit position
                    exit_price = row['close']
                    pnl = (entry_price - exit_price) * abs(position)
                    commission = abs(exit_price * abs(position)) * 0.0002
                    pnl -= commission

                    capital += pnl
                    trades.append({
                        'entry_date': position_price,
                        'exit_date': date,
                        'side': 'SHORT',
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'quantity': abs(position),
                        'pnl': pnl,
                        'pnl_pct': pnl / (entry_price * abs(position)) * 100
                    })

                    position = 0
                    position_price = 0

        # Entry logic
        elif long_signal or short_signal:
            # Calculate position size
            risk_amount = capital * (risk_percent / 100)
            stop_distance = row['atr'] * 2.0
            qty = risk_amount / stop_distance
            qty = max(1, qty)  # At least 1 share

            # Check if we have enough capital
            cost = qty * row['close']
            if cost <= capital:
                if long_signal:
                    position = qty
                    position_price = row['close']
                elif short_signal:
                    position = -qty
                    position_price = row['close']

                # Commission
                commission = cost * 0.0002
                capital -= commission

        # Record equity
        equity_curve.append(capital)

    return trades, equity_curve

def print_results(trades, equity_curve, initial_capital):
    """Print backtest results"""
    if not get_unified_validator().validate_required(trades):
        get_logger(__name__).info("No trades executed!")
        return

    get_logger(__name__).info("\n" + "="*60)
    get_logger(__name__).info("BACKTEST RESULTS - TSLA ATR Pullback Strategy")
    get_logger(__name__).info("="*60)

    # Basic statistics
    winning_trades = [t for t in trades if t['pnl'] > 0]
    losing_trades = [t for t in trades if t['pnl'] < 0]

    total_trades = len(trades)
    winning_count = len(winning_trades)
    losing_count = len(losing_trades)
    win_rate = winning_count / total_trades if total_trades > 0 else 0

    total_pnl = sum(t['pnl'] for t in trades)
    gross_profit = sum(t['pnl'] for t in winning_trades)
    gross_loss = abs(sum(t['pnl'] for t in losing_trades))
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')

    avg_win = gross_profit / winning_count if winning_count > 0 else 0
    avg_loss = gross_loss / losing_count if losing_count > 0 else 0
    avg_trade = total_pnl / total_trades if total_trades > 0 else 0

    final_capital = equity_curve[-1]
    total_return = ((final_capital - initial_capital) / initial_capital) * 100

    # Calculate max drawdown
    equity_series = pd.Series(equity_curve)
    peak = equity_series.expanding().max()
    drawdown = (equity_series - peak) / peak * 100
    max_drawdown = drawdown.min()

    get_logger(__name__).info(f"Initial Capital: ${initial_capital:,.2f}")
    get_logger(__name__).info(f"Final Capital: ${final_capital:,.2f}")
    get_logger(__name__).info(f"Total Return: {total_return:.2f}%")
    get_logger(__name__).info(f"Total Trades: {total_trades}")
    get_logger(__name__).info(f"Winning Trades: {winning_count}")
    get_logger(__name__).info(f"Losing Trades: {losing_count}")
    get_logger(__name__).info(f"Win Rate: {win_rate:.2f}%")
    get_logger(__name__).info(f"Profit Factor: {profit_factor:.2f}")
    get_logger(__name__).info(f"Average Win: ${avg_win:.2f}")
    get_logger(__name__).info(f"Average Loss: ${avg_loss:.2f}")
    get_logger(__name__).info(f"Average Trade: ${avg_trade:.2f}")
    get_logger(__name__).info(f"Max Drawdown: {max_drawdown:.2f}%")

    get_logger(__name__).info("\n" + "="*60)
    get_logger(__name__).info("RECENT TRADES")
    get_logger(__name__).info("="*60)

    # Show last 10 trades
    for i, trade in enumerate(trades[-10:], 1):
        get_logger(__name__).info(f"{i}. {trade['side']} | Entry: ${trade['entry_price']:.2f} | "
              f"Exit: ${trade['exit_price']:.2f} | P&L: ${trade['pnl']:.2f} ({trade['pnl_pct']:.2f}%)")


if __name__ == "__main__":
    main()

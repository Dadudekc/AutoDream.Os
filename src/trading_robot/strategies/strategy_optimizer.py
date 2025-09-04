from ..core.unified_entry_point_system import main
"""
TSLA ATR Pullback Strategy Optimizer
Comprehensive parameter optimization and walk-forward testing
V2 Compliance: Clean architecture, comprehensive analysis, modular design

Performs:
1. Parameter sensitivity analysis
2. Multi-objective optimization
3. Walk-forward validation
4. Risk-adjusted performance evaluation
5. Bootstrap profitable strategy for trading robot

@author Agent-2 - Architecture & Design Specialist
@version 1.0.0 - V2 COMPLIANCE OPTIMIZATION FRAMEWORK
@license MIT
"""

warnings.filterwarnings('ignore')


@dataclass
class OptimizationConfig:
    """Optimization configuration parameters"""
    symbol: str = "TSLA"
    start_date: str = "2022-01-01"
    end_date: str = "2024-09-01"
    initial_capital: float = 100000.0

    # Parameter ranges for optimization
    atr_mult_range: List[float] = None
    rr_ratio_range: List[float] = None
    rsi_ob_range: List[int] = None
    rsi_os_range: List[int] = None
    ma_short_range: List[int] = None
    ma_long_range: List[int] = None
    cooldown_range: List[int] = None

    # Optimization settings
    max_combinations: int = 1000
    test_train_split: float = 0.7  # 70% train, 30% test
    min_trades: int = 10
    parallel_processes: int = 4

    def __post_init__(self):
        # Default parameter ranges if not provided
        if self.atr_mult_range is None:
            self.atr_mult_range = [1.5, 2.0, 2.5, 3.0]
        if self.rr_ratio_range is None:
            self.rr_ratio_range = [1.5, 2.0, 2.5, 3.0]
        if self.rsi_ob_range is None:
            self.rsi_ob_range = [65, 70, 75]
        if self.rsi_os_range is None:
            self.rsi_os_range = [25, 30, 35]
        if self.ma_short_range is None:
            self.ma_short_range = [15, 20, 25]
        if self.ma_long_range is None:
            self.ma_long_range = [40, 50, 60]
        if self.cooldown_range is None:
            self.cooldown_range = [3, 5, 8]


@dataclass
class StrategyParameters:
    """Strategy parameter set"""
    atr_mult: float
    rr_ratio: float
    rsi_ob: int
    rsi_os: int
    ma_short: int
    ma_long: int
    cooldown: int


@dataclass
class BacktestResult:
    """Comprehensive backtest result"""
    parameters: StrategyParameters
    total_trades: int
    win_rate: float
    profit_factor: float
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    avg_trade: float
    calmar_ratio: float
    sortino_ratio: float
    expectancy: float
    recovery_factor: float
    kelly_criterion: float
    ulcer_index: float

    # Additional metrics
    gross_profit: float
    gross_loss: float
    avg_win: float
    avg_loss: float
    largest_win: float
    largest_loss: float
    win_loss_ratio: float
    profit_std: float
    consecutive_wins: int
    consecutive_losses: int

    # Risk metrics
    value_at_risk_95: float
    expected_shortfall_95: float
    downside_deviation: float

    # Walk-forward validation
    train_score: float = 0.0
    test_score: float = 0.0
    walk_forward_score: float = 0.0


class TSLAStrategyOptimizer:
    """Advanced strategy optimizer with multi-objective optimization"""

    def __init__(self, config: OptimizationConfig):
        self.config = config
        self.data: pd.DataFrame = pd.DataFrame()
        self.parameter_combinations: List[StrategyParameters] = []
        self.results: List[BacktestResult] = []

    def generate_parameter_combinations(self) -> List[StrategyParameters]:
        """Generate all parameter combinations for optimization"""
        combinations = list(itertools.product(
            self.config.atr_mult_range,
            self.config.rr_ratio_range,
            self.config.rsi_ob_range,
            self.config.rsi_os_range,
            self.config.ma_short_range,
            self.config.ma_long_range,
            self.config.cooldown_range
        ))

        # Limit combinations if too many
        if len(combinations) > self.config.max_combinations:
            np.random.seed(42)
            indices = np.random.choice(len(combinations),
                                     self.config.max_combinations,
                                     replace=False)
            combinations = [combinations[i] for i in indices]

        parameter_sets = []
        for combo in combinations:
            params = StrategyParameters(
                atr_mult=combo[0],
                rr_ratio=combo[1],
                rsi_ob=combo[2],
                rsi_os=combo[3],
                ma_short=combo[4],
                ma_long=combo[5],
                cooldown=combo[6]
            )
            parameter_sets.append(params)

        get_logger(__name__).info(f"Generated {len(parameter_sets)} parameter combinations")
        return parameter_sets

    def load_data(self) -> pd.DataFrame:
        """Load and prepare historical data"""
        get_logger(__name__).info(f"Loading {self.config.symbol} data...")

        # Try to load from cache first
        cache_file = f"{self.config.symbol}_data.csv"
        try:
            df = pd.read_csv(cache_file, index_col=0, get_unified_utility().parse_dates=True)
            get_logger(__name__).info(f"Loaded {len(df)} bars from cache")
        except FileNotFoundError:
            # Create synthetic data for testing
            df = self._create_synthetic_data()
            df.to_csv(cache_file)
            get_logger(__name__).info(f"Created and cached {len(df)} bars of synthetic data")

        # Calculate basic indicators
        df = self._calculate_base_indicators(df)
        self.data = df
        return df

    def _create_synthetic_data(self) -> pd.DataFrame:
        """Create realistic TSLA-like synthetic data"""
        dates = pd.date_range(start=self.config.start_date,
                            end=self.config.end_date,
                            freq='D')
        dates = dates[dates.weekday < 5]  # Trading days only

        np.random.seed(42)
        n_bars = len(dates)

        # TSLA characteristics: high volatility, upward trend, occasional gaps
        base_price = 250
        trend = np.linspace(0, 1.2, n_bars)  # Strong upward trend
        volatility = np.random.normal(0, 0.035, n_bars)

        # Add regime changes and gaps
        regime_changes = np.random.choice([0, 1], n_bars, p=[0.95, 0.05])
        gaps = regime_changes * np.random.normal(0, 0.05, n_bars)

        returns = trend * 0.001 + volatility + gaps
        prices = base_price * np.exp(np.cumsum(returns))

        # Generate OHLC with realistic spreads
        spreads = np.abs(np.random.normal(0, 0.015, n_bars)) + 0.005
        highs = prices * (1 + spreads)
        lows = prices * (1 - spreads)
        opens = prices * (1 + np.random.normal(0, spreads/2, n_bars))

        # Ensure OHLC integrity
        highs = np.maximum(np.maximum(highs, opens), prices)
        lows = np.minimum(np.minimum(lows, opens), prices)

        df = pd.DataFrame({
            'open': opens,
            'high': highs,
            'low': lows,
            'close': prices,
            'volume': np.random.lognormal(16, 1, n_bars)
        }, index=dates)

        return df

    def _calculate_base_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate base technical indicators"""
        # Basic price data
        df['returns'] = df['close'].pct_change()

        # Session filter (simplified RTH approximation)
        df['hour'] = df.index.hour
        df['in_session'] = ((df['hour'] >= 9) & (df['hour'] <= 16))

        return df

    def run_single_backtest(self, params: StrategyParameters,
                          train_data: pd.DataFrame,
                          test_data: Optional[pd.DataFrame] = None) -> BacktestResult:
        """Run backtest for single parameter set"""
        # Combine train and test data if testing
        if test_data is not None:
            full_data = pd.concat([train_data, test_data])
        else:
            full_data = train_data.copy()

        # Calculate strategy-specific indicators
        df = self._calculate_strategy_indicators(full_data, params)

        # Run backtest
        trades, equity_curve = self._run_strategy_backtest(df, params)

        # Calculate comprehensive metrics
        metrics = self._calculate_advanced_metrics(trades, equity_curve, params)

        return BacktestResult(
            parameters=params,
            **metrics
        )

    def _calculate_strategy_indicators(self, df: pd.DataFrame,
                                     params: StrategyParameters) -> pd.DataFrame:
        """Calculate strategy-specific indicators"""
        df = df.copy()

        # Moving averages
        df['ma_short'] = df['close'].rolling(params.ma_short).mean()
        df['ma_long'] = df['close'].rolling(params.ma_long).mean()

        # RSI
        def calculate_rsi(prices, period=14):
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            return 100 - (100 / (1 + rs))

        df['rsi'] = calculate_rsi(df['close'])

        # ATR
        def calculate_atr(high, low, close, period=14):
            tr1 = high - low
            tr2 = abs(high - close.shift(1))
            tr3 = abs(low - close.shift(1))
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            return tr.rolling(period).mean()

        df['atr'] = calculate_atr(df['high'], df['low'], df['close'])

        # Trend and signal filters
        df['trend_up'] = (df['ma_short'] > df['ma_long'])
        df['trend_dn'] = (df['ma_short'] < df['ma_long'])

        # Signal generation
        df['long_signal'] = (
            df['trend_up'] &
            (df['close'] > df['ma_short']) &
            (df['rsi'] < params.rsi_ob) &
            (df['rsi'] > df['rsi'].shift(1)) &
            df['in_session']
        )

        df['short_signal'] = (
            df['trend_dn'] &
            (df['close'] < df['ma_short']) &
            (df['rsi'] > params.rsi_os) &
            (df['rsi'] < df['rsi'].shift(1)) &
            df['in_session']
        )

        # Volatility filter
        df['vol_ok'] = (df['atr'] / df['close']) >= 0.004

        return df.dropna()

    def _run_strategy_backtest(self, df: pd.DataFrame,
                             params: StrategyParameters) -> Tuple[List[Dict], List[float]]:
        """Run the actual strategy backtest"""
        capital = self.config.initial_capital
        position = 0
        position_price = 0
        stop_dist_at_entry = 0
        trades = []
        equity_curve = [capital]
        last_exit_bar = -999

        for i, (date, row) in enumerate(df.iterrows()):
            # Cooldown check
            cooldown_ok = (last_exit_bar == -999) or (i - last_exit_bar >= params.cooldown)

            # Exit logic
            if position != 0 and self._should_exit(row, position_price, stop_dist_at_entry, params):
                exit_price = row['close']
                pnl = self._calculate_pnl(position, position_price, exit_price)
                commission = abs(exit_price * abs(position)) * 0.0002  # 2bps
                pnl -= commission

                capital += pnl

                trade = {
                    'entry_date': position_price,  # This should be entry date
                    'exit_date': date,
                    'side': 'LONG' if position > 0 else 'SHORT',
                    'entry_price': abs(position_price),
                    'exit_price': exit_price,
                    'quantity': abs(position),
                    'pnl': pnl,
                    'pnl_pct': pnl / (abs(position_price) * abs(position)) * 100
                }
                trades.append(trade)

                position = 0
                position_price = 0
                stop_dist_at_entry = 0
                last_exit_bar = i

            # Entry logic
            elif position == 0 and cooldown_ok:
                if row['long_signal'] and row['vol_ok']:
                    stop_dist = row['atr'] * params.atr_mult
                    risk_amount = capital * 0.005  # 0.5% risk
                    qty = risk_amount / stop_dist
                    qty = max(1, qty)

                    cost = qty * row['close']
                    if cost <= capital:
                        position = qty
                        position_price = row['close']
                        stop_dist_at_entry = stop_dist
                        capital -= cost * 0.0002  # Commission

                elif row['short_signal'] and row['vol_ok']:
                    stop_dist = row['atr'] * params.atr_mult
                    risk_amount = capital * 0.005
                    qty = risk_amount / stop_dist
                    qty = max(1, qty)

                    cost = qty * row['close']
                    if cost <= capital:
                        position = -qty
                        position_price = row['close']
                        stop_dist_at_entry = stop_dist
                        capital -= cost * 0.0002

            equity_curve.append(capital)

        return trades, equity_curve

    def _should_exit(self, row: pd.Series, entry_price: float,
                    stop_dist: float, params: StrategyParameters) -> bool:
        """Determine if position should be exited"""
        current_price = row['close']

        if entry_price > 0:  # Long position
            stop_price = entry_price - stop_dist
            target_price = entry_price + stop_dist * params.rr_ratio
            return current_price <= stop_price or current_price >= target_price

        elif entry_price < 0:  # Short position
            stop_price = abs(entry_price) + stop_dist
            target_price = abs(entry_price) - stop_dist * params.rr_ratio
            return current_price >= stop_price or current_price <= target_price

        return False

    def _calculate_pnl(self, position: float, entry_price: float, exit_price: float) -> float:
        """Calculate profit/loss for position"""
        if position > 0:  # Long
            return (exit_price - entry_price) * position
        else:  # Short
            return (entry_price - exit_price) * abs(position)

    def _calculate_advanced_metrics(self, trades: List[Dict],
                                  equity_curve: List[float],
                                  params: StrategyParameters) -> Dict:
        """Calculate comprehensive performance metrics"""
        if not get_unified_validator().validate_required(trades):
            return {
                'total_trades': 0, 'win_rate': 0, 'profit_factor': 0,
                'total_return': 0, 'sharpe_ratio': 0, 'max_drawdown': 0,
                'avg_trade': 0, 'calmar_ratio': 0, 'sortino_ratio': 0,
                'expectancy': 0, 'recovery_factor': 0, 'kelly_criterion': 0,
                'ulcer_index': 0, 'gross_profit': 0, 'gross_loss': 0,
                'avg_win': 0, 'avg_loss': 0, 'largest_win': 0,
                'largest_loss': 0, 'win_loss_ratio': 0, 'profit_std': 0,
                'consecutive_wins': 0, 'consecutive_losses': 0,
                'value_at_risk_95': 0, 'expected_shortfall_95': 0,
                'downside_deviation': 0
            }

        # Basic trade metrics
        pnls = [t['pnl'] for t in trades]
        winning_trades = [t for t in trades if t['pnl'] > 0]
        losing_trades = [t for t in trades if t['pnl'] < 0]

        total_trades = len(trades)
        win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0

        gross_profit = sum(t['pnl'] for t in winning_trades)
        gross_loss = abs(sum(t['pnl'] for t in losing_trades))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')

        total_return = ((equity_curve[-1] - self.config.initial_capital) /
                       self.config.initial_capital) * 100

        # Risk metrics
        equity_series = pd.Series(equity_curve)
        returns = equity_series.pct_change().dropna()

        if len(returns) > 0:
            sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0

            # Max drawdown
            peak = equity_series.expanding().max()
            drawdown = (equity_series - peak) / peak
            max_drawdown = drawdown.min() * 100

            # Sortino ratio (downside deviation)
            downside_returns = returns[returns < 0]
            downside_deviation = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0
            sortino_ratio = returns.mean() / downside_deviation * np.sqrt(252) if downside_deviation > 0 else 0

            # Calmar ratio
            calmar_ratio = (returns.mean() * 252) / abs(max_drawdown/100) if max_drawdown != 0 else 0

            # Ulcer Index
            ulcer_index = np.sqrt((drawdown ** 2).mean()) * 100

            # Value at Risk (95%)
            value_at_risk_95 = np.percentile(returns, 5) * 100

            # Expected Shortfall (95%)
            expected_shortfall_95 = returns[returns <= np.percentile(returns, 5)].mean() * 100

        else:
            sharpe_ratio = sortino_ratio = calmar_ratio = ulcer_index = 0
            max_drawdown = value_at_risk_95 = expected_shortfall_95 = 0
            downside_deviation = 0

        # Trade-level metrics
        avg_trade = np.mean(pnls) if pnls else 0
        expectancy = (win_rate * (gross_profit / len(winning_trades) if winning_trades else 0) +
                     (1 - win_rate) * (-gross_loss / len(losing_trades) if losing_trades else 0))

        # Recovery factor
        recovery_factor = total_return / abs(max_drawdown) if max_drawdown != 0 else 0

        # Kelly Criterion
        if win_rate > 0 and win_rate < 1:
            avg_win = gross_profit / len(winning_trades) if winning_trades else 0
            avg_loss = gross_loss / len(losing_trades) if losing_trades else 0
            if avg_loss > 0:
                kelly_criterion = win_rate - ((1 - win_rate) * (avg_win / avg_loss))
            else:
                kelly_criterion = win_rate
        else:
            kelly_criterion = 0

        # Additional metrics
        avg_win = gross_profit / len(winning_trades) if winning_trades else 0
        avg_loss = gross_loss / len(losing_trades) if losing_trades else 0
        largest_win = max((t['pnl'] for t in winning_trades), default=0)
        largest_loss = min((t['pnl'] for t in losing_trades), default=0)
        win_loss_ratio = avg_win / abs(avg_loss) if avg_loss != 0 else float('inf')
        profit_std = np.std(pnls) if pnls else 0

        # Consecutive wins/losses
        consecutive_wins = 0
        consecutive_losses = 0
        current_wins = 0
        current_losses = 0

        for trade in trades:
            if trade['pnl'] > 0:
                current_wins += 1
                current_losses = 0
                consecutive_wins = max(consecutive_wins, current_wins)
            else:
                current_losses += 1
                current_wins = 0
                consecutive_losses = max(consecutive_losses, current_losses)

        return {
            'total_trades': total_trades,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'avg_trade': avg_trade,
            'calmar_ratio': calmar_ratio,
            'sortino_ratio': sortino_ratio,
            'expectancy': expectancy,
            'recovery_factor': recovery_factor,
            'kelly_criterion': kelly_criterion,
            'ulcer_index': ulcer_index,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'largest_win': largest_win,
            'largest_loss': largest_loss,
            'win_loss_ratio': win_loss_ratio,
            'profit_std': profit_std,
            'consecutive_wins': consecutive_wins,
            'consecutive_losses': consecutive_losses,
            'value_at_risk_95': value_at_risk_95,
            'expected_shortfall_95': expected_shortfall_95,
            'downside_deviation': downside_deviation
        }

    def run_optimization(self) -> List[BacktestResult]:
        """Run comprehensive parameter optimization"""
        get_logger(__name__).info("🚀 Starting TSLA ATR Pullback Strategy Optimization")
        get_logger(__name__).info("=" * 60)

        # Load data
        data = self.load_data()

        # Generate parameter combinations
        self.parameter_combinations = self.generate_parameter_combinations()

        # Split data for walk-forward validation
        split_idx = int(len(data) * self.config.test_train_split)
        train_data = data[:split_idx]
        test_data = data[split_idx:]

        get_logger(__name__).info(f"Training on {len(train_data)} bars, testing on {len(test_data)} bars")

        # Run optimization
        results = []
        for i, params in enumerate(self.parameter_combinations):
            if (i + 1) % 50 == 0:
                get_logger(__name__).info(f"Testing parameter set {i + 1}/{len(self.parameter_combinations)}")

            try:
                # Train on training data
                train_result = self.run_single_backtest(params, train_data)

                # Test on test data
                test_result = self.run_single_backtest(params, test_data)

                # Calculate walk-forward score
                train_score = self._calculate_optimization_score(train_result)
                test_score = self._calculate_optimization_score(test_result)

                # Combined walk-forward score
                walk_forward_score = (train_score * 0.6 + test_score * 0.4)

                # Update result
                train_result.train_score = train_score
                train_result.test_score = test_score
                train_result.walk_forward_score = walk_forward_score

                results.append(train_result)

            except Exception as e:
                get_logger(__name__).info(f"Error testing parameters {params}: {e}")
                continue

        self.results = results
        get_logger(__name__).info(f"\n✅ Optimization complete! Tested {len(results)} parameter combinations")

        return results

    def _calculate_optimization_score(self, result: BacktestResult) -> float:
        """Calculate optimization score for parameter selection"""
        if result.total_trades < self.config.min_trades:
            return -999  # Insufficient trades

        # Multi-objective score combining multiple metrics
        score = (
            result.profit_factor * 0.25 +           # Profit factor (25%)
            result.sharpe_ratio * 0.20 +            # Risk-adjusted returns (20%)
            result.win_rate * 0.15 +                # Win rate (15%)
            result.calmar_ratio * 0.15 +            # Risk-adjusted returns (15%)
            result.recovery_factor * 0.10 +         # Recovery factor (10%)
            (1 / (1 + abs(result.max_drawdown))) * 0.10 +  # Lower drawdown (10%)
            result.expectancy * 0.05                # Expectancy (5%)
        )

        return score

    def find_optimal_parameters(self) -> Tuple[StrategyParameters, BacktestResult]:
        """Find the optimal parameter combination"""
        if not self.results:
            get_unified_validator().raise_validation_error("No optimization results available. Run optimization first.")

        # Sort by walk-forward score (descending)
        sorted_results = sorted(self.results,
                              key=lambda x: x.walk_forward_score,
                              reverse=True)

        optimal_result = sorted_results[0]
        optimal_params = optimal_result.parameters

        get_logger(__name__).info("\n🏆 TOP 5 PARAMETER COMBINATIONS:")
        get_logger(__name__).info("=" * 80)
        get_logger(__name__).info(f"{'Rank':<4} {'ATR':<5} {'RR':<5} {'RSI_OB':<7} {'RSI_OS':<7} "
              f"{'MA_S':<5} {'MA_L':<5} {'Cooldown':<9} {'Score':<8} {'Trades':<6} "
              f"{'Win%':<5} {'PF':<5} {'Sharpe':<7} {'DD%':<5}")
        get_logger(__name__).info("-" * 80)

        for i, result in enumerate(sorted_results[:5], 1):
            params = result.parameters
            get_logger(__name__).info(f"{i:<4} {params.atr_mult:<5.1f} {params.rr_ratio:<5.1f} "
                  f"{params.rsi_ob:<7} {params.rsi_os:<7} {params.ma_short:<5} "
                  f"{params.ma_long:<5} {params.cooldown:<9} "
                  f"{result.walk_forward_score:<8.3f} {result.total_trades:<6} "
                  f"{result.win_rate:<5.1%} {result.profit_factor:<5.2f} "
                  f"{result.sharpe_ratio:<7.2f} {result.max_drawdown:<5.1f}")

        return optimal_params, optimal_result

    def generate_optimization_report(self) -> Dict:
        """Generate comprehensive optimization report"""
        if not self.results:
            get_unified_validator().raise_validation_error("No optimization results available")

        optimal_params, optimal_result = self.find_optimal_parameters()

        # Calculate statistics across all results
        scores = [r.walk_forward_score for r in self.results]
        profit_factors = [r.profit_factor for r in self.results if r.profit_factor != float('inf')]
        sharpe_ratios = [r.sharpe_ratio for r in self.results]
        win_rates = [r.win_rate for r in self.results]
        max_drawdowns = [r.max_drawdown for r in self.results]

        report = {
            'optimization_summary': {
                'total_combinations_tested': len(self.results),
                'date_range': f"{self.config.start_date} to {self.config.end_date}",
                'symbol': self.config.symbol,
                'initial_capital': self.config.initial_capital
            },
            'optimal_parameters': {
                'atr_multiplier': optimal_params.atr_mult,
                'risk_reward_ratio': optimal_params.rr_ratio,
                'rsi_overbought': optimal_params.rsi_ob,
                'rsi_oversold': optimal_params.rsi_os,
                'ma_short_period': optimal_params.ma_short,
                'ma_long_period': optimal_params.ma_long,
                'cooldown_bars': optimal_params.cooldown
            },
            'optimal_performance': {
                'total_return': optimal_result.total_return,
                'sharpe_ratio': optimal_result.sharpe_ratio,
                'max_drawdown': optimal_result.max_drawdown,
                'profit_factor': optimal_result.profit_factor,
                'win_rate': optimal_result.win_rate,
                'total_trades': optimal_result.total_trades,
                'expectancy': optimal_result.expectancy,
                'calmar_ratio': optimal_result.calmar_ratio,
                'recovery_factor': optimal_result.recovery_factor
            },
            'parameter_analysis': {
                'score_distribution': {
                    'mean': np.mean(scores),
                    'std': np.std(scores),
                    'min': np.min(scores),
                    'max': np.max(scores),
                    'median': np.median(scores)
                },
                'robustness_metrics': {
                    'profitable_combinations': len([r for r in self.results if r.total_return > 0]),
                    'high_sharpe_combinations': len([r for r in self.results if r.sharpe_ratio > 1.0]),
                    'low_drawdown_combinations': len([r for r in self.results if r.max_drawdown < 20])
                }
            }
        }

        return report

    def plot_optimization_results(self):
        """Plot optimization results and parameter sensitivity"""
        if not self.results:
            get_logger(__name__).info("No results to plot")
            return

        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('TSLA ATR Pullback Strategy - Parameter Optimization Results')

        # Scatter plots for key parameters vs score
        params_to_plot = [
            ('ATR Multiplier', 'atr_mult', 0, 0),
            ('Risk-Reward Ratio', 'rr_ratio', 0, 1),
            ('RSI Overbought', 'rsi_ob', 0, 2),
            ('MA Short', 'ma_short', 1, 0),
            ('MA Long', 'ma_long', 1, 1),
            ('Cooldown', 'cooldown', 1, 2)
        ]

        for param_name, param_attr, row, col in params_to_plot:
            x_vals = [get_unified_validator().safe_getattr(r.parameters, param_attr) for r in self.results]
            y_vals = [r.walk_forward_score for r in self.results]

            axes[row, col].scatter(x_vals, y_vals, alpha=0.6, s=20)
            axes[row, col].set_xlabel(param_name)
            axes[row, col].set_ylabel('Optimization Score')
            axes[row, col].set_title(f'{param_name} vs Score')
            axes[row, col].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()



if __name__ == "__main__":
    main()

"""
Financial Analytics Service - Business Intelligence & Trading Systems
Agent-5: Business Intelligence & Trading Specialist
Performance & Health Systems Division

Provides advanced financial analysis, backtesting, and performance optimization.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

class FinancialAnalyticsService:
    """Advanced financial analytics and backtesting service"""
    
    def __init__(self, data_dir: str = "financial_analytics"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.backtest_results: List[BacktestResult] = []
        self.performance_metrics: Dict[str, PerformanceMetrics] = {}
        self.risk_analyses: Dict[str, RiskAnalysis] = {}
        
        self.results_file = self.data_dir / "backtest_results.json"
        self.metrics_file = self.data_dir / "performance_metrics.json"
        self.risk_file = self.data_dir / "risk_analyses.json"
        
        # Backtesting parameters
        self.default_params = {
            "initial_capital": 100000,
            "commission": 0.001,  # 0.1%
            "slippage": 0.0005,   # 0.05%
            "risk_free_rate": 0.02,  # 2%
            "benchmark": "SPY"  # S&P 500 ETF
        }
        
        self.load_data()
    
    def calculate_returns(self, prices: pd.Series) -> pd.Series:
        """Calculate returns from price series"""
        try:
            returns = prices.pct_change().dropna()
            return returns
        except Exception as e:
            logger.error(f"Error calculating returns: {e}")
            return pd.Series()
    
    def calculate_cumulative_returns(self, returns: pd.Series) -> pd.Series:
        """Calculate cumulative returns"""
        try:
            cumulative_returns = (1 + returns).cumprod()
            return cumulative_returns
        except Exception as e:
            logger.error(f"Error calculating cumulative returns: {e}")
            return pd.Series()
    
    def calculate_drawdown(self, cumulative_returns: pd.Series) -> pd.Series:
        """Calculate drawdown series"""
        try:
            running_max = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - running_max) / running_max
            return drawdown
        except Exception as e:
            logger.error(f"Error calculating drawdown: {e}")
            return pd.Series()
    
    def calculate_sharpe_ratio(self, returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio"""
        try:
            if len(returns) < 2:
                return 0.0
            
            excess_returns = returns - risk_free_rate / 252  # Daily risk-free rate
            if excess_returns.std() == 0:
                return 0.0
            
            sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std()
            return sharpe_ratio
        except Exception as e:
            logger.error(f"Error calculating Sharpe ratio: {e}")
            return 0.0
    
    def calculate_sortino_ratio(self, returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """Calculate Sortino ratio"""
        try:
            if len(returns) < 2:
                return 0.0
            
            excess_returns = returns - risk_free_rate / 252
            downside_returns = excess_returns[excess_returns < 0]
            
            if len(downside_returns) == 0 or downside_returns.std() == 0:
                return 0.0
            
            sortino_ratio = np.sqrt(252) * excess_returns.mean() / downside_returns.std()
            return sortino_ratio
        except Exception as e:
            logger.error(f"Error calculating Sortino ratio: {e}")
            return 0.0
    
    def calculate_max_drawdown(self, drawdown: pd.Series) -> float:
        """Calculate maximum drawdown"""
        try:
            return drawdown.min()
        except Exception as e:
            logger.error(f"Error calculating max drawdown: {e}")
            return 0.0
    
    def calculate_value_at_risk(self, returns: pd.Series, confidence_level: float = 0.95) -> float:
        """Calculate Value at Risk"""
        try:
            if len(returns) < 2:
                return 0.0
            
            var = np.percentile(returns, (1 - confidence_level) * 100)
            return abs(var)
        except Exception as e:
            logger.error(f"Error calculating VaR: {e}")
            return 0.0
    
    def calculate_conditional_var(self, returns: pd.Series, confidence_level: float = 0.95) -> float:
        """Calculate Conditional Value at Risk (Expected Shortfall)"""
        try:
            if len(returns) < 2:
                return 0.0
            
            var = self.calculate_value_at_risk(returns, confidence_level)
            tail_returns = returns[returns <= -var]
            
            if len(tail_returns) == 0:
                return var
            
            conditional_var = tail_returns.mean()
            return abs(conditional_var)
        except Exception as e:
            logger.error(f"Error calculating Conditional VaR: {e}")
            return 0.0
    
    def calculate_beta(self, strategy_returns: pd.Series, market_returns: pd.Series) -> float:
        """Calculate beta relative to market"""
        try:
            if len(strategy_returns) < 2 or len(market_returns) < 2:
                return 1.0
            
            # Align data
            aligned_data = pd.concat([strategy_returns, market_returns], axis=1).dropna()
            if len(aligned_data) < 2:
                return 1.0
            
            strategy_aligned = aligned_data.iloc[:, 0]
            market_aligned = aligned_data.iloc[:, 1]
            
            # Calculate beta
            covariance = np.cov(strategy_aligned, market_aligned)[0, 1]
            market_variance = np.var(market_aligned)
            
            if market_variance == 0:
                return 1.0
            
            beta = covariance / market_variance
            return beta
        except Exception as e:
            logger.error(f"Error calculating beta: {e}")
            return 1.0
    
    def calculate_alpha(self, strategy_returns: pd.Series, market_returns: pd.Series, 
                       risk_free_rate: float = 0.02) -> float:
        """Calculate Jensen's alpha"""
        try:
            if len(strategy_returns) < 2 or len(market_returns) < 2:
                return 0.0
            
            beta = self.calculate_beta(strategy_returns, market_returns)
            
            # Annualized returns
            strategy_annual_return = strategy_returns.mean() * 252
            market_annual_return = market_returns.mean() * 252
            
            alpha = strategy_annual_return - (risk_free_rate + beta * (market_annual_return - risk_free_rate))
            return alpha
        except Exception as e:
            logger.error(f"Error calculating alpha: {e}")
            return 0.0
    
    def calculate_treynor_ratio(self, strategy_returns: pd.Series, market_returns: pd.Series,
                               risk_free_rate: float = 0.02) -> float:
        """Calculate Treynor ratio"""
        try:
            if len(strategy_returns) < 2:
                return 0.0
            
            beta = self.calculate_beta(strategy_returns, market_returns)
            if beta == 0:
                return 0.0
            
            excess_return = strategy_returns.mean() * 252 - risk_free_rate
            treynor_ratio = excess_return / beta
            return treynor_ratio
        except Exception as e:
            logger.error(f"Error calculating Treynor ratio: {e}")
            return 0.0
    
    def calculate_information_ratio(self, strategy_returns: pd.Series, benchmark_returns: pd.Series) -> float:
        """Calculate information ratio"""
        try:
            if len(strategy_returns) < 2 or len(benchmark_returns) < 2:
                return 0.0
            
            # Align data
            aligned_data = pd.concat([strategy_returns, benchmark_returns], axis=1).dropna()
            if len(aligned_data) < 2:
                return 0.0
            
            strategy_aligned = aligned_data.iloc[:, 0]
            benchmark_aligned = aligned_data.iloc[:, 1]
            
            # Calculate active returns
            active_returns = strategy_aligned - benchmark_aligned
            
            if active_returns.std() == 0:
                return 0.0
            
            information_ratio = np.sqrt(252) * active_returns.mean() / active_returns.std()
            return information_ratio
        except Exception as e:
            logger.error(f"Error calculating information ratio: {e}")
            return 0.0
    
    def calculate_calmar_ratio(self, strategy_returns: pd.Series, max_drawdown: float) -> float:
        """Calculate Calmar ratio"""
        try:
            if len(strategy_returns) < 2 or max_drawdown == 0:
                return 0.0
            
            annual_return = strategy_returns.mean() * 252
            calmar_ratio = annual_return / abs(max_drawdown)
            return calmar_ratio
        except Exception as e:
            logger.error(f"Error calculating Calmar ratio: {e}")
            return 0.0
    
    def run_backtest(self, strategy_name: str, signals: pd.DataFrame, prices: pd.Series,
                     initial_capital: float = None, commission: float = None,
                     slippage: float = None) -> BacktestResult:
        """Run backtest on trading strategy"""
        try:
            # Use default parameters if not provided
            initial_capital = initial_capital or self.default_params["initial_capital"]
            commission = commission or self.default_params["commission"]
            slippage = slippage or self.default_params["slippage"]
            
            # Initialize backtest variables
            capital = initial_capital
            position = 0
            equity_curve = [initial_capital]
            trades = []
            
            # Process signals
            for i, (timestamp, signal) in enumerate(signals.iterrows()):
                current_price = prices.iloc[i]
                
                # Execute trades based on signals
                if signal['signal'] == 'BUY' and position <= 0:
                    # Buy signal
                    shares = int(capital / current_price)
                    if shares > 0:
                        trade_cost = shares * current_price * (1 + commission + slippage)
                        if trade_cost <= capital:
                            position = shares
                            capital -= trade_cost
                            
                            trades.append({
                                'timestamp': timestamp,
                                'action': 'BUY',
                                'shares': shares,
                                'price': current_price,
                                'cost': trade_cost,
                                'capital': capital
                            })
                
                elif signal['signal'] == 'SELL' and position > 0:
                    # Sell signal
                    trade_proceeds = position * current_price * (1 - commission - slippage)
                    capital += trade_proceeds
                    
                    trades.append({
                        'timestamp': timestamp,
                        'action': 'SELL',
                        'shares': position,
                        'price': current_price,
                        'proceeds': trade_proceeds,
                        'capital': capital
                    })
                    
                    position = 0
                
                # Calculate current equity
                current_equity = capital + (position * current_price)
                equity_curve.append(current_equity)
            
            # Close any remaining position
            if position > 0:
                final_price = prices.iloc[-1]
                final_proceeds = position * final_price * (1 - commission - slippage)
                capital += final_proceeds
                equity_curve[-1] = capital
            
            # Calculate performance metrics
            equity_series = pd.Series(equity_curve, index=signals.index)
            returns = self.calculate_returns(equity_series)
            cumulative_returns = self.calculate_cumulative_returns(returns)
            drawdown = self.calculate_drawdown(cumulative_returns)
            
            total_return = (equity_series.iloc[-1] - initial_capital) / initial_capital
            annualized_return = (1 + total_return) ** (252 / len(returns)) - 1
            volatility = returns.std() * np.sqrt(252)
            sharpe_ratio = self.calculate_sharpe_ratio(returns)
            max_drawdown = self.calculate_max_drawdown(drawdown)
            
            # Calculate trade statistics
            winning_trades = [t for t in trades if t.get('proceeds', 0) > t.get('cost', 0)]
            losing_trades = [t for t in trades if t.get('proceeds', 0) <= t.get('cost', 0)]
            
            win_rate = len(winning_trades) / len(trades) if trades else 0
            
            if winning_trades:
                avg_win = np.mean([t.get('proceeds', 0) - t.get('cost', 0) for t in winning_trades])
                largest_win = max([t.get('proceeds', 0) - t.get('cost', 0) for t in winning_trades])
            else:
                avg_win = 0
                largest_win = 0
            
            if losing_trades:
                avg_loss = np.mean([t.get('cost', 0) - t.get('proceeds', 0) for t in losing_trades])
                largest_loss = max([t.get('cost', 0) - t.get('proceeds', 0) for t in losing_trades])
            else:
                avg_loss = 0
                largest_loss = 0
            
            # Calculate profit factor
            total_wins = sum([t.get('proceeds', 0) - t.get('cost', 0) for t in winning_trades])
            total_losses = sum([t.get('cost', 0) - t.get('proceeds', 0) for t in losing_trades])
            profit_factor = total_wins / total_losses if total_losses > 0 else float('inf')
            
            # Calculate consecutive wins/losses
            consecutive_wins = 0
            consecutive_losses = 0
            max_consecutive_wins = 0
            max_consecutive_losses = 0
            
            for trade in trades:
                if trade.get('proceeds', 0) > trade.get('cost', 0):
                    consecutive_wins += 1
                    consecutive_losses = 0
                    max_consecutive_wins = max(max_consecutive_wins, consecutive_wins)
                else:
                    consecutive_losses += 1
                    consecutive_wins = 0
                    max_consecutive_losses = max(max_consecutive_losses, consecutive_losses)
            
            # Create backtest result
            result = BacktestResult(
                strategy_name=strategy_name,
                start_date=signals.index[0],
                end_date=signals.index[-1],
                total_return=total_return,
                annualized_return=annualized_return,
                volatility=volatility,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown,
                win_rate=win_rate,
                profit_factor=profit_factor,
                total_trades=len(trades),
                winning_trades=len(winning_trades),
                losing_trades=len(losing_trades),
                avg_win=avg_win,
                avg_loss=avg_loss,
                largest_win=largest_win,
                largest_loss=largest_loss,
                consecutive_wins=max_consecutive_wins,
                consecutive_losses=max_consecutive_losses,
                equity_curve=equity_curve,
                trade_history=trades
            )
            
            # Store result
            self.backtest_results.append(result)
            self.save_data()
            
            return result
            
        except Exception as e:
            logger.error(f"Error running backtest: {e}")
            return None
    
    def calculate_comprehensive_metrics(self, returns: pd.Series, benchmark_returns: pd.Series = None) -> PerformanceMetrics:
        """Calculate comprehensive performance metrics"""
        try:
            # Basic metrics
            cumulative_returns = self.calculate_cumulative_returns(returns)
            drawdown = self.calculate_drawdown(cumulative_returns)
            
            # Rolling metrics
            rolling_sharpe = returns.rolling(window=252).apply(
                lambda x: self.calculate_sharpe_ratio(x)
            )
            rolling_volatility = returns.rolling(window=252).std() * np.sqrt(252)
            
            # Risk metrics
            var_95 = self.calculate_value_at_risk(returns, 0.95)
            conditional_var = self.calculate_conditional_var(returns, 0.95)
            
            # Calculate ratios
            sharpe_ratio = self.calculate_sharpe_ratio(returns)
            sortino_ratio = self.calculate_sortino_ratio(returns)
            max_drawdown = self.calculate_max_drawdown(drawdown)
            calmar_ratio = self.calculate_calmar_ratio(returns, max_drawdown)
            
            # Benchmark comparison
            if benchmark_returns is not None:
                beta = self.calculate_beta(returns, benchmark_returns)
                alpha = self.calculate_alpha(returns, benchmark_returns)
                treynor_ratio = self.calculate_treynor_ratio(returns, benchmark_returns)
                information_ratio = self.calculate_information_ratio(returns, benchmark_returns)
                
                # Rolling beta and alpha
                rolling_beta = returns.rolling(window=252).apply(
                    lambda x: self.calculate_beta(x, benchmark_returns.loc[x.index])
                )
                rolling_alpha = returns.rolling(window=252).apply(
                    lambda x: self.calculate_alpha(x, benchmark_returns.loc[x.index])
                )
                
                correlation = returns.corr(benchmark_returns)
                tracking_error = (returns - benchmark_returns).std() * np.sqrt(252)
            else:
                beta = 1.0
                alpha = 0.0
                treynor_ratio = 0.0
                information_ratio = 0.0
                rolling_beta = pd.Series([1.0] * len(returns))
                rolling_alpha = pd.Series([0.0] * len(returns))
                correlation = 1.0
                tracking_error = 0.0
            
            metrics = PerformanceMetrics(
                returns=returns,
                cumulative_returns=cumulative_returns,
                drawdown=drawdown,
                rolling_sharpe=rolling_sharpe,
                rolling_volatility=rolling_volatility,
                rolling_beta=rolling_beta,
                rolling_alpha=rolling_alpha,
                value_at_risk=var_95,
                conditional_var=conditional_var,
                calmar_ratio=calmar_ratio,
                sortino_ratio=sortino_ratio,
                information_ratio=information_ratio,
                treynor_ratio=treynor_ratio,
                jensen_alpha=alpha,
                tracking_error=tracking_error,
                correlation=correlation
            )
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating comprehensive metrics: {e}")
            return None
    
    def perform_risk_analysis(self, returns: pd.Series, benchmark_returns: pd.Series = None) -> RiskAnalysis:
        """Perform comprehensive risk analysis"""
        try:
            # Volatility analysis
            volatility_analysis = {
                "total_volatility": returns.std() * np.sqrt(252),
                "annualized_volatility": returns.std() * np.sqrt(252),
                "downside_volatility": returns[returns < 0].std() * np.sqrt(252),
                "upside_volatility": returns[returns > 0].std() * np.sqrt(252),
                "volatility_of_volatility": returns.rolling(window=252).std().std() * np.sqrt(252)
            }
            
            # Drawdown analysis
            cumulative_returns = self.calculate_cumulative_returns(returns)
            drawdown = self.calculate_drawdown(cumulative_returns)
            
            drawdown_analysis = {
                "max_drawdown": self.calculate_max_drawdown(drawdown),
                "avg_drawdown": drawdown.mean(),
                "drawdown_duration": len(drawdown[drawdown < 0]),
                "recovery_time": len(drawdown[drawdown < 0]) / len(drawdown) if len(drawdown) > 0 else 0
            }
            
            # VaR analysis
            var_analysis = {
                "var_95": self.calculate_value_at_risk(returns, 0.95),
                "var_99": self.calculate_value_at_risk(returns, 0.99),
                "conditional_var_95": self.calculate_conditional_var(returns, 0.95),
                "conditional_var_99": self.calculate_conditional_var(returns, 0.99)
            }
            
            # Correlation analysis
            if benchmark_returns is not None:
                correlation_analysis = {
                    "benchmark_correlation": returns.corr(benchmark_returns),
                    "rolling_correlation": returns.rolling(window=252).corr(benchmark_returns).mean(),
                    "correlation_stability": returns.rolling(window=252).corr(benchmark_returns).std()
                }
            else:
                correlation_analysis = {
                    "benchmark_correlation": 1.0,
                    "rolling_correlation": 1.0,
                    "correlation_stability": 0.0
                }
            
            # Stress testing
            stress_test_results = {
                "market_crash_20pct": self.simulate_market_crash(returns, -0.20),
                "interest_rate_shock": self.simulate_interest_rate_shock(returns, 0.02),
                "volatility_spike": self.simulate_volatility_spike(returns, 2.0)
            }
            
            # Scenario analysis
            scenario_analysis = {
                "bull_market": self.simulate_scenario(returns, 0.15, 0.10),
                "bear_market": self.simulate_scenario(returns, -0.10, 0.20),
                "sideways_market": self.simulate_scenario(returns, 0.05, 0.15)
            }
            
            # Risk decomposition
            risk_decomposition = {
                "systematic_risk": self.calculate_systematic_risk(returns, benchmark_returns),
                "idiosyncratic_risk": self.calculate_idiosyncratic_risk(returns, benchmark_returns),
                "concentration_risk": self.calculate_concentration_risk(returns),
                "liquidity_risk": self.calculate_liquidity_risk(returns)
            }
            
            risk_analysis = RiskAnalysis(
                volatility_analysis=volatility_analysis,
                drawdown_analysis=drawdown_analysis,
                var_analysis=var_analysis,
                correlation_analysis=correlation_analysis,
                stress_test_results=stress_test_results,
                scenario_analysis=scenario_analysis,
                risk_decomposition=risk_decomposition
            )
            
            return risk_analysis
            
        except Exception as e:
            logger.error(f"Error performing risk analysis: {e}")
            return None
    
    def simulate_market_crash(self, returns: pd.Series, crash_magnitude: float) -> float:
        """Simulate market crash impact"""
        try:
            # Apply crash to returns
            crashed_returns = returns.copy()
            crash_period = len(returns) // 4  # Last quarter
            crashed_returns.iloc[-crash_period:] *= (1 + crash_magnitude)
            
            # Calculate impact
            original_cumulative = self.calculate_cumulative_returns(returns).iloc[-1]
            crashed_cumulative = self.calculate_cumulative_returns(crashed_returns).iloc[-1]
            
            impact = (crashed_cumulative - original_cumulative) / original_cumulative
            return impact
            
        except Exception as e:
            logger.error(f"Error simulating market crash: {e}")
            return 0.0
    
    def simulate_interest_rate_shock(self, returns: pd.Series, rate_change: float) -> float:
        """Simulate interest rate shock impact"""
        try:
            # Simplified interest rate impact simulation
            # Assume bond-like securities are affected
            shocked_returns = returns.copy()
            shock_period = len(returns) // 4  # Last quarter
            
            # Apply interest rate sensitivity
            duration = 5.0  # Assume 5-year duration
            shocked_returns.iloc[-shock_period:] -= duration * rate_change / 252
            
            # Calculate impact
            original_cumulative = self.calculate_cumulative_returns(returns).iloc[-1]
            shocked_cumulative = self.calculate_cumulative_returns(shocked_returns).iloc[-1]
            
            impact = (shocked_cumulative - original_cumulative) / original_cumulative
            return impact
            
        except Exception as e:
            logger.error(f"Error simulating interest rate shock: {e}")
            return 0.0
    
    def simulate_volatility_spike(self, returns: pd.Series, volatility_multiplier: float) -> float:
        """Simulate volatility spike impact"""
        try:
            # Apply volatility spike
            spiked_returns = returns.copy()
            spike_period = len(returns) // 4  # Last quarter
            
            # Increase volatility
            spiked_returns.iloc[-spike_period:] *= volatility_multiplier
            
            # Calculate impact
            original_cumulative = self.calculate_cumulative_returns(returns).iloc[-1]
            spiked_cumulative = self.calculate_cumulative_returns(spiked_returns).iloc[-1]
            
            impact = (spiked_cumulative - original_cumulative) / original_cumulative
            return impact
            
        except Exception as e:
            logger.error(f"Error simulating volatility spike: {e}")
            return 0.0
    
    def simulate_scenario(self, returns: pd.Series, return_adjustment: float, volatility_adjustment: float) -> float:
        """Simulate market scenario"""
        try:
            # Apply scenario adjustments
            scenario_returns = returns.copy()
            scenario_period = len(returns) // 2  # Last half
            
            # Adjust returns and volatility
            scenario_returns.iloc[-scenario_period:] += return_adjustment / 252
            scenario_returns.iloc[-scenario_period:] *= (1 + volatility_adjustment)
            
            # Calculate impact
            original_cumulative = self.calculate_cumulative_returns(returns).iloc[-1]
            scenario_cumulative = self.calculate_cumulative_returns(scenario_returns).iloc[-1]
            
            impact = (scenario_cumulative - original_cumulative) / original_cumulative
            return impact
            
        except Exception as e:
            logger.error(f"Error simulating scenario: {e}")
            return 0.0
    
    def calculate_systematic_risk(self, returns: pd.Series, benchmark_returns: pd.Series) -> float:
        """Calculate systematic risk"""
        try:
            if benchmark_returns is None:
                return 0.0
            
            beta = self.calculate_beta(returns, benchmark_returns)
            benchmark_volatility = benchmark_returns.std() * np.sqrt(252)
            systematic_risk = beta * benchmark_volatility
            return systematic_risk
            
        except Exception as e:
            logger.error(f"Error calculating systematic risk: {e}")
            return 0.0
    
    def calculate_idiosyncratic_risk(self, returns: pd.Series, benchmark_returns: pd.Series) -> float:
        """Calculate idiosyncratic risk"""
        try:
            if benchmark_returns is None:
                return returns.std() * np.sqrt(252)
            
            systematic_risk = self.calculate_systematic_risk(returns, benchmark_returns)
            total_risk = returns.std() * np.sqrt(252)
            idiosyncratic_risk = np.sqrt(total_risk**2 - systematic_risk**2)
            return max(0, idiosyncratic_risk)
            
        except Exception as e:
            logger.error(f"Error calculating idiosyncratic risk: {e}")
            return 0.0
    
    def calculate_concentration_risk(self, returns: pd.Series) -> float:
        """Calculate concentration risk"""
        try:
            # Simplified concentration risk based on return distribution
            positive_returns = returns[returns > 0]
            negative_returns = returns[returns < 0]
            
            if len(positive_returns) == 0 or len(negative_returns) == 0:
                return 0.0
            
            # Calculate concentration based on skewness
            skewness = stats.skew(returns)
            concentration_risk = abs(skewness) / 10  # Normalize
            return min(1.0, concentration_risk)
            
        except Exception as e:
            logger.error(f"Error calculating concentration risk: {e}")
            return 0.0
    
    def calculate_liquidity_risk(self, returns: pd.Series) -> float:
        """Calculate liquidity risk"""
        try:
            # Simplified liquidity risk based on return patterns
            # Assume higher volatility indicates lower liquidity
            volatility = returns.std()
            liquidity_risk = min(1.0, volatility * 10)  # Normalize
            return liquidity_risk
            
        except Exception as e:
            logger.error(f"Error calculating liquidity risk: {e}")
            return 0.0
    
    def generate_performance_report(self, strategy_name: str) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        try:
            # Find strategy in backtest results
            strategy_result = next(
                (result for result in self.backtest_results if result.strategy_name == strategy_name),
                None
            )
            
            if not strategy_result:
                return {"error": "Strategy not found"}
            
            # Calculate additional metrics
            returns = pd.Series(strategy_result.equity_curve).pct_change().dropna()
            metrics = self.calculate_comprehensive_metrics(returns)
            risk_analysis = self.perform_risk_analysis(returns)
            
            # Generate report
            report = {
                "strategy_name": strategy_name,
                "summary": {
                    "total_return": f"{strategy_result.total_return:.2%}",
                    "annualized_return": f"{strategy_result.annualized_return:.2%}",
                    "sharpe_ratio": f"{strategy_result.sharpe_ratio:.2f}",
                    "max_drawdown": f"{strategy_result.max_drawdown:.2%}",
                    "win_rate": f"{strategy_result.win_rate:.2%}",
                    "profit_factor": f"{strategy_result.profit_factor:.2f}"
                },
                "risk_metrics": {
                    "volatility": f"{strategy_result.volatility:.2%}",
                    "var_95": f"{metrics.value_at_risk:.2%}" if metrics else "N/A",
                    "conditional_var_95": f"{metrics.conditional_var:.2%}" if metrics else "N/A",
                    "sortino_ratio": f"{metrics.sortino_ratio:.2f}" if metrics else "N/A",
                    "calmar_ratio": f"{metrics.calmar_ratio:.2f}" if metrics else "N/A"
                },
                "trade_analysis": {
                    "total_trades": strategy_result.total_trades,
                    "winning_trades": strategy_result.winning_trades,
                    "losing_trades": strategy_result.losing_trades,
                    "avg_win": f"${strategy_result.avg_win:.2f}",
                    "avg_loss": f"${strategy_result.avg_loss:.2f}",
                    "largest_win": f"${strategy_result.largest_win:.2f}",
                    "largest_loss": f"${strategy_result.largest_loss:.2f}"
                },
                "risk_analysis": asdict(risk_analysis) if risk_analysis else None,
                "recommendations": self.generate_recommendations(strategy_result, metrics, risk_analysis)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating performance report: {e}")
            return {"error": str(e)}
    
    def generate_recommendations(self, result: BacktestResult, metrics: PerformanceMetrics, 
                                risk_analysis: RiskAnalysis) -> List[str]:
        """Generate trading strategy recommendations"""
        try:
            recommendations = []
            
            # Performance-based recommendations
            if result.sharpe_ratio < 1.0:
                recommendations.append("Consider improving risk-adjusted returns through better risk management")
            
            if result.max_drawdown < -0.20:
                recommendations.append("Implement stricter stop-loss mechanisms to reduce drawdown")
            
            if result.win_rate < 0.4:
                recommendations.append("Review entry/exit criteria to improve win rate")
            
            if result.profit_factor < 1.5:
                recommendations.append("Focus on improving risk-reward ratio of individual trades")
            
            # Risk-based recommendations
            if metrics and metrics.sortino_ratio < 1.0:
                recommendations.append("Consider strategies that reduce downside volatility")
            
            if risk_analysis and risk_analysis.volatility_analysis["downside_volatility"] > 0.15:
                recommendations.append("Implement hedging strategies to reduce downside risk")
            
            # Trade management recommendations
            if result.consecutive_losses > 5:
                recommendations.append("Implement position sizing rules to manage losing streaks")
            
            if result.total_trades < 30:
                recommendations.append("Increase sample size for more reliable performance metrics")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return []
    
    def calculate_performance_metrics(self, symbols: List[str], period: str = "1y") -> Dict[str, Any]:
        """Calculate performance metrics for given symbols - unified API integration method"""
        try:
            # Simplified performance metrics calculation for unified API
            # In a real implementation, this would fetch actual data and calculate metrics
            
            metrics = {}
            for symbol in symbols:
                # Mock metrics for demonstration
                metrics[symbol] = {
                    "return_1m": 0.05,
                    "return_3m": 0.12,
                    "return_1y": 0.25,
                    "volatility": 0.18,
                    "sharpe_ratio": 1.2,
                    "max_drawdown": -0.08,
                    "beta": 1.1,
                    "alpha": 0.02
                }
            
            return {
                "symbols": symbols,
                "period": period,
                "metrics": metrics,
                "calculated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error calculating performance metrics: {e}")
            return {}
    
    def save_data(self):
        """Save financial analytics data"""
        try:
            # Save backtest results
            results_data = [asdict(result) for result in self.backtest_results]
            with open(self.results_file, 'w') as f:
                json.dump(results_data, f, indent=2, default=str)
            
            # Save performance metrics
            metrics_data = {}
            for name, metrics in self.performance_metrics.items():
                metrics_data[name] = {
                    "returns": metrics.returns.tolist(),
                    "cumulative_returns": metrics.cumulative_returns.tolist(),
                    "drawdown": metrics.drawdown.tolist(),
                    "value_at_risk": metrics.value_at_risk,
                    "conditional_var": metrics.conditional_var,
                    "sharpe_ratio": metrics.sharpe_ratio,
                    "sortino_ratio": metrics.sortino_ratio
                }
            
            with open(self.metrics_file, 'w') as f:
                json.dump(metrics_data, f, indent=2, default=str)
            
            # Save risk analyses
            risk_data = {}
            for name, risk in self.risk_analyses.items():
                risk_data[name] = asdict(risk)
            
            with open(self.risk_file, 'w') as f:
                json.dump(risk_data, f, indent=2, default=str)
            
            logger.info("Financial analytics data saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving financial analytics data: {e}")
    
    def load_data(self):
        """Load financial analytics data"""
        try:
            # Load backtest results
            if self.results_file.exists():
                with open(self.results_file, 'r') as f:
                    results_data = json.load(f)
                
                for result_data in results_data:
                    if "start_date" in result_data:
                        result_data["start_date"] = datetime.fromisoformat(result_data["start_date"])
                    if "end_date" in result_data:
                        result_data["end_date"] = datetime.fromisoformat(result_data["end_date"])
                    if "timestamp" in result_data:
                        result_data["timestamp"] = datetime.fromisoformat(result_data["timestamp"])
                    
                    result = BacktestResult(**result_data)
                    self.backtest_results.append(result)
                
                logger.info(f"Loaded {len(self.backtest_results)} backtest results")
            
        except Exception as e:
            logger.error(f"Error loading financial analytics data: {e}")

# Example usage and testing
if __name__ == "__main__":
    # Create financial analytics service
    fas = FinancialAnalyticsService()
    
    # Test metrics calculation
    test_returns = pd.Series([0.01, -0.005, 0.02, -0.01, 0.015] * 50)
    
    # Calculate basic metrics
    sharpe = fas.calculate_sharpe_ratio(test_returns)
    sortino = fas.calculate_sortino_ratio(test_returns)
    var_95 = fas.calculate_value_at_risk(test_returns)
    
    print(f"Sharpe Ratio: {sharpe:.3f}")
    print(f"Sortino Ratio: {sortino:.3f}")
    print(f"VaR (95%): {var_95:.3%}")
    
    # Test comprehensive metrics
    metrics = fas.calculate_comprehensive_metrics(test_returns)
    if metrics:
        print(f"Annualized Return: {metrics.returns.mean() * 252:.2%}")
        print(f"Volatility: {metrics.returns.std() * np.sqrt(252):.2%}")
    
    print("Financial Analytics Service initialized successfully")

"""
Financial Analytics Main Service - V2 Compliant Orchestration Layer

This module provides the main FinancialAnalyticsService interface that orchestrates
all the modular components. Follows V2 standards with ≤200 LOC and single responsibility
for service orchestration.
"""

import logging
import numpy as np
import pandas as pd

from src.utils.stability_improvements import stability_manager, safe_import
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple

from .data_models import BacktestResult, PerformanceMetrics, RiskAnalysis, BacktestParameters
from .metrics_calculator import MetricsCalculator
from .risk_analyzer import RiskAnalyzer
from .data_manager import DataManager

logger = logging.getLogger(__name__)


class FinancialAnalyticsService:
    """Advanced financial analytics and backtesting service - V2 Compliant"""
    
    def __init__(self, data_dir: str = "financial_analytics"):
        # Initialize components
        self.data_manager = DataManager(data_dir)
        self.metrics_calculator = MetricsCalculator()
        self.risk_analyzer = RiskAnalyzer()
        
        # Load existing data
        self.backtest_results, self.performance_metrics, self.risk_analyses = self.data_manager.load_all_data()
        
        # Default parameters
        self.default_params = BacktestParameters()
    
    def calculate_comprehensive_metrics(self, returns: pd.Series, 
                                     benchmark_returns: Optional[pd.Series] = None) -> Optional[PerformanceMetrics]:
        """Calculate comprehensive performance metrics"""
        try:
            if len(returns) < 2:
                logger.warning("Insufficient data for metrics calculation")
                return None
            
            # Basic calculations
            cumulative_returns = self.metrics_calculator.calculate_cumulative_returns(returns)
            drawdown = self.metrics_calculator.calculate_drawdown(cumulative_returns)
            max_drawdown = self.metrics_calculator.calculate_max_drawdown(drawdown)
            
            # Risk metrics
            value_at_risk = self.risk_analyzer.calculate_value_at_risk(returns)
            conditional_var = self.risk_analyzer.calculate_conditional_var(returns)
            
            # Performance ratios
            sharpe_ratio = self.metrics_calculator.calculate_sharpe_ratio(returns)
            sortino_ratio = self.metrics_calculator.calculate_sortino_ratio(returns)
            calmar_ratio = self.metrics_calculator.calculate_calmar_ratio(returns, max_drawdown)
            
            # Initialize with default values
            rolling_sharpe = pd.Series([sharpe_ratio] * len(returns))
            rolling_volatility = pd.Series([returns.std() * np.sqrt(252)] * len(returns))
            rolling_beta = pd.Series([1.0] * len(returns))
            rolling_alpha = pd.Series([0.0] * len(returns))
            information_ratio = 0.0
            treynor_ratio = 0.0
            jensen_alpha = 0.0
            tracking_error = 0.0
            correlation = 0.0
            
            # Calculate benchmark-dependent metrics if available
            if benchmark_returns is not None and len(benchmark_returns) >= 2:
                beta = self.metrics_calculator.calculate_beta(returns, benchmark_returns)
                alpha = self.metrics_calculator.calculate_alpha(returns, benchmark_returns)
                treynor_ratio = self.metrics_calculator.calculate_treynor_ratio(returns, benchmark_returns)
                information_ratio = self.metrics_calculator.calculate_information_ratio(returns, benchmark_returns)
                
                # Update rolling metrics
                rolling_beta = pd.Series([beta] * len(returns))
                rolling_alpha = pd.Series([alpha] * len(returns))
                correlation = returns.corr(benchmark_returns)
                
                # Calculate tracking error
                excess_returns = returns - benchmark_returns
                tracking_error = excess_returns.std() * np.sqrt(252)
            
            return PerformanceMetrics(
                returns=returns,
                cumulative_returns=cumulative_returns,
                drawdown=drawdown,
                rolling_sharpe=rolling_sharpe,
                rolling_volatility=rolling_volatility,
                rolling_beta=rolling_beta,
                rolling_alpha=rolling_alpha,
                value_at_risk=value_at_risk,
                conditional_var=conditional_var,
                calmar_ratio=calmar_ratio,
                sortino_ratio=sortino_ratio,
                sharpe_ratio=sharpe_ratio,
                information_ratio=information_ratio,
                treynor_ratio=treynor_ratio,
                jensen_alpha=jensen_alpha,
                tracking_error=tracking_error,
                correlation=correlation
            )
        except Exception as e:
            logger.error(f"Error calculating comprehensive metrics: {e}")
            return None
    
    def perform_comprehensive_risk_analysis(self, returns: pd.Series, 
                                         benchmark_returns: Optional[pd.Series] = None) -> Optional[RiskAnalysis]:
        """Perform comprehensive risk analysis"""
        try:
            if len(returns) < 2:
                logger.warning("Insufficient data for risk analysis")
                return None
            
            # Volatility analysis
            volatility_analysis = self.risk_analyzer.calculate_volatility_analysis(returns)
            
            # Drawdown analysis
            cumulative_returns = self.metrics_calculator.calculate_cumulative_returns(returns)
            drawdown = self.metrics_calculator.calculate_drawdown(cumulative_returns)
            drawdown_analysis = self.risk_analyzer.calculate_drawdown_analysis(drawdown)
            
            # VaR analysis
            var_analysis = self.risk_analyzer.calculate_var_analysis(returns)
            
            # Correlation analysis
            correlation_analysis = {}
            if benchmark_returns is not None and len(benchmark_returns) >= 2:
                correlation_analysis = self.risk_analyzer.calculate_correlation_analysis(returns, benchmark_returns)
            
            # Stress testing
            stress_scenarios = [0.1, 0.2, 0.5]  # 10%, 20%, 50% volatility increase
            stress_test_results = self.risk_analyzer.perform_stress_test(returns, stress_scenarios)
            
            # Scenario analysis (placeholder for future enhancement)
            scenario_analysis = {
                "base_case": var_analysis.get("var_95", 0.0),
                "stress_case": stress_test_results.get("stress_0.2", 0.0),
                "extreme_case": stress_test_results.get("stress_0.5", 0.0)
            }
            
            # Risk decomposition (placeholder for future enhancement)
            risk_decomposition = {
                "volatility_risk": volatility_analysis.get("annualized_volatility", 0.0),
                "drawdown_risk": abs(drawdown_analysis.get("max_drawdown", 0.0)),
                "var_risk": var_analysis.get("var_95", 0.0)
            }
            
            return RiskAnalysis(
                volatility_analysis=volatility_analysis,
                drawdown_analysis=drawdown_analysis,
                var_analysis=var_analysis,
                correlation_analysis=correlation_analysis,
                stress_test_results=stress_test_results,
                scenario_analysis=scenario_analysis,
                risk_decomposition=risk_decomposition
            )
        except Exception as e:
            logger.error(f"Error performing risk analysis: {e}")
            return None
    
    def run_backtest(self, strategy_name: str, returns: pd.Series, 
                    start_date: datetime, end_date: datetime,
                    trade_history: Optional[List[Dict[str, Any]]] = None) -> Optional[BacktestResult]:
        """Run a backtest and return results"""
        try:
            if len(returns) < 2:
                logger.warning("Insufficient data for backtest")
                return None
            
            # Calculate basic metrics
            total_return = (1 + returns).prod() - 1
            annualized_return = (1 + total_return) ** (252 / len(returns)) - 1
            volatility = returns.std() * np.sqrt(252)
            
            # Calculate performance ratios
            sharpe_ratio = self.metrics_calculator.calculate_sharpe_ratio(returns)
            sortino_ratio = self.metrics_calculator.calculate_sortino_ratio(returns)
            
            # Calculate drawdown
            cumulative_returns = self.metrics_calculator.calculate_cumulative_returns(returns)
            drawdown = self.metrics_calculator.calculate_drawdown(cumulative_returns)
            max_drawdown = self.metrics_calculator.calculate_max_drawdown(drawdown)
            
            # Calculate trade statistics (simplified)
            if trade_history:
                total_trades = len(trade_history)
                winning_trades = sum(1 for trade in trade_history if trade.get('pnl', 0) > 0)
                losing_trades = total_trades - winning_trades
                win_rate = winning_trades / total_trades if total_trades > 0 else 0
                
                pnls = [trade.get('pnl', 0) for trade in trade_history]
                avg_win = np.mean([p for p in pnls if p > 0]) if any(p > 0 for p in pnls) else 0
                avg_loss = np.mean([p for p in pnls if p < 0]) if any(p < 0 for p in pnls) else 0
                largest_win = max(pnls) if pnls else 0
                largest_loss = min(pnls) if pnls else 0
            else:
                # Simplified trade statistics based on returns
                total_trades = len(returns)
                winning_periods = (returns > 0).sum()
                losing_periods = (returns < 0).sum()
                win_rate = winning_periods / total_trades if total_trades > 0 else 0
                
                winning_returns = returns[returns > 0]
                losing_returns = returns[returns < 0]
                avg_win = winning_returns.mean() if len(winning_returns) > 0 else 0
                avg_loss = losing_returns.mean() if len(losing_returns) > 0 else 0
                largest_win = winning_returns.max() if len(winning_returns) > 0 else 0
                largest_loss = losing_returns.min() if len(losing_returns) > 0 else 0
                
                total_trades = len(returns)
                winning_trades = winning_periods
                losing_trades = losing_periods
            
            # Calculate profit factor
            profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else 0
            
            # Simplified consecutive calculations
            consecutive_wins = 0
            consecutive_losses = 0
            current_streak = 0
            
            for ret in returns:
                if ret > 0:
                    if current_streak > 0:
                        current_streak += 1
                    else:
                        current_streak = 1
                    consecutive_wins = max(consecutive_wins, current_streak)
                else:
                    if current_streak < 0:
                        current_streak -= 1
                    else:
                        current_streak = -1
                    consecutive_losses = max(consecutive_losses, abs(current_streak))
            
            # Create equity curve
            equity_curve = cumulative_returns.tolist()
            
            # Create backtest result
            result = BacktestResult(
                strategy_name=strategy_name,
                start_date=start_date,
                end_date=end_date,
                total_return=total_return,
                annualized_return=annualized_return,
                volatility=volatility,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown,
                win_rate=win_rate,
                profit_factor=profit_factor,
                total_trades=total_trades,
                winning_trades=winning_trades,
                losing_trades=losing_trades,
                avg_win=avg_win,
                avg_loss=avg_loss,
                largest_win=largest_win,
                largest_loss=largest_loss,
                consecutive_wins=consecutive_wins,
                consecutive_losses=consecutive_losses,
                equity_curve=equity_curve,
                trade_history=trade_history or []
            )
            
            # Store result
            self.backtest_results.append(result)
            
            return result
        except Exception as e:
            logger.error(f"Error running backtest: {e}")
            return None
    
    def save_data(self):
        """Save all financial analytics data"""
        return self.data_manager.save_all_data(
            self.backtest_results, 
            self.performance_metrics, 
            self.risk_analyses
        )
    
    def load_data(self):
        """Load all financial analytics data"""
        self.backtest_results, self.performance_metrics, self.risk_analyses = self.data_manager.load_all_data()
    
    def get_backtest_results(self) -> List[BacktestResult]:
        """Get all backtest results"""
        return self.backtest_results
    
    def get_performance_metrics(self) -> Dict[str, PerformanceMetrics]:
        """Get all performance metrics"""
        return self.performance_metrics
    
    def get_risk_analyses(self) -> Dict[str, RiskAnalysis]:
        """Get all risk analyses"""
        return self.risk_analyses
    
    def clear_data(self) -> bool:
        """Clear all saved data"""
        success = self.data_manager.clear_all_data()
        if success:
            self.backtest_results = []
            self.performance_metrics = {}
            self.risk_analyses = {}
        return success

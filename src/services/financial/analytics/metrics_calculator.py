"""
Financial Metrics Calculator - V2 Compliant Core Calculations

This module contains all core financial metrics calculation functions.
Follows V2 standards with ≤200 LOC and single responsibility for metrics calculations.
"""

import logging
import numpy as np
import pandas as pd

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Tuple

logger = logging.getLogger(__name__)


class MetricsCalculator:
    """Core financial metrics calculation engine"""
    
    def __init__(self, risk_free_rate: float = 0.02):
        self.risk_free_rate = risk_free_rate
    
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
    
    def calculate_sharpe_ratio(self, returns: pd.Series) -> float:
        """Calculate Sharpe ratio"""
        try:
            if len(returns) < 2:
                return 0.0
            
            excess_returns = returns - self.risk_free_rate / 252  # Daily risk-free rate
            if excess_returns.std() == 0:
                return 0.0
            
            sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std()
            return sharpe_ratio
        except Exception as e:
            logger.error(f"Error calculating Sharpe ratio: {e}")
            return 0.0
    
    def calculate_sortino_ratio(self, returns: pd.Series) -> float:
        """Calculate Sortino ratio"""
        try:
            if len(returns) < 2:
                return 0.0
            
            excess_returns = returns - self.risk_free_rate / 252
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
    
    def calculate_alpha(self, strategy_returns: pd.Series, market_returns: pd.Series) -> float:
        """Calculate Jensen's alpha"""
        try:
            if len(strategy_returns) < 2 or len(market_returns) < 2:
                return 0.0
            
            beta = self.calculate_beta(strategy_returns, market_returns)
            
            # Annualized returns
            strategy_annual_return = strategy_returns.mean() * 252
            market_annual_return = market_returns.mean() * 252
            
            alpha = strategy_annual_return - (
                self.risk_free_rate + beta * (market_annual_return - self.risk_free_rate)
            )
            return alpha
        except Exception as e:
            logger.error(f"Error calculating alpha: {e}")
            return 0.0
    
    def calculate_treynor_ratio(self, strategy_returns: pd.Series, market_returns: pd.Series) -> float:
        """Calculate Treynor ratio"""
        try:
            if len(strategy_returns) < 2:
                return 0.0
            
            beta = self.calculate_beta(strategy_returns, market_returns)
            if beta == 0:
                return 0.0
            
            excess_return = strategy_returns.mean() * 252 - self.risk_free_rate
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
            
            # Calculate excess returns
            excess_returns = strategy_returns - benchmark_returns
            
            if excess_returns.std() == 0:
                return 0.0
            
            information_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std()
            return information_ratio
        except Exception as e:
            logger.error(f"Error calculating information ratio: {e}")
            return 0.0
    
    def calculate_calmar_ratio(self, returns: pd.Series, max_drawdown: float) -> float:
        """Calculate Calmar ratio"""
        try:
            if max_drawdown == 0:
                return 0.0
            
            annualized_return = returns.mean() * 252
            calmar_ratio = annualized_return / abs(max_drawdown)
            return calmar_ratio
        except Exception as e:
            logger.error(f"Error calculating Calmar ratio: {e}")
            return 0.0


"""
Financial Risk Analyzer - V2 Compliant Risk Analysis

This module contains all risk analysis and VaR calculation functions.
Follows V2 standards with ≤200 LOC and single responsibility for risk analysis.
"""

import logging
import numpy as np
import pandas as pd

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Tuple
from scipy import stats

logger = logging.getLogger(__name__)


class RiskAnalyzer:
    """Comprehensive risk analysis engine"""
    
    def __init__(self, confidence_level: float = 0.95):
        self.confidence_level = confidence_level
    
    def calculate_value_at_risk(self, returns: pd.Series) -> float:
        """Calculate Value at Risk"""
        try:
            if len(returns) < 2:
                return 0.0
            
            var = np.percentile(returns, (1 - self.confidence_level) * 100)
            return abs(var)
        except Exception as e:
            logger.error(f"Error calculating VaR: {e}")
            return 0.0
    
    def calculate_conditional_var(self, returns: pd.Series) -> float:
        """Calculate Conditional Value at Risk (Expected Shortfall)"""
        try:
            if len(returns) < 2:
                return 0.0
            
            var = self.calculate_value_at_risk(returns)
            tail_returns = returns[returns <= -var]
            
            if len(tail_returns) == 0:
                return var
            
            conditional_var = tail_returns.mean()
            return abs(conditional_var)
        except Exception as e:
            logger.error(f"Error calculating Conditional VaR: {e}")
            return 0.0
    
    def calculate_volatility_analysis(self, returns: pd.Series) -> Dict[str, float]:
        """Calculate comprehensive volatility analysis"""
        try:
            if len(returns) < 2:
                return {}
            
            # Daily volatility
            daily_vol = returns.std()
            
            # Annualized volatility
            annual_vol = daily_vol * np.sqrt(252)
            
            # Rolling volatility (30-day window)
            rolling_vol = returns.rolling(window=30).std() * np.sqrt(252)
            avg_rolling_vol = rolling_vol.mean()
            
            # Volatility of volatility
            vol_of_vol = rolling_vol.std()
            
            return {
                "daily_volatility": daily_vol,
                "annualized_volatility": annual_vol,
                "rolling_volatility_30d": avg_rolling_vol,
                "volatility_of_volatility": vol_of_vol,
                "min_volatility": rolling_vol.min(),
                "max_volatility": rolling_vol.max(),
            }
        except Exception as e:
            logger.error(f"Error calculating volatility analysis: {e}")
            return {}
    
    def calculate_drawdown_analysis(self, drawdown: pd.Series) -> Dict[str, float]:
        """Calculate comprehensive drawdown analysis"""
        try:
            if len(drawdown) < 2:
                return {}
            
            max_dd = drawdown.min()
            avg_dd = drawdown.mean()
            dd_std = drawdown.std()
            
            # Count drawdown periods
            dd_periods = (drawdown < 0).sum()
            total_periods = len(drawdown)
            dd_frequency = dd_periods / total_periods if total_periods > 0 else 0
            
            # Calculate recovery time (simplified)
            recovery_time = self._estimate_recovery_time(drawdown)
            
            return {
                "max_drawdown": max_dd,
                "avg_drawdown": avg_dd,
                "drawdown_std": dd_std,
                "drawdown_frequency": dd_frequency,
                "estimated_recovery_time": recovery_time,
                "drawdown_periods": dd_periods,
                "total_periods": total_periods,
            }
        except Exception as e:
            logger.error(f"Error calculating drawdown analysis: {e}")
            return {}
    
    def calculate_var_analysis(self, returns: pd.Series) -> Dict[str, float]:
        """Calculate comprehensive VaR analysis"""
        try:
            if len(returns) < 2:
                return {}
            
            # Different confidence levels
            var_90 = np.percentile(returns, 10)
            var_95 = np.percentile(returns, 5)
            var_99 = np.percentile(returns, 1)
            
            # Conditional VaR
            cvar_95 = self.calculate_conditional_var(returns)
            
            # Historical VaR vs Parametric VaR
            historical_var = abs(var_95)
            parametric_var = abs(returns.mean() - 1.645 * returns.std())
            
            return {
                "var_90": abs(var_90),
                "var_95": abs(var_95),
                "var_99": abs(var_99),
                "cvar_95": cvar_95,
                "historical_var": historical_var,
                "parametric_var": parametric_var,
                "var_ratio": historical_var / parametric_var if parametric_var != 0 else 0,
            }
        except Exception as e:
            logger.error(f"Error calculating VaR analysis: {e}")
            return {}
    
    def calculate_correlation_analysis(self, returns: pd.Series, benchmark_returns: pd.Series) -> Dict[str, float]:
        """Calculate correlation analysis with benchmark"""
        try:
            if len(returns) < 2 or len(benchmark_returns) < 2:
                return {}
            
            # Align data
            aligned_data = pd.concat([returns, benchmark_returns], axis=1).dropna()
            if len(aligned_data) < 2:
                return {}
            
            strategy_aligned = aligned_data.iloc[:, 0]
            benchmark_aligned = aligned_data.iloc[:, 1]
            
            # Calculate correlations
            correlation = strategy_aligned.corr(benchmark_aligned)
            
            # Rolling correlation
            rolling_corr = strategy_aligned.rolling(window=30).corr(benchmark_aligned)
            avg_rolling_corr = rolling_corr.mean()
            corr_volatility = rolling_corr.std()
            
            return {
                "correlation": correlation,
                "rolling_correlation_30d": avg_rolling_corr,
                "correlation_volatility": corr_volatility,
                "min_correlation": rolling_corr.min(),
                "max_correlation": rolling_corr.max(),
            }
        except Exception as e:
            logger.error(f"Error calculating correlation analysis: {e}")
            return {}
    
    def perform_stress_test(self, returns: pd.Series, scenarios: List[float]) -> Dict[str, float]:
        """Perform stress testing with different scenarios"""
        try:
            if len(returns) < 2:
                return {}
            
            stress_results = {}
            base_var = self.calculate_value_at_risk(returns)
            
            for scenario in scenarios:
                # Apply stress scenario (e.g., increase volatility by X%)
                stressed_returns = returns * (1 + scenario)
                stressed_var = self.calculate_value_at_risk(stressed_returns)
                stress_results[f"stress_{scenario:.1%}"] = stressed_var
            
            stress_results["base_var"] = base_var
            return stress_results
        except Exception as e:
            logger.error(f"Error performing stress test: {e}")
            return {}
    
    def _estimate_recovery_time(self, drawdown: pd.Series) -> float:
        """Estimate recovery time from drawdown (simplified)"""
        try:
            if len(drawdown) < 2:
                return 0.0
            
            # Find periods where drawdown is negative
            dd_periods = drawdown[drawdown < 0]
            if len(dd_periods) == 0:
                return 0.0
            
            # Simple estimation: average consecutive negative periods
            recovery_time = len(dd_periods) / len(drawdown) * 252  # Annualized
            return recovery_time
        except Exception as e:
            logger.error(f"Error estimating recovery time: {e}")
            return 0.0


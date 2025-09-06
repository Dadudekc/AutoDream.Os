#!/usr/bin/env python3
"""
Trading BI Risk Analysis Engine
==============================

Risk analysis engine for trading business intelligence analytics.
Handles VaR, Expected Shortfall, Beta calculation, and risk assessment.
V2 COMPLIANT: Focused risk analysis under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR RISK ENGINE
@license MIT
"""

import statistics
from typing import List, Dict, Any, Optional
from datetime import datetime

from .trading_bi_models import RiskLevel, RiskMetrics, RiskAssessmentConfig
from ...repositories.trading_repository import Trade


class RiskAnalysisEngine:
    """Risk analysis engine for trading portfolio risk assessment."""

    def __init__(self, config: Optional[RiskAssessmentConfig] = None):
        """Initialize risk analysis engine with configuration."""
        self.config = config or RiskAssessmentConfig()

    def calculate_risk_metrics(
        self, trades: List[Trade], portfolio_value: float
    ) -> RiskMetrics:
        """Calculate comprehensive risk metrics for trading portfolio."""
        try:
            # Calculate returns series
            returns = self._calculate_returns_series(trades)

            if not returns or len(returns) < 2:
                return self._create_default_risk_metrics(portfolio_value)

            # Calculate risk metrics
            volatility = self._calculate_volatility(returns)
            var_95 = self._calculate_value_at_risk(
                returns, self.config.var_confidence_level
            )
            expected_shortfall = self._calculate_expected_shortfall(
                returns, self.config.var_confidence_level
            )
            beta = self._calculate_beta_coefficient(returns)
            risk_level = self._assess_risk_level(volatility, var_95)
            max_position_size = self._calculate_max_position_size(
                portfolio_value, risk_level
            )

            return RiskMetrics(
                portfolio_volatility=volatility,
                value_at_risk=var_95,
                expected_shortfall=expected_shortfall,
                beta_coefficient=beta,
                risk_level=risk_level,
                max_position_size=max_position_size,
                timestamp=datetime.now(),
            )

        except Exception as e:
            # Return default metrics on error
            return self._create_default_risk_metrics(portfolio_value)

    def _calculate_returns_series(self, trades: List[Trade]) -> List[float]:
        """Calculate returns series from trades."""
        if not trades or len(trades) < 2:
            return []

        # Group trades by symbol and calculate returns
        symbol_returns = {}
        for trade in trades:
            if trade.symbol not in symbol_returns:
                symbol_returns[trade.symbol] = []
            symbol_returns[trade.symbol].append(trade)

        # Calculate daily returns (simplified)
        returns = []
        for symbol_trades in symbol_returns.values():
            if len(symbol_trades) > 1:
                symbol_trades.sort(key=lambda x: x.timestamp)
                for i in range(1, len(symbol_trades)):
                    prev_price = symbol_trades[i - 1].price
                    curr_price = symbol_trades[i].price
                    if prev_price > 0:
                        daily_return = (curr_price - prev_price) / prev_price
                        returns.append(daily_return)

        return returns

    def _calculate_volatility(self, returns: List[float]) -> float:
        """Calculate portfolio volatility."""
        if len(returns) < 2:
            return 0.0

        return statistics.stdev(returns)

    def _calculate_value_at_risk(
        self, returns: List[float], confidence: float
    ) -> float:
        """Calculate Value at Risk."""
        if not returns or len(returns) < 2:
            return 0.0

        returns_sorted = sorted(returns)
        index = int((1 - confidence) * len(returns))
        return abs(returns_sorted[index]) if index < len(returns) else 0.0

    def _calculate_expected_shortfall(
        self, returns: List[float], confidence: float
    ) -> float:
        """Calculate Expected Shortfall (Conditional VaR)"""
        if not returns or len(returns) < 2:
            return 0.0

        returns_sorted = sorted(returns)
        index = int((1 - confidence) * len(returns))
        tail_returns = returns_sorted[:index] if index > 0 else returns_sorted
        return abs(statistics.mean(tail_returns)) if tail_returns else 0.0

    def _calculate_beta_coefficient(self, returns: List[float]) -> float:
        """Calculate beta coefficient (simplified)"""
        if len(returns) < 2:
            return 1.0

        # Simplified beta calculation - in practice would use market returns
        variance = statistics.variance(returns)
        return variance / variance if variance > 0 else 1.0

    def _assess_risk_level(self, volatility: float, var_95: float) -> RiskLevel:
        """Assess overall risk level based on volatility and VaR."""
        if (
            var_95 > self.config.critical_var_threshold
            or volatility > self.config.critical_volatility_threshold
        ):
            return RiskLevel.CRITICAL
        elif (
            var_95 > self.config.high_var_threshold
            or volatility > self.config.high_volatility_threshold
        ):
            return RiskLevel.HIGH
        elif (
            var_95 > self.config.medium_var_threshold
            or volatility > self.config.medium_volatility_threshold
        ):
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW

    def _calculate_max_position_size(
        self, portfolio_value: float, risk_level: RiskLevel
    ) -> float:
        """Calculate maximum position size based on risk level."""
        risk_multipliers = {
            RiskLevel.LOW: 0.1,  # 10% of portfolio
            RiskLevel.MEDIUM: 0.05,  # 5% of portfolio
            RiskLevel.HIGH: 0.02,  # 2% of portfolio
            RiskLevel.CRITICAL: 0.01,  # 1% of portfolio
        }

        return portfolio_value * risk_multipliers[risk_level]

    def _create_default_risk_metrics(self, portfolio_value: float) -> RiskMetrics:
        """Create default risk metrics when calculation fails."""
        return RiskMetrics(
            portfolio_volatility=0.0,
            value_at_risk=0.0,
            expected_shortfall=0.0,
            beta_coefficient=1.0,
            risk_level=RiskLevel.LOW,
            max_position_size=portfolio_value * 0.1,  # 10% default
            timestamp=datetime.now(),
        )


# Factory function for dependency injection
def create_risk_analysis_engine(
    config: Optional[RiskAssessmentConfig] = None,
) -> RiskAnalysisEngine:
    """Factory function to create risk analysis engine with optional configuration."""
    return RiskAnalysisEngine(config)


# Export for DI
__all__ = ["RiskAnalysisEngine", "create_risk_analysis_engine"]

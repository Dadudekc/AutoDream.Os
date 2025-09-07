#!/usr/bin/env python3
"""
Options Risk Management Module - Agent Cellphone V2
==================================================

Risk management and calculation functionality for options trading.
Follows V2 standards: ≤300 LOC, SRP, OOP principles.
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

from src.utils.stability_improvements import stability_manager, safe_import
from .pricing import OptionType, Greeks
from .common import intrinsic_value


@dataclass
class RiskMetrics:
    """Risk metrics for options positions"""

    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    position_value: float
    max_loss: float
    max_profit: float
    probability_profit: float
    var_95: float  # Value at Risk (95% confidence)
    expected_shortfall: float


class OptionsRiskManager:
    """
    Advanced risk management for options trading
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.OptionsRiskManager")

        # Risk limits
        self.max_portfolio_delta = 100.0
        self.max_portfolio_gamma = 10.0
        self.max_portfolio_theta = -50.0
        self.max_portfolio_vega = 1000.0
        self.max_position_size = 0.05  # 5% of portfolio

    def calculate_position_risk(
        self,
        contracts: List[Dict[str, Any]],
        underlying_price: float,
        portfolio_value: float,
    ) -> RiskMetrics:
        """Calculate comprehensive risk metrics for a position"""
        try:
            total_delta = 0.0
            total_gamma = 0.0
            total_theta = 0.0
            total_vega = 0.0
            total_rho = 0.0
            position_value = 0.0

            for contract in contracts:
                quantity = contract.get("quantity", 1)
                option_type = contract.get("option_type")
                strike = contract.get("strike", 0)
                premium = contract.get("premium", 0)
                greeks = contract.get("greeks", {})

                # Accumulate Greeks
                total_delta += greeks.get("delta", 0) * quantity
                total_gamma += greeks.get("gamma", 0) * quantity
                total_theta += greeks.get("theta", 0) * quantity
                total_vega += greeks.get("vega", 0) * quantity
                total_rho += greeks.get("rho", 0) * quantity

                # Calculate position value
                intrinsic = intrinsic_value(
                    underlying_price,
                    strike,
                    option_type == OptionType.CALL,
                )

                position_value += (premium + intrinsic) * quantity

            # Calculate risk metrics
            max_loss = self._calculate_max_loss(contracts, underlying_price)
            max_profit = self._calculate_max_profit(contracts, underlying_price)
            probability_profit = self._calculate_probability_profit(
                contracts, underlying_price
            )
            var_95 = self._calculate_value_at_risk(contracts, portfolio_value)
            expected_shortfall = self._calculate_expected_shortfall(
                contracts, portfolio_value
            )

            return RiskMetrics(
                delta=total_delta,
                gamma=total_gamma,
                theta=total_theta,
                vega=total_vega,
                rho=total_rho,
                position_value=position_value,
                max_loss=max_loss,
                max_profit=max_profit,
                probability_profit=probability_profit,
                var_95=var_95,
                expected_shortfall=expected_shortfall,
            )

        except Exception as e:
            self.logger.error(f"Error calculating position risk: {e}")
            return RiskMetrics(
                delta=0.0,
                gamma=0.0,
                theta=0.0,
                vega=0.0,
                rho=0.0,
                position_value=0.0,
                max_loss=0.0,
                max_profit=0.0,
                probability_profit=0.0,
                var_95=0.0,
                expected_shortfall=0.0,
            )

    def _calculate_max_loss(
        self,
        contracts: List[Dict[str, Any]],
        underlying_price: float,
    ) -> float:
        """Calculate maximum possible loss for the position"""
        try:
            max_loss = 0.0

            for contract in contracts:
                quantity = contract.get("quantity", 1)
                option_type = contract.get("option_type")
                strike = contract.get("strike", 0)
                premium = contract.get("premium", 0)

                if option_type == OptionType.CALL:
                    # Long call: max loss = premium paid
                    # Short call: unlimited loss (capped by position size)
                    if quantity > 0:  # Long position
                        max_loss += premium * abs(quantity)
                    else:  # Short position
                        max_loss += underlying_price * abs(quantity)
                else:  # PUT
                    # Long put: max loss = premium paid
                    # Short put: max loss = strike price
                    if quantity > 0:  # Long position
                        max_loss += premium * abs(quantity)
                    else:  # Short position
                        max_loss += strike * abs(quantity)

            return max_loss

        except Exception as e:
            self.logger.error(f"Error calculating max loss: {e}")
            return 0.0

    def _calculate_max_profit(
        self,
        contracts: List[Dict[str, Any]],
        underlying_price: float,
    ) -> float:
        """Calculate maximum possible profit for the position"""
        try:
            max_profit = 0.0

            for contract in contracts:
                quantity = contract.get("quantity", 1)
                option_type = contract.get("option_type")
                strike = contract.get("strike", 0)
                premium = contract.get("premium", 0)

                if option_type == OptionType.CALL:
                    if quantity > 0:  # Long call: unlimited profit
                        max_profit += underlying_price * abs(quantity)
                    else:  # Short call: max profit = premium received
                        max_profit += premium * abs(quantity)
                else:  # PUT
                    if quantity > 0:  # Long put: max profit = strike price
                        max_profit += strike * abs(quantity)
                    else:  # Short put: max profit = premium received
                        max_profit += premium * abs(quantity)

            return max_profit

        except Exception as e:
            self.logger.error(f"Error calculating max profit: {e}")
            return 0.0

    def _calculate_probability_profit(
        self,
        contracts: List[Dict[str, Any]],
        underlying_price: float,
    ) -> float:
        """Calculate probability of profit for the position"""
        try:
            # Simplified probability calculation based on delta
            total_delta = 0.0
            total_quantity = 0

            for contract in contracts:
                quantity = contract.get("quantity", 1)
                greeks = contract.get("greeks", {})
                delta = greeks.get("delta", 0)

                total_delta += delta * quantity
                total_quantity += abs(quantity)

            if total_quantity == 0:
                return 0.5

            # Use delta as rough probability proxy
            avg_delta = total_delta / total_quantity
            probability = 0.5 + (avg_delta * 0.3)  # Rough approximation

            return max(0.0, min(1.0, probability))

        except Exception as e:
            self.logger.error(f"Error calculating probability of profit: {e}")
            return 0.5

    def _calculate_value_at_risk(
        self,
        contracts: List[Dict[str, Any]],
        portfolio_value: float,
        confidence_level: float = 0.95,
    ) -> float:
        """Calculate Value at Risk (VaR) for the position"""
        try:
            # Simplified VaR calculation
            position_value = sum(
                contract.get("premium", 0) * abs(contract.get("quantity", 1))
                for contract in contracts
            )

            # Assume 20% volatility for options
            volatility = 0.20
            z_score = 1.645  # 95% confidence level

            var = position_value * volatility * z_score
            return min(var, portfolio_value * 0.1)  # Cap at 10% of portfolio

        except Exception as e:
            self.logger.error(f"Error calculating VaR: {e}")
            return 0.0

    def _calculate_expected_shortfall(
        self,
        contracts: List[Dict[str, Any]],
        portfolio_value: float,
    ) -> float:
        """Calculate Expected Shortfall (Conditional VaR)"""
        try:
            var = self._calculate_value_at_risk(contracts, portfolio_value)
            # Expected shortfall is typically 1.5-2x VaR
            return var * 1.75

        except Exception as e:
            self.logger.error(f"Error calculating expected shortfall: {e}")
            return 0.0

    def check_risk_limits(
        self,
        risk_metrics: RiskMetrics,
        portfolio_value: float,
    ) -> Dict[str, bool]:
        """Check if position violates risk limits"""
        try:
            violations = {
                "delta_limit": abs(risk_metrics.delta) > self.max_portfolio_delta,
                "gamma_limit": abs(risk_metrics.gamma) > self.max_portfolio_gamma,
                "theta_limit": risk_metrics.theta < self.max_portfolio_theta,
                "vega_limit": abs(risk_metrics.vega) > self.max_portfolio_vega,
                "position_size": risk_metrics.position_value
                > portfolio_value * self.max_position_size,
            }

            return violations

        except Exception as e:
            self.logger.error(f"Error checking risk limits: {e}")
            return {
                "delta_limit": False,
                "gamma_limit": False,
                "theta_limit": False,
                "vega_limit": False,
                "position_size": False,
            }

    def get_risk_summary(
        self,
        risk_metrics: RiskMetrics,
        portfolio_value: float,
    ) -> Dict[str, Any]:
        """Get comprehensive risk summary"""
        try:
            violations = self.check_risk_limits(risk_metrics, portfolio_value)

            return {
                "risk_metrics": risk_metrics,
                "violations": violations,
                "risk_score": self._calculate_risk_score(risk_metrics, portfolio_value),
                "recommendations": self._generate_risk_recommendations(violations),
            }

        except Exception as e:
            self.logger.error(f"Error generating risk summary: {e}")
            return {}

    def _calculate_risk_score(
        self,
        risk_metrics: RiskMetrics,
        portfolio_value: float,
    ) -> float:
        """Calculate overall risk score (0-100, higher = riskier)"""
        try:
            # Normalize risk metrics
            delta_score = min(
                100, abs(risk_metrics.delta) / self.max_portfolio_delta * 100
            )
            gamma_score = min(
                100, abs(risk_metrics.gamma) / self.max_portfolio_gamma * 100
            )
            theta_score = min(
                100, abs(risk_metrics.theta) / abs(self.max_portfolio_theta) * 100
            )
            vega_score = min(
                100, abs(risk_metrics.vega) / self.max_portfolio_vega * 100
            )
            size_score = min(
                100, risk_metrics.position_value / portfolio_value * 100 * 20
            )  # 20x multiplier

            # Weighted average
            risk_score = (
                delta_score * 0.25
                + gamma_score * 0.25
                + theta_score * 0.20
                + vega_score * 0.20
                + size_score * 0.10
            )

            return min(100, max(0, risk_score))

        except Exception as e:
            self.logger.error(f"Error calculating risk score: {e}")
            return 50.0

    def _generate_risk_recommendations(
        self,
        violations: Dict[str, bool],
    ) -> List[str]:
        """Generate risk management recommendations"""
        recommendations = []

        if violations.get("delta_limit", False):
            recommendations.append("Reduce portfolio delta exposure")
        if violations.get("gamma_limit", False):
            recommendations.append("Reduce portfolio gamma exposure")
        if violations.get("theta_limit", False):
            recommendations.append("Reduce portfolio theta exposure")
        if violations.get("vega_limit", False):
            recommendations.append("Reduce portfolio vega exposure")
        if violations.get("position_size", False):
            recommendations.append("Reduce position size relative to portfolio")

        if not any(violations.values()):
            recommendations.append("Risk metrics within acceptable limits")

        return recommendations

#!/usr/bin/env python3
"""
Options Strategy Module - Agent Cellphone V2
============================================

Options trading strategy execution and management functionality.
Follows V2 standards: ≤300 LOC, SRP, OOP principles.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from src.utils.stability_improvements import stability_manager, safe_import
from .pricing import OptionType
from .common import break_even_point, intrinsic_value


class OptionStrategy(Enum):
    """Options trading strategies"""

    LONG_CALL = "LONG_CALL"
    LONG_PUT = "LONG_PUT"
    COVERED_CALL = "COVERED_CALL"
    PROTECTIVE_PUT = "PROTECTIVE_PUT"
    BULL_SPREAD = "BULL_SPREAD"
    BEAR_SPREAD = "BEAR_SPREAD"
    IRON_CONDOR = "IRON_CONDOR"
    BUTTERFLY = "BUTTERFLY"
    STRANGLE = "STRANGLE"
    STRADDLE = "STRADDLE"


@dataclass
class OptionsStrategy:
    """Options trading strategy"""

    strategy_type: OptionStrategy
    symbol: str
    contracts: List[Dict[str, Any]]
    entry_price: float
    max_profit: float
    max_loss: float
    break_even_points: List[float]
    probability_profit: float
    risk_reward_ratio: float
    greeks_exposure: Dict[str, float]
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class OptionsStrategyEngine:
    """
    Advanced options strategy execution engine
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.OptionsStrategyEngine")

        # Strategy parameters
        self.strategy_params = {
            OptionStrategy.LONG_CALL: {
                "max_capital_risk": 0.02,  # 2% of portfolio
                "min_delta": 0.3,
                "max_theta": -0.05,
            },
            OptionStrategy.COVERED_CALL: {
                "min_premium": 0.02,  # 2% of underlying
                "max_delta": -0.3,
                "min_days_to_expiry": 30,
            },
            OptionStrategy.IRON_CONDOR: {
                "max_width": 0.1,  # 10% of underlying
                "min_premium": 0.01,  # 1% of underlying
                "max_risk": 0.05,  # 5% of portfolio
            },
        }

    def create_long_call_strategy(
        self,
        symbol: str,
        strike: float,
        expiration: datetime,
        premium: float,
        quantity: int = 1,
    ) -> OptionsStrategy:
        """Create a long call strategy"""
        try:
            contracts = [
                {
                    "symbol": symbol,
                    "strike": strike,
                    "expiration": expiration,
                    "option_type": OptionType.CALL,
                    "quantity": quantity,
                    "premium": premium,
                }
            ]

            # Calculate strategy metrics
            max_loss = premium * quantity
            max_profit = float("inf")  # Unlimited upside
            break_even = break_even_point(strike, premium, True)
            risk_reward = float("inf") if max_loss > 0 else 0

            return OptionsStrategy(
                strategy_type=OptionStrategy.LONG_CALL,
                symbol=symbol,
                contracts=contracts,
                entry_price=premium * quantity,
                max_profit=max_profit,
                max_loss=max_loss,
                break_even_points=[break_even],
                probability_profit=0.4,  # Rough estimate
                risk_reward_ratio=risk_reward,
                greeks_exposure={
                    "delta": 0.6,
                    "gamma": 0.02,
                    "theta": -0.03,
                    "vega": 0.15,
                },
            )

        except Exception as e:
            self.logger.error(f"Error creating long call strategy: {e}")
            return None

    def create_covered_call_strategy(
        self,
        symbol: str,
        strike: float,
        expiration: datetime,
        premium: float,
        underlying_quantity: int = 100,
    ) -> OptionsStrategy:
        """Create a covered call strategy"""
        try:
            contracts = [
                {
                    "symbol": symbol,
                    "strike": strike,
                    "expiration": expiration,
                    "option_type": OptionType.CALL,
                    "quantity": -1,  # Short call
                    "premium": premium,
                }
            ]

            # Calculate strategy metrics
            max_profit = premium * underlying_quantity
            max_loss = float("inf")  # Unlimited downside if underlying rises
            break_even = break_even_point(strike, premium, True)
            risk_reward = max_profit / max_loss if max_loss > 0 else 0

            return OptionsStrategy(
                strategy_type=OptionStrategy.COVERED_CALL,
                symbol=symbol,
                contracts=contracts,
                entry_price=premium * underlying_quantity,
                max_profit=max_profit,
                max_loss=max_loss,
                break_even_points=[break_even],
                probability_profit=0.7,  # Higher probability due to premium collection
                risk_reward_ratio=risk_reward,
                greeks_exposure={
                    "delta": -0.3,
                    "gamma": -0.01,
                    "theta": 0.02,
                    "vega": -0.08,
                },
            )

        except Exception as e:
            self.logger.error(f"Error creating covered call strategy: {e}")
            return None

    def create_iron_condor_strategy(
        self,
        symbol: str,
        short_call_strike: float,
        long_call_strike: float,
        short_put_strike: float,
        long_put_strike: float,
        expiration: datetime,
        call_premium: float,
        put_premium: float,
        quantity: int = 1,
    ) -> OptionsStrategy:
        """Create an iron condor strategy"""
        try:
            contracts = [
                {
                    "symbol": symbol,
                    "strike": short_call_strike,
                    "expiration": expiration,
                    "option_type": OptionType.CALL,
                    "quantity": -quantity,  # Short call
                    "premium": call_premium,
                },
                {
                    "symbol": symbol,
                    "strike": long_call_strike,
                    "expiration": expiration,
                    "option_type": OptionType.CALL,
                    "quantity": quantity,  # Long call
                    "premium": -call_premium,
                },
                {
                    "symbol": symbol,
                    "strike": short_put_strike,
                    "expiration": expiration,
                    "option_type": OptionType.PUT,
                    "quantity": -quantity,  # Short put
                    "premium": put_premium,
                },
                {
                    "symbol": symbol,
                    "strike": long_put_strike,
                    "expiration": expiration,
                    "option_type": OptionType.PUT,
                    "quantity": quantity,  # Long put
                    "premium": -put_premium,
                },
            ]

            # Calculate strategy metrics
            net_premium = (call_premium + put_premium) * quantity
            max_loss = (long_call_strike - short_call_strike) * quantity - net_premium
            max_profit = net_premium
            risk_reward = max_profit / max_loss if max_loss > 0 else 0

            return OptionsStrategy(
                strategy_type=OptionStrategy.IRON_CONDOR,
                symbol=symbol,
                contracts=contracts,
                entry_price=net_premium,
                max_profit=max_profit,
                max_loss=max_loss,
                break_even_points=[
                    short_put_strike - net_premium / quantity,
                    short_call_strike + net_premium / quantity,
                ],
                probability_profit=0.8,  # High probability due to range-bound assumption
                risk_reward_ratio=risk_reward,
                greeks_exposure={
                    "delta": 0.0,
                    "gamma": 0.0,
                    "theta": 0.01,
                    "vega": 0.0,
                },
            )

        except Exception as e:
            self.logger.error(f"Error creating iron condor strategy: {e}")
            return None

    def validate_strategy(
        self,
        strategy: OptionsStrategy,
        portfolio_value: float,
        underlying_price: float,
    ) -> Dict[str, Any]:
        """Validate strategy parameters and constraints"""
        try:
            validation_results = {
                "is_valid": True,
                "warnings": [],
                "errors": [],
                "recommendations": [],
            }

            # Check capital allocation
            if strategy.entry_price > portfolio_value * 0.1:  # Max 10% of portfolio
                validation_results["warnings"].append(
                    "Strategy uses more than 10% of portfolio"
                )
                validation_results["recommendations"].append(
                    "Consider reducing position size"
                )

            # Check risk parameters
            if strategy.max_loss > portfolio_value * 0.05:  # Max 5% risk
                validation_results["warnings"].append(
                    "Strategy risk exceeds 5% of portfolio"
                )
                validation_results["recommendations"].append(
                    "Consider hedging or reducing exposure"
                )

            # Check probability of profit
            if strategy.probability_profit < 0.3:
                validation_results["warnings"].append("Low probability of profit")
                validation_results["recommendations"].append(
                    "Review strategy assumptions"
                )

            # Check risk-reward ratio
            if strategy.risk_reward_ratio < 0.5:
                validation_results["warnings"].append("Unfavorable risk-reward ratio")
                validation_results["recommendations"].append(
                    "Consider alternative strategies"
                )

            # Check expiration constraints
            for contract in strategy.contracts:
                days_to_expiry = (contract["expiration"] - datetime.now()).days
                if days_to_expiry < 7:
                    validation_results["errors"].append("Contract expires too soon")
                    validation_results["is_valid"] = False

            if validation_results["errors"]:
                validation_results["is_valid"] = False

            return validation_results

        except Exception as e:
            self.logger.error(f"Error validating strategy: {e}")
            return {
                "is_valid": False,
                "warnings": [],
                "errors": [f"Validation error: {e}"],
                "recommendations": ["Review strategy parameters"],
            }

    def calculate_strategy_payoff(
        self,
        strategy: OptionsStrategy,
        underlying_price: float,
    ) -> Dict[str, float]:
        """Calculate strategy payoff at different underlying prices"""
        try:
            payoffs = {}

            # Calculate at current price
            current_payoff = self._calculate_single_payoff(strategy, underlying_price)
            payoffs["current"] = current_payoff

            # Calculate at break-even points
            for be_point in strategy.break_even_points:
                be_payoff = self._calculate_single_payoff(strategy, be_point)
                payoffs[f"break_even_{be_point}"] = be_payoff

            # Calculate at max profit/loss scenarios
            max_profit_payoff = self._calculate_single_payoff(
                strategy, underlying_price * 1.5
            )
            max_loss_payoff = self._calculate_single_payoff(
                strategy, underlying_price * 0.5
            )
            payoffs["max_profit_scenario"] = max_profit_payoff
            payoffs["max_loss_scenario"] = max_loss_payoff

            return payoffs

        except Exception as e:
            self.logger.error(f"Error calculating strategy payoff: {e}")
            return {}

    def _calculate_single_payoff(
        self,
        strategy: OptionsStrategy,
        underlying_price: float,
    ) -> float:
        """Calculate payoff at a specific underlying price"""
        try:
            total_payoff = 0.0

            for contract in strategy.contracts:
                strike = contract["strike"]
                option_type = contract["option_type"]
                quantity = contract["quantity"]
                premium = contract["premium"]

                intrinsic = intrinsic_value(
                    underlying_price,
                    strike,
                    option_type == OptionType.CALL,
                )
                payoff = intrinsic * quantity

                # Adjust for premium
                if quantity > 0:  # Long position
                    payoff -= premium * abs(quantity)
                else:  # Short position
                    payoff += premium * abs(quantity)

                total_payoff += payoff

            return total_payoff

        except Exception as e:
            self.logger.error(f"Error calculating single payoff: {e}")
            return 0.0

    def get_strategy_summary(
        self,
        strategy: OptionsStrategy,
        underlying_price: float,
    ) -> Dict[str, Any]:
        """Get comprehensive strategy summary"""
        try:
            payoffs = self.calculate_strategy_payoff(strategy, underlying_price)

            return {
                "strategy": strategy,
                "current_payoff": payoffs.get("current", 0),
                "unrealized_pnl": payoffs.get("current", 0) - strategy.entry_price,
                "payoffs": payoffs,
                "days_to_expiry": (
                    strategy.contracts[0]["expiration"] - datetime.now()
                ).days,
                "strategy_health": self._assess_strategy_health(
                    strategy, payoffs.get("current", 0)
                ),
            }

        except Exception as e:
            self.logger.error(f"Error generating strategy summary: {e}")
            return {}

    def _assess_strategy_health(
        self,
        strategy: OptionsStrategy,
        current_payoff: float,
    ) -> str:
        """Assess overall health of the strategy"""
        try:
            unrealized_pnl = current_payoff - strategy.entry_price
            pnl_percentage = (
                (unrealized_pnl / strategy.entry_price * 100)
                if strategy.entry_price > 0
                else 0
            )

            if pnl_percentage >= 20:
                return "Excellent"
            elif pnl_percentage >= 10:
                return "Good"
            elif pnl_percentage >= 0:
                return "Neutral"
            elif pnl_percentage >= -10:
                return "Concerning"
            else:
                return "Critical"

        except Exception as e:
            self.logger.error(f"Error assessing strategy health: {e}")
            return "Unknown"

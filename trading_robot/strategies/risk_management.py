"""
Risk Management - V2 Compliant
===============================

Position sizing and risk calculations.
Extracted from base_strategy.py for V2 compliance.

Author: Agent-3 - Infrastructure & DevOps Specialist (extracted)
"""

from .signal_processing import Signal, StrategyResult


class RiskManagement:
    """Risk management utilities for trading strategies."""

    @staticmethod
    def calculate_position_size(
        account_balance: float, price: float, risk_pct: float = 0.01
    ) -> int:
        """Calculate position size based on risk management."""
        risk_amount = account_balance * risk_pct
        position_size = risk_amount / price
        return max(1, int(position_size))

    @staticmethod
    def get_consensus_signal(results: list[StrategyResult]) -> tuple[Signal, float]:
        """Get consensus signal from multiple strategies."""
        if not results:
            return Signal.HOLD, 0.0

        buy_votes = sum(1 for r in results if r.signal == Signal.BUY)
        sell_votes = sum(1 for r in results if r.signal == Signal.SELL)
        hold_votes = sum(1 for r in results if r.signal == Signal.HOLD)

        total = len(results)
        buy_conf = sum(r.confidence for r in results if r.signal == Signal.BUY)
        sell_conf = sum(r.confidence for r in results if r.signal == Signal.SELL)

        if buy_votes > sell_votes and buy_votes > hold_votes:
            return Signal.BUY, buy_conf / buy_votes if buy_votes > 0 else 0.0
        elif sell_votes > buy_votes and sell_votes > hold_votes:
            return Signal.SELL, sell_conf / sell_votes if sell_votes > 0 else 0.0
        else:
            return Signal.HOLD, 0.0

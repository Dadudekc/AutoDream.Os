"""Risk service wrapper."""
from __future__ import annotations

from typing import Optional

from .risk_management_service import RiskManager
from .portfolio_service import PortfolioService


class RiskService:
    """Provide access to risk management features."""

    def __init__(self, portfolio: Optional[PortfolioService] = None) -> None:
        portfolio_manager = portfolio.manager if portfolio else None
        self.manager = RiskManager(portfolio_manager=portfolio_manager)

    def get_risk_profile(self):
        """Return a fresh risk profile."""
        return self.manager.get_risk_profile()

"""
Trading Repository Interfaces - V2 Compliant Modular Architecture
================================================================

Modular trading repository interfaces with clean separation of concerns.
Each module handles a specific aspect of trading data access.

V2 Compliance: < 300 lines per module, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from .trading_repository_interface import TradingRepositoryInterface
from .position_repository_interface import PositionRepositoryInterface
from .portfolio_repository_interface import PortfolioRepositoryInterface

__all__ = [
    'TradingRepositoryInterface',
    'PositionRepositoryInterface',
    'PortfolioRepositoryInterface'
]
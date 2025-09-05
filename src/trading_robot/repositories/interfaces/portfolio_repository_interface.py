"""
Portfolio Repository Interface - V2 Compliant Module
===================================================

Abstract interface for portfolio data access with V2 compliance.
Extracted from trading_repository.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..models import Portfolio


class PortfolioRepositoryInterface(ABC):
    """
    Abstract interface for portfolio data access with V2 compliance.

    V2 COMPLIANCE: Repository pattern with async operations and comprehensive error handling.
    DESIGN PATTERN: Repository pattern providing clean data access abstraction.
    """

    @abstractmethod
    async def save_portfolio(self, portfolio: Portfolio) -> bool:
        """
        Save portfolio to storage.

        Args:
            portfolio: Portfolio object to save

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def get_portfolio(self, portfolio_id: str) -> Optional[Portfolio]:
        """
        Retrieve portfolio by ID.

        Args:
            portfolio_id: Unique identifier for the portfolio

        Returns:
            Portfolio object if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_all_portfolios(self) -> List[Portfolio]:
        """
        Get all portfolios.

        Returns:
            List of Portfolio objects
        """
        pass

    @abstractmethod
    async def update_portfolio(self, portfolio: Portfolio) -> bool:
        """
        Update existing portfolio.

        Args:
            portfolio: Portfolio object to update

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def delete_portfolio(self, portfolio_id: str) -> bool:
        """
        Delete portfolio by ID.

        Args:
            portfolio_id: Unique identifier for the portfolio

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def get_portfolio_by_name(self, name: str) -> Optional[Portfolio]:
        """
        Retrieve portfolio by name.

        Args:
            name: Portfolio name

        Returns:
            Portfolio object if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_portfolio_count(self) -> int:
        """
        Get total number of portfolios.

        Returns:
            Total number of portfolios in storage
        """
        pass

    @abstractmethod
    async def clear_all_portfolios(self) -> bool:
        """
        Clear all portfolios from storage.

        Returns:
            True if successful, False otherwise
        """
        pass

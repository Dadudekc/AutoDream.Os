"""
Position Repository Interface - V2 Compliant Module
==================================================

Abstract interface for position data access with V2 compliance.
Extracted from trading_repository.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..models import Position


class PositionRepositoryInterface(ABC):
    """
    Abstract interface for position data access with V2 compliance.

    V2 COMPLIANCE: Repository pattern with async operations and comprehensive error handling.
    DESIGN PATTERN: Repository pattern providing clean data access abstraction.
    """

    @abstractmethod
    async def save_position(self, position: Position) -> bool:
        """
        Save position to storage.

        Args:
            position: Position object to save

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def get_position(self, symbol: str) -> Optional[Position]:
        """
        Retrieve position by symbol.

        Args:
            symbol: Trading symbol

        Returns:
            Position object if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_all_positions(self) -> List[Position]:
        """
        Get all positions.

        Returns:
            List of Position objects
        """
        pass

    @abstractmethod
    async def update_position(self, position: Position) -> bool:
        """
        Update existing position.

        Args:
            position: Position object to update

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def delete_position(self, symbol: str) -> bool:
        """
        Delete position by symbol.

        Args:
            symbol: Trading symbol

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def get_long_positions(self) -> List[Position]:
        """
        Get all long positions.

        Returns:
            List of long Position objects
        """
        pass

    @abstractmethod
    async def get_short_positions(self) -> List[Position]:
        """
        Get all short positions.

        Returns:
            List of short Position objects
        """
        pass

    @abstractmethod
    async def get_flat_positions(self) -> List[Position]:
        """
        Get all flat positions.

        Returns:
            List of flat Position objects
        """
        pass

    @abstractmethod
    async def get_profitable_positions(self) -> List[Position]:
        """
        Get all profitable positions.

        Returns:
            List of profitable Position objects
        """
        pass

    @abstractmethod
    async def get_losing_positions(self) -> List[Position]:
        """
        Get all losing positions.

        Returns:
            List of losing Position objects
        """
        pass

    @abstractmethod
    async def update_position_prices(self, price_updates: dict) -> bool:
        """
        Update current prices for positions.

        Args:
            price_updates: Dictionary of symbol -> price mappings

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def get_position_count(self) -> int:
        """
        Get total number of positions.

        Returns:
            Total number of positions in storage
        """
        pass

    @abstractmethod
    async def clear_all_positions(self) -> bool:
        """
        Clear all positions from storage.

        Returns:
            True if successful, False otherwise
        """
        pass

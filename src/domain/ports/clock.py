"""
Clock Port - Domain Interface
=============================

Defines the contract for time operations.
This enables the domain to be testable with controllable time.
"""

from typing import Protocol
from datetime import datetime


class Clock(Protocol):
    """
    Port for time operations.

    This protocol allows the domain to work with time in a testable way.
    Implementations can provide real time or controlled/fixed time for testing.
    """

    def now(self) -> datetime:
        """
        Get the current time.

        Returns:
            Current datetime in UTC
        """
        ...

    def utcnow(self) -> datetime:
        """
        Get the current UTC time.

        Returns:
            Current UTC datetime
        """
        ...

    def from_timestamp(self, timestamp: float) -> datetime:
        """
        Create datetime from Unix timestamp.

        Args:
            timestamp: Unix timestamp (seconds since epoch)

        Returns:
            Datetime object
        """
        ...

    def to_timestamp(self, dt: datetime) -> float:
        """
        Convert datetime to Unix timestamp.

        Args:
            dt: Datetime object

        Returns:
            Unix timestamp (seconds since epoch)
        """
        ...

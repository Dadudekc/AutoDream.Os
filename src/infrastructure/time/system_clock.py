"""
System Clock - Infrastructure Adapter
=====================================

Concrete implementation of Clock using system time.
"""

from datetime import datetime
from src.domain.ports.clock import Clock


class SystemClock(Clock):
    """
    System clock implementation using Python's datetime.

    This adapter provides real system time for the domain layer.
    """

    def now(self) -> datetime:
        """
        Get the current time.

        Returns:
            Current datetime in UTC
        """
        return datetime.now()

    def utcnow(self) -> datetime:
        """
        Get the current UTC time.

        Returns:
            Current UTC datetime
        """
        return datetime.utcnow()

    def from_timestamp(self, timestamp: float) -> datetime:
        """
        Create datetime from Unix timestamp.

        Args:
            timestamp: Unix timestamp (seconds since epoch)

        Returns:
            Datetime object
        """
        return datetime.fromtimestamp(timestamp)

    def to_timestamp(self, dt: datetime) -> float:
        """
        Convert datetime to Unix timestamp.

        Args:
            dt: Datetime object

        Returns:
            Unix timestamp (seconds since epoch)
        """
        return dt.timestamp()

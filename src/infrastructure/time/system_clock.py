#!/usr/bin/env python3
"""
System Clock and Time Operations - V2 Compliance Module
======================================================

Time management functionality extracted from unified_logging_time.py.

Author: Agent-5 (Business Intelligence & Team Beta Leader) - V2 Refactoring
License: MIT
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta, timezone


@dataclass
class TimeConfig:
    """Configuration for time operations."""

    timezone: str = "UTC"
    time_format: str = "%Y-%m-%d %H:%M:%S"
    date_format: str = "%Y-%m-%d"
    datetime_format: str = "%Y-%m-%d %H:%M:%S"


class ClockInterface(ABC):
    """Abstract interface for time operations."""

    @abstractmethod
    def now(self) -> datetime:
        """Get current time."""
        pass

    @abstractmethod
    def utcnow(self) -> datetime:
        """Get current UTC time."""
        pass

    @abstractmethod
    def from_timestamp(self, timestamp: float) -> datetime:
        """Create datetime from Unix timestamp."""
        pass

    @abstractmethod
    def to_timestamp(self, dt: datetime) -> float:
        """Convert datetime to Unix timestamp."""
        pass


class SystemClock(ClockInterface):
    """System clock implementation with timezone support."""

    def __init__(self, config: TimeConfig):
        """Initialize system clock."""
        self.config = config
        self._timezone = self._get_timezone()

    def _get_timezone(self) -> timezone:
        """Get timezone from configuration."""
        if self.config.timezone == "UTC":
            return UTC
        else:
            # For simplicity, using UTC offset parsing
            # In production, you might want to use pytz or dateutil
            try:
                offset_hours = int(self.config.timezone.replace("UTC", ""))
                return timezone(timedelta(hours=offset_hours))
            except:
                return UTC

    def now(self) -> datetime:
        """Get current time in configured timezone."""
        return datetime.now(self._timezone)

    def utcnow(self) -> datetime:
        """Get current UTC time."""
        return datetime.now(UTC)

    def from_timestamp(self, timestamp: float) -> datetime:
        """Create datetime from Unix timestamp."""
        return datetime.fromtimestamp(timestamp, self._timezone)

    def to_timestamp(self, dt: datetime) -> float:
        """Convert datetime to Unix timestamp."""
        # Ensure datetime is timezone-aware
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=self._timezone)
        return dt.timestamp()


class TimeFormatter:
    """Utility class for time formatting operations."""

    def __init__(self, config: TimeConfig):
        """Initialize time formatter."""
        self.config = config

    def format_time(self, dt: datetime) -> str:
        """Format datetime to time string."""
        return dt.strftime(self.config.time_format)

    def format_date(self, dt: datetime) -> str:
        """Format datetime to date string."""
        return dt.strftime(self.config.date_format)

    def format_datetime(self, dt: datetime) -> str:
        """Format datetime to full datetime string."""
        return dt.strftime(self.config.datetime_format)

    def parse_time(self, time_str: str) -> datetime:
        """Parse time string to datetime."""
        return datetime.strptime(time_str, self.config.time_format)

    def parse_date(self, date_str: str) -> datetime:
        """Parse date string to datetime."""
        return datetime.strptime(date_str, self.config.date_format)

    def parse_datetime(self, datetime_str: str) -> datetime:
        """Parse datetime string to datetime."""
        return datetime.strptime(datetime_str, self.config.datetime_format)


class TimeCalculator:
    """Utility class for time calculation operations."""

    def __init__(self, clock: ClockInterface):
        """Initialize time calculator."""
        self.clock = clock

    def add_days(self, dt: datetime, days: int) -> datetime:
        """Add days to datetime."""
        return dt + timedelta(days=days)

    def add_hours(self, dt: datetime, hours: int) -> datetime:
        """Add hours to datetime."""
        return dt + timedelta(hours=hours)

    def add_minutes(self, dt: datetime, minutes: int) -> datetime:
        """Add minutes to datetime."""
        return dt + timedelta(minutes=minutes)

    def time_diff_seconds(self, start: datetime, end: datetime) -> float:
        """Calculate time difference in seconds."""
        return (end - start).total_seconds()

    def time_diff_minutes(self, start: datetime, end: datetime) -> float:
        """Calculate time difference in minutes."""
        return self.time_diff_seconds(start, end) / 60

    def time_diff_hours(self, start: datetime, end: datetime) -> float:
        """Calculate time difference in hours."""
        return self.time_diff_seconds(start, end) / 3600

    def time_diff_days(self, start: datetime, end: datetime) -> float:
        """Calculate time difference in days."""
        return self.time_diff_seconds(start, end) / 86400

    def is_expired(self, dt: datetime, expiry_seconds: float) -> bool:
        """Check if datetime has expired."""
        now = self.clock.now()
        return self.time_diff_seconds(dt, now) > expiry_seconds

    def get_age_seconds(self, dt: datetime) -> float:
        """Get age of datetime in seconds."""
        now = self.clock.now()
        return self.time_diff_seconds(dt, now)

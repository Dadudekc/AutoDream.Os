#!/usr/bin/env python3
"""
Unified Logging and Time Service - V2 Compliance Module
=======================================================

Consolidated logging and time management system following SOLID principles.
Combines functionality from:
- logging/std_logger.py (logging infrastructure)
- time/system_clock.py (time infrastructure)

SOLID Implementation:
- SRP: Each service handles one concern (logging vs time)
- OCP: Extensible logging levels and time operations
- DIP: Dependencies injected via constructor

Author: Agent-3 (DevOps Specialist)
License: MIT
"""

import logging
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta, timezone
from enum import Enum
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class LogLevel(Enum):
    """Enumeration of log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LoggingConfig:
    """Configuration for logging operations."""
    level: LogLevel = LogLevel.INFO
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    console_enabled: bool = True
    file_enabled: bool = True
    log_file: str = "logs/unified.log"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    enable_colors: bool = True


@dataclass
class TimeConfig:
    """Configuration for time operations."""
    timezone: str = "UTC"
    time_format: str = "%Y-%m-%d %H:%M:%S"
    date_format: str = "%Y-%m-%d"
    datetime_format: str = "%Y-%m-%d %H:%M:%S"


class LoggerInterface(ABC):
    """Abstract interface for logging operations."""

    @abstractmethod
    def debug(self, message: str, **context: Any) -> None:
        """Log debug message."""
        pass

    @abstractmethod
    def info(self, message: str, **context: Any) -> None:
        """Log info message."""
        pass

    @abstractmethod
    def warning(self, message: str, **context: Any) -> None:
        """Log warning message."""
        pass

    @abstractmethod
    def error(self, message: str, exception: Exception = None, **context: Any) -> None:
        """Log error message."""
        pass

    @abstractmethod
    def critical(self, message: str, exception: Exception = None, **context: Any) -> None:
        """Log critical message."""
        pass

    @abstractmethod
    def log(self, level: LogLevel, message: str, exception: Exception = None, **context: Any) -> None:
        """Log message with specific level."""
        pass


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


class ColorFormatter(logging.Formatter):
    """Logging formatter with color support."""

    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }

    def __init__(self, fmt: str, datefmt: str, use_colors: bool = True):
        """Initialize color formatter."""
        super().__init__(fmt, datefmt)
        self.use_colors = use_colors

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with optional colors."""
        if self.use_colors and record.levelname in self.COLORS:
            colored_level = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
            record.levelname = colored_level

        return super().format(record)


class UnifiedLogger(LoggerInterface):
    """Unified logger implementation combining multiple logging targets."""

    def __init__(self, name: str, config: LoggingConfig):
        """Initialize unified logger."""
        self.name = name
        self.config = config
        self._logger = logging.getLogger(name)

        # Prevent duplicate handlers
        if self._logger.handlers:
            self._logger.handlers.clear()

        # Set log level
        level_mapping = {
            LogLevel.DEBUG: logging.DEBUG,
            LogLevel.INFO: logging.INFO,
            LogLevel.WARNING: logging.WARNING,
            LogLevel.ERROR: logging.ERROR,
            LogLevel.CRITICAL: logging.CRITICAL
        }
        self._logger.setLevel(level_mapping[config.level])

        # Add handlers
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Setup logging handlers based on configuration."""
        formatter = ColorFormatter(
            self.config.format,
            self.config.date_format,
            self.config.enable_colors
        )

        # Console handler
        if self.config.console_enabled:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)

        # File handler
        if self.config.file_enabled:
            # Ensure log directory exists
            log_dir = Path(self.config.log_file).parent
            log_dir.mkdir(parents=True, exist_ok=True)

            # Rotating file handler
            file_handler = RotatingFileHandler(
                self.config.log_file,
                maxBytes=self.config.max_file_size,
                backupCount=self.config.backup_count
            )
            file_handler.setFormatter(ColorFormatter(
                self.config.format,
                self.config.date_format,
                False  # No colors in log files
            ))
            self._logger.addHandler(file_handler)

    def _map_log_level(self, level: LogLevel) -> int:
        """Map domain LogLevel to logging module level."""
        mapping = {
            LogLevel.DEBUG: logging.DEBUG,
            LogLevel.INFO: logging.INFO,
            LogLevel.WARNING: logging.WARNING,
            LogLevel.ERROR: logging.ERROR,
            LogLevel.CRITICAL: logging.CRITICAL,
        }
        return mapping[level]

    def debug(self, message: str, **context: Any) -> None:
        """Log debug message."""
        self._logger.debug(message, extra=context)

    def info(self, message: str, **context: Any) -> None:
        """Log info message."""
        self._logger.info(message, extra=context)

    def warning(self, message: str, **context: Any) -> None:
        """Log warning message."""
        self._logger.warning(message, extra=context)

    def error(self, message: str, exception: Exception = None, **context: Any) -> None:
        """Log error message."""
        if exception:
            context["exception"] = str(exception)
        self._logger.error(message, extra=context)

    def critical(self, message: str, exception: Exception = None, **context: Any) -> None:
        """Log critical message."""
        if exception:
            context["exception"] = str(exception)
        self._logger.critical(message, extra=context)

    def log(self, level: LogLevel, message: str, exception: Exception = None, **context: Any) -> None:
        """Log message with specific level."""
        if exception:
            context["exception"] = str(exception)
        self._logger.log(self._map_log_level(level), message, extra=context)


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
                offset_hours = int(self.config.timezone.replace('UTC', ''))
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


class LogStatistics:
    """Provides statistics about logging operations."""

    def __init__(self, logger: UnifiedLogger):
        """Initialize log statistics."""
        self.logger = logger
        self.stats: dict[str, int] = {
            'debug': 0,
            'info': 0,
            'warning': 0,
            'error': 0,
            'critical': 0
        }

    def increment_stat(self, level: str) -> None:
        """Increment statistics for a log level."""
        if level.lower() in self.stats:
            self.stats[level.lower()] += 1

    def get_stats(self) -> dict[str, int]:
        """Get logging statistics."""
        return self.stats.copy()

    def reset_stats(self) -> None:
        """Reset all statistics."""
        for key in self.stats:
            self.stats[key] = 0


class UnifiedLoggingTimeService:
    """Main unified logging and time service interface."""

    def __init__(
        self,
        logging_config: LoggingConfig | None = None,
        time_config: TimeConfig | None = None
    ):
        """Initialize unified logging and time service."""
        self.logging_config = logging_config or LoggingConfig()
        self.time_config = time_config or TimeConfig()

        # Initialize components
        self.logger = UnifiedLogger("unified_service", self.logging_config)
        self.clock = SystemClock(self.time_config)
        self.formatter = TimeFormatter(self.time_config)
        self.calculator = TimeCalculator(self.clock)
        self.log_stats = LogStatistics(self.logger)

    # Logging operations
    def get_logger(self, name: str) -> UnifiedLogger:
        """Get a logger instance."""
        return UnifiedLogger(name, self.logging_config)

    def debug(self, message: str, **context: Any) -> None:
        """Log debug message."""
        self.logger.debug(message, **context)
        self.log_stats.increment_stat('debug')

    def info(self, message: str, **context: Any) -> None:
        """Log info message."""
        self.logger.info(message, **context)
        self.log_stats.increment_stat('info')

    def warning(self, message: str, **context: Any) -> None:
        """Log warning message."""
        self.logger.warning(message, **context)
        self.log_stats.increment_stat('warning')

    def error(self, message: str, exception: Exception = None, **context: Any) -> None:
        """Log error message."""
        self.logger.error(message, exception, **context)
        self.log_stats.increment_stat('error')

    def critical(self, message: str, exception: Exception = None, **context: Any) -> None:
        """Log critical message."""
        self.logger.critical(message, exception, **context)
        self.log_stats.increment_stat('critical')

    # Time operations
    def now(self) -> datetime:
        """Get current time."""
        return self.clock.now()

    def utcnow(self) -> datetime:
        """Get current UTC time."""
        return self.clock.utcnow()

    def from_timestamp(self, timestamp: float) -> datetime:
        """Create datetime from Unix timestamp."""
        return self.clock.from_timestamp(timestamp)

    def to_timestamp(self, dt: datetime) -> float:
        """Convert datetime to Unix timestamp."""
        return self.clock.to_timestamp(dt)

    # Time formatting operations
    def format_time(self, dt: datetime) -> str:
        """Format datetime to time string."""
        return self.formatter.format_time(dt)

    def format_date(self, dt: datetime) -> str:
        """Format datetime to date string."""
        return self.formatter.format_date(dt)

    def format_datetime(self, dt: datetime) -> str:
        """Format datetime to full datetime string."""
        return self.formatter.format_datetime(dt)

    def parse_datetime(self, datetime_str: str) -> datetime:
        """Parse datetime string to datetime."""
        return self.formatter.parse_datetime(datetime_str)

    # Time calculation operations
    def add_days(self, dt: datetime, days: int) -> datetime:
        """Add days to datetime."""
        return self.calculator.add_days(dt, days)

    def add_hours(self, dt: datetime, hours: int) -> datetime:
        """Add hours to datetime."""
        return self.calculator.add_hours(dt, hours)

    def time_diff_seconds(self, start: datetime, end: datetime) -> float:
        """Calculate time difference in seconds."""
        return self.calculator.time_diff_seconds(start, end)

    def time_diff_minutes(self, start: datetime, end: datetime) -> float:
        """Calculate time difference in minutes."""
        return self.calculator.time_diff_minutes(start, end)

    def is_expired(self, dt: datetime, expiry_seconds: float) -> bool:
        """Check if datetime has expired."""
        return self.calculator.is_expired(dt, expiry_seconds)

    def get_age_seconds(self, dt: datetime) -> float:
        """Get age of datetime in seconds."""
        return self.calculator.get_age_seconds(dt)

    # Statistics and monitoring
    def get_log_stats(self) -> dict[str, int]:
        """Get logging statistics."""
        return self.log_stats.get_stats()

    def reset_log_stats(self) -> None:
        """Reset logging statistics."""
        self.log_stats.reset_stats()

    def get_service_info(self) -> dict[str, Any]:
        """Get comprehensive service information."""
        return {
            "current_time": self.format_datetime(self.now()),
            "utc_time": self.format_datetime(self.utcnow()),
            "timezone": self.time_config.timezone,
            "log_level": self.logging_config.level.value,
            "console_logging": self.logging_config.console_enabled,
            "file_logging": self.logging_config.file_enabled,
            "log_file": self.logging_config.log_file,
            "log_stats": self.get_log_stats()
        }


def create_logging_time_service(
    log_level: LogLevel = LogLevel.INFO,
    timezone: str = "UTC",
    enable_file_logging: bool = True
) -> UnifiedLoggingTimeService:
    """Factory function to create logging and time service."""
    logging_config = LoggingConfig(
        level=log_level,
        file_enabled=enable_file_logging
    )
    time_config = TimeConfig(timezone=timezone)

    return UnifiedLoggingTimeService(logging_config, time_config)


if __name__ == '__main__':
    # Example usage
    service = create_logging_time_service()

    # Test logging
    service.info("🎉 Unified logging and time service started")
    service.debug("Debug message with context", module="test", version="1.0")
    service.warning("Warning message", component="test_component")
    service.error("Error message", exception=ValueError("Test error"))

    # Test time operations
    now = service.now()
    print(f"📅 Current time: {service.format_datetime(now)}")

    # Test time calculations
    tomorrow = service.add_days(now, 1)
    print(f"📅 Tomorrow: {service.format_datetime(tomorrow)}")

    # Test time differences
    diff_seconds = service.time_diff_seconds(now, tomorrow)
    print(f"⏰ Time difference: {diff_seconds} seconds ({diff_seconds/86400:.1f} days)")

    # Get service info
    info = service.get_service_info()
    print(f"📊 Service info: {info}")

    service.info("✅ Unified logging and time service test complete!")

#!/usr/bin/env python3
"""
🐝 UNIFIED LOGGING SYSTEM - Agent-2 Phase 2 Batch 2A
Consolidated Logging Infrastructure for SWARM Operations

This module provides a unified logging system that consolidates:
- std_logger.py (standard library adapter)
- logger.py (enhanced V2 logger)
- unified_logging_time.py (time-based logging)

Features:
- Structured JSON logging with multiple output formats
- Configurable log levels and filtering
- Performance monitoring and metrics
- Multi-output support (console, file, structured)
- SWARM operation correlation and tracing
"""

from __future__ import annotations

import json
import logging
import logging.config
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from queue import Queue
from typing import Any


class LogLevel(Enum):
    """Unified log levels across all SWARM operations."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogFormat(Enum):

EXAMPLE USAGE:
==============

# Basic usage example
from src.infrastructure.logging.unified_logging_system import Unified_Logging_System

# Initialize and use
instance = Unified_Logging_System()
result = instance.execute()
print(f"Execution result: {result}")

# Advanced configuration
config = {
    "option1": "value1",
    "option2": True
}

instance = Unified_Logging_System(config)
advanced_result = instance.execute_advanced()
print(f"Advanced result: {advanced_result}")

    """Available log output formats."""

    CONSOLE = "console"
    JSON = "json"
    STRUCTURED = "structured"
    MINIMAL = "minimal"


class LogOutput(Enum):
    """Available log output destinations."""

    CONSOLE = "console"
    FILE = "file"
    BOTH = "both"


@dataclass
class LogEntry:
    """Represents a structured log entry."""

    timestamp: datetime
    level: LogLevel
    logger_name: str
    message: str
    module: str = ""
    function: str = ""
    line: int = 0
    correlation_id: str | None = None
    swarm_context: dict[str, Any] = field(default_factory=dict)
    extra_data: dict[str, Any] = field(default_factory=dict)
    performance_metrics: dict[str, Any] = field(default_factory=dict)


@dataclass
class LogConfig:
    """Configuration for the unified logging system."""

    level: LogLevel = LogLevel.INFO
    format: LogFormat = LogFormat.STRUCTURED
    output: LogOutput = LogOutput.BOTH
    log_file: str | None = None
    max_file_size_mb: int = 10
    backup_count: int = 5
    enable_performance_monitoring: bool = True
    enable_swarm_correlation: bool = True
    console_format: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


class StructuredFormatter(logging.Formatter):
    """Enhanced structured JSON formatter with SWARM context."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as enhanced structured JSON."""
        # Extract SWARM context if available
        swarm_context = getattr(record, "swarm_context", {})
        correlation_id = getattr(record, "correlation_id", None)
        performance_metrics = getattr(record, "performance_metrics", {})

        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": getattr(record, "module", record.module),
            "function": getattr(record, "funcName", record.funcName),
            "line": getattr(record, "lineno", record.lineno),
        }

        # Add SWARM-specific fields
        if correlation_id:
            log_entry["correlation_id"] = correlation_id

        if swarm_context:
            log_entry["swarm_context"] = swarm_context

        if performance_metrics:
            log_entry["performance"] = performance_metrics

        # Add any extra fields
        if hasattr(record, "extra_fields"):
            log_entry.update(record.extra_fields)

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, default=str)


class UnifiedLogger:
    """
    Unified logging system for SWARM operations.

    Combines the best features of:
    - Standard library logging (std_logger.py)
    - Enhanced V2 logging (logger.py)
    - Time-based logging (unified_logging_time.py)

    Provides:
    - Structured JSON output with SWARM context
    - Performance monitoring and metrics
    - Correlation ID tracking for request tracing
    - Multiple output formats and destinations
    - Thread-safe operations
    """

    _instance: UnifiedLogger | None = None
    _lock = threading.Lock()

    def __new__(cls) -> UnifiedLogger:
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return

        self._initialized = True
        self.config = LogConfig()
        self.loggers: dict[str, logging.Logger] = {}
        self.performance_queue: Queue = Queue()
        self.shutdown_event = threading.Event()

        # Start performance monitoring thread
        self.performance_thread = threading.Thread(
            target=self._performance_monitor, daemon=True, name="LogPerformanceMonitor"
        )
        self.performance_thread.start()

    def configure(self, config: LogConfig) -> None:
        """Configure the logging system."""
        self.config = config
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Setup logging configuration based on current config."""
        # Clear existing handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Set root logger level
        level_map = {
            LogLevel.DEBUG: logging.DEBUG,
            LogLevel.INFO: logging.INFO,
            LogLevel.WARNING: logging.WARNING,
            LogLevel.ERROR: logging.ERROR,
            LogLevel.CRITICAL: logging.CRITICAL,
        }
        root_logger.setLevel(level_map[self.config.level])

        # Add console handler if needed
        if self.config.output in [LogOutput.CONSOLE, LogOutput.BOTH]:
            console_handler = logging.StreamHandler()
            if self.config.format == LogFormat.JSON:
                console_handler.setFormatter(StructuredFormatter())
            elif self.config.format == LogFormat.STRUCTURED:
                console_handler.setFormatter(StructuredFormatter())
            else:
                console_handler.setFormatter(logging.Formatter(self.config.console_format))
            root_logger.addHandler(console_handler)

        # Add file handler if needed
        if self.config.output in [LogOutput.FILE, LogOutput.BOTH] and self.config.log_file:
            from logging.handlers import RotatingFileHandler

            file_handler = RotatingFileHandler(
                self.config.log_file,
                maxBytes=self.config.max_file_size_mb * 1024 * 1024,
                backupCount=self.config.backup_count,
            )

            if self.config.format in [LogFormat.JSON, LogFormat.STRUCTURED]:
                file_handler.setFormatter(StructuredFormatter())
            else:
                file_handler.setFormatter(logging.Formatter(self.config.console_format))

            root_logger.addHandler(file_handler)

    def get_logger(self, name: str) -> SwarmLogger:
        """Get a logger instance for the specified name."""
        if name not in self.loggers:
            logger = logging.getLogger(name)
            swarm_logger = SwarmLogger(logger, self)
            self.loggers[name] = swarm_logger
        return self.loggers[name]

    def set_correlation_id(self, correlation_id: str) -> None:
        """Set correlation ID for request tracing."""
        self._correlation_id = correlation_id

    def get_correlation_id(self) -> str | None:
        """Get current correlation ID."""
        return getattr(self, "_correlation_id", None)

    def add_swarm_context(self, **context) -> None:
        """Add SWARM-specific context to all future log entries."""
        self._swarm_context = getattr(self, "_swarm_context", {})
        self._swarm_context.update(context)

    def get_swarm_context(self) -> dict[str, Any]:
        """Get current SWARM context."""
        return getattr(self, "_swarm_context", {})

    def log_performance_metric(
        self, operation: str, duration_ms: float, metadata: dict[str, Any] | None = None
    ) -> None:
        """Log a performance metric."""
        if self.config.enable_performance_monitoring:
            self.performance_queue.put(
                {
                    "operation": operation,
                    "duration_ms": duration_ms,
                    "timestamp": datetime.now(),
                    "metadata": metadata or {},
                }
            )

    def _performance_monitor(self) -> None:
        """Monitor and aggregate performance metrics."""
        performance_data: dict[str, list[float]] = {}

        while not self.shutdown_event.is_set():
            try:
                # Process performance metrics
                while not self.performance_queue.empty():
                    metric = self.performance_queue.get_nowait()
                    operation = metric["operation"]

                    if operation not in performance_data:
                        performance_data[operation] = []

                    performance_data[operation].append(metric["duration_ms"])

                    # Keep only last 100 measurements per operation
                    if len(performance_data[operation]) > 100:
                        performance_data[operation] = performance_data[operation][-100:]

                # Log aggregated performance data every 5 minutes
                if int(time.time()) % 300 == 0 and performance_data:
                    self._log_performance_summary(performance_data)

                time.sleep(10)  # Check every 10 seconds

            except Exception:
                # Don't let performance monitoring break the main system
                time.sleep(60)

    def _log_performance_summary(self, performance_data: dict[str, list[float]]) -> None:
        """Log aggregated performance summary."""
        summary = {}
        for operation, durations in performance_data.items():
            if durations:
                summary[operation] = {
                    "count": len(durations),
                    "avg_ms": sum(durations) / len(durations),
                    "min_ms": min(durations),
                    "max_ms": max(durations),
                    "p95_ms": sorted(durations)[int(len(durations) * 0.95)],
                }

        perf_logger = self.get_logger("performance")
        perf_logger.info(
            "Performance metrics summary",
            extra_fields={"performance_summary": summary, "time_window": "5_minutes"},
        )

    def shutdown(self) -> None:
        """Shutdown the logging system gracefully."""
        self.shutdown_event.set()
        if hasattr(self, "performance_thread"):
            self.performance_thread.join(timeout=5)


class SwarmLogger:
    """
    SWARM-aware logger that adds correlation and context to log entries.

    Compatible with standard logging interface while adding SWARM-specific features.
    """

    def __init__(self, logger: logging.Logger, unified_logger: UnifiedLogger):
        self._logger = logger
        self._unified_logger = unified_logger

    def _prepare_log_record(
        self,
        level: LogLevel,
        message: str,
        correlation_id: str | None = None,
        swarm_context: dict[str, Any] | None = None,
        performance_metrics: dict[str, Any] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Prepare log record with SWARM context."""

        # Get correlation ID from various sources
        corr_id = (
            correlation_id
            or self._unified_logger.get_correlation_id()
            or getattr(threading.current_thread(), "correlation_id", None)
        )

        # Merge SWARM contexts
        swarm_ctx = {}
        swarm_ctx.update(self._unified_logger.get_swarm_context())
        if swarm_context:
            swarm_ctx.update(swarm_context)

        # Prepare extra fields for logging
        extra_fields = extra or {}
        if corr_id:
            extra_fields["correlation_id"] = corr_id
        if swarm_ctx:
            extra_fields["swarm_context"] = swarm_ctx
        if performance_metrics:
            extra_fields["performance_metrics"] = performance_metrics

        return {"level": level, "message": message, "extra": extra_fields}

    def debug(
        self,
        message: str,
        correlation_id: str | None = None,
        swarm_context: dict[str, Any] | None = None,
        performance_metrics: dict[str, Any] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        """Log debug message with SWARM context."""
        record = self._prepare_log_record(
            LogLevel.DEBUG, message, correlation_id, swarm_context, performance_metrics, extra
        )
        self._logger.debug(record["message"], extra=record["extra"])

    def info(
        self,
        message: str,
        correlation_id: str | None = None,
        swarm_context: dict[str, Any] | None = None,
        performance_metrics: dict[str, Any] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        """Log info message with SWARM context."""
        record = self._prepare_log_record(
            LogLevel.INFO, message, correlation_id, swarm_context, performance_metrics, extra
        )
        self._logger.info(record["message"], extra=record["extra"])

    def warning(
        self,
        message: str,
        correlation_id: str | None = None,
        swarm_context: dict[str, Any] | None = None,
        performance_metrics: dict[str, Any] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        """Log warning message with SWARM context."""
        record = self._prepare_log_record(
            LogLevel.WARNING, message, correlation_id, swarm_context, performance_metrics, extra
        )
        self._logger.warning(record["message"], extra=record["extra"])

    def error(
        self,
        message: str,
        correlation_id: str | None = None,
        swarm_context: dict[str, Any] | None = None,
        performance_metrics: dict[str, Any] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        """Log error message with SWARM context."""
        record = self._prepare_log_record(
            LogLevel.ERROR, message, correlation_id, swarm_context, performance_metrics, extra
        )
        self._logger.error(record["message"], extra=record["extra"])

    def critical(
        self,
        message: str,
        correlation_id: str | None = None,
        swarm_context: dict[str, Any] | None = None,
        performance_metrics: dict[str, Any] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        """Log critical message with SWARM context."""
        record = self._prepare_log_record(
            LogLevel.CRITICAL, message, correlation_id, swarm_context, performance_metrics, extra
        )
        self._logger.critical(record["message"], extra=record["extra"])

    def log_performance(
        self, operation: str, duration_ms: float, metadata: dict[str, Any] | None = None
    ) -> None:
        """Log a performance metric."""
        self._unified_logger.log_performance_metric(operation, duration_ms, metadata)


# Global instance
_unified_logger = UnifiedLogger()


def get_unified_logger(name: str = "swarm") -> SwarmLogger:
    """Get a unified logger instance."""
    return _unified_logger.get_logger(name)


def configure_logging(
    level: LogLevel = LogLevel.INFO,
    format: LogFormat = LogFormat.STRUCTURED,
    output: LogOutput = LogOutput.BOTH,
    log_file: str | None = None,
) -> None:
    """Configure the unified logging system."""
    config = LogConfig(level=level, format=format, output=output, log_file=log_file)
    _unified_logger.configure(config)


def set_correlation_id(correlation_id: str) -> None:
    """Set correlation ID for request tracing."""
    _unified_logger.set_correlation_id(correlation_id)


def add_swarm_context(**context) -> None:
    """Add SWARM context to all log entries."""
    _unified_logger.add_swarm_context(**context)


# Backwards compatibility functions
def get_logger(name: str = "swarm") -> SwarmLogger:
    """Backwards compatible logger getter."""
    return get_unified_logger(name)


def shutdown_logging() -> None:
    """Shutdown the logging system."""
    _unified_logger.shutdown()


# Initialize with default configuration
configure_logging()

"""
Discord Commander Optimization Models - V2 Compliant
=====================================================

Data models for Discord commander optimization system.
V2 Compliance: ≤400 lines, ≤5 classes, KISS principle
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict


@dataclass
class DiscordPerformanceMetrics:
    """Performance metrics for Discord Commander."""
    
    message_processing_time: float
    command_execution_time: float
    event_handling_time: float
    memory_usage: float
    messages_per_second: float
    commands_per_second: float
    error_rate: float
    uptime_seconds: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "message_processing_time": self.message_processing_time,
            "command_execution_time": self.command_execution_time,
            "event_handling_time": self.event_handling_time,
            "memory_usage": self.memory_usage,
            "messages_per_second": self.messages_per_second,
            "commands_per_second": self.commands_per_second,
            "error_rate": self.error_rate,
            "uptime_seconds": self.uptime_seconds,
        }


@dataclass
class OptimizationConfig:
    """Optimization configuration."""
    
    cache_size: int = 1000
    cache_ttl: int = 300
    rate_limit_per_minute: int = 60
    max_concurrent_operations: int = 10
    enable_compression: bool = True
    enable_caching: bool = True


@dataclass
class PerformanceThresholds:
    """Performance thresholds."""
    
    max_message_processing_time: float = 1.0
    max_command_execution_time: float = 2.0
    max_event_handling_time: float = 0.5
    max_memory_usage: float = 100.0
    min_messages_per_second: float = 10.0
    min_commands_per_second: float = 5.0
    max_error_rate: float = 0.05


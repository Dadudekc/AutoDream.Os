#!/usr/bin/env python3
"""
Messaging Optimizer Models - V2 Compliance Module
=================================================

Data structures and enums for messaging integration optimization.

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Any, Dict


class DeliveryStrategy(Enum):
    """Delivery strategies for messaging."""

    IMMEDIATE = "immediate"
    BATCH = "batch"
    ASYNC = "async"
    HYBRID = "hybrid"


class OptimizationMode(Enum):
    """Optimization modes."""

    THROUGHPUT = "throughput"
    LATENCY = "latency"
    BALANCED = "balanced"
    RESOURCE_EFFICIENT = "resource_efficient"


@dataclass
class MessagingConfig:
    """Configuration for messaging optimization."""

    # Core settings
    delivery_strategy: DeliveryStrategy = DeliveryStrategy.HYBRID
    optimization_mode: OptimizationMode = OptimizationMode.BALANCED
    target_improvement: float = 0.25  # 25%

    # Batching settings
    batch_size: int = 100
    batch_timeout_ms: float = 1000.0
    enable_batching: bool = True

    # Async settings
    max_concurrent_deliveries: int = 50
    enable_async_delivery: bool = True

    # Retry settings
    max_retries: int = 3
    retry_delay_ms: float = 100.0
    backoff_multiplier: float = 2.0

    # Performance settings
    connection_pool_size: int = 10
    queue_size: int = 1000
    monitoring_interval: float = 30.0

    def validate(self) -> bool:
        """Validate configuration."""
        if not 0.0 <= self.target_improvement <= 1.0:
            raise ValueError("Target improvement must be between 0.0 and 1.0")
        if self.batch_size <= 0:
            raise ValueError("Batch size must be positive")
        if self.batch_timeout_ms <= 0:
            raise ValueError("Batch timeout must be positive")
        if self.max_concurrent_deliveries <= 0:
            raise ValueError("Max concurrent deliveries must be positive")
        if self.max_retries < 0:
            raise ValueError("Max retries cannot be negative")
        if self.retry_delay_ms <= 0:
            raise ValueError("Retry delay must be positive")
        if self.connection_pool_size <= 0:
            raise ValueError("Connection pool size must be positive")
        if self.queue_size <= 0:
            raise ValueError("Queue size must be positive")
        if self.monitoring_interval <= 0:
            raise ValueError("Monitoring interval must be positive")
        return True


@dataclass
class MessagingMetrics:
    """Metrics for messaging performance."""

    timestamp: datetime = field(default_factory=datetime.now)
    messages_processed: int = 0
    messages_per_second: float = 0.0
    average_latency_ms: float = 0.0
    success_rate: float = 0.0
    retry_rate: float = 0.0
    batch_efficiency: float = 0.0
    queue_utilization: float = 0.0
    connection_pool_usage: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "messages_processed": self.messages_processed,
            "messages_per_second": self.messages_per_second,
            "average_latency_ms": self.average_latency_ms,
            "success_rate": self.success_rate,
            "retry_rate": self.retry_rate,
            "batch_efficiency": self.batch_efficiency,
            "queue_utilization": self.queue_utilization,
            "connection_pool_usage": self.connection_pool_usage,
        }


@dataclass
class OptimizationResult:
    """Result of an optimization operation."""

    status: str
    execution_time_ms: float
    optimization_count: int
    batch_optimization: Dict[str, Any]
    async_optimization: Dict[str, Any]
    retry_optimization: Dict[str, Any]
    connection_optimization: Dict[str, Any]
    current_metrics: Dict[str, Any]
    error: str = None


@dataclass
class SystemInfo:
    """System information for optimization summary."""

    is_active: bool
    uptime_seconds: float = None
    optimization_count: int = 0
    queue_size: int = 0
    batch_queue_size: int = 0
    active_connections: int = 0


@dataclass
class ConfigurationInfo:
    """Configuration information for optimization summary."""

    delivery_strategy: str
    optimization_mode: str
    target_improvement: float
    batching_enabled: bool
    async_enabled: bool

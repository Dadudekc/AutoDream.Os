#!/usr/bin/env python3
"""
Messaging Protocol Models - V2 Compliance Module
===============================================

Data models and configuration classes for messaging protocol optimization.
Extracted from monolithic messaging_protocol_optimizer.py for V2 compliance.

Responsibilities:
- Protocol optimization strategies and enums
- Message routing and batching models
- Performance metrics data structures
- Configuration and validation classes
- Factory functions for model creation

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
Original: Agent-6 - Gaming & Entertainment Specialist
License: MIT
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta

# Import messaging components
from ..models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    SenderType,
    RecipientType
)


class ProtocolOptimizationStrategy(Enum):
    """Protocol optimization strategies."""
    ROUTE_OPTIMIZATION = "route_optimization"
    MESSAGE_BATCHING = "message_batching"
    PRIORITY_QUEUING = "priority_queuing"
    ADAPTIVE_TIMEOUT = "adaptive_timeout"
    LOAD_BALANCING = "load_balancing"
    CACHING = "caching"


class MessageRoute(Enum):
    """Message routing strategies."""
    DIRECT = "direct"
    BATCHED = "batched"
    QUEUED = "queued"
    LOAD_BALANCED = "load_balanced"
    CACHED = "cached"
    OPTIMIZED = "optimized"


@dataclass
class ProtocolMetrics:
    """Performance metrics for protocol optimization."""
    total_messages_sent: int = 0
    total_messages_failed: int = 0
    average_delivery_time: float = 0.0
    peak_throughput: float = 0.0
    optimization_efficiency: float = 0.0
    cache_hit_rate: float = 0.0
    batch_utilization: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)
    
    def calculate_success_rate(self) -> float:
        """Calculate message delivery success rate."""
        total = self.total_messages_sent + self.total_messages_failed
        if total == 0:
            return 1.0
        return self.total_messages_sent / total
    
    def update_metrics(self, delivery_time: float, success: bool):
        """Update metrics with new delivery data."""
        if success:
            self.total_messages_sent += 1
            # Update average delivery time (exponential moving average)
            alpha = 0.1
            self.average_delivery_time = (
                alpha * delivery_time + (1 - alpha) * self.average_delivery_time
            )
        else:
            self.total_messages_failed += 1
        
        self.last_updated = datetime.now()


@dataclass
class MessageBatch:
    """Message batch for optimized delivery."""
    batch_id: str
    messages: List[UnifiedMessage] = field(default_factory=list)
    target_recipient: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    delivery_strategy: MessageRoute = MessageRoute.BATCHED
    optimization_applied: List[ProtocolOptimizationStrategy] = field(default_factory=list)
    max_size: int = 10
    timeout_seconds: float = 5.0
    
    def add_message(self, message: UnifiedMessage) -> bool:
        """Add message to batch if space available."""
        if len(self.messages) < self.max_size:
            self.messages.append(message)
            return True
        return False
    
    def is_ready_for_delivery(self) -> bool:
        """Check if batch is ready for delivery."""
        # Ready if batch is full or timeout exceeded
        is_full = len(self.messages) >= self.max_size
        is_timeout = (datetime.now() - self.created_at).total_seconds() >= self.timeout_seconds
        return is_full or (len(self.messages) > 0 and is_timeout)
    
    def get_batch_size(self) -> int:
        """Get current batch size."""
        return len(self.messages)


@dataclass
class OptimizationConfig:
    """Configuration for messaging protocol optimization."""
    
    # Batching settings
    batch_size_threshold: int = 5
    batch_timeout_seconds: float = 2.0
    enable_message_batching: bool = True
    
    # Priority settings
    enable_priority_queuing: bool = True
    priority_weights: Dict[UnifiedMessagePriority, float] = field(default_factory=lambda: {
        UnifiedMessagePriority.URGENT: 1.0,
        UnifiedMessagePriority.REGULAR: 0.5
    })
    
    # Routing settings
    enable_route_optimization: bool = True
    enable_load_balancing: bool = True
    max_retry_attempts: int = 3
    
    # Timeout settings
    enable_adaptive_timeout: bool = True
    adaptive_timeout_base: float = 5.0
    timeout_multiplier: float = 1.5
    
    # Caching settings
    enable_caching: bool = True
    cache_ttl_seconds: int = 300  # 5 minutes
    max_cache_size: int = 1000
    
    # Performance settings
    target_efficiency_improvement: float = 0.45  # 45%
    monitoring_interval: float = 1.0
    metrics_retention_hours: int = 24
    
    def validate(self) -> bool:
        """Validate configuration settings."""
        if self.batch_size_threshold < 1:
            raise ValueError("Batch size threshold must be at least 1")
        if self.batch_timeout_seconds < 0.1:
            raise ValueError("Batch timeout must be at least 0.1 seconds")
        if self.max_retry_attempts < 1:
            raise ValueError("Max retry attempts must be at least 1")
        if self.adaptive_timeout_base < 1.0:
            raise ValueError("Adaptive timeout base must be at least 1.0 seconds")
        if not 0.0 <= self.target_efficiency_improvement <= 1.0:
            raise ValueError("Target efficiency improvement must be between 0.0 and 1.0")
        if self.cache_ttl_seconds < 60:
            raise ValueError("Cache TTL must be at least 60 seconds")
        if self.max_cache_size < 10:
            raise ValueError("Max cache size must be at least 10")
        if self.monitoring_interval < 0.1:
            raise ValueError("Monitoring interval must be at least 0.1 seconds")
        if self.metrics_retention_hours < 1:
            raise ValueError("Metrics retention must be at least 1 hour")
        return True


@dataclass
class RouteOptimization:
    """Route optimization data."""
    route_id: str
    source: str
    destination: str
    strategy: MessageRoute
    latency_ms: float
    success_rate: float
    last_used: datetime = field(default_factory=datetime.now)
    usage_count: int = 0
    
    def update_performance(self, latency: float, success: bool):
        """Update route performance metrics."""
        # Update latency with exponential moving average
        alpha = 0.2
        self.latency_ms = alpha * latency + (1 - alpha) * self.latency_ms
        
        # Update success rate
        if success:
            self.success_rate = min(1.0, self.success_rate + 0.01)
        else:
            self.success_rate = max(0.0, self.success_rate - 0.05)
        
        self.last_used = datetime.now()
        self.usage_count += 1


@dataclass
class DeliveryResult:
    """Result of message delivery attempt."""
    message_id: str
    success: bool
    delivery_time_ms: float
    route_used: MessageRoute
    optimization_strategies: List[ProtocolOptimizationStrategy]
    error_message: Optional[str] = None
    retry_count: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging/storage."""
        return {
            'message_id': self.message_id,
            'success': self.success,
            'delivery_time_ms': self.delivery_time_ms,
            'route_used': self.route_used.value,
            'optimization_strategies': [s.value for s in self.optimization_strategies],
            'error_message': self.error_message,
            'retry_count': self.retry_count,
            'timestamp': self.timestamp.isoformat()
        }


# Constants
DEFAULT_OPTIMIZATION_STRATEGIES = [
    ProtocolOptimizationStrategy.ROUTE_OPTIMIZATION,
    ProtocolOptimizationStrategy.MESSAGE_BATCHING,
    ProtocolOptimizationStrategy.PRIORITY_QUEUING
]

ROUTE_PRIORITY_ORDER = [
    MessageRoute.CACHED,
    MessageRoute.DIRECT,
    MessageRoute.OPTIMIZED,
    MessageRoute.BATCHED,
    MessageRoute.LOAD_BALANCED,
    MessageRoute.QUEUED
]

# Validation functions
def validate_protocol_metrics(metrics: ProtocolMetrics) -> bool:
    """Validate protocol metrics."""
    return (
        metrics.total_messages_sent >= 0 and
        metrics.total_messages_failed >= 0 and
        metrics.average_delivery_time >= 0.0 and
        0.0 <= metrics.optimization_efficiency <= 1.0 and
        0.0 <= metrics.cache_hit_rate <= 1.0 and
        0.0 <= metrics.batch_utilization <= 1.0
    )

def validate_message_batch(batch: MessageBatch) -> bool:
    """Validate message batch."""
    return (
        batch.batch_id and
        isinstance(batch.messages, list) and
        len(batch.messages) <= batch.max_size and
        batch.timeout_seconds > 0
    )

def validate_optimization_config(config: OptimizationConfig) -> bool:
    """Validate optimization configuration."""
    try:
        return config.validate()
    except ValueError:
        return False

# Factory functions
def create_default_config() -> OptimizationConfig:
    """Create default optimization configuration."""
    return OptimizationConfig()

def create_message_batch(batch_id: str, target_recipient: str = "", 
                        max_size: int = 10, timeout_seconds: float = 5.0) -> MessageBatch:
    """Create message batch with validation."""
    batch = MessageBatch(
        batch_id=batch_id,
        target_recipient=target_recipient,
        max_size=max_size,
        timeout_seconds=timeout_seconds
    )
    if not validate_message_batch(batch):
        raise ValueError("Invalid message batch configuration")
    return batch

def create_route_optimization(route_id: str, source: str, destination: str,
                            strategy: MessageRoute = MessageRoute.DIRECT) -> RouteOptimization:
    """Create route optimization with default values."""
    return RouteOptimization(
        route_id=route_id,
        source=source,
        destination=destination,
        strategy=strategy,
        latency_ms=100.0,  # Default latency
        success_rate=1.0   # Start with perfect success rate
    )

def create_delivery_result(message_id: str, success: bool, delivery_time_ms: float,
                         route_used: MessageRoute, 
                         optimization_strategies: List[ProtocolOptimizationStrategy],
                         error_message: Optional[str] = None) -> DeliveryResult:
    """Create delivery result with validation."""
    return DeliveryResult(
        message_id=message_id,
        success=success,
        delivery_time_ms=delivery_time_ms,
        route_used=route_used,
        optimization_strategies=optimization_strategies,
        error_message=error_message
    )

#!/usr/bin/env python3
"""
Vector Optimization Models - V2 Compliance Module
================================================

Data models and enums for vector database optimization.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timedelta


class CacheStrategy(Enum):
    """Cache strategies for vector operations."""
    LRU = "lru"
    TTL = "ttl"
    HYBRID = "hybrid"


@dataclass
class VectorSearchConfig:
    """Configuration for vector search optimization."""
    
    enable_caching: bool = True
    cache_strategy: CacheStrategy = CacheStrategy.HYBRID
    cache_ttl: int = 3600
    max_cache_size: int = 1000
    enable_connection_pooling: bool = True
    max_connections: int = 10
    enable_async_operations: bool = True
    thread_pool_size: int = 4
    enable_performance_monitoring: bool = True
    performance_threshold: float = 0.1


@dataclass
class VectorSearchResult:
    """Result of vector search operation."""
    
    query: str
    results: List[Dict[str, Any]]
    execution_time: float
    cache_hit: bool = False
    performance_metrics: Optional[Dict[str, Any]] = None


@dataclass
class PerformanceMetrics:
    """Performance metrics for vector operations."""
    
    operation_type: str
    execution_time: float
    result_count: int
    timestamp: datetime = field(default_factory=datetime.now)
    cache_hit: bool = False
    memory_usage: Optional[int] = None


@dataclass
class CacheStats:
    """Cache statistics."""
    
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    total_size: int = 0
    
    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


@dataclass
class ConnectionPoolStats:
    """Connection pool statistics."""
    
    active_connections: int = 0
    idle_connections: int = 0
    total_connections: int = 0
    max_connections: int = 10
    
    @property
    def utilization_rate(self) -> float:
        """Calculate pool utilization rate."""
        return self.active_connections / self.max_connections if self.max_connections > 0 else 0.0


@dataclass
class OptimizationTargets:
    """Performance optimization targets."""
    
    target_improvement_percent: int = 25
    max_execution_time: float = 0.1
    min_cache_hit_rate: float = 0.8
    max_memory_usage_mb: int = 100
    
    def is_target_achieved(self, metrics: PerformanceMetrics) -> bool:
        """Check if optimization targets are achieved."""
        return (
            metrics.execution_time <= self.max_execution_time and
            metrics.memory_usage is None or metrics.memory_usage <= self.max_memory_usage_mb * 1024 * 1024
        )

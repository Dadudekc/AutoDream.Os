#!/usr/bin/env python3
"""
Data Optimization Models - V2 Compliance Module
==============================================

Data models and enums for data processing optimization.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union
import time


class ProcessingStrategy(Enum):
    """Data processing strategies."""

    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    STREAMING = "streaming"
    BATCH = "batch"
    ADAPTIVE = "adaptive"


class OptimizationLevel(Enum):
    """Optimization levels."""

    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    MAXIMUM = "maximum"


@dataclass
class ProcessingMetrics:
    """Processing performance metrics."""

    operations_processed: int = 0
    processing_time_ms: float = 0.0
    memory_usage_mb: float = 0.0
    cache_hit_rate: float = 0.0
    parallel_efficiency: float = 0.0
    throughput_ops_per_sec: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "operations_processed": self.operations_processed,
            "processing_time_ms": self.processing_time_ms,
            "memory_usage_mb": self.memory_usage_mb,
            "cache_hit_rate": self.cache_hit_rate,
            "parallel_efficiency": self.parallel_efficiency,
            "throughput_ops_per_sec": self.throughput_ops_per_sec,
        }

    def reset(self) -> None:
        """Reset all metrics to zero."""
        self.operations_processed = 0
        self.processing_time_ms = 0.0
        self.memory_usage_mb = 0.0
        self.cache_hit_rate = 0.0
        self.parallel_efficiency = 0.0
        self.throughput_ops_per_sec = 0.0


@dataclass
class OptimizationConfig:
    """Configuration for data processing optimization."""

    strategy: ProcessingStrategy = ProcessingStrategy.ADAPTIVE
    optimization_level: OptimizationLevel = OptimizationLevel.INTERMEDIATE
    target_improvement: float = 25.0  # Target 25% improvement
    cache_enabled: bool = True
    max_cache_size: int = 1000
    cache_ttl_seconds: int = 3600
    enable_parallel_processing: bool = True
    max_workers: int = 4
    enable_streaming: bool = True
    streaming_chunk_size: int = 1000
    enable_memory_optimization: bool = True
    max_memory_usage_mb: int = 512
    enable_performance_monitoring: bool = True
    metrics_retention_days: int = 7


@dataclass
class OptimizationResult:
    """Result of optimization operation."""

    success: bool
    strategy_used: str
    execution_time_ms: float
    result: Any = None
    metrics: Optional[ProcessingMetrics] = None
    error_message: Optional[str] = None
    cache_hit: bool = False
    memory_used_mb: float = 0.0


@dataclass
class CacheEntry:
    """Cache entry for optimization results."""

    key: str
    value: Any
    timestamp: float = field(default_factory=time.time)
    ttl_seconds: int = 3600

    def is_expired(self) -> bool:
        """Check if cache entry is expired."""
        return time.time() - self.timestamp > self.ttl_seconds


@dataclass
class PerformanceProfile:
    """Performance profile for optimization decisions."""

    data_size: int
    operation_type: str
    recommended_strategy: ProcessingStrategy
    estimated_time_ms: float
    memory_requirement_mb: float
    parallel_efficiency: float = 0.0
    cache_benefit: float = 0.0

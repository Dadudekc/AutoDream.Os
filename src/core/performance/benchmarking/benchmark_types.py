#!/usr/bin/env python3
"""
Benchmark Types - V2 Modular Architecture
=========================================

Data structures for performance benchmarking.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class BenchmarkType(Enum):
    """Types of benchmarks."""
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    CONCURRENCY = "concurrency"
    GENERIC = "generic"


class BenchmarkStatus(Enum):
    """Benchmark execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class BenchmarkPhase(Enum):
    """Benchmark execution phases."""
    INITIALIZATION = "initialization"
    WARMUP = "warmup"
    EXECUTION = "execution"
    COOLDOWN = "cooldown"
    CLEANUP = "cleanup"


@dataclass
class BenchmarkMetrics:
    """Metrics collected during benchmark execution."""
    response_time_ms: float
    throughput_ops_per_sec: float
    error_rate_percent: float
    cpu_usage_percent: float
    memory_usage_percent: float
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "response_time_ms": self.response_time_ms,
            "throughput_ops_per_sec": self.throughput_ops_per_sec,
            "error_rate_percent": self.error_rate_percent,
            "cpu_usage_percent": self.cpu_usage_percent,
            "memory_usage_percent": self.memory_usage_percent,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class BenchmarkResult:
    """Result of a benchmark execution."""
    id: str
    name: str
    component: str
    start_time: str
    end_time: str
    duration: float
    iterations: int
    metrics: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None
    
    def is_completed(self) -> bool:
        """Check if benchmark completed successfully."""
        return self.success
    
    def is_failed(self) -> bool:
        """Check if benchmark failed."""
        return not self.success
    
    def get_average_metrics(self) -> Optional[Dict[str, Any]]:
        """Calculate average metrics across all collected data points."""
        if not self.metrics:
            return None
        
        # For now, return the metrics as-is since they're already aggregated
        return self.metrics.copy()


@dataclass
class BenchmarkConfig:
    """Configuration for benchmark execution."""
    name: str
    benchmark_type: BenchmarkType
    duration_seconds: int = 30
    iterations: int = 1
    timeout_seconds: int = 300
    parallel_execution: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

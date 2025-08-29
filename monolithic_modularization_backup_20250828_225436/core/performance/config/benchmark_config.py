#!/usr/bin/env python3
"""
Benchmark Configuration - V2 Modular Architecture
================================================

Benchmark execution and configuration management.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class BenchmarkType(Enum):
    """Benchmark type enumeration."""
    LOAD_TEST = "load_test"
    STRESS_TEST = "stress_test"
    ENDURANCE_TEST = "endurance_test"
    SPIKE_TEST = "spike_test"
    SCALABILITY_TEST = "scalability_test"


class BenchmarkStatus(Enum):
    """Benchmark execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class BenchmarkConfig:
    """Benchmark execution configuration."""
    benchmark_type: BenchmarkType
    name: str
    description: str
    enabled: bool = True
    timeout_seconds: int = 300
    max_iterations: int = 5
    warmup_iterations: int = 2
    target_metrics: Dict[str, Any] = field(default_factory=dict)
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def is_valid(self) -> bool:
        """Validate benchmark configuration."""
        return (
            self.timeout_seconds > 0 and
            self.max_iterations > 0 and
            self.warmup_iterations >= 0 and
            self.warmup_iterations < self.max_iterations
        )


@dataclass
class BenchmarkExecutionConfig:
    """Benchmark execution runtime configuration."""
    config: BenchmarkConfig
    execution_id: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    status: BenchmarkStatus = BenchmarkStatus.PENDING
    results: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def start_execution(self):
        """Mark benchmark as started."""
        self.status = BenchmarkStatus.RUNNING
        self.start_time = "now"  # Simplified for demo
    
    def complete_execution(self, results: Dict[str, Any]):
        """Mark benchmark as completed."""
        self.status = BenchmarkStatus.COMPLETED
        self.end_time = "now"  # Simplified for demo
        self.results = results
    
    def fail_execution(self, error: str):
        """Mark benchmark as failed."""
        self.status = BenchmarkStatus.FAILED
        self.end_time = "now"  # Simplified for demo
        self.metadata["error"] = error

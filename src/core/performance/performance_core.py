#!/usr/bin/env python3
"""
Performance Core - Core Performance Management Classes

Extracted from unified_performance_system.py to achieve V2 compliance.
Contains core enums, data models, and base functionality.

Author: Agent-8 (Technical Debt Specialist)
License: MIT
"""

from __future__ import annotations

import json
import logging
import os
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union
import time
import threading
import statistics


# ============================================================================
# ENUMS AND DATA MODELS
# ============================================================================

class PerformanceLevel(Enum):
    """Performance classification levels."""
    NOT_READY = "not_ready"
    BASIC = "basic"
    STANDARD = "standard"
    GOOD = "good"
    EXCELLENT = "excellent"
    ENTERPRISE_READY = "enterprise_ready"
    PRODUCTION_READY = "production_ready"


class ValidationSeverity(Enum):
    """Validation rule severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class BenchmarkType(Enum):
    """Types of performance benchmarks."""
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    CONCURRENCY = "concurrency"
    STRESS = "stress"
    LOAD = "load"
    END_TO_END = "end_to_end"


class MetricType(Enum):
    """Types of performance metrics."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


@dataclass
class PerformanceMetric:
    """Individual performance metric."""
    name: str
    value: Union[int, float]
    unit: str
    metric_type: MetricType
    timestamp: datetime
    labels: Dict[str, str]
    description: str


@dataclass
class ValidationRule:
    """Performance validation rule definition."""
    rule_name: str
    metric_name: str
    threshold: float
    operator: str  # 'gt', 'lt', 'eq', 'gte', 'lte'
    severity: ValidationSeverity
    description: str
    enabled: bool = True


@dataclass
class ValidationThreshold:
    """Performance threshold configuration."""
    metric_name: str
    warning_threshold: float
    critical_threshold: float


@dataclass
class PerformanceBenchmark:
    """Performance benchmark definition."""
    benchmark_id: str
    name: str
    description: str
    benchmark_type: BenchmarkType
    metrics: List[str]
    duration: int  # seconds
    iterations: int
    enabled: bool = True


@dataclass
class PerformanceResult:
    """Performance test result."""
    test_id: str
    benchmark_name: str
    start_time: datetime
    end_time: datetime
    duration: float
    metrics: Dict[str, PerformanceMetric]
    validation_results: List[Dict[str, Any]]
    overall_score: float
    performance_level: PerformanceLevel


# ============================================================================
# CORE PERFORMANCE SYSTEM
# ============================================================================

class UnifiedPerformanceSystem:
    """
    Core performance management system.
    
    Provides unified performance monitoring, validation, and reporting
    across all system components.
    """
    
    def __init__(self):
        """Initialize the unified performance system."""
        self.logger = logging.getLogger(__name__)

        # Core components
        self.metrics: Dict[str, PerformanceMetric] = {}
        self.validation_rules: Dict[str, ValidationRule] = {}
        self.benchmarks: Dict[str, PerformanceBenchmark] = {}
        self.results: Dict[str, PerformanceResult] = {}

        # Configuration
        self.config_path = Path(
            os.getenv("UNIFIED_PERFORMANCE_CONFIG_PATH", "config/system/performance.json")
        )
        self.config: Dict[str, Any] = {}

        # Extension hooks
        self.extension_hooks: Dict[str, List[Callable]] = {
            "validation_rules": [],
            "benchmarks": [],
        }
        
        # System state
        self.is_initialized = False
        self.monitoring_active = False
        
        self.logger.info("Unified Performance System initialized")
    
    def initialize(self) -> bool:
        """Initialize the performance system."""
        try:
            self.logger.info("Initializing Unified Performance System...")
            
            # Load configuration
            self._load_configuration()
            
            # Setup validation rules
            self._setup_default_validation_rules()
            
            # Setup benchmarks
            self._setup_default_benchmarks()
            
            self.is_initialized = True
            self.logger.info("Unified Performance System initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize performance system: {e}")
            return False
    
    def _load_configuration(self):
        """Load performance system configuration."""
        default_config = {
            "validation_rules": [],
            "benchmarks": [],
        }

        env_config = os.getenv("UNIFIED_PERFORMANCE_CONFIG")

        try:
            if env_config:
                self.config = json.loads(env_config)
            elif self.config_path.exists():
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            self.config = default_config

        return self.config

    def _setup_default_validation_rules(self):
        """Setup default performance validation rules."""
        rules_config = self.config.get("validation_rules")
        if not rules_config:
            rules_config = [
                {
                    "rule_name": "cpu_usage_limit",
                    "metric_name": "cpu_usage_percent",
                    "threshold": 80.0,
                    "operator": "lt",
                    "severity": "warning",
                    "description": "CPU usage should remain below 80%",
                },
                {
                    "rule_name": "memory_usage_limit",
                    "metric_name": "memory_usage_percent",
                    "threshold": 80.0,
                    "operator": "lt",
                    "severity": "warning",
                    "description": "Memory usage should remain below 80%",
                },
                {
                    "rule_name": "response_time_limit",
                    "metric_name": "response_time_ms",
                    "threshold": 500.0,
                    "operator": "lt",
                    "severity": "critical",
                    "description": "Response time should be under 500ms",
                },
            ]

        for rule_def in rules_config:
            try:
                rule = ValidationRule(
                    rule_name=rule_def["rule_name"],
                    metric_name=rule_def["metric_name"],
                    threshold=float(rule_def.get("threshold", 0)),
                    operator=rule_def.get("operator", "lt"),
                    severity=ValidationSeverity(rule_def.get("severity", "warning")),
                    description=rule_def.get("description", ""),
                    enabled=rule_def.get("enabled", True),
                )
                self.validation_rules[rule.rule_name] = rule
            except Exception as e:
                self.logger.error(f"Failed to setup validation rule {rule_def}: {e}")

        self.logger.info(
            f"Setup {len(self.validation_rules)} validation rules"
        )
        self._run_extension_hooks("validation_rules")

    def _setup_default_benchmarks(self):
        """Setup default performance benchmarks."""
        benchmarks_config = self.config.get("benchmarks")
        if not benchmarks_config:
            benchmarks_config = [
                {
                    "benchmark_id": "baseline_throughput",
                    "name": "Baseline Throughput",
                    "description": "Basic throughput benchmark",
                    "benchmark_type": "throughput",
                    "metrics": ["operations_per_second"],
                    "duration": 60,
                    "iterations": 1,
                },
                {
                    "benchmark_id": "baseline_latency",
                    "name": "Baseline Latency",
                    "description": "Basic response time benchmark",
                    "benchmark_type": "response_time",
                    "metrics": ["response_time_ms"],
                    "duration": 60,
                    "iterations": 1,
                },
            ]

        for bench_def in benchmarks_config:
            try:
                benchmark = PerformanceBenchmark(
                    benchmark_id=bench_def.get("benchmark_id", str(uuid.uuid4())),
                    name=bench_def["name"],
                    description=bench_def.get("description", ""),
                    benchmark_type=BenchmarkType(bench_def.get("benchmark_type", "cpu")),
                    metrics=list(bench_def.get("metrics", [])),
                    duration=int(bench_def.get("duration", 60)),
                    iterations=int(bench_def.get("iterations", 1)),
                    enabled=bench_def.get("enabled", True),
                )
                self.benchmarks[benchmark.benchmark_id] = benchmark
            except Exception as e:
                self.logger.error(
                    f"Failed to setup benchmark {bench_def}: {e}"
                )

        self.logger.info(
            f"Setup {len(self.benchmarks)} benchmarks"
        )
        self._run_extension_hooks("benchmarks")

    # Extension hooks -----------------------------------------------------
    def register_extension_hook(self, hook_type: str, handler: Callable[["UnifiedPerformanceSystem"], None]):
        """Register a custom extension hook."""
        self.extension_hooks.setdefault(hook_type, []).append(handler)

    def _run_extension_hooks(self, hook_type: str) -> None:
        """Execute registered extension hooks."""
        for handler in self.extension_hooks.get(hook_type, []):
            try:
                handler(self)
            except Exception as e:
                self.logger.error(
                    f"Extension hook '{hook_type}' failed: {e}"
                )
    
    def get_metric(self, metric_name: str) -> Optional[PerformanceMetric]:
        """Get a performance metric by name."""
        return self.metrics.get(metric_name)
    
    def add_metric(self, metric: PerformanceMetric):
        """Add a performance metric."""
        self.metrics[metric.name] = metric
    
    def get_validation_rules(self) -> List[ValidationRule]:
        """Get all validation rules."""
        return list(self.validation_rules.values())
    
    def get_benchmarks(self) -> List[PerformanceBenchmark]:
        """Get all performance benchmarks."""
        return list(self.benchmarks.values())
    
    def get_results(self) -> List[PerformanceResult]:
        """Get all performance results."""
        return list(self.results.values())


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Initialize logging
    logging.basicConfig(level=logging.INFO)
    
    # Create and test performance system
    system = UnifiedPerformanceSystem()
    if system.initialize():
        print("✅ Performance system initialized successfully")
        print(f"📊 Metrics: {len(system.metrics)}")
        print(f"🔍 Validation Rules: {len(system.validation_rules)}")
        print(f"⚡ Benchmarks: {len(system.benchmarks)}")
    else:
        print("❌ Failed to initialize performance system")

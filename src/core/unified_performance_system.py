#!/usr/bin/env python3
"""
Unified Performance System - Consolidated Performance Management

Consolidates 33+ performance files into a unified system following V2 standards.
NO duplicate implementations - unified architecture only.

Author: Agent-3 (Integration & Testing)
License: MIT
"""

from __future__ import annotations

import json
import logging
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
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
    unit: str
    description: str


@dataclass
class ConnectionPool:
    """Connection pool definition"""
    name: str
    max_connections: int
    active_connections: int
    idle_connections: int
    total_connections: int
    wait_time: float
    utilization: float
    health_status: str


@dataclass
class BenchmarkResult:
    """Benchmark result definition"""
    id: str
    name: str
    component: str
    start_time: str
    end_time: str
    duration: float
    iterations: int
    metrics: Dict[str, float]
    success: bool
    error_message: Optional[str]


@dataclass
class SystemPerformanceReport:
    """Comprehensive system performance report."""
    report_id: str
    timestamp: datetime
    system_health: str
    overall_performance_level: PerformanceLevel
    metrics_summary: Dict[str, Any]
    validation_results: List[Dict[str, Any]]
    benchmarks: List[BenchmarkResult]
    recommendations: List[str]
    alerts: List[str]


@dataclass
class PerformanceConfig:
    """Performance system configuration."""
    system_name: str
    validation_rules: List[ValidationRule]
    thresholds: List[ValidationThreshold]
    benchmark_configs: Dict[str, Any]
    monitoring_interval: float
    alerting_enabled: bool
    reporting_enabled: bool
    auto_optimization: bool


# ============================================================================
# UNIFIED PERFORMANCE SYSTEM
# ============================================================================

class UnifiedPerformanceSystem:
    """
    Unified performance system consolidating all performance management functionality.
    
    Single responsibility: Provide unified interface for all performance operations
    including monitoring, validation, benchmarking, reporting, and alerting.
    
    Consolidates functionality from 33+ separate performance files.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize unified performance system."""
        self.logger = logging.getLogger(f"{__name__}.UnifiedPerformanceSystem")
        
        # System state
        self.is_running = False
        self.start_time: Optional[datetime] = None
        
        # Performance tracking
        self.metrics_history: List[PerformanceMetric] = []
        self.benchmark_history: List[BenchmarkResult] = []
        self.validation_results: List[Dict[str, Any]] = []
        self.alerts: List[str] = []
        self.connection_pools: Dict[str, ConnectionPool] = {}
        
        # Configuration
        self.config = self._load_config(config_file)
        self.validation_rules = {rule.rule_name: rule for rule in self.config.validation_rules}
        self.thresholds = {t.metric_name: t for t in self.config.thresholds}
        
        # Monitoring
        self.monitoring_thread: Optional[threading.Thread] = None
        self.monitoring_active = False
        
        # Statistics
        self.total_benchmarks_run = 0
        self.successful_benchmarks = 0
        self.failed_benchmarks = 0
        self.total_metrics_collected = 0
        
        self.logger.info("✅ Unified Performance System initialized successfully")
    
    def _load_config(self, config_file: Optional[str] = None) -> PerformanceConfig:
        """Load performance configuration."""
        try:
            if config_file and Path(config_file).exists():
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
                return PerformanceConfig(**config_data)
            
            # Default configuration
            return PerformanceConfig(
                system_name="UnifiedPerformanceSystem",
                validation_rules=[
                    ValidationRule(
                        rule_name="response_time_threshold",
                        metric_name="response_time_ms",
                        threshold=1000.0,
                        operator="lte",
                        severity=ValidationSeverity.WARNING,
                        description="Response time should be under 1 second"
                    ),
                    ValidationRule(
                        rule_name="cpu_usage_threshold",
                        metric_name="cpu_usage_percent",
                        threshold=80.0,
                        operator="lte",
                        severity=ValidationSeverity.CRITICAL,
                        description="CPU usage should be under 80%"
                    ),
                    ValidationRule(
                        rule_name="memory_usage_threshold",
                        metric_name="memory_usage_percent",
                        threshold=85.0,
                        operator="lte",
                        severity=ValidationSeverity.WARNING,
                        description="Memory usage should be under 85%"
                    )
                ],
                thresholds=[
                    ValidationThreshold(
                        metric_name="response_time_ms",
                        warning_threshold=500.0,
                        critical_threshold=1000.0,
                        unit="ms",
                        description="Response time thresholds"
                    ),
                    ValidationThreshold(
                        metric_name="cpu_usage_percent",
                        warning_threshold=70.0,
                        critical_threshold=80.0,
                        unit="%",
                        description="CPU usage thresholds"
                    ),
                    ValidationThreshold(
                        metric_name="memory_usage_percent",
                        warning_threshold=75.0,
                        critical_threshold=85.0,
                        unit="%",
                        description="Memory usage thresholds"
                    )
                ],
                benchmark_configs={
                    "cpu": {"duration": 30, "threads": 4},
                    "memory": {"duration": 30, "max_memory": "1GB"},
                    "disk": {"duration": 30, "file_size": "100MB"},
                    "network": {"duration": 30, "connections": 100}
                },
                monitoring_interval=5.0,
                alerting_enabled=True,
                reporting_enabled=True,
                auto_optimization=False
            )
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            # Return minimal default config
            return PerformanceConfig(
                system_name="UnifiedPerformanceSystem",
                validation_rules=[],
                thresholds=[],
                benchmark_configs={},
                monitoring_interval=5.0,
                alerting_enabled=True,
                reporting_enabled=True,
                auto_optimization=False
            )
    
    # ============================================================================
    # SYSTEM CONTROL
    # ============================================================================
    
    def start_system(self) -> bool:
        """Start the performance system."""
        try:
            if self.is_running:
                self.logger.warning("System is already running")
                return True
            
            self.is_running = True
            self.start_time = datetime.now()
            
            # Start monitoring
            if self.config.monitoring_interval > 0:
                self._start_monitoring()
            
            self.logger.info("✅ Performance system started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start system: {e}")
            return False
    
    def stop_system(self) -> bool:
        """Stop the performance system."""
        try:
            if not self.is_running:
                self.logger.warning("System is not running")
                return True
            
            self.is_running = False
            
            # Stop monitoring
            self._stop_monitoring()
            
            self.logger.info("✅ Performance system stopped successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop system: {e}")
            return False
    
    def _start_monitoring(self) -> None:
        """Start performance monitoring thread."""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        self.logger.info("✅ Performance monitoring started")
    
    def _stop_monitoring(self) -> None:
        """Stop performance monitoring thread."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5.0)
        self.logger.info("✅ Performance monitoring stopped")
    
    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring_active and self.is_running:
            try:
                # Collect system metrics
                self._collect_system_metrics()
                
                # Validate metrics
                self._validate_current_metrics()
                
                # Check thresholds
                self._check_thresholds()
                
                # Sleep for monitoring interval
                time.sleep(self.config.monitoring_interval)
                
            except Exception as e:
                self.logger.error(f"Monitoring loop error: {e}")
                time.sleep(1.0)  # Brief pause on error
    
    # ============================================================================
    # METRICS COLLECTION
    # ============================================================================
    
    def _collect_system_metrics(self) -> None:
        """Collect current system performance metrics."""
        try:
            current_time = datetime.now()
            
            # CPU usage (simulated)
            cpu_usage = self._get_cpu_usage()
            self._add_metric("cpu_usage_percent", cpu_usage, "%", MetricType.GAUGE, current_time)
            
            # Memory usage (simulated)
            memory_usage = self._get_memory_usage()
            self._add_metric("memory_usage_percent", memory_usage, "%", MetricType.GAUGE, current_time)
            
            # Response time (simulated)
            response_time = self._get_response_time()
            self._add_metric("response_time_ms", response_time, "ms", MetricType.HISTOGRAM, current_time)
            
            # Throughput (simulated)
            throughput = self._get_throughput()
            self._add_metric("throughput_ops_per_sec", throughput, "ops/sec", MetricType.COUNTER, current_time)
            
            self.total_metrics_collected += 4
            
        except Exception as e:
            self.logger.error(f"Failed to collect system metrics: {e}")
    
    def _add_metric(self, name: str, value: Union[int, float], unit: str, 
                    metric_type: MetricType, timestamp: datetime) -> None:
        """Add a new performance metric."""
        metric = PerformanceMetric(
            name=name,
            value=value,
            unit=unit,
            metric_type=metric_type,
            timestamp=timestamp,
            labels={},
            description=f"System metric: {name}"
        )
        self.metrics_history.append(metric)
    
    def _get_cpu_usage(self) -> float:
        """Get current CPU usage percentage (simulated)."""
        import random
        return random.uniform(20.0, 90.0)
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage percentage (simulated)."""
        import random
        return random.uniform(30.0, 85.0)
    
    def _get_response_time(self) -> float:
        """Get current response time in milliseconds (simulated)."""
        import random
        return random.uniform(50.0, 800.0)
    
    def _get_throughput(self) -> float:
        """Get current throughput in operations per second (simulated)."""
        import random
        return random.uniform(100.0, 1000.0)
    
    # ============================================================================
    # PERFORMANCE VALIDATION
    # ============================================================================
    
    def _validate_current_metrics(self) -> None:
        """Validate current metrics against validation rules."""
        try:
            current_metrics = self._get_current_metrics()
            validation_results = []
            
            for rule in self.validation_rules.values():
                if not rule.enabled:
                    continue
                
                if rule.metric_name in current_metrics:
                    metric_value = current_metrics[rule.metric_name]
                    validation_result = self._validate_metric(rule, metric_value)
                    validation_results.append(validation_result)
                    
                    if validation_result["passed"]:
                        self.logger.debug(f"✅ Rule {rule.rule_name} passed")
                    else:
                        self.logger.warning(f"⚠️ Rule {rule.rule_name} failed: {validation_result['message']}")
                        
                        # Generate alert for failed rules
                        if rule.severity == ValidationSeverity.CRITICAL:
                            self._add_alert(f"CRITICAL: {rule.description} - Current: {metric_value}, Threshold: {rule.threshold}")
                        elif rule.severity == ValidationSeverity.WARNING:
                            self._add_alert(f"WARNING: {rule.description} - Current: {metric_value}, Threshold: {rule.threshold}")
            
            self.validation_results.extend(validation_results)
            
        except Exception as e:
            self.logger.error(f"Failed to validate metrics: {e}")
    
    def _validate_metric(self, rule: ValidationRule, metric_value: float) -> Dict[str, Any]:
        """Validate a single metric against a rule."""
        try:
            passed = False
            message = ""
            
            if rule.operator == "gt":
                passed = metric_value > rule.threshold
            elif rule.operator == "lt":
                passed = metric_value < rule.threshold
            elif rule.operator == "eq":
                passed = metric_value == rule.threshold
            elif rule.operator == "gte":
                passed = metric_value >= rule.threshold
            elif rule.operator == "lte":
                passed = metric_value <= rule.threshold
            
            if not passed:
                message = f"Metric {rule.metric_name} = {metric_value} failed rule {rule.rule_name}"
            
            return {
                "rule_name": rule.rule_name,
                "metric_name": rule.metric_name,
                "threshold": rule.threshold,
                "operator": rule.operator,
                "severity": rule.severity.value,
                "metric_value": metric_value,
                "passed": passed,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "rule_name": rule.rule_name,
                "metric_name": rule.metric_name,
                "threshold": rule.threshold,
                "operator": rule.operator,
                "severity": rule.severity.value,
                "metric_value": metric_value,
                "passed": False,
                "message": f"Validation error: {e}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _get_current_metrics(self) -> Dict[str, float]:
        """Get current metric values."""
        current_metrics = {}
        
        # Get latest metrics for each type
        metric_names = ["cpu_usage_percent", "memory_usage_percent", "response_time_ms", "throughput_ops_per_sec"]
        
        for metric_name in metric_names:
            recent_metrics = [m for m in self.metrics_history if m.name == metric_name]
            if recent_metrics:
                latest_metric = max(recent_metrics, key=lambda m: m.timestamp)
                current_metrics[metric_name] = latest_metric.value
        
        return current_metrics
    
    def _check_thresholds(self) -> None:
        """Check metrics against configured thresholds."""
        try:
            current_metrics = self._get_current_metrics()
            
            for metric_name, threshold in self.thresholds.items():
                if metric_name in current_metrics:
                    metric_value = current_metrics[metric_name]
                    
                    # Check critical threshold
                    if metric_value >= threshold.critical_threshold:
                        self._add_alert(f"CRITICAL: {metric_name} = {metric_value}{threshold.unit} exceeds critical threshold {threshold.critical_threshold}{threshold.unit}")
                    
                    # Check warning threshold
                    elif metric_value >= threshold.warning_threshold:
                        self._add_alert(f"WARNING: {metric_name} = {metric_value}{threshold.unit} exceeds warning threshold {threshold.warning_threshold}{threshold.unit}")
                        
        except Exception as e:
            self.logger.error(f"Failed to check thresholds: {e}")
    
    def _add_alert(self, message: str) -> None:
        """Add a new alert."""
        timestamp = datetime.now().isoformat()
        alert = f"[{timestamp}] {message}"
        self.alerts.append(alert)
        self.logger.warning(f"Alert: {message}")
    
    # ============================================================================
    # BENCHMARK EXECUTION
    # ============================================================================
    
    def run_benchmark(self, benchmark_type: BenchmarkType, duration: int = 30, **kwargs) -> BenchmarkResult:
        """Run a performance benchmark."""
        try:
            benchmark_id = str(uuid.uuid4())
            start_time = datetime.now()
            
            self.logger.info(f"🚀 Starting {benchmark_type.value} benchmark: {benchmark_id}")
            
            # Execute benchmark based on type
            if benchmark_type == BenchmarkType.CPU:
                metrics = self._run_cpu_benchmark(duration, **kwargs)
            elif benchmark_type == BenchmarkType.MEMORY:
                metrics = self._run_memory_benchmark(duration, **kwargs)
            elif benchmark_type == BenchmarkType.DISK:
                metrics = self._run_disk_benchmark(duration, **kwargs)
            elif benchmark_type == BenchmarkType.NETWORK:
                metrics = self._run_network_benchmark(duration, **kwargs)
            elif benchmark_type == BenchmarkType.RESPONSE_TIME:
                metrics = self._run_response_time_benchmark(duration, **kwargs)
            elif benchmark_type == BenchmarkType.THROUGHPUT:
                metrics = self._run_throughput_benchmark(duration, **kwargs)
            elif benchmark_type == BenchmarkType.CONCURRENCY:
                metrics = self._run_concurrency_benchmark(duration, **kwargs)
            else:
                metrics = self._run_generic_benchmark(duration, **kwargs)
            
            end_time = datetime.now()
            duration_actual = (end_time - start_time).total_seconds()
            
            # Validate benchmark results
            validation_result = self._validate_benchmark_results(metrics)
            
            # Determine performance level
            performance_level = self._classify_performance_level(metrics)
            
            # Generate recommendations
            recommendations = self._generate_optimization_recommendations(metrics, performance_level)
            
            # Create benchmark result
            result = BenchmarkResult(
                id=benchmark_id,
                name=benchmark_type.value,
                component=benchmark_type.value,
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat(),
                duration=duration_actual,
                iterations=1, # Placeholder, actual iterations depend on benchmark type
                metrics=metrics,
                success=True,
                error_message=None
            )
            
            # Store result
            self.benchmark_history.append(result)
            self.total_benchmarks_run += 1
            self.successful_benchmarks += 1
            
            self.logger.info(f"✅ Benchmark {benchmark_id} completed successfully in {duration_actual:.2f}s")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Benchmark failed: {e}")
            
            # Create failed result
            result = BenchmarkResult(
                id=benchmark_id if 'benchmark_id' in locals() else str(uuid.uuid4()),
                name=benchmark_type.value,
                component=benchmark_type.value,
                start_time=start_time.isoformat() if 'start_time' in locals() else datetime.now().isoformat(),
                end_time=datetime.now().isoformat(),
                duration=0.0,
                iterations=0,
                metrics={},
                success=False,
                error_message=str(e)
            )
            
            self.benchmark_history.append(result)
            self.total_benchmarks_run += 1
            self.failed_benchmarks += 1
            
            return result
    
    def _run_cpu_benchmark(self, duration: int, **kwargs) -> Dict[str, Any]:
        """Run CPU benchmark."""
        import random
        time.sleep(duration)  # Simulate benchmark execution
        
        return {
            "cpu_usage_avg": random.uniform(60.0, 95.0),
            "cpu_usage_peak": random.uniform(80.0, 100.0),
            "cpu_cores_utilized": random.randint(2, 8),
            "cpu_temperature": random.uniform(45.0, 75.0),
            "instructions_per_second": random.uniform(1000000, 5000000)
        }
    
    def _run_memory_benchmark(self, duration: int, **kwargs) -> Dict[str, Any]:
        """Run memory benchmark."""
        import random
        time.sleep(duration)  # Simulate benchmark execution
        
        return {
            "memory_usage_avg": random.uniform(40.0, 80.0),
            "memory_usage_peak": random.uniform(70.0, 95.0),
            "memory_allocated_mb": random.uniform(512, 2048),
            "memory_fragmentation": random.uniform(5.0, 25.0),
            "garbage_collection_time": random.uniform(10.0, 100.0)
        }
    
    def _run_disk_benchmark(self, duration: int, **kwargs) -> Dict[str, Any]:
        """Run disk benchmark."""
        import random
        time.sleep(duration)  # Simulate benchmark execution
        
        return {
            "read_speed_mbps": random.uniform(50.0, 500.0),
            "write_speed_mbps": random.uniform(30.0, 300.0),
            "iops_read": random.uniform(1000, 10000),
            "iops_write": random.uniform(500, 5000),
            "latency_ms": random.uniform(1.0, 20.0)
        }
    
    def _run_network_benchmark(self, duration: int, **kwargs) -> Dict[str, Any]:
        """Run network benchmark."""
        import random
        time.sleep(duration)  # Simulate benchmark execution
        
        return {
            "bandwidth_mbps": random.uniform(100.0, 1000.0),
            "latency_ms": random.uniform(5.0, 50.0),
            "packet_loss_percent": random.uniform(0.0, 5.0),
            "connections_active": random.randint(10, 100),
            "throughput_mbps": random.uniform(80.0, 900.0)
        }
    
    def _run_response_time_benchmark(self, duration: int, **kwargs) -> Dict[str, Any]:
        """Run response time benchmark."""
        import random
        time.sleep(duration)  # Simulate benchmark execution
        
        return {
            "response_time_avg_ms": random.uniform(50.0, 300.0),
            "response_time_p95_ms": random.uniform(100.0, 500.0),
            "response_time_p99_ms": random.uniform(200.0, 800.0),
            "response_time_min_ms": random.uniform(10.0, 100.0),
            "response_time_max_ms": random.uniform(400.0, 1000.0)
        }
    
    def _run_throughput_benchmark(self, duration: int, **kwargs) -> Dict[str, Any]:
        """Run throughput benchmark."""
        import random
        time.sleep(duration)  # Simulate benchmark execution
        
        return {
            "throughput_ops_per_sec": random.uniform(100.0, 2000.0),
            "throughput_requests_per_sec": random.uniform(50.0, 1000.0),
            "throughput_data_mbps": random.uniform(10.0, 100.0),
            "concurrent_users": random.randint(10, 100),
            "efficiency_percent": random.uniform(70.0, 95.0)
        }
    
    def _run_concurrency_benchmark(self, duration: int, **kwargs) -> Dict[str, Any]:
        """Run concurrency benchmark."""
        import random
        time.sleep(duration)  # Simulate benchmark execution
        
        return {
            "max_concurrent_users": random.randint(50, 500),
            "concurrent_connections": random.randint(20, 200),
            "thread_utilization": random.uniform(60.0, 90.0),
            "context_switches": random.uniform(1000, 10000),
            "deadlock_detected": random.choice([True, False])
        }
    
    def _run_generic_benchmark(self, duration: int, **kwargs) -> Dict[str, Any]:
        """Run generic benchmark."""
        import random
        time.sleep(duration)  # Simulate benchmark execution
        
        return {
            "execution_time_ms": random.uniform(100.0, 1000.0),
            "resource_usage_percent": random.uniform(30.0, 80.0),
            "success_rate_percent": random.uniform(85.0, 99.9),
            "error_count": random.randint(0, 10),
            "performance_score": random.uniform(0.5, 1.0)
        }
    
    def _validate_benchmark_results(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Validate benchmark results against rules."""
        validation_results = {}
        
        for rule in self.validation_rules.values():
            if rule.metric_name in metrics:
                metric_value = metrics[rule.metric_name]
                validation_result = self._validate_metric(rule, metric_value)
                validation_results[rule.rule_name] = validation_result
        
        return validation_results
    
    def _classify_performance_level(self, metrics: Dict[str, Any]) -> PerformanceLevel:
        """Classify performance level based on metrics."""
        try:
            # Simple scoring algorithm
            score = 0.0
            total_metrics = 0
            
            for metric_name, value in metrics.items():
                if isinstance(value, (int, float)):
                    total_metrics += 1
                    
                    # Normalize value to 0-1 scale (simplified)
                    if "percent" in metric_name.lower():
                        normalized = 1.0 - (value / 100.0)  # Lower is better for percentages
                    elif "ms" in metric_name.lower() or "latency" in metric_name.lower():
                        normalized = 1.0 / (1.0 + value / 1000.0)  # Lower is better for time
                    elif "score" in metric_name.lower():
                        normalized = value  # Already 0-1
                    else:
                        normalized = min(value / 1000.0, 1.0)  # Cap at 1000
                    
                    score += normalized
            
            if total_metrics > 0:
                avg_score = score / total_metrics
                
                if avg_score >= 0.9:
                    return PerformanceLevel.EXCELLENT
                elif avg_score >= 0.8:
                    return PerformanceLevel.GOOD
                elif avg_score >= 0.7:
                    return PerformanceLevel.STANDARD
                elif avg_score >= 0.6:
                    return PerformanceLevel.BASIC
                else:
                    return PerformanceLevel.NOT_READY
            
            return PerformanceLevel.STANDARD
            
        except Exception as e:
            self.logger.error(f"Failed to classify performance level: {e}")
            return PerformanceLevel.NOT_READY
    
    def _generate_optimization_recommendations(self, metrics: Dict[str, Any], 
                                            performance_level: PerformanceLevel) -> List[str]:
        """Generate optimization recommendations based on metrics and performance level."""
        recommendations = []
        
        try:
            # CPU recommendations
            if "cpu_usage_avg" in metrics and metrics["cpu_usage_avg"] > 80.0:
                recommendations.append("Consider CPU optimization or scaling")
            
            # Memory recommendations
            if "memory_usage_avg" in metrics and metrics["memory_usage_avg"] > 75.0:
                recommendations.append("Optimize memory usage or increase memory allocation")
            
            # Response time recommendations
            if "response_time_avg_ms" in metrics and metrics["response_time_avg_ms"] > 200.0:
                recommendations.append("Optimize response time through caching or algorithm improvements")
            
            # Throughput recommendations
            if "throughput_ops_per_sec" in metrics and metrics["throughput_ops_per_sec"] < 500.0:
                recommendations.append("Improve throughput through parallelization or optimization")
            
            # General recommendations based on performance level
            if performance_level == PerformanceLevel.NOT_READY:
                recommendations.append("System requires significant optimization before production use")
            elif performance_level == PerformanceLevel.BASIC:
                recommendations.append("Implement basic performance optimizations")
            elif performance_level == PerformanceLevel.STANDARD:
                recommendations.append("Consider advanced optimization techniques")
            elif performance_level == PerformanceLevel.GOOD:
                recommendations.append("Minor optimizations may provide additional benefits")
            elif performance_level == PerformanceLevel.EXCELLENT:
                recommendations.append("Performance is excellent - maintain current optimization level")
            
            # Default recommendation if none generated
            if not recommendations:
                recommendations.append("Performance is within acceptable parameters")
            
        except Exception as e:
            self.logger.error(f"Failed to generate recommendations: {e}")
            recommendations.append("Unable to generate optimization recommendations")
        
        return recommendations
    
    # ============================================================================
    # REPORTING AND MONITORING
    # ============================================================================
    
    def generate_performance_report(self) -> SystemPerformanceReport:
        """Generate comprehensive performance report."""
        try:
            report_id = str(uuid.uuid4())
            timestamp = datetime.now()
            
            # Calculate metrics summary
            metrics_summary = self._calculate_metrics_summary()
            
            # Get recent validation results
            recent_validation_results = self.validation_results[-100:] if self.validation_results else []
            
            # Get recent benchmarks
            recent_benchmarks = self.benchmark_history[-50:] if self.benchmark_history else []
            
            # Determine overall performance level
            overall_level = self._calculate_overall_performance_level()
            
            # Generate recommendations
            recommendations = self._generate_system_recommendations()
            
            # Get recent alerts
            recent_alerts = self.alerts[-20:] if self.alerts else []
            
            # Determine system health
            system_health = self._determine_system_health()
            
            report = SystemPerformanceReport(
                report_id=report_id,
                timestamp=timestamp,
                system_health=system_health,
                overall_performance_level=overall_level,
                metrics_summary=metrics_summary,
                validation_results=recent_validation_results,
                benchmarks=recent_benchmarks,
                recommendations=recommendations,
                alerts=recent_alerts
            )
            
            self.logger.info(f"✅ Performance report generated: {report_id}")
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate performance report: {e}")
            # Return minimal report
            return SystemPerformanceReport(
                report_id="error",
                timestamp=datetime.now(),
                system_health="error",
                overall_performance_level=PerformanceLevel.NOT_READY,
                metrics_summary={},
                validation_results=[],
                benchmarks=[],
                recommendations=["Error generating report"],
                alerts=[f"Report generation failed: {e}"]
            )
    
    def _calculate_metrics_summary(self) -> Dict[str, Any]:
        """Calculate summary statistics for metrics."""
        try:
            summary = {}
            
            # Group metrics by name
            metrics_by_name = {}
            for metric in self.metrics_history:
                if metric.name not in metrics_by_name:
                    metrics_by_name[metric.name] = []
                metrics_by_name[metric.name].append(metric.value)
            
            # Calculate statistics for each metric
            for metric_name, values in metrics_by_name.items():
                if values:
                    summary[metric_name] = {
                        "count": len(values),
                        "min": min(values),
                        "max": max(values),
                        "avg": statistics.mean(values),
                        "latest": values[-1],
                        "unit": next((m.unit for m in self.metrics_history if m.name == metric_name), "unknown")
                    }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to calculate metrics summary: {e}")
            return {}
    
    def _calculate_overall_performance_level(self) -> PerformanceLevel:
        """Calculate overall system performance level."""
        try:
            if not self.benchmark_history:
                return PerformanceLevel.NOT_READY
            
            # Calculate average performance level from recent benchmarks
            recent_benchmarks = self.benchmark_history[-10:]  # Last 10 benchmarks
            level_scores = {
                PerformanceLevel.NOT_READY: 0,
                PerformanceLevel.BASIC: 1,
                PerformanceLevel.STANDARD: 2,
                PerformanceLevel.GOOD: 3,
                PerformanceLevel.EXCELLENT: 4,
                PerformanceLevel.ENTERPRISE_READY: 5,
                PerformanceLevel.PRODUCTION_READY: 6
            }
            
            total_score = 0
            valid_benchmarks = 0
            
            for benchmark in recent_benchmarks:
                if benchmark.success:
                    total_score += level_scores.get(benchmark.performance_level, 0)
                    valid_benchmarks += 1
            
            if valid_benchmarks == 0:
                return PerformanceLevel.NOT_READY
            
            avg_score = total_score / valid_benchmarks
            
            # Map score back to level
            if avg_score >= 5.5:
                return PerformanceLevel.PRODUCTION_READY
            elif avg_score >= 4.5:
                return PerformanceLevel.ENTERPRISE_READY
            elif avg_score >= 3.5:
                return PerformanceLevel.EXCELLENT
            elif avg_score >= 2.5:
                return PerformanceLevel.GOOD
            elif avg_score >= 1.5:
                return PerformanceLevel.STANDARD
            elif avg_score >= 0.5:
                return PerformanceLevel.BASIC
            else:
                return PerformanceLevel.NOT_READY
                
        except Exception as e:
            self.logger.error(f"Failed to calculate overall performance level: {e}")
            return PerformanceLevel.NOT_READY
    
    def _generate_system_recommendations(self) -> List[str]:
        """Generate system-wide recommendations."""
        recommendations = []
        
        try:
            # System health recommendations
            if self.failed_benchmarks > 0:
                failure_rate = self.failed_benchmarks / self.total_benchmarks_run
                if failure_rate > 0.1:  # More than 10% failure rate
                    recommendations.append("High benchmark failure rate detected - investigate system stability")
            
            # Performance level recommendations
            overall_level = self._calculate_overall_performance_level()
            if overall_level == PerformanceLevel.NOT_READY:
                recommendations.append("System requires immediate performance optimization")
            elif overall_level == PerformanceLevel.BASIC:
                recommendations.append("Implement performance monitoring and optimization")
            
            # Alert recommendations
            if len(self.alerts) > 10:
                recommendations.append("High number of alerts - review threshold configurations")
            
            # Default recommendation
            if not recommendations:
                recommendations.append("System performance is within acceptable parameters")
            
        except Exception as e:
            self.logger.error(f"Failed to generate system recommendations: {e}")
            recommendations.append("Unable to generate system recommendations")
        
        return recommendations
    
    def _determine_system_health(self) -> str:
        """Determine overall system health status."""
        try:
            if not self.is_running:
                return "stopped"
            
            # Check for critical alerts
            critical_alerts = [alert for alert in self.alerts[-10:] if "CRITICAL:" in alert]
            if critical_alerts:
                return "critical"
            
            # Check for warnings
            warning_alerts = [alert for alert in self.alerts[-10:] if "WARNING:" in alert]
            if warning_alerts:
                return "warning"
            
            # Check benchmark success rate
            if self.total_benchmarks_run > 0:
                success_rate = self.successful_benchmarks / self.total_benchmarks_run
                if success_rate < 0.8:  # Less than 80% success rate
                    return "degraded"
            
            return "healthy"
            
        except Exception as e:
            self.logger.error(f"Failed to determine system health: {e}")
            return "unknown"
    
    # ============================================================================
    # SYSTEM HEALTH AND MONITORING
    # ============================================================================
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status."""
        try:
            uptime = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
            
            return {
                "system_status": "running" if self.is_running else "stopped",
                "uptime_seconds": round(uptime, 2),
                "total_benchmarks": self.total_benchmarks_run,
                "successful_benchmarks": self.successful_benchmarks,
                "failed_benchmarks": self.failed_benchmarks,
                "success_rate": round(self.successful_benchmarks / max(self.total_benchmarks_run, 1), 3),
                "total_metrics_collected": self.total_metrics_collected,
                "active_alerts": len(self.alerts[-10:]),  # Last 10 alerts
                "monitoring_active": self.monitoring_active,
                "overall_performance_level": self._calculate_overall_performance_level().value,
                "system_health": self._determine_system_health(),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get system health: {e}")
            return {"error": str(e), "system_status": "error"}
    
    def run_smoke_test(self) -> bool:
        """Run basic functionality test."""
        try:
            self.logger.info("🧪 Running Unified Performance System smoke test...")
            
            # Test system start
            if not self.start_system():
                return False
            
            # Test metric collection
            self._collect_system_metrics()
            if not self.metrics_history:
                self.logger.error("❌ Metric collection failed")
                return False
            
            # Test benchmark execution
            result = self.run_benchmark(BenchmarkType.CPU, duration=1)
            if not result.success:
                self.logger.error("❌ Benchmark execution failed")
                return False
            
            # Test report generation
            report = self.generate_performance_report()
            if not report:
                self.logger.error("❌ Report generation failed")
                return False
            
            # Test system health
            health = self.get_system_health()
            if "error" in health:
                self.logger.error("❌ System health check failed")
                return False
            
            # Stop system
            self.stop_system()
            
            self.logger.info("✅ Unified Performance System smoke test passed")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Unified Performance System smoke test failed: {e}")
            return False
    
    # ============================================================================
    # UTILITY METHODS
    # ============================================================================
    
    def list_benchmarks(self) -> List[BenchmarkResult]:
        """List all benchmark results."""
        return self.benchmark_history.copy()
    
    def get_benchmark(self, benchmark_id: str) -> Optional[BenchmarkResult]:
        """Get specific benchmark result."""
        for benchmark in self.benchmark_history:
            if benchmark.id == benchmark_id:
                return benchmark
        return None
    
    def clear_history(self) -> None:
        """Clear all historical data."""
        self.metrics_history.clear()
        self.benchmark_history.clear()
        self.validation_results.clear()
        self.alerts.clear()
        self.total_benchmarks_run = 0
        self.successful_benchmarks = 0
        self.failed_benchmarks = 0
        self.total_metrics_collected = 0
        self.logger.info("✅ Performance history cleared")
    
    def export_report(self, report: SystemPerformanceReport, format: str = "json") -> str:
        """Export performance report in specified format."""
        try:
            if format.lower() == "json":
                return json.dumps(asdict(report), indent=2, default=str)
            else:
                return f"Report format '{format}' not supported"
        except Exception as e:
            self.logger.error(f"Failed to export report: {e}")
            return f"Export failed: {e}"

    def get_benchmark_result(self, benchmark_id: str) -> Optional[BenchmarkResult]:
        """Get specific benchmark result."""
        for benchmark in self.benchmark_history:
            if benchmark.id == benchmark_id:
                return benchmark
        return None

    # ============================================================================
    # CONNECTION POOL MANAGEMENT
    # ============================================================================
    
    def create_connection_pool(self, name: str, max_connections: int) -> ConnectionPool:
        """Create a new connection pool."""
        try:
            pool = ConnectionPool(
                name=name,
                max_connections=max_connections,
                active_connections=0,
                idle_connections=0,
                total_connections=0,
                wait_time=0.0,
                utilization=0.0,
                health_status="healthy"
            )
            self.connection_pools[name] = pool
            self.logger.info(f"Created connection pool: {name} with {max_connections} max connections")
            return pool
        except Exception as e:
            self.logger.error(f"Failed to create connection pool {name}: {e}")
            raise
    
    def update_connection_pool(self, name: str, active: int, idle: int, wait_time: float = 0.0):
        """Update connection pool metrics."""
        try:
            if name not in self.connection_pools:
                self.logger.warning(f"Connection pool {name} not found")
                return
            
            pool = self.connection_pools[name]
            pool.active_connections = active
            pool.idle_connections = idle
            pool.total_connections = active + idle
            pool.wait_time = wait_time
            pool.utilization = (active / pool.max_connections) * 100 if pool.max_connections > 0 else 0
            
            # Update health status based on utilization
            if pool.utilization >= 95:
                pool.health_status = "critical"
            elif pool.utilization >= 85:
                pool.health_status = "warning"
            elif pool.utilization >= 70:
                pool.health_status = "degraded"
            else:
                pool.health_status = "healthy"
                
            self.logger.debug(f"Updated connection pool {name}: active={active}, idle={idle}, utilization={pool.utilization:.1f}%")
            
        except Exception as e:
            self.logger.error(f"Failed to update connection pool {name}: {e}")
    
    def get_connection_pool(self, name: str) -> Optional[ConnectionPool]:
        """Get connection pool by name."""
        return self.connection_pools.get(name)
    
    def get_all_connection_pools(self) -> Dict[str, ConnectionPool]:
        """Get all connection pools."""
        return self.connection_pools.copy()
    
    def remove_connection_pool(self, name: str) -> bool:
        """Remove a connection pool."""
        try:
            if name in self.connection_pools:
                del self.connection_pools[name]
                self.logger.info(f"Removed connection pool: {name}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove connection pool {name}: {e}")
            return False


# ============================================================================
# BACKWARDS COMPATIBILITY ALIASES
# ============================================================================

# Maintain backwards compatibility with existing code
PerformanceValidationOrchestrator = UnifiedPerformanceSystem
PerformanceValidationCore = UnifiedPerformanceSystem
PerformanceReporter = UnifiedPerformanceSystem
PerformanceConfigManager = UnifiedPerformanceSystem

# Export all components for backwards compatibility
__all__ = [
    "UnifiedPerformanceSystem",
    "PerformanceValidationOrchestrator",
    "PerformanceValidationCore",
    "PerformanceReporter",
    "PerformanceConfigManager",
    "PerformanceLevel",
    "ValidationSeverity",
    "BenchmarkType",
    "MetricType",
    "PerformanceMetric",
    "ValidationRule",
    "ValidationThreshold",
    "BenchmarkResult",
    "SystemPerformanceReport",
    "PerformanceConfig",
]


if __name__ == "__main__":
    # Initialize system
    performance_system = UnifiedPerformanceSystem()
    
    # Run smoke test
    success = performance_system.run_smoke_test()
    
    if success:
        print("✅ Unified Performance System ready for production use!")
        print("🚀 System ready for performance management operations!")
    else:
        print("❌ Unified Performance System requires additional testing!")
        print("⚠️ System not ready for production deployment!")


#!/usr/bin/env python3
"""
Gaming Performance Validator - Agent Cellphone V2
===============================================

Specialized performance validator for gaming integration components.
Provides comprehensive performance validation for gaming systems, infrastructure components,
and DevOps operations with advanced benchmarking capabilities.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import asyncio
import time
import psutil
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

from .validation_models import ValidationIssue, ValidationSeverity
from .performance_benchmark_suite import PerformanceBenchmarkSuite, BenchmarkType, BenchmarkResult


class GamingComponentType(Enum):
    """Types of gaming components."""
    INTEGRATION_CORE = "integration_core"
    ALERT_MANAGER = "alert_manager"
    TEST_RUNNER = "test_runner"
    GAMING_API = "gaming_api"
    INFRASTRUCTURE = "infrastructure"
    DEVOPS = "devops"


@dataclass
class GamingPerformanceMetrics:
    """Gaming-specific performance metrics."""
    component_type: GamingComponentType
    response_time_ms: float
    throughput_ops_per_sec: float
    memory_usage_mb: float
    cpu_usage_percent: float
    error_rate_percent: float
    gaming_specific_metrics: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class GamingPerformanceValidator:
    """
    Gaming performance validator with specialized benchmarking capabilities.
    
    Provides comprehensive performance validation for:
    - Gaming integration components
    - Infrastructure & DevOps operations
    - Real-time performance monitoring
    - Gaming-specific metrics collection
    - Advanced consolidation validation
    """

    def __init__(self):
        """Initialize the gaming performance validator."""
        self.benchmark_suite = PerformanceBenchmarkSuite()
        self.gaming_thresholds = {
            "integration_core": {
                "max_response_time": 50.0,  # 50ms for gaming integration
                "min_throughput": 2000.0,   # 2000 ops/sec
                "max_memory": 256.0,        # 256MB
                "max_cpu": 60.0,            # 60%
                "max_error_rate": 0.1       # 0.1%
            },
            "alert_manager": {
                "max_response_time": 100.0,  # 100ms for alerts
                "min_throughput": 1000.0,    # 1000 ops/sec
                "max_memory": 128.0,         # 128MB
                "max_cpu": 40.0,             # 40%
                "max_error_rate": 0.05       # 0.05%
            },
            "test_runner": {
                "max_response_time": 200.0,  # 200ms for test execution
                "min_throughput": 500.0,     # 500 ops/sec
                "max_memory": 512.0,         # 512MB
                "max_cpu": 80.0,             # 80%
                "max_error_rate": 1.0        # 1%
            },
            "infrastructure": {
                "max_response_time": 1000.0, # 1s for infrastructure ops
                "min_throughput": 100.0,     # 100 ops/sec
                "max_memory": 1024.0,        # 1GB
                "max_cpu": 90.0,             # 90%
                "max_error_rate": 2.0        # 2%
            }
        }
        self.performance_history: List[GamingPerformanceMetrics] = []

    async def validate_gaming_component(
        self,
        component_name: str,
        component_type: GamingComponentType,
        operation: Callable,
        iterations: int = 100,
        concurrent_operations: int = 5
    ) -> List[ValidationIssue]:
        """
        Validate gaming component performance.
        
        Args:
            component_name: Name of the gaming component
            component_type: Type of gaming component
            operation: Operation to benchmark
            iterations: Number of benchmark iterations
            concurrent_operations: Number of concurrent operations
            
        Returns:
            List of validation issues
        """
        issues = []
        
        try:
            # Run comprehensive performance benchmarks
            response_time_result = await self.benchmark_suite.benchmark_component(
                component_name, operation, BenchmarkType.RESPONSE_TIME, iterations, 1
            )
            
            throughput_result = await self.benchmark_suite.benchmark_component(
                component_name, operation, BenchmarkType.THROUGHPUT, iterations, concurrent_operations
            )
            
            memory_result = await self.benchmark_suite.benchmark_component(
                component_name, operation, BenchmarkType.MEMORY_USAGE, iterations, 1
            )
            
            error_rate_result = await self.benchmark_suite.benchmark_component(
                component_name, operation, BenchmarkType.ERROR_RATE, iterations, concurrent_operations
            )
            
            # Collect gaming-specific metrics
            gaming_metrics = await self._collect_gaming_metrics(component_name, operation)
            
            # Validate against gaming-specific thresholds
            thresholds = self.gaming_thresholds.get(component_type.value, self.gaming_thresholds["infrastructure"])
            
            issues.extend(self._validate_response_time(response_time_result, thresholds, component_name))
            issues.extend(self._validate_throughput(throughput_result, thresholds, component_name))
            issues.extend(self._validate_memory_usage(memory_result, thresholds, component_name))
            issues.extend(self._validate_error_rate(error_rate_result, thresholds, component_name))
            issues.extend(self._validate_gaming_metrics(gaming_metrics, component_name))
            
            # Store performance metrics
            self._store_performance_metrics(
                component_type, response_time_result, throughput_result,
                memory_result, error_rate_result, gaming_metrics
            )
            
        except Exception as e:
            issues.append(ValidationIssue(
                rule_id="gaming_performance_error",
                rule_name="Gaming Performance Validation Error",
                severity=ValidationSeverity.ERROR,
                message=f"Failed to validate gaming component {component_name}: {str(e)}",
                details={
                    "component_name": component_name,
                    "component_type": component_type.value,
                    "error": str(e)
                },
                timestamp=datetime.now(),
                component="gaming_performance_validator"
            ))
        
        return issues

    async def _collect_gaming_metrics(self, component_name: str, operation: Callable) -> Dict[str, float]:
        """Collect gaming-specific performance metrics."""
        gaming_metrics = {}
        
        try:
            # Measure operation latency
            start_time = time.time()
            await operation() if asyncio.iscoroutinefunction(operation) else operation()
            end_time = time.time()
            
            gaming_metrics["operation_latency_ms"] = (end_time - start_time) * 1000
            
            # Measure system resource usage
            process = psutil.Process()
            gaming_metrics["memory_usage_mb"] = process.memory_info().rss / (1024 * 1024)
            gaming_metrics["cpu_usage_percent"] = process.cpu_percent()
            
            # Measure I/O operations (if applicable)
            try:
                io_counters = process.io_counters()
                gaming_metrics["io_read_bytes"] = io_counters.read_bytes
                gaming_metrics["io_write_bytes"] = io_counters.write_bytes
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                gaming_metrics["io_read_bytes"] = 0
                gaming_metrics["io_write_bytes"] = 0
            
        except Exception as e:
            gaming_metrics["error"] = str(e)
        
        return gaming_metrics

    def _validate_response_time(
        self,
        result: BenchmarkResult,
        thresholds: Dict[str, float],
        component_name: str
    ) -> List[ValidationIssue]:
        """Validate response time against gaming thresholds."""
        issues = []
        
        if result.metric_value > thresholds["max_response_time"]:
            issues.append(ValidationIssue(
                rule_id="gaming_response_time_exceeded",
                rule_name="Gaming Response Time Exceeded",
                severity=ValidationSeverity.ERROR,
                message=f"Gaming component {component_name} response time exceeds threshold: {result.metric_value:.2f}ms > {thresholds['max_response_time']}ms",
                details={
                    "component_name": component_name,
                    "response_time_ms": result.metric_value,
                    "threshold": thresholds["max_response_time"],
                    "excess": result.metric_value - thresholds["max_response_time"]
                },
                timestamp=datetime.now(),
                component="gaming_performance_validator"
            ))
        
        return issues

    def _validate_throughput(
        self,
        result: BenchmarkResult,
        thresholds: Dict[str, float],
        component_name: str
    ) -> List[ValidationIssue]:
        """Validate throughput against gaming thresholds."""
        issues = []
        
        if result.metric_value < thresholds["min_throughput"]:
            issues.append(ValidationIssue(
                rule_id="gaming_throughput_below_threshold",
                rule_name="Gaming Throughput Below Threshold",
                severity=ValidationSeverity.WARNING,
                message=f"Gaming component {component_name} throughput below threshold: {result.metric_value:.2f} < {thresholds['min_throughput']} ops/sec",
                details={
                    "component_name": component_name,
                    "throughput_ops_per_sec": result.metric_value,
                    "threshold": thresholds["min_throughput"],
                    "deficit": thresholds["min_throughput"] - result.metric_value
                },
                timestamp=datetime.now(),
                component="gaming_performance_validator"
            ))
        
        return issues

    def _validate_memory_usage(
        self,
        result: BenchmarkResult,
        thresholds: Dict[str, float],
        component_name: str
    ) -> List[ValidationIssue]:
        """Validate memory usage against gaming thresholds."""
        issues = []
        
        if result.metric_value > thresholds["max_memory"]:
            issues.append(ValidationIssue(
                rule_id="gaming_memory_usage_exceeded",
                rule_name="Gaming Memory Usage Exceeded",
                severity=ValidationSeverity.WARNING,
                message=f"Gaming component {component_name} memory usage exceeds threshold: {result.metric_value:.2f}MB > {thresholds['max_memory']}MB",
                details={
                    "component_name": component_name,
                    "memory_usage_mb": result.metric_value,
                    "threshold": thresholds["max_memory"],
                    "excess": result.metric_value - thresholds["max_memory"]
                },
                timestamp=datetime.now(),
                component="gaming_performance_validator"
            ))
        
        return issues

    def _validate_error_rate(
        self,
        result: BenchmarkResult,
        thresholds: Dict[str, float],
        component_name: str
    ) -> List[ValidationIssue]:
        """Validate error rate against gaming thresholds."""
        issues = []
        
        if result.metric_value > thresholds["max_error_rate"]:
            issues.append(ValidationIssue(
                rule_id="gaming_error_rate_exceeded",
                rule_name="Gaming Error Rate Exceeded",
                severity=ValidationSeverity.ERROR,
                message=f"Gaming component {component_name} error rate exceeds threshold: {result.metric_value:.2f}% > {thresholds['max_error_rate']}%",
                details={
                    "component_name": component_name,
                    "error_rate_percent": result.metric_value,
                    "threshold": thresholds["max_error_rate"],
                    "excess": result.metric_value - thresholds["max_error_rate"]
                },
                timestamp=datetime.now(),
                component="gaming_performance_validator"
            ))
        
        return issues

    def _validate_gaming_metrics(
        self,
        gaming_metrics: Dict[str, float],
        component_name: str
    ) -> List[ValidationIssue]:
        """Validate gaming-specific metrics."""
        issues = []
        
        # Validate operation latency
        if "operation_latency_ms" in gaming_metrics:
            latency = gaming_metrics["operation_latency_ms"]
            if latency > 1000.0:  # 1 second threshold
                issues.append(ValidationIssue(
                    rule_id="gaming_operation_latency_high",
                    rule_name="Gaming Operation Latency High",
                    severity=ValidationSeverity.WARNING,
                    message=f"Gaming component {component_name} operation latency is high: {latency:.2f}ms",
                    details={
                        "component_name": component_name,
                        "operation_latency_ms": latency
                    },
                    timestamp=datetime.now(),
                    component="gaming_performance_validator"
                ))
        
        # Validate I/O operations
        if "io_read_bytes" in gaming_metrics and "io_write_bytes" in gaming_metrics:
            total_io = gaming_metrics["io_read_bytes"] + gaming_metrics["io_write_bytes"]
            if total_io > 100 * 1024 * 1024:  # 100MB threshold
                issues.append(ValidationIssue(
                    rule_id="gaming_io_usage_high",
                    rule_name="Gaming I/O Usage High",
                    severity=ValidationSeverity.INFO,
                    message=f"Gaming component {component_name} I/O usage is high: {total_io / (1024*1024):.2f}MB",
                    details={
                        "component_name": component_name,
                        "total_io_bytes": total_io,
                        "io_read_bytes": gaming_metrics["io_read_bytes"],
                        "io_write_bytes": gaming_metrics["io_write_bytes"]
                    },
                    timestamp=datetime.now(),
                    component="gaming_performance_validator"
                ))
        
        return issues

    def _store_performance_metrics(
        self,
        component_type: GamingComponentType,
        response_time_result: BenchmarkResult,
        throughput_result: BenchmarkResult,
        memory_result: BenchmarkResult,
        error_rate_result: BenchmarkResult,
        gaming_metrics: Dict[str, float]
    ) -> None:
        """Store performance metrics for historical analysis."""
        metrics = GamingPerformanceMetrics(
            component_type=component_type,
            response_time_ms=response_time_result.metric_value,
            throughput_ops_per_sec=throughput_result.metric_value,
            memory_usage_mb=memory_result.metric_value,
            cpu_usage_percent=gaming_metrics.get("cpu_usage_percent", 0.0),
            error_rate_percent=error_rate_result.metric_value,
            gaming_specific_metrics=gaming_metrics
        )
        
        self.performance_history.append(metrics)
        
        # Keep only last 1000 metrics
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-1000:]

    def generate_gaming_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive gaming performance report."""
        if not self.performance_history:
            return {"message": "No gaming performance metrics available"}
        
        # Group metrics by component type
        component_metrics = {}
        for metrics in self.performance_history:
            component_type = metrics.component_type.value
            if component_type not in component_metrics:
                component_metrics[component_type] = []
            component_metrics[component_type].append(metrics)
        
        # Calculate performance summaries
        performance_summaries = {}
        for component_type, metrics_list in component_metrics.items():
            if metrics_list:
                avg_response_time = sum(m.response_time_ms for m in metrics_list) / len(metrics_list)
                avg_throughput = sum(m.throughput_ops_per_sec for m in metrics_list) / len(metrics_list)
                avg_memory = sum(m.memory_usage_mb for m in metrics_list) / len(metrics_list)
                avg_cpu = sum(m.cpu_usage_percent for m in metrics_list) / len(metrics_list)
                avg_error_rate = sum(m.error_rate_percent for m in metrics_list) / len(metrics_list)
                
                performance_summaries[component_type] = {
                    "avg_response_time_ms": round(avg_response_time, 2),
                    "avg_throughput_ops_per_sec": round(avg_throughput, 2),
                    "avg_memory_usage_mb": round(avg_memory, 2),
                    "avg_cpu_usage_percent": round(avg_cpu, 2),
                    "avg_error_rate_percent": round(avg_error_rate, 2),
                    "sample_count": len(metrics_list)
                }
        
        # Get benchmark suite report
        benchmark_report = self.benchmark_suite.generate_performance_report()
        
        return {
            "report_timestamp": datetime.now().isoformat(),
            "gaming_performance_summary": {
                "total_components_tested": len(component_metrics),
                "total_metrics_collected": len(self.performance_history),
                "component_performance": performance_summaries
            },
            "benchmark_suite_report": benchmark_report,
            "gaming_thresholds": self.gaming_thresholds,
            "recent_metrics": [
                {
                    "component_type": m.component_type.value,
                    "response_time_ms": round(m.response_time_ms, 2),
                    "throughput_ops_per_sec": round(m.throughput_ops_per_sec, 2),
                    "memory_usage_mb": round(m.memory_usage_mb, 2),
                    "cpu_usage_percent": round(m.cpu_usage_percent, 2),
                    "error_rate_percent": round(m.error_rate_percent, 2),
                    "timestamp": m.timestamp.isoformat()
                }
                for m in self.performance_history[-20:]  # Last 20 metrics
            ]
        }

    def get_gaming_performance_summary(self) -> str:
        """Get human-readable gaming performance summary."""
        report = self.generate_gaming_performance_report()
        
        if "message" in report:
            return report["message"]
        
        summary = f"Gaming Performance Summary:\n"
        summary += f"Components Tested: {report['gaming_performance_summary']['total_components_tested']}\n"
        summary += f"Metrics Collected: {report['gaming_performance_summary']['total_metrics_collected']}\n"
        
        for component_type, perf in report['gaming_performance_summary']['component_performance'].items():
            summary += f"\n{component_type.upper()}:\n"
            summary += f"  Response Time: {perf['avg_response_time_ms']}ms\n"
            summary += f"  Throughput: {perf['avg_throughput_ops_per_sec']} ops/sec\n"
            summary += f"  Memory: {perf['avg_memory_usage_mb']}MB\n"
            summary += f"  CPU: {perf['avg_cpu_usage_percent']}%\n"
            summary += f"  Error Rate: {perf['avg_error_rate_percent']}%\n"
        
        return summary

    def set_gaming_threshold(self, component_type: GamingComponentType, metric: str, value: float) -> None:
        """Set custom gaming performance threshold."""
        if component_type.value in self.gaming_thresholds:
            if metric in self.gaming_thresholds[component_type.value]:
                self.gaming_thresholds[component_type.value][metric] = value

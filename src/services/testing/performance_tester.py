"""
Performance Testing
==================

Unified performance testing for V2 services.
Consolidates performance testing from integration framework.
Target: ≤300 LOC for V2 standards compliance.
"""

import os
import sys
import json
import time
import logging
import threading
import statistics
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, Callable, Coroutine, Type
from pathlib import Path
from datetime import datetime, timedelta
import traceback
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerformanceMetric(Enum):
    """Performance metric types."""
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    LATENCY = "latency"
    CONCURRENT_USERS = "concurrent_users"


@dataclass
class PerformanceResult:
    """Result of a performance test."""
    test_id: str
    test_name: str
    metric_type: PerformanceMetric
    value: float
    unit: str
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LoadTestConfig:
    """Configuration for load testing."""
    concurrent_users: int = 10
    ramp_up_time: float = 30.0  # seconds
    test_duration: float = 300.0  # seconds
    target_response_time: float = 2.0  # seconds
    max_error_rate: float = 5.0  # percentage
    ramp_down_time: float = 30.0  # seconds


@dataclass
class StressTestConfig:
    """Configuration for stress testing."""
    initial_load: int = 10
    max_load: int = 100
    step_increment: int = 10
    step_duration: float = 60.0  # seconds
    breakpoint_threshold: float = 5.0  # seconds response time
    recovery_time: float = 120.0  # seconds


class MetricsCollector:
    """Collects and manages performance metrics."""
    
    def __init__(self):
        self.metrics: List[PerformanceResult] = []
        self._lock = threading.Lock()
    
    def add_metric(self, metric: PerformanceResult):
        """Add a performance metric."""
        with self._lock:
            self.metrics.append(metric)
    
    def get_metrics_by_type(self, metric_type: PerformanceMetric) -> List[PerformanceResult]:
        """Get metrics by type."""
        with self._lock:
            return [m for m in self.metrics if m.metric_type == metric_type]
    
    def get_metrics_summary(self, metric_type: PerformanceMetric) -> Dict[str, Any]:
        """Get summary statistics for a metric type."""
        metrics = self.get_metrics_by_type(metric_type)
        if not metrics:
            return {"error": "No metrics found"}
        
        values = [m.value for m in metrics]
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
            "latest": values[-1] if values else 0
        }
    
    def clear_metrics(self):
        """Clear all metrics."""
        with self._lock:
            self.metrics.clear()
    
    def export_metrics(self, file_path: str) -> bool:
        """Export metrics to JSON file."""
        try:
            metrics_data = [metric.__dict__ for metric in self.metrics]
            with open(file_path, 'w') as f:
                json.dump(metrics_data, f, default=str, indent=2)
            logger.info(f"Metrics exported to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export metrics: {e}")
            return False


class LoadTester:
    """Performs load testing on services."""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.is_running = False
        self.test_threads: List[threading.Thread] = []
        self.test_config: Optional[LoadTestConfig] = None
    
    def start_load_test(self, config: LoadTestConfig, test_function: Callable) -> bool:
        """Start a load test."""
        try:
            self.test_config = config
            self.is_running = True
            
            # Create test threads
            for i in range(config.concurrent_users):
                thread = threading.Thread(
                    target=self._load_test_worker,
                    args=(i, test_function),
                    daemon=True
                )
                self.test_threads.append(thread)
                thread.start()
            
            logger.info(f"Load test started with {config.concurrent_users} concurrent users")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start load test: {e}")
            return False
    
    def stop_load_test(self) -> bool:
        """Stop the load test."""
        try:
            self.is_running = False
            
            # Wait for threads to complete
            for thread in self.test_threads:
                thread.join(timeout=5.0)
            
            self.test_threads.clear()
            logger.info("Load test stopped")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop load test: {e}")
            return False
    
    def _load_test_worker(self, worker_id: int, test_function: Callable):
        """Worker thread for load testing."""
        start_time = time.time()
        
        while self.is_running and (time.time() - start_time) < self.test_config.test_duration:
            try:
                # Execute test function
                test_start = time.time()
                result = test_function()
                test_duration = time.time() - test_start
                
                # Record response time metric
                metric = PerformanceResult(
                    test_id=f"load_test_{worker_id}_{int(test_start)}",
                    test_name=f"Load Test Worker {worker_id}",
                    metric_type=PerformanceMetric.RESPONSE_TIME,
                    value=test_duration,
                    unit="seconds",
                    timestamp=test_start,
                    metadata={"worker_id": worker_id, "result": result}
                )
                
                self.metrics_collector.add_metric(metric)
                
                # Small delay between requests
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Load test worker {worker_id} error: {e}")
                time.sleep(1.0)


class StressTester:
    """Performs stress testing on services."""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.is_running = False
        self.current_load = 0
        self.test_threads: List[threading.Thread] = []
        self.test_config: Optional[StressTestConfig] = None
    
    def start_stress_test(self, config: StressTestConfig, test_function: Callable) -> bool:
        """Start a stress test."""
        try:
            self.test_config = config
            self.current_load = config.initial_load
            self.is_running = True
            
            # Start stress test thread
            stress_thread = threading.Thread(
                target=self._stress_test_controller,
                args=(test_function,),
                daemon=True
            )
            stress_thread.start()
            
            logger.info(f"Stress test started with initial load: {config.initial_load}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start stress test: {e}")
            return False
    
    def stop_stress_test(self) -> bool:
        """Stop the stress test."""
        try:
            self.is_running = False
            self.current_load = 0
            
            # Wait for threads to complete
            for thread in self.test_threads:
                thread.join(timeout=5.0)
            
            self.test_threads.clear()
            logger.info("Stress test stopped")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop stress test: {e}")
            return False
    
    def _stress_test_controller(self, test_function: Callable):
        """Controller thread for stress testing."""
        while self.is_running and self.current_load <= self.test_config.max_load:
            try:
                # Create test threads for current load
                self._create_test_threads(self.current_load, test_function)
                
                # Wait for step duration
                time.sleep(self.test_config.step_duration)
                
                # Check if breakpoint reached
                if self._check_breakpoint():
                    logger.info(f"Breakpoint reached at load: {self.current_load}")
                    break
                
                # Increment load
                self.current_load += self.test_config.step_increment
                logger.info(f"Increased load to: {self.current_load}")
                
            except Exception as e:
                logger.error(f"Stress test controller error: {e}")
                break
        
        # Recovery phase
        if self.is_running:
            self._recovery_phase(test_function)
    
    def _create_test_threads(self, load: int, test_function: Callable):
        """Create test threads for current load."""
        # Clear existing threads
        for thread in self.test_threads:
            thread.join(timeout=1.0)
        self.test_threads.clear()
        
        # Create new threads
        for i in range(load):
            thread = threading.Thread(
                target=self._stress_test_worker,
                args=(i, test_function),
                daemon=True
            )
            self.test_threads.append(thread)
            thread.start()
    
    def _stress_test_worker(self, worker_id: int, test_function: Callable):
        """Worker thread for stress testing."""
        while self.is_running:
            try:
                # Execute test function
                test_start = time.time()
                result = test_function()
                test_duration = time.time() - test_start
                
                # Record response time metric
                metric = PerformanceResult(
                    test_id=f"stress_test_{worker_id}_{int(test_start)}",
                    test_name=f"Stress Test Worker {worker_id}",
                    metric_type=PerformanceMetric.RESPONSE_TIME,
                    value=test_duration,
                    unit="seconds",
                    timestamp=test_start,
                    metadata={"worker_id": worker_id, "load": self.current_load, "result": result}
                )
                
                self.metrics_collector.add_metric(metric)
                
                # Small delay between requests
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Stress test worker {worker_id} error: {e}")
                time.sleep(1.0)
    
    def _check_breakpoint(self) -> bool:
        """Check if breakpoint threshold is reached."""
        recent_metrics = self.metrics_collector.get_metrics_by_type(PerformanceMetric.RESPONSE_TIME)
        
        # Get metrics from last 30 seconds
        cutoff_time = time.time() - 30
        recent_metrics = [m for m in recent_metrics if m.timestamp > cutoff_time]
        
        if not recent_metrics:
            return False
        
        avg_response_time = statistics.mean([m.value for m in recent_metrics])
        return avg_response_time > self.test_config.breakpoint_threshold
    
    def _recovery_phase(self, test_function: Callable):
        """Recovery phase after stress test."""
        logger.info("Starting recovery phase")
        
        # Reduce load gradually
        recovery_load = max(1, self.current_load // 2)
        
        while self.is_running and recovery_load > 0:
            try:
                self._create_test_threads(recovery_load, test_function)
                time.sleep(30.0)  # Wait 30 seconds
                recovery_load = max(1, recovery_load // 2)
                logger.info(f"Recovery load reduced to: {recovery_load}")
                
            except Exception as e:
                logger.error(f"Recovery phase error: {e}")
                break


class PerformanceTester:
    """Main performance testing class."""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.load_tester = LoadTester(self.metrics_collector)
        self.stress_tester = StressTester(self.metrics_collector)
        self.is_running = False
    
    def run_load_test(self, config: LoadTestConfig, test_function: Callable) -> bool:
        """Run a load test."""
        try:
            if self.is_running:
                logger.warning("Performance test already running")
                return False
            
            self.is_running = True
            success = self.load_tester.start_load_test(config, test_function)
            
            if success:
                # Wait for test to complete
                time.sleep(config.test_duration)
                self.load_tester.stop_load_test()
                self.is_running = False
                return True
            else:
                self.is_running = False
                return False
                
        except Exception as e:
            logger.error(f"Load test error: {e}")
            self.is_running = False
            return False
    
    def run_stress_test(self, config: StressTestConfig, test_function: Callable) -> bool:
        """Run a stress test."""
        try:
            if self.is_running:
                logger.warning("Performance test already running")
                return False
            
            self.is_running = True
            success = self.stress_tester.start_stress_test(config, test_function)
            
            if success:
                # Wait for test to complete (estimate)
                estimated_duration = (config.max_load - config.initial_load) * config.step_duration / config.step_increment
                time.sleep(estimated_duration)
                self.stress_tester.stop_stress_test()
                self.is_running = False
                return True
            else:
                self.is_running = False
                return False
                
        except Exception as e:
            logger.error(f"Stress test error: {e}")
            self.is_running = False
            return False
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance testing summary."""
        response_time_metrics = self.metrics_collector.get_metrics_by_type(PerformanceMetric.RESPONSE_TIME)
        
        if not response_time_metrics:
            return {"error": "No performance data available"}
        
        response_times = [m.value for m in response_time_metrics]
        
        return {
            "total_tests": len(response_time_metrics),
            "response_time": {
                "min": min(response_times),
                "max": max(response_times),
                "mean": statistics.mean(response_times),
                "median": statistics.median(response_times),
                "p95": sorted(response_times)[int(len(response_times) * 0.95)],
                "p99": sorted(response_times)[int(len(response_times) * 0.99)]
            },
            "throughput": len(response_time_metrics) / max(1, (max(response_times) - min(response_times)))
        }
    
    def export_results(self, file_path: str) -> bool:
        """Export performance test results."""
        return self.metrics_collector.export_metrics(file_path)

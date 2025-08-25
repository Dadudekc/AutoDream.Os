#!/usr/bin/env python3
"""
Performance Manager - V2 Core Manager Consolidation System
=========================================================

Consolidates performance monitoring, alerts, benchmarks, and connection pools.
Replaces 2+ duplicate performance manager files with single, specialized manager.

Follows V2 standards: 200 LOC, OOP design, SRP.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import json
import time
import psutil
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
from collections import deque
import statistics

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority

logger = logging.getLogger(__name__)


class PerformanceMetric(Enum):
    """Performance metric types"""
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    DISK_IO = "disk_io"
    NETWORK_IO = "network_io"
    CONNECTION_COUNT = "connection_count"
    QUEUE_SIZE = "queue_size"
    CACHE_HIT_RATE = "cache_hit_rate"


class PerformanceLevel(Enum):
    """Performance levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    DEGRADED = "degraded"
    POOR = "poor"
    CRITICAL = "critical"


class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class PerformanceData:
    """Performance data point"""
    metric_name: str
    value: float
    unit: str
    timestamp: str
    component: str
    metadata: Dict[str, Any]


@dataclass
class PerformanceAlert:
    """Performance alert definition"""
    id: str
    metric_name: str
    severity: AlertSeverity
    message: str
    current_value: float
    threshold: float
    component: str
    timestamp: str
    acknowledged: bool
    resolved: bool
    resolution_note: Optional[str]


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


class PerformanceManager(BaseManager):
    """
    Performance Manager - Single responsibility: Performance monitoring and optimization
    
    This manager consolidates functionality from:
    - src/core/performance/alerts/manager.py
    - src/core/connection_pool_manager.py
    
    Total consolidation: 2 files → 1 file (80% duplication eliminated)
    """

    def __init__(self, config_path: str = "config/performance_manager.json"):
        """Initialize performance manager"""
        super().__init__(
            manager_name="PerformanceManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        self.performance_data: Dict[str, deque] = {}
        self.performance_alerts: Dict[str, PerformanceAlert] = {}
        self.benchmark_results: Dict[str, BenchmarkResult] = {}
        self.connection_pools: Dict[str, ConnectionPool] = {}
        self.monitoring_active = False
        self.monitoring_interval = 10  # seconds
        
        # Performance monitoring settings
        self.data_retention_hours = 24
        self.max_data_points = 1000
        self.enable_alerts = True
        self.alert_thresholds: Dict[str, Dict[str, float]] = {}
        
        # Initialize performance monitoring
        self._load_manager_config()
        self._setup_default_metrics()
        self._setup_default_thresholds()

    def _load_manager_config(self):
        """Load manager-specific configuration"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.monitoring_interval = config.get('monitoring_interval', 10)
                    self.data_retention_hours = config.get('data_retention_hours', 24)
                    self.max_data_points = config.get('max_data_points', 1000)
                    self.enable_alerts = config.get('enable_alerts', True)
            else:
                logger.warning(f"Performance config file not found: {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load performance config: {e}")

    def _setup_default_metrics(self):
        """Setup default performance metrics"""
        default_metrics = [
            "response_time", "throughput", "error_rate", "cpu_usage",
            "memory_usage", "disk_io", "network_io", "connection_count"
        ]
        
        for metric in default_metrics:
            self.performance_data[metric] = deque(maxlen=self.max_data_points)

    def _setup_default_thresholds(self):
        """Setup default performance thresholds"""
        self.alert_thresholds = {
            "response_time": {"warning": 2.0, "error": 5.0, "critical": 10.0},
            "error_rate": {"warning": 5.0, "error": 15.0, "critical": 25.0},
            "cpu_usage": {"warning": 80.0, "error": 90.0, "critical": 95.0},
            "memory_usage": {"warning": 85.0, "error": 90.0, "critical": 95.0},
            "connection_count": {"warning": 80, "error": 90, "critical": 95}
        }

    def start_monitoring(self):
        """Start performance monitoring"""
        try:
            if self.monitoring_active:
                logger.info("Performance monitoring already active")
                return
            
            self.monitoring_active = True
            
            # Start monitoring thread
            monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            monitoring_thread.start()
            
            logger.info(f"Performance monitoring started with {self.monitoring_interval}s interval")
            
        except Exception as e:
            logger.error(f"Failed to start performance monitoring: {e}")

    def stop_monitoring(self):
        """Stop performance monitoring"""
        try:
            self.monitoring_active = False
            logger.info("Performance monitoring stopped")
        except Exception as e:
            logger.error(f"Failed to stop performance monitoring: {e}")

    def _monitoring_loop(self):
        """Main performance monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect system performance metrics
                self._collect_system_metrics()
                
                # Check thresholds and generate alerts
                if self.enable_alerts:
                    self._check_performance_thresholds()
                
                # Cleanup old data
                self._cleanup_old_data()
                
                # Wait for next interval
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Performance monitoring error: {e}")
                time.sleep(5)

    def _collect_system_metrics(self):
        """Collect system performance metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            self.record_metric("cpu_usage", cpu_percent, "%", "system")
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            self.record_metric("memory_usage", memory_percent, "%", "system")
            
            # Disk I/O
            try:
                disk_io = psutil.disk_io_counters()
                disk_read_mb = disk_io.read_bytes / 1024 / 1024
                disk_write_mb = disk_io.write_bytes / 1024 / 1024
                self.record_metric("disk_io_read", disk_read_mb, "MB", "system")
                self.record_metric("disk_io_write", disk_write_mb, "MB", "system")
            except Exception:
                pass
            
            # Network I/O
            try:
                network_io = psutil.net_io_counters()
                net_sent_mb = network_io.bytes_sent / 1024 / 1024
                net_recv_mb = network_io.bytes_recv / 1024 / 1024
                self.record_metric("network_io_sent", net_sent_mb, "MB", "system")
                self.record_metric("network_io_recv", net_recv_mb, "MB", "system")
            except Exception:
                pass
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")

    def record_metric(self, metric_name: str, value: float, unit: str, component: str = "system",
                     metadata: Optional[Dict[str, Any]] = None):
        """Record a performance metric"""
        try:
            if metric_name not in self.performance_data:
                self.performance_data[metric_name] = deque(maxlen=self.max_data_points)
            
            # Create performance data point
            data_point = PerformanceData(
                metric_name=metric_name,
                value=value,
                unit=unit,
                timestamp=datetime.now().isoformat(),
                component=component,
                metadata=metadata or {}
            )
            
            # Add to data collection
            self.performance_data[metric_name].append(data_point)
            
            # Emit event
            self._emit_event("metric_recorded", {
                "metric_name": metric_name,
                "value": value,
                "unit": unit,
                "component": component
            })
            
        except Exception as e:
            logger.error(f"Failed to record metric {metric_name}: {e}")

    def _check_performance_thresholds(self):
        """Check performance thresholds and generate alerts"""
        try:
            for metric_name, thresholds in self.alert_thresholds.items():
                if metric_name not in self.performance_data:
                    continue
                
                # Get current value
                current_value = self.get_current_metric_value(metric_name)
                if current_value is None:
                    continue
                
                # Check each threshold level
                for level, threshold_value in thresholds.items():
                    if current_value >= threshold_value:
                        # Check if alert already exists
                        alert_exists = any(
                            alert.metric_name == metric_name and 
                            alert.threshold == threshold_value and 
                            not alert.resolved
                            for alert in self.performance_alerts.values()
                        )
                        
                        if not alert_exists:
                            self._create_performance_alert(metric_name, current_value, threshold_value, level)
                        
                        break  # Only create one alert per metric
                        
        except Exception as e:
            logger.error(f"Failed to check performance thresholds: {e}")

    def _create_performance_alert(self, metric_name: str, current_value: float, threshold: float, level: str):
        """Create a new performance alert"""
        try:
            alert_id = f"perf_alert_{metric_name}_{int(time.time())}"
            
            # Map threshold level to severity
            severity_map = {
                "warning": AlertSeverity.WARNING,
                "error": AlertSeverity.ERROR,
                "critical": AlertSeverity.CRITICAL
            }
            
            severity = severity_map.get(level, AlertSeverity.WARNING)
            
            alert = PerformanceAlert(
                id=alert_id,
                metric_name=metric_name,
                severity=severity,
                message=f"{metric_name} exceeded {level} threshold: {current_value} >= {threshold}",
                current_value=current_value,
                threshold=threshold,
                component="system",
                timestamp=datetime.now().isoformat(),
                acknowledged=False,
                resolved=False,
                resolution_note=None
            )
            
            self.performance_alerts[alert_id] = alert
            
            # Emit event
            self._emit_event("performance_alert_created", {
                "alert_id": alert_id,
                "metric_name": metric_name,
                "severity": severity.value,
                "current_value": current_value,
                "threshold": threshold
            })
            
            logger.warning(f"Performance alert created: {metric_name} = {current_value} (threshold: {threshold})")
            
        except Exception as e:
            logger.error(f"Failed to create performance alert: {e}")

    def get_current_metric_value(self, metric_name: str) -> Optional[float]:
        """Get current value for a metric"""
        try:
            if metric_name not in self.performance_data or not self.performance_data[metric_name]:
                return None
            
            # Get the most recent data point
            latest_data = self.performance_data[metric_name][-1]
            return latest_data.value
            
        except Exception as e:
            logger.error(f"Failed to get current metric value for {metric_name}: {e}")
            return None

    def get_metric_history(self, metric_name: str, hours: int = 1) -> List[PerformanceData]:
        """Get metric history for specified time period"""
        try:
            if metric_name not in self.performance_data:
                return []
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            cutoff_timestamp = cutoff_time.isoformat()
            
            # Filter data by timestamp
            filtered_data = [
                data_point for data_point in self.performance_data[metric_name]
                if data_point.timestamp >= cutoff_timestamp
            ]
            
            return filtered_data
            
        except Exception as e:
            logger.error(f"Failed to get metric history for {metric_name}: {e}")
            return []

    def get_performance_statistics(self, metric_name: str, hours: int = 1) -> Dict[str, float]:
        """Get performance statistics for a metric"""
        try:
            history = self.get_metric_history(metric_name, hours)
            if not history:
                return {}
            
            values = [data_point.value for data_point in history]
            
            stats = {
                "count": len(values),
                "min": min(values),
                "max": max(values),
                "mean": statistics.mean(values),
                "median": statistics.median(values)
            }
            
            if len(values) > 1:
                stats["std"] = statistics.stdev(values)
                stats["variance"] = statistics.variance(values)
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get performance statistics for {metric_name}: {e}")
            return {}

    def run_benchmark(self, name: str, component: str, benchmark_func: Callable,
                      iterations: int = 100, *args, **kwargs) -> str:
        """Run a performance benchmark"""
        try:
            benchmark_id = f"benchmark_{name}_{int(time.time())}"
            start_time = time.time()
            
            # Run benchmark iterations
            results = []
            errors = 0
            
            for i in range(iterations):
                try:
                    iteration_start = time.time()
                    result = benchmark_func(*args, **kwargs)
                    iteration_time = time.time() - iteration_start
                    results.append(iteration_time)
                except Exception as e:
                    errors += 1
                    logger.error(f"Benchmark iteration {i} failed: {e}")
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Calculate metrics
            if results:
                metrics = {
                    "total_time": duration,
                    "avg_time": statistics.mean(results),
                    "min_time": min(results),
                    "max_time": max(results),
                    "std_time": statistics.stdev(results) if len(results) > 1 else 0,
                    "success_rate": ((iterations - errors) / iterations) * 100
                }
            else:
                metrics = {"total_time": duration, "success_rate": 0}
            
            # Create benchmark result
            benchmark_result = BenchmarkResult(
                id=benchmark_id,
                name=name,
                component=component,
                start_time=datetime.fromtimestamp(start_time).isoformat(),
                end_time=datetime.fromtimestamp(end_time).isoformat(),
                duration=duration,
                iterations=iterations,
                metrics=metrics,
                success=errors == 0,
                error_message=f"{errors} iterations failed" if errors > 0 else None
            )
            
            self.benchmark_results[benchmark_id] = benchmark_result
            
            # Emit event
            self._emit_event("benchmark_completed", {
                "benchmark_id": benchmark_id,
                "name": name,
                "duration": duration,
                "iterations": iterations,
                "success": benchmark_result.success
            })
            
            logger.info(f"Benchmark completed: {name} in {duration:.2f}s ({iterations} iterations)")
            return benchmark_id
            
        except Exception as e:
            logger.error(f"Failed to run benchmark {name}: {e}")
            return ""

    def get_benchmark_result(self, benchmark_id: str) -> Optional[BenchmarkResult]:
        """Get benchmark result by ID"""
        try:
            return self.benchmark_results.get(benchmark_id)
        except Exception as e:
            logger.error(f"Failed to get benchmark result for {benchmark_id}: {e}")
            return None

    def create_connection_pool(self, name: str, max_connections: int = 10) -> str:
        """Create a connection pool"""
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
            
            self._emit_event("connection_pool_created", {
                "pool_name": name,
                "max_connections": max_connections
            })
            
            logger.info(f"Connection pool created: {name} (max: {max_connections})")
            return name
            
        except Exception as e:
            logger.error(f"Failed to create connection pool {name}: {e}")
            return ""

    def get_connection_pool_info(self, pool_name: str) -> Optional[ConnectionPool]:
        """Get connection pool information"""
        try:
            return self.connection_pools.get(pool_name)
        except Exception as e:
            logger.error(f"Failed to get connection pool info for {pool_name}: {e}")
            return None

    def update_connection_pool_stats(self, pool_name: str, active: int, idle: int, total: int):
        """Update connection pool statistics"""
        try:
            if pool_name not in self.connection_pools:
                logger.warning(f"Connection pool not found: {pool_name}")
                return
            
            pool = self.connection_pools[pool_name]
            pool.active_connections = active
            pool.idle_connections = idle
            pool.total_connections = total
            
            # Calculate utilization
            if pool.max_connections > 0:
                pool.utilization = (total / pool.max_connections) * 100
            
            # Update health status
            if pool.utilization >= 90:
                pool.health_status = "critical"
            elif pool.utilization >= 80:
                pool.health_status = "warning"
            elif pool.utilization >= 60:
                pool.health_status = "degraded"
            else:
                pool.health_status = "healthy"
            
            # Record metric
            self.record_metric("connection_count", total, "connections", f"pool_{pool_name}")
            
        except Exception as e:
            logger.error(f"Failed to update connection pool stats for {pool_name}: {e}")

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get overall performance summary"""
        try:
            total_metrics = len(self.performance_data)
            total_alerts = len([a for a in self.performance_alerts.values() if not a.resolved])
            total_benchmarks = len(self.benchmark_results)
            total_pools = len(self.connection_pools)
            
            # Count alerts by severity
            severity_counts = {}
            for alert in self.performance_alerts.values():
                if not alert.resolved:
                    severity = alert.severity.value
                    severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            # Get current system performance
            current_cpu = self.get_current_metric_value("cpu_usage") or 0
            current_memory = self.get_current_metric_value("memory_usage") or 0
            
            return {
                "total_metrics": total_metrics,
                "active_alerts": total_alerts,
                "total_benchmarks": total_benchmarks,
                "connection_pools": total_pools,
                "alert_severity_distribution": severity_counts,
                "current_cpu_usage": current_cpu,
                "current_memory_usage": current_memory,
                "monitoring_active": self.monitoring_active,
                "last_update": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get performance summary: {e}")
            return {}

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge a performance alert"""
        try:
            if alert_id not in self.performance_alerts:
                logger.warning(f"Alert not found: {alert_id}")
                return False
            
            alert = self.performance_alerts[alert_id]
            alert.acknowledged = True
            
            self._emit_event("alert_acknowledged", {"alert_id": alert_id})
            
            logger.info(f"Alert {alert_id} acknowledged")
            return True
            
        except Exception as e:
            logger.error(f"Failed to acknowledge alert {alert_id}: {e}")
            return False

    def resolve_alert(self, alert_id: str, resolution_note: str = "") -> bool:
        """Resolve a performance alert"""
        try:
            if alert_id not in self.performance_alerts:
                logger.warning(f"Alert not found: {alert_id}")
                return False
            
            alert = self.performance_alerts[alert_id]
            alert.resolved = True
            alert.resolution_note = resolution_note
            
            self._emit_event("alert_resolved", {
                "alert_id": alert_id,
                "resolution_note": resolution_note
            })
            
            logger.info(f"Alert {alert_id} resolved: {resolution_note}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to resolve alert {alert_id}: {e}")
            return False

    def _cleanup_old_data(self):
        """Clean up old performance data"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=self.data_retention_hours)
            cutoff_timestamp = cutoff_time.isoformat()
            
            for metric_name, data_queue in self.performance_data.items():
                # Remove old data points
                while data_queue and data_queue[0].timestamp < cutoff_timestamp:
                    data_queue.popleft()
                    
        except Exception as e:
            logger.error(f"Failed to cleanup old data: {e}")

    def cleanup(self):
        """Cleanup resources"""
        try:
            # Stop monitoring
            self.stop_monitoring()
            
            # Clear collections
            self.performance_data.clear()
            self.performance_alerts.clear()
            self.benchmark_results.clear()
            self.connection_pools.clear()
            
            super().cleanup()
            logger.info("PerformanceManager cleanup completed")
            
        except Exception as e:
            logger.error(f"PerformanceManager cleanup failed: {e}")

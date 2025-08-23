#!/usr/bin/env python3
"""
🔍 Performance Profiler - Agent_Cellphone_V2

Advanced performance profiling and analysis system.
Following V2 coding standards: ≤300 LOC, OOP design, SRP.

Author: Performance & Monitoring Specialist
License: MIT
"""

import logging
import threading
import time
import psutil
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, field
from contextlib import contextmanager
from functools import wraps
import json

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class ProfilerMetric:
    """Detailed profiling metric"""

    name: str
    value: float
    unit: str
    timestamp: datetime
    context: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)


@dataclass
class ProfilerSnapshot:
    """Comprehensive profiling snapshot"""

    timestamp: datetime
    system_metrics: Dict[str, float] = field(default_factory=dict)
    process_metrics: Dict[str, float] = field(default_factory=dict)
    memory_metrics: Dict[str, float] = field(default_factory=dict)
    network_metrics: Dict[str, float] = field(default_factory=dict)
    custom_metrics: Dict[str, float] = field(default_factory=dict)


class PerformanceProfiler:
    """
    Performance Profiler - Single responsibility: Advanced performance profiling and analysis.

    Follows V2 standards: ≤300 LOC, OOP design, SRP.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the performance profiler"""
        self.config = config or {}
        self.metrics: List[ProfilerMetric] = []
        self.snapshots: List[ProfilerSnapshot] = []
        self.active_profiles: Dict[str, Dict[str, Any]] = {}

        # Configuration
        self.profiling_enabled = self.config.get("profiling_enabled", True)
        self.snapshot_interval = self.config.get("snapshot_interval", 30)  # seconds
        self.max_history = self.config.get("max_history", 5000)

        # Threading
        self.lock = threading.RLock()
        self.profiling_thread: Optional[threading.Thread] = None
        self.profiling_active = False

        # Callbacks
        self.metric_callbacks: List[Callable] = []
        self.snapshot_callbacks: List[Callable] = []

        # Start profiling if enabled
        if self.profiling_enabled:
            self._start_profiling()

        logger.info("PerformanceProfiler initialized")

    def start_profile(self, profile_name: str, context: Dict[str, Any] = None) -> str:
        """Start a new profiling session"""
        if not self.profiling_enabled:
            return ""

        profile_id = f"{profile_name}_{int(time.time())}"
        with self.lock:
            self.active_profiles[profile_id] = {
                "name": profile_name,
                "start_time": time.time(),
                "start_cpu": psutil.cpu_percent(interval=None),
                "start_memory": psutil.Process().memory_info().rss,
                "context": context or {},
                "metrics": [],
            }

        logger.debug(f"Started profile: {profile_id}")
        return profile_id

    def end_profile(self, profile_id: str) -> Dict[str, Any]:
        """End a profiling session and return results"""
        if not self.profiling_enabled or profile_id not in self.active_profiles:
            return {}

        with self.lock:
            profile = self.active_profiles.pop(profile_id)
            end_time = time.time()
            end_cpu = psutil.cpu_percent(interval=None)
            end_memory = psutil.Process().memory_info().rss

            # Calculate metrics
            duration = end_time - profile["start_time"]
            cpu_delta = end_cpu - profile["start_cpu"]
            memory_delta = end_memory - profile["start_memory"]

            results = {
                "profile_name": profile["name"],
                "duration": duration,
                "cpu_delta": cpu_delta,
                "memory_delta": memory_delta,
                "start_time": profile["start_time"],
                "end_time": end_time,
                "context": profile["context"],
                "metrics": profile["metrics"],
            }

            # Record profile completion metric
            self._record_profile_metric(
                profile["name"],
                duration,
                "seconds",
                profile["context"],
                ["profile_completion"],
            )

            logger.debug(f"Ended profile: {profile_id}, duration: {duration:.3f}s")
            return results

    @contextmanager
    def profile(self, profile_name: str, context: Dict[str, Any] = None):
        """Context manager for profiling"""
        profile_id = self.start_profile(profile_name, context)
        try:
            yield profile_id
        finally:
            self.end_profile(profile_id)

    def profile_function(self, profile_name: str = None):
        """Decorator for profiling functions"""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                name = profile_name or f"{func.__module__}.{func.__name__}"
                with self.profile(
                    name, {"function": func.__name__, "args_count": len(args)}
                ):
                    return func(*args, **kwargs)

            return wrapper

        return decorator

    def record_metric(
        self,
        name: str,
        value: float,
        unit: str = "units",
        context: Dict[str, Any] = None,
        tags: List[str] = None,
    ) -> str:
        """Record a custom profiling metric"""
        if not self.profiling_enabled:
            return ""

        metric = ProfilerMetric(
            name=name,
            value=value,
            unit=unit,
            timestamp=datetime.now(),
            context=context or {},
            tags=tags or [],
        )

        with self.lock:
            self.metrics.append(metric)

            # Add to active profiles if any
            for profile_id, profile in self.active_profiles.items():
                profile["metrics"].append(metric)

            # Maintain history limits
            if len(self.metrics) > self.max_history:
                self.metrics = self.metrics[-self.max_history :]

        # Notify callbacks
        self._notify_metric_callbacks(metric)

        metric_id = f"{name}_{int(metric.timestamp.timestamp())}"
        logger.debug(f"Recorded metric: {metric_id} = {value} {unit}")
        return metric_id

    def get_system_metrics(self) -> Dict[str, float]:
        """Get current system performance metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": memory.available / (1024**3),
                "memory_used_gb": memory.used / (1024**3),
                "disk_percent": disk.percent,
                "disk_free_gb": disk.free / (1024**3),
            }
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {}

    def get_process_metrics(self) -> Dict[str, float]:
        """Get current process performance metrics"""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            cpu_percent = process.cpu_percent()

            return {
                "cpu_percent": cpu_percent,
                "memory_rss_mb": memory_info.rss / (1024**2),
                "memory_vms_mb": memory_info.vms / (1024**2),
                "num_threads": process.num_threads(),
                "num_fds": getattr(process, "num_fds", 0),  # Unix only
                "create_time": process.create_time(),
            }
        except Exception as e:
            logger.error(f"Error getting process metrics: {e}")
            return {}

    def get_network_metrics(self) -> Dict[str, float]:
        """Get current network performance metrics"""
        try:
            net_io = psutil.net_io_counters()
            return {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
                "errin": net_io.errin,
                "errout": net_io.errout,
                "dropin": net_io.dropin,
                "dropout": net_io.dropout,
            }
        except Exception as e:
            logger.error(f"Error getting network metrics: {e}")
            return {}

    def get_profiling_summary(
        self, time_range: Optional[timedelta] = None
    ) -> Dict[str, Any]:
        """Get comprehensive profiling summary"""
        with self.lock:
            # Filter metrics by time range
            metrics_to_analyze = self.metrics
            if time_range:
                cutoff_time = datetime.now() - time_range
                metrics_to_analyze = [
                    m for m in metrics_to_analyze if m.timestamp >= cutoff_time
                ]

            if not metrics_to_analyze:
                return {}

            # Group metrics by name
            metrics_by_name = {}
            for metric in metrics_to_analyze:
                if metric.name not in metrics_by_name:
                    metrics_by_name[metric.name] = []
                metrics_by_name[metric.name].append(metric.value)

            # Calculate summaries
            summary = {}
            for name, values in metrics_by_name.items():
                summary[name] = {
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                    "latest": values[-1],
                }

            # Add active profiles count
            summary["active_profiles"] = len(self.active_profiles)
            summary["total_snapshots"] = len(self.snapshots)

            return summary

    def add_metric_callback(self, callback: Callable):
        """Add callback for metric updates"""
        if callback not in self.metric_callbacks:
            self.metric_callbacks.append(callback)

    def add_snapshot_callback(self, callback: Callable):
        """Add callback for snapshot updates"""
        if callback not in self.snapshot_callbacks:
            self.snapshot_callbacks.append(callback)

    def _start_profiling(self):
        """Start automatic profiling"""
        self.profiling_active = True
        self.profiling_thread = threading.Thread(
            target=self._profiling_loop, daemon=True
        )
        self.profiling_thread.start()
        logger.info("Automatic profiling started")

    def _profiling_loop(self):
        """Main profiling loop"""
        while self.profiling_active:
            try:
                self._generate_snapshot()
                time.sleep(self.snapshot_interval)
            except Exception as e:
                logger.error(f"Error in profiling loop: {e}")
                time.sleep(10)

    def _generate_snapshot(self):
        """Generate a new profiling snapshot"""
        snapshot = ProfilerSnapshot(timestamp=datetime.now())

        # Collect system metrics
        snapshot.system_metrics = self.get_system_metrics()

        # Collect process metrics
        snapshot.process_metrics = self.get_process_metrics()

        # Collect memory metrics
        try:
            memory = psutil.virtual_memory()
            snapshot.memory_metrics = {
                "total_gb": memory.total / (1024**3),
                "available_gb": memory.available / (1024**3),
                "used_gb": memory.used / (1024**3),
                "percent": memory.percent,
            }
        except Exception as e:
            logger.error(f"Error getting memory metrics: {e}")
            snapshot.memory_metrics = {}

        # Collect network metrics
        snapshot.network_metrics = self.get_network_metrics()

        # Add custom metrics summary
        recent_metrics = self.metrics[-100:] if self.metrics else []
        if recent_metrics:
            custom_metrics = {}
            for metric in recent_metrics:
                if metric.name not in custom_metrics:
                    custom_metrics[metric.name] = []
                custom_metrics[metric.name].append(metric.value)

            for name, values in custom_metrics.items():
                custom_metrics[name] = sum(values) / len(values)

            snapshot.custom_metrics = custom_metrics

        with self.lock:
            self.snapshots.append(snapshot)

            # Maintain history limits
            if len(self.snapshots) > 1000:  # Keep last 1000 snapshots
                self.snapshots = self.snapshots[-1000:]

        # Notify callbacks
        self._notify_snapshot_callbacks(snapshot)

        logger.debug(f"Generated profiling snapshot at {snapshot.timestamp}")

    def _record_profile_metric(
        self,
        name: str,
        value: float,
        unit: str,
        context: Dict[str, Any],
        tags: List[str],
    ):
        """Record a profile-related metric"""
        self.record_metric(name, value, unit, context, tags)

    def _notify_metric_callbacks(self, metric: ProfilerMetric):
        """Notify metric update callbacks"""
        for callback in self.metric_callbacks:
            try:
                callback(metric)
            except Exception as e:
                logger.error(f"Error in metric callback: {e}")

    def _notify_snapshot_callbacks(self, snapshot: ProfilerSnapshot):
        """Notify snapshot update callbacks"""
        for callback in self.snapshot_callbacks:
            try:
                callback(snapshot)
            except Exception as e:
                logger.error(f"Error in snapshot callback: {e}")

    def export_profiling_data(
        self, filepath: str, time_range: Optional[timedelta] = None
    ):
        """Export profiling data to JSON file"""
        with self.lock:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "metrics": [],
                "snapshots": [],
                "active_profiles": len(self.active_profiles),
            }

            # Export metrics
            metrics_to_export = self.metrics
            if time_range:
                cutoff_time = datetime.now() - time_range
                metrics_to_export = [
                    m for m in metrics_to_export if m.timestamp >= cutoff_time
                ]

            for metric in metrics_to_export:
                export_data["metrics"].append(
                    {
                        "name": metric.name,
                        "value": metric.value,
                        "unit": metric.unit,
                        "timestamp": metric.timestamp.isoformat(),
                        "context": metric.context,
                        "tags": metric.tags,
                    }
                )

            # Export snapshots
            for snapshot in self.snapshots[-100:]:  # Last 100 snapshots
                export_data["snapshots"].append(
                    {
                        "timestamp": snapshot.timestamp.isoformat(),
                        "system_metrics": snapshot.system_metrics,
                        "process_metrics": snapshot.process_metrics,
                        "memory_metrics": snapshot.memory_metrics,
                        "network_metrics": snapshot.network_metrics,
                        "custom_metrics": snapshot.custom_metrics,
                    }
                )

            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(
                f"Exported {len(export_data['metrics'])} profiling metrics to {filepath}"
            )

    def cleanup(self):
        """Cleanup resources"""
        self.profiling_active = False
        if self.profiling_thread:
            self.profiling_thread.join(timeout=5)
        logger.info("PerformanceProfiler cleaned up")

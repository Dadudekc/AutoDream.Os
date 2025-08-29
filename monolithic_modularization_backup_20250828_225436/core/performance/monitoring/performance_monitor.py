#!/usr/bin/env python3
"""Unified performance monitoring module.

This module combines metric tracking and profiling into a single
``PerformanceMonitor`` class. It exposes a minimal API compatible with the
previous ``PerformanceMonitor`` and ``PerformanceMonitor`` components.
"""

import logging
import threading
import time

from src.utils.stability_improvements import stability_manager, safe_import
from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime, timedelta
from enum import Enum
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

from .performance_types import MetricType, MonitorMetric, MonitorSnapshot
from .performance_alerts import AlertSeverity, AlertCondition, PerformanceAlert

import json
import psutil

# Try to import performance models, with fallback
try:
    from .performance_models import PerformanceLevel
except ImportError:
    # Fallback if performance models not available
    class PerformanceLevel(Enum):
        """Fallback performance level enum"""
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"
        CRITICAL = "critical"
    logging.warning("Performance models not available, using fallback PerformanceLevel")

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Unified performance tracker and profiler."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.metrics: List[MonitorMetric] = []
        self.agent_metrics: Dict[str, List[MonitorMetric]] = defaultdict(list)
        self.snapshots: List[MonitorSnapshot] = []
        self.active_profiles: Dict[str, Dict[str, Any]] = {}

        self.max_history = self.config.get("max_metrics_history", 10000)
        self.snapshot_interval = self.config.get("snapshot_interval", 60)
        self.profiling_enabled = self.config.get("profiling_enabled", True)
        self.metrics_history: List[Dict[str, Any]] = []
        self.max_history_size = self.config.get("max_history_size", 100)

        self.lock = threading.RLock()
        self.metric_callbacks: List[Callable] = []
        self.snapshot_callbacks: List[Callable] = []

        self.snapshot_thread: Optional[threading.Thread] = None
        self.snapshot_active = False
        self.is_active = False

        # Start monitoring immediately
        self.start_monitoring()
        logger.info("PerformanceMonitor initialized")

    # ------------------------------------------------------------------
    # Metric collection
    # ------------------------------------------------------------------
    def record_metric(
        self,
        name_or_type: Any,
        value: float,
        agent_id: Optional[str] = None,
        unit: str = "units",
        context: Dict[str, Any] = None,
        tags: List[str] = None,
    ) -> str:
        """Record a performance metric."""

        name = name_or_type.value if isinstance(name_or_type, MetricType) else str(name_or_type)
        metric = MonitorMetric(
            name=name,
            value=value,
            unit=unit,
            agent_id=agent_id,
            context=context or {},
            tags=tags or [],
        )

        with self.lock:
            self.metrics.append(metric)
            if agent_id:
                self.agent_metrics[agent_id].append(metric)

            if len(self.metrics) > self.max_history:
                self.metrics = self.metrics[-self.max_history :]

        self._notify_metric_callbacks(metric)
        return f"{name}_{int(metric.timestamp.timestamp())}"

    def get_metrics(
        self,
        name: Any = None,
        agent_id: Optional[str] = None,
        time_range: Optional[timedelta] = None,
    ) -> List[MonitorMetric]:
        """Retrieve metrics with optional filtering."""

        with self.lock:
            metrics = list(self.metrics)

        if name is not None:
            name_val = name.value if isinstance(name, MetricType) else str(name)
            metrics = [m for m in metrics if m.name == name_val]

        if agent_id is not None:
            metrics = [m for m in metrics if m.agent_id == agent_id]

        if time_range is not None:
            cutoff = datetime.now() - time_range
            metrics = [m for m in metrics if m.timestamp >= cutoff]

        return metrics

    def get_agent_performance_summary(
        self, agent_id: str, time_range: Optional[timedelta] = None
    ) -> Dict[str, Any]:
        """Return summary statistics for a specific agent."""

        with self.lock:
            agent_metrics = list(self.agent_metrics.get(agent_id, []))

        if time_range is not None:
            cutoff = datetime.now() - time_range
            agent_metrics = [m for m in agent_metrics if m.timestamp >= cutoff]

        if not agent_metrics:
            return {}

        metrics_by_name: Dict[str, List[float]] = defaultdict(list)
        for metric in agent_metrics:
            metrics_by_name[metric.name].append(metric.value)

        summary = {}
        for name, values in metrics_by_name.items():
            summary[name] = {
                "count": len(values),
                "min": min(values),
                "max": max(values),
                "avg": sum(values) / len(values),
                "latest": values[-1],
            }
        return summary

    # ------------------------------------------------------------------
    # System metrics history
    # ------------------------------------------------------------------
    def _store_history(self, metrics: Dict[str, Any]):
        """Store system metrics in history for averaging."""
        with self.lock:
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > self.max_history_size:
                self.metrics_history = self.metrics_history[-self.max_history_size :]

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Collect and return current system metrics."""
        metrics = self.get_system_metrics()
        metrics["timestamp"] = time.time()
        self._store_history(metrics)
        return metrics

    def get_metrics_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Return recorded system metrics history."""
        with self.lock:
            history = list(self.metrics_history)
        if limit is not None:
            return history[-limit:]
        return history

    def get_average_metrics(self, time_window_minutes: int = 5) -> Dict[str, Any]:
        """Return average system metrics over a time window."""
        cutoff = time.time() - (time_window_minutes * 60)
        history = [m for m in self.get_metrics_history() if m.get("timestamp", 0) >= cutoff]
        if not history:
            return {}
        avg: Dict[str, float] = {}
        for key in [
            "cpu_percent",
            "memory_percent",
            "memory_used_gb",
            "memory_available_gb",
            "disk_percent",
            "disk_free_gb",
        ]:
            values = [h.get(key, 0) for h in history if key in h]
            if values:
                avg[key] = sum(values) / len(values)
        avg_metrics = {
            "sample_count": len(history),
            "time_window_minutes": time_window_minutes,
            **avg,
        }
        return avg_metrics

    # ------------------------------------------------------------------
    # Profiling
    # ------------------------------------------------------------------
    def start_profile(self, profile_name: str, context: Dict[str, Any] = None) -> str:
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
        return profile_id

    def end_profile(self, profile_id: str) -> Dict[str, Any]:
        if not self.profiling_enabled:
            return {}
        with self.lock:
            profile = self.active_profiles.pop(profile_id, None)
        if not profile:
            return {}

        end_time = time.time()
        end_cpu = psutil.cpu_percent(interval=None)
        end_memory = psutil.Process().memory_info().rss

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

        self.record_metric(
            profile["name"],
            duration,
            unit="seconds",
            context=profile["context"],
            tags=["profile_completion"],
        )
        return results

    @contextmanager
    def profile(self, profile_name: str, context: Dict[str, Any] = None):
        profile_id = self.start_profile(profile_name, context)
        try:
            yield profile_id
        finally:
            self.end_profile(profile_id)

    def profile_function(self, profile_name: str = None):
        def decorator(func):
            name = profile_name or f"{func.__module__}.{func.__name__}"

            @wraps(func)
            def wrapper(*args, **kwargs):
                with self.profile(name, {"function": func.__name__}):
                    return func(*args, **kwargs)

            return wrapper

        return decorator

    def profile_operation(self, operation: str, component: str):
        """Decorator used by cursor capture tests."""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                with self.profile(operation, {"component": component}):
                    return func(*args, **kwargs)

            return wrapper

        return decorator

    def get_profiling_summary(self, time_range: Optional[timedelta] = None) -> Dict[str, Any]:
        metrics = self.get_metrics(time_range=time_range)
        if not metrics:
            return {}

        metrics_by_name: Dict[str, List[float]] = defaultdict(list)
        for metric in metrics:
            metrics_by_name[metric.name].append(metric.value)

        summary = {}
        for name, values in metrics_by_name.items():
            summary[name] = {
                "count": len(values),
                "min": min(values),
                "max": max(values),
                "avg": sum(values) / len(values),
                "latest": values[-1],
            }

        summary["active_profiles"] = len(self.active_profiles)
        summary["total_snapshots"] = len(self.snapshots)
        return summary

    # ------------------------------------------------------------------
    # System metrics & snapshots
    # ------------------------------------------------------------------
    def get_system_metrics(self) -> Dict[str, float]:
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": memory.available / (1024 ** 3),
                "memory_used_gb": memory.used / (1024 ** 3),
                "disk_percent": disk.percent,
                "disk_free_gb": disk.free / (1024 ** 3),
            }
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {}

    def _generate_snapshot(self):
        snapshot = MonitorSnapshot(timestamp=datetime.now())
        snapshot.system_metrics = self.get_system_metrics()

        with self.lock:
            # Aggregate agent metrics
            for agent_id, metrics in self.agent_metrics.items():
                by_type: Dict[str, List[float]] = defaultdict(list)
                for metric in metrics[-100:]:
                    by_type[metric.name].append(metric.value)
                if by_type:
                    snapshot.agent_metrics[agent_id] = {
                        name: sum(vals) / len(vals) for name, vals in by_type.items()
                    }

            # Aggregate global metrics
            by_name: Dict[str, List[float]] = defaultdict(list)
            for metric in self.metrics[-1000:]:
                by_name[metric.name].append(metric.value)
            snapshot.custom_metrics = {
                name: sum(vals) / len(vals) for name, vals in by_name.items()
            }

            self.snapshots.append(snapshot)
            if len(self.snapshots) > 1000:
                self.snapshots = self.snapshots[-1000:]

        self._notify_snapshot_callbacks(snapshot)

    def _snapshot_loop(self):
        while self.snapshot_active:
            try:
                self._generate_snapshot()
                time.sleep(self.snapshot_interval)
            except Exception as e:
                logger.error(f"Error in snapshot generation: {e}")
                time.sleep(10)

    def get_performance_snapshots(self, count: int = 10) -> List[MonitorSnapshot]:
        with self.lock:
            return self.snapshots[-count:]

    # ------------------------------------------------------------------
    # Monitoring control
    # ------------------------------------------------------------------
    def start_monitoring(self):
        if self.is_active:
            return
        self.is_active = True
        self.snapshot_active = True
        self.snapshot_thread = threading.Thread(target=self._snapshot_loop, daemon=True)
        self.snapshot_thread.start()

    def stop_monitoring(self):
        self.is_active = False
        self.snapshot_active = False
        if self.snapshot_thread:
            self.snapshot_thread.join(timeout=5)

    # ------------------------------------------------------------------
    # Callbacks & export
    # ------------------------------------------------------------------
    def add_metric_callback(self, callback: Callable):
        if callback not in self.metric_callbacks:
            self.metric_callbacks.append(callback)

    def add_snapshot_callback(self, callback: Callable):
        if callback not in self.snapshot_callbacks:
            self.snapshot_callbacks.append(callback)

    def _notify_metric_callbacks(self, metric: MonitorMetric):
        for callback in self.metric_callbacks:
            try:
                callback(metric)
            except Exception as e:
                logger.error(f"Error in metric callback: {e}")

    def _notify_snapshot_callbacks(self, snapshot: MonitorSnapshot):
        for callback in self.snapshot_callbacks:
            try:
                callback(snapshot)
            except Exception as e:
                logger.error(f"Error in snapshot callback: {e}")

    def export_metrics(self, filepath: str, time_range: Optional[timedelta] = None):
        with self.lock:
            metrics = list(self.metrics)
            snapshots = list(self.snapshots)

        if time_range is not None:
            cutoff = datetime.now() - time_range
            metrics = [m for m in metrics if m.timestamp >= cutoff]

        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "metrics": [
                {
                    "name": m.name,
                    "value": m.value,
                    "unit": m.unit,
                    "timestamp": m.timestamp.isoformat(),
                    "agent_id": m.agent_id,
                    "context": m.context,
                    "tags": m.tags,
                }
                for m in metrics
            ],
            "snapshots": [
                {
                    "timestamp": s.timestamp.isoformat(),
                    "system_metrics": s.system_metrics,
                    "agent_metrics": s.agent_metrics,
                    "custom_metrics": s.custom_metrics,
                }
                for s in snapshots[-100:]
            ],
        }

        with open(filepath, "w") as f:
            json.dump(export_data, f, indent=2, default=str)

    def export_profiling_data(self, filepath: str, time_range: Optional[timedelta] = None):
        # Reuse export_metrics for compatibility
        self.export_metrics(filepath, time_range)

    def cleanup(self):
        self.stop_monitoring()
        logger.info("PerformanceMonitor cleaned up")


# Backwards compatible aliases
PerformanceTracker = PerformanceMonitor
PerformanceProfiler = PerformanceMonitor
PerformanceMetric = MonitorMetric
PerformanceSnapshot = MonitorSnapshot

__all__ = [
    "PerformanceMonitor",
    "PerformanceTracker",
    "PerformanceProfiler",
    "PerformanceLevel",
    "MetricType",
    "PerformanceMetric",
    "PerformanceSnapshot",
    "AlertSeverity",
    "AlertCondition",
    "PerformanceAlert",
]

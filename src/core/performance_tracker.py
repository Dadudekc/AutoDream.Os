#!/usr/bin/env python3
"""
🔍 Performance Tracker - Agent_Cellphone_V2

Real-time performance metrics collection and tracking system.
Following V2 coding standards: ≤300 LOC, OOP design, SRP.

Author: Performance & Monitoring Specialist
License: MIT
"""

import logging
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import json

# Configure logging
logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Performance metric types"""

    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    NETWORK_LATENCY = "network_latency"
    AGENT_HEALTH = "agent_health"
    TASK_COMPLETION = "task_completion"
    SYSTEM_LOAD = "system_load"


@dataclass
class PerformanceMetric:
    """Individual performance metric data point"""

    metric_type: MetricType
    value: float
    timestamp: datetime
    agent_id: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceSnapshot:
    """Snapshot of performance metrics at a specific time"""

    timestamp: datetime
    metrics: Dict[str, float] = field(default_factory=dict)
    agent_metrics: Dict[str, Dict[str, float]] = field(default_factory=dict)
    system_metrics: Dict[str, float] = field(default_factory=dict)


class PerformanceTracker:
    """
    Performance Tracker - Single responsibility: Real-time performance metrics collection.

    Follows V2 standards: ≤300 LOC, OOP design, SRP.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the performance tracker"""
        self.config = config or {}
        self.metrics: List[PerformanceMetric] = []
        self.snapshots: List[PerformanceSnapshot] = []
        self.agent_metrics: Dict[str, List[PerformanceMetric]] = defaultdict(list)

        # Configuration
        self.max_metrics_history = self.config.get("max_metrics_history", 10000)
        self.snapshot_interval = self.config.get("snapshot_interval", 60)  # seconds
        self.metric_retention_days = self.config.get("metric_retention_days", 30)

        # Threading
        self.lock = threading.RLock()
        self.snapshot_thread: Optional[threading.Thread] = None
        self.snapshot_active = False

        # Callbacks for real-time updates
        self.metric_callbacks: List[Callable] = []
        self.snapshot_callbacks: List[Callable] = []

        # Start snapshot generation
        self._start_snapshot_generation()

        logger.info("PerformanceTracker initialized")

    def record_metric(
        self,
        metric_type: MetricType,
        value: float,
        agent_id: Optional[str] = None,
        context: Dict[str, Any] = None,
        metadata: Dict[str, Any] = None,
    ) -> str:
        """Record a new performance metric"""
        with self.lock:
            metric = PerformanceMetric(
                metric_type=metric_type,
                value=value,
                timestamp=datetime.now(),
                agent_id=agent_id,
                context=context or {},
                metadata=metadata or {},
            )

            # Add to main metrics list
            self.metrics.append(metric)

            # Add to agent-specific metrics if agent_id provided
            if agent_id:
                self.agent_metrics[agent_id].append(metric)

            # Maintain history limits
            self._maintain_history_limits()

            # Notify callbacks
            self._notify_metric_callbacks(metric)

            metric_id = f"{metric_type.value}_{metric.timestamp.timestamp()}"
            logger.debug(f"Recorded metric: {metric_id} = {value}")
            return metric_id

    def get_metrics(
        self,
        metric_type: Optional[MetricType] = None,
        agent_id: Optional[str] = None,
        time_range: Optional[timedelta] = None,
    ) -> List[PerformanceMetric]:
        """Get metrics with optional filtering"""
        with self.lock:
            filtered_metrics = self.metrics

            # Filter by metric type
            if metric_type:
                filtered_metrics = [
                    m for m in filtered_metrics if m.metric_type == metric_type
                ]

            # Filter by agent
            if agent_id:
                filtered_metrics = [
                    m for m in filtered_metrics if m.agent_id == agent_id
                ]

            # Filter by time range
            if time_range:
                cutoff_time = datetime.now() - time_range
                filtered_metrics = [
                    m for m in filtered_metrics if m.timestamp >= cutoff_time
                ]

            return filtered_metrics.copy()

    def get_latest_metric(
        self, metric_type: MetricType, agent_id: Optional[str] = None
    ) -> Optional[PerformanceMetric]:
        """Get the latest metric of a specific type"""
        metrics = self.get_metrics(metric_type, agent_id)
        if metrics:
            return max(metrics, key=lambda m: m.timestamp)
        return None

    def get_metric_summary(
        self,
        metric_type: MetricType,
        agent_id: Optional[str] = None,
        time_range: Optional[timedelta] = None,
    ) -> Dict[str, float]:
        """Get summary statistics for a metric type"""
        metrics = self.get_metrics(metric_type, agent_id, time_range)
        if not metrics:
            return {}

        values = [m.value for m in metrics]
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "latest": values[-1] if values else 0,
        }

    def get_performance_snapshots(self, count: int = 10) -> List[PerformanceSnapshot]:
        """Get recent performance snapshots"""
        with self.lock:
            return self.snapshots[-count:].copy()

    def get_agent_performance_summary(
        self, agent_id: str, time_range: Optional[timedelta] = None
    ) -> Dict[str, Any]:
        """Get comprehensive performance summary for an agent"""
        with self.lock:
            if agent_id not in self.agent_metrics:
                return {}

            agent_metrics = self.agent_metrics[agent_id]
            if time_range:
                cutoff_time = datetime.now() - time_range
                agent_metrics = [m for m in agent_metrics if m.timestamp >= cutoff_time]

            if not agent_metrics:
                return {}

            # Group by metric type
            metrics_by_type = defaultdict(list)
            for metric in agent_metrics:
                metrics_by_type[metric.metric_type.value].append(metric.value)

            # Calculate summaries
            summary = {}
            for metric_type, values in metrics_by_type.items():
                summary[metric_type] = {
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                    "latest": values[-1],
                }

            return summary

    def add_metric_callback(self, callback: Callable):
        """Add callback for metric updates"""
        if callback not in self.metric_callbacks:
            self.metric_callbacks.append(callback)

    def add_snapshot_callback(self, callback: Callable):
        """Add callback for snapshot updates"""
        if callback not in self.snapshot_callbacks:
            self.snapshot_callbacks.append(callback)

    def _start_snapshot_generation(self):
        """Start automatic snapshot generation"""
        self.snapshot_active = True
        self.snapshot_thread = threading.Thread(target=self._snapshot_loop, daemon=True)
        self.snapshot_thread.start()
        logger.info("Snapshot generation started")

    def _snapshot_loop(self):
        """Main snapshot generation loop"""
        while self.snapshot_active:
            try:
                self._generate_snapshot()
                time.sleep(self.snapshot_interval)
            except Exception as e:
                logger.error(f"Error in snapshot generation: {e}")
                time.sleep(10)

    def _generate_snapshot(self):
        """Generate a new performance snapshot"""
        with self.lock:
            snapshot = PerformanceSnapshot(timestamp=datetime.now())

            # Aggregate current metrics by type
            current_metrics = defaultdict(list)
            for metric in self.metrics[-1000:]:  # Last 1000 metrics
                current_metrics[metric.metric_type.value].append(metric.value)

            # Calculate averages for each metric type
            for metric_type, values in current_metrics.items():
                if values:
                    snapshot.metrics[metric_type] = sum(values) / len(values)

            # Aggregate agent metrics
            for agent_id, agent_metrics_list in self.agent_metrics.items():
                if agent_metrics_list:
                    agent_snapshot = {}
                    agent_metrics_by_type = defaultdict(list)
                    for metric in agent_metrics_list[-100:]:  # Last 100 per agent
                        agent_metrics_by_type[metric.metric_type.value].append(
                            metric.value
                        )

                    for metric_type, values in agent_metrics_by_type.items():
                        if values:
                            agent_snapshot[metric_type] = sum(values) / len(values)

                    if agent_snapshot:
                        snapshot.agent_metrics[agent_id] = agent_snapshot

            # Add system-level metrics
            snapshot.system_metrics = {
                "total_metrics": len(self.metrics),
                "total_agents": len(self.agent_metrics),
                "snapshot_count": len(self.snapshots),
            }

            self.snapshots.append(snapshot)

            # Maintain snapshot history
            if len(self.snapshots) > 1000:  # Keep last 1000 snapshots
                self.snapshots = self.snapshots[-1000:]

            # Notify callbacks
            self._notify_snapshot_callbacks(snapshot)

            logger.debug(f"Generated snapshot at {snapshot.timestamp}")

    def _maintain_history_limits(self):
        """Maintain metric history limits"""
        # Remove old metrics
        if len(self.metrics) > self.max_metrics_history:
            cutoff_time = datetime.now() - timedelta(days=self.metric_retention_days)
            self.metrics = [m for m in self.metrics if m.timestamp >= cutoff_time]

        # Clean up old agent metrics
        for agent_id in list(self.agent_metrics.keys()):
            if len(self.agent_metrics[agent_id]) > self.max_metrics_history:
                cutoff_time = datetime.now() - timedelta(
                    days=self.metric_retention_days
                )
                self.agent_metrics[agent_id] = [
                    m
                    for m in self.agent_metrics[agent_id]
                    if m.timestamp >= cutoff_time
                ]

    def _notify_metric_callbacks(self, metric: PerformanceMetric):
        """Notify metric update callbacks"""
        for callback in self.metric_callbacks:
            try:
                callback(metric)
            except Exception as e:
                logger.error(f"Error in metric callback: {e}")

    def _notify_snapshot_callbacks(self, snapshot: PerformanceSnapshot):
        """Notify snapshot update callbacks"""
        for callback in self.snapshot_callbacks:
            try:
                callback(snapshot)
            except Exception as e:
                logger.error(f"Error in snapshot callback: {e}")

    def export_metrics(self, filepath: str, time_range: Optional[timedelta] = None):
        """Export metrics to JSON file"""
        with self.lock:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "metrics": [],
                "snapshots": [],
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
                        "type": metric.metric_type.value,
                        "value": metric.value,
                        "timestamp": metric.timestamp.isoformat(),
                        "agent_id": metric.agent_id,
                        "context": metric.context,
                        "metadata": metric.metadata,
                    }
                )

            # Export snapshots
            for snapshot in self.snapshots[-100:]:  # Last 100 snapshots
                export_data["snapshots"].append(
                    {
                        "timestamp": snapshot.timestamp.isoformat(),
                        "metrics": snapshot.metrics,
                        "agent_metrics": snapshot.agent_metrics,
                        "system_metrics": snapshot.system_metrics,
                    }
                )

            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(f"Exported {len(export_data['metrics'])} metrics to {filepath}")

    def cleanup(self):
        """Cleanup resources"""
        self.snapshot_active = False
        if self.snapshot_thread:
            self.snapshot_thread.join(timeout=5)
        logger.info("PerformanceTracker cleaned up")

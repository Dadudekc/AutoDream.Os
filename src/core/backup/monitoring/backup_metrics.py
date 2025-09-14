#!/usr/bin/env python3
"""
Backup Metrics - V2 Compliant
=============================

Focused module for backup metrics collection and analysis.
V2 COMPLIANT: Under 300 lines, single responsibility.

Author: Agent-3 (Infrastructure Specialist)
License: MIT
"""

from __future__ import annotations

import logging
import statistics
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of backup metrics."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


@dataclass
class BackupMetric:
    """Backup metric data structure."""
    name: str
    value: float
    metric_type: MetricType
    timestamp: datetime
    labels: Dict[str, str] = None
    description: str = ""
    
    def __post_init__(self):
        if self.labels is None:
            self.labels = {}


@dataclass
class MetricSummary:
    """Summary statistics for a metric."""
    name: str
    count: int
    min_value: float
    max_value: float
    mean_value: float
    median_value: float
    std_dev: float
    time_range: timedelta


class BackupMetricsCollector:
    """Collects and analyzes backup metrics."""
    
    def __init__(self, retention_hours: int = 24):
        self.retention_hours = retention_hours
        self.metrics: List[BackupMetric] = []
        self.logger = logging.getLogger(__name__)
    
    def record_metric(self, name: str, value: float, metric_type: MetricType,
                     labels: Dict[str, str] = None, description: str = "") -> None:
        """Record a new metric."""
        metric = BackupMetric(
            name=name,
            value=value,
            metric_type=metric_type,
            timestamp=datetime.now(),
            labels=labels or {},
            description=description
        )
        
        self.metrics.append(metric)
        self._cleanup_old_metrics()
    
    def _cleanup_old_metrics(self) -> None:
        """Remove metrics older than retention period."""
        cutoff_time = datetime.now() - timedelta(hours=self.retention_hours)
        self.metrics = [m for m in self.metrics if m.timestamp > cutoff_time]
    
    def get_metric_summary(self, metric_name: str, 
                          labels_filter: Dict[str, str] = None,
                          time_window_minutes: int = 60) -> Optional[MetricSummary]:
        """Get summary statistics for a metric."""
        filtered_metrics = self._filter_metrics(metric_name, labels_filter, time_window_minutes)
        
        if not filtered_metrics:
            return None
        
        values = [m.value for m in filtered_metrics]
        
        return MetricSummary(
            name=metric_name,
            count=len(values),
            min_value=min(values),
            max_value=max(values),
            mean_value=statistics.mean(values),
            median_value=statistics.median(values),
            std_dev=statistics.stdev(values) if len(values) > 1 else 0.0,
            time_range=filtered_metrics[-1].timestamp - filtered_metrics[0].timestamp
        )
    
    def _filter_metrics(self, metric_name: str, labels_filter: Dict[str, str] = None,
                       time_window_minutes: int = 60) -> List[BackupMetric]:
        """Filter metrics by name, labels, and time window."""
        cutoff_time = datetime.now() - timedelta(minutes=time_window_minutes)
        
        filtered = []
        for metric in self.metrics:
            if metric.name != metric_name:
                continue
            
            if metric.timestamp < cutoff_time:
                continue
            
            # Check labels filter
            if labels_filter:
                if not all(metric.labels.get(k) == v for k, v in labels_filter.items()):
                    continue
            
            filtered.append(metric)
        
        return filtered
    
    def get_backup_health_score(self, backup_id: str, time_window_minutes: int = 60) -> float:
        """Calculate health score for a backup (0-100)."""
        # Get metrics for this backup
        backup_metrics = self._filter_metrics("backup_health", {"backup_id": backup_id}, time_window_minutes)
        
        if not backup_metrics:
            return 50.0  # Neutral score if no data
        
        # Calculate score based on various factors
        score = 100.0
        
        # Check for failures
        failure_metrics = self._filter_metrics("backup_failed", {"backup_id": backup_id}, time_window_minutes)
        if failure_metrics:
            score -= len(failure_metrics) * 20  # -20 points per failure
        
        # Check for size changes (potential corruption)
        size_metrics = self._filter_metrics("backup_size_bytes", {"backup_id": backup_id}, time_window_minutes)
        if len(size_metrics) > 1:
            sizes = [m.value for m in size_metrics]
            if max(sizes) - min(sizes) > min(sizes) * 0.1:  # >10% size change
                score -= 15
        
        # Check for age (stale backups)
        age_metrics = self._filter_metrics("backup_age_hours", {"backup_id": backup_id}, time_window_minutes)
        if age_metrics:
            max_age = max(m.value for m in age_metrics)
            if max_age > 168:  # >7 days
                score -= 25
        
        return max(0.0, min(100.0, score))
    
    def get_system_health_summary(self, time_window_minutes: int = 60) -> Dict[str, Any]:
        """Get overall system health summary."""
        cutoff_time = datetime.now() - timedelta(minutes=time_window_minutes)
        recent_metrics = [m for m in self.metrics if m.timestamp > cutoff_time]
        
        # Count by metric type
        type_counts = {}
        for metric in recent_metrics:
            type_counts[metric.metric_type.value] = type_counts.get(metric.metric_type.value, 0) + 1
        
        # Count by metric name
        name_counts = {}
        for metric in recent_metrics:
            name_counts[metric.name] = name_counts.get(metric.name, 0) + 1
        
        # Calculate overall health
        total_failures = sum(m.value for m in recent_metrics if m.name == "backup_failed")
        total_successes = sum(m.value for m in recent_metrics if m.name == "backup_success")
        
        health_score = 100.0
        if total_failures + total_successes > 0:
            failure_rate = total_failures / (total_failures + total_successes)
            health_score = (1.0 - failure_rate) * 100.0
        
        return {
            "time_window_minutes": time_window_minutes,
            "total_metrics": len(recent_metrics),
            "metric_types": type_counts,
            "metric_names": name_counts,
            "total_failures": total_failures,
            "total_successes": total_successes,
            "health_score": round(health_score, 2),
            "retention_hours": self.retention_hours,
            "oldest_metric": min((m.timestamp for m in recent_metrics), default=None),
            "newest_metric": max((m.timestamp for m in recent_metrics), default=None)
        }
    
    def get_top_metrics(self, metric_name: str, limit: int = 10,
                       time_window_minutes: int = 60) -> List[Dict[str, Any]]:
        """Get top metrics by value."""
        filtered_metrics = self._filter_metrics(metric_name, time_window_minutes=time_window_minutes)
        
        # Sort by value (descending)
        sorted_metrics = sorted(filtered_metrics, key=lambda m: m.value, reverse=True)
        
        return [
            {
                "value": metric.value,
                "timestamp": metric.timestamp.isoformat(),
                "labels": metric.labels,
                "description": metric.description
            }
            for metric in sorted_metrics[:limit]
        ]
    
    def export_metrics(self, format_type: str = "json", 
                      time_window_minutes: int = 60) -> str:
        """Export metrics in specified format."""
        cutoff_time = datetime.now() - timedelta(minutes=time_window_minutes)
        recent_metrics = [m for m in self.metrics if m.timestamp > cutoff_time]
        
        if format_type.lower() == "json":
            import json
            return json.dumps([
                {
                    "name": m.name,
                    "value": m.value,
                    "type": m.metric_type.value,
                    "timestamp": m.timestamp.isoformat(),
                    "labels": m.labels,
                    "description": m.description
                }
                for m in recent_metrics
            ], indent=2)
        
        elif format_type.lower() == "csv":
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow(["name", "value", "type", "timestamp", "labels", "description"])
            
            # Write data
            for metric in recent_metrics:
                writer.writerow([
                    metric.name,
                    metric.value,
                    metric.metric_type.value,
                    metric.timestamp.isoformat(),
                    str(metric.labels),
                    metric.description
                ])
            
            return output.getvalue()
        
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def clear_metrics(self) -> None:
        """Clear all metrics."""
        self.metrics.clear()
        self.logger.info("Cleared all metrics")


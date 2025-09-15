#!/usr/bin/env python3
"""
Infrastructure Performance Metrics

This module provides performance metrics collection and monitoring for infrastructure components.
"""

from __future__ import annotations

import logging
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

try:
    from ...core.health.monitoring.health_monitoring_service import HealthMetric
except ImportError:
    from dataclasses import dataclass, field
    from datetime import datetime
    
    @dataclass
    class HealthMetric:
        name: str
        value: Any
        unit: str = ""
        timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class PerformanceMetrics:
    """Performance metrics data structure."""
    response_times: List[float] = field(default_factory=list)
    error_counts: Dict[str, int] = field(default_factory=dict)
    cache_hit_rates: Dict[str, float] = field(default_factory=dict)
    resource_usage: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class PerformanceMetricsCollector:
    """
    Performance metrics collector for infrastructure monitoring.
    
    Collects and tracks performance metrics including response times,
    error rates, cache performance, and resource usage.
    """
    
    def __init__(self, max_history: int = 1000):
        """Initialize performance metrics collector."""
        self.logger = logging.getLogger(__name__)
        self.max_history = max_history
        
        # Response time tracking
        self.response_times = deque(maxlen=max_history)
        self.operation_times = defaultdict(lambda: deque(maxlen=100))
        
        # Error tracking
        self.error_counts = defaultdict(int)
        self.error_history = deque(maxlen=max_history)
        
        # Cache performance tracking
        self.cache_stats = defaultdict(lambda: {"hits": 0, "misses": 0})
        
        # Resource usage tracking
        self.resource_usage = defaultdict(lambda: deque(maxlen=100))
        
    def record_response_time(self, operation: str, response_time: float) -> None:
        """Record response time for an operation."""
        self.response_times.append(response_time)
        self.operation_times[operation].append(response_time)
        
    def record_error(self, operation: str, error_type: str) -> None:
        """Record an error occurrence."""
        self.error_counts[f"{operation}:{error_type}"] += 1
        self.error_history.append({
            "operation": operation,
            "error_type": error_type,
            "timestamp": datetime.now()
        })
        
    def record_cache_hit(self, cache_name: str) -> None:
        """Record a cache hit."""
        self.cache_stats[cache_name]["hits"] += 1
        
    def record_cache_miss(self, cache_name: str) -> None:
        """Record a cache miss."""
        self.cache_stats[cache_name]["misses"] += 1
        
    def record_resource_usage(self, resource: str, usage: float) -> None:
        """Record resource usage."""
        self.resource_usage[resource].append(usage)
        
    def get_average_response_time(self, operation: Optional[str] = None) -> float:
        """Get average response time for operation or overall."""
        if operation:
            times = self.operation_times[operation]
            return sum(times) / len(times) if times else 0.0
        else:
            return sum(self.response_times) / len(self.response_times) if self.response_times else 0.0
            
    def get_error_rate(self, operation: Optional[str] = None) -> float:
        """Get error rate for operation or overall."""
        if operation:
            total_operations = len(self.operation_times[operation])
            errors = sum(count for key, count in self.error_counts.items() if key.startswith(f"{operation}:"))
            return (errors / total_operations * 100) if total_operations > 0 else 0.0
        else:
            total_operations = len(self.response_times)
            total_errors = sum(self.error_counts.values())
            return (total_errors / total_operations * 100) if total_operations > 0 else 0.0
            
    def get_cache_hit_rate(self, cache_name: str) -> float:
        """Get cache hit rate for a specific cache."""
        stats = self.cache_stats[cache_name]
        total_requests = stats["hits"] + stats["misses"]
        return (stats["hits"] / total_requests * 100) if total_requests > 0 else 0.0
        
    def get_resource_usage_stats(self, resource: str) -> Dict[str, float]:
        """Get resource usage statistics."""
        usage_data = self.resource_usage[resource]
        if not usage_data:
            return {"current": 0.0, "average": 0.0, "max": 0.0, "min": 0.0}
            
        return {
            "current": usage_data[-1] if usage_data else 0.0,
            "average": sum(usage_data) / len(usage_data),
            "max": max(usage_data),
            "min": min(usage_data)
        }
        
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        return {
            "response_times": {
                "average": self.get_average_response_time(),
                "count": len(self.response_times),
                "operations": {
                    op: {
                        "average": self.get_average_response_time(op),
                        "count": len(times)
                    }
                    for op, times in self.operation_times.items()
                }
            },
            "error_rates": {
                "overall": self.get_error_rate(),
                "by_operation": {
                    op: self.get_error_rate(op)
                    for op in self.operation_times.keys()
                },
                "total_errors": sum(self.error_counts.values())
            },
            "cache_performance": {
                cache: {
                    "hit_rate": self.get_cache_hit_rate(cache),
                    "hits": stats["hits"],
                    "misses": stats["misses"]
                }
                for cache, stats in self.cache_stats.items()
            },
            "resource_usage": {
                resource: self.get_resource_usage_stats(resource)
                for resource in self.resource_usage.keys()
            },
            "timestamp": datetime.now().isoformat()
        }
        
    def get_health_metrics(self) -> List[HealthMetric]:
        """Get performance metrics as health metrics."""
        metrics = []
        
        # Response time metrics
        avg_response_time = self.get_average_response_time()
        if avg_response_time > 0:
            metrics.append(HealthMetric(
                name="average_response_time",
                value=round(avg_response_time, 2),
                unit="ms"
            ))
            
        # Error rate metrics
        error_rate = self.get_error_rate()
        if error_rate >= 0:
            metrics.append(HealthMetric(
                name="error_rate",
                value=round(error_rate, 2),
                unit="%"
            ))
            
        # Cache performance metrics
        for cache_name in self.cache_stats.keys():
            hit_rate = self.get_cache_hit_rate(cache_name)
            metrics.append(HealthMetric(
                name=f"cache_hit_rate_{cache_name}",
                value=round(hit_rate, 2),
                unit="%"
            ))
            
        # Resource usage metrics
        for resource in self.resource_usage.keys():
            stats = self.get_resource_usage_stats(resource)
            metrics.append(HealthMetric(
                name=f"resource_usage_{resource}",
                value=round(stats["current"], 2),
                unit="%"
            ))
            
        return metrics
        
    def reset_metrics(self) -> None:
        """Reset all performance metrics."""
        self.response_times.clear()
        self.operation_times.clear()
        self.error_counts.clear()
        self.error_history.clear()
        self.cache_stats.clear()
        self.resource_usage.clear()
        self.logger.info("Performance metrics reset")

"""
Unified Metric Manager - DUP-014 Consolidation
==============================================

Consolidates duplicate metric management from:
- src/core/managers/monitoring/metric_manager.py
- src/core/performance/unified_dashboard/metric_manager.py

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Integration & Core Systems Specialist
Mission: DUP-014 Metric/Widget Managers Consolidation
License: MIT
"""

import logging
import threading
from collections.abc import Callable
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


class MetricType(Enum):
    """Metric types for monitoring."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


@dataclass
class PerformanceMetric:
    """Performance metric data structure."""
    metric_id: str
    metric_type: MetricType
    current_value: Any
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class UnifiedMetricManager:
    """
    Unified metric management.
    
    Consolidates functionality from monitoring and unified_dashboard metric managers.
    Provides metric recording, history tracking, and callback support.
    """
    
    def __init__(self, max_history_size: int = 1000):
        """
        Initialize unified metric manager.
        
        Args:
            max_history_size: Maximum number of history entries per metric
        """
        self.logger = logging.getLogger(__name__)
        self.metrics: Dict[str, PerformanceMetric] = {}
        self.metric_callbacks: Dict[str, Callable] = {}
        self.metric_history: Dict[str, List[Dict[str, Any]]] = {}
        self._metric_lock = threading.Lock()
        self.max_history_size = max_history_size
    
    def record_metric(self, metric_name: str, metric_value: Any, metric_type: MetricType = MetricType.GAUGE) -> bool:
        """
        Record a metric value.
        
        Args:
            metric_name: Name of the metric
            metric_value: Value to record
            metric_type: Type of metric
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self._metric_lock:
                if metric_name not in self.metrics:
                    # Create new metric
                    self.metrics[metric_name] = PerformanceMetric(
                        metric_id=metric_name,
                        metric_type=metric_type,
                        current_value=metric_value,
                        count=1
                    )
                    self.metric_history[metric_name] = []
                else:
                    # Update existing metric
                    metric = self.metrics[metric_name]
                    metric.current_value = metric_value
                    metric.updated_at = datetime.now()
                    metric.count += 1
                
                # Add to history
                history_entry = {
                    "value": metric_value,
                    "timestamp": datetime.now().isoformat(),
                }
                self.metric_history[metric_name].append(history_entry)
                
                # Trim history if needed
                if len(self.metric_history[metric_name]) > self.max_history_size:
                    self.metric_history[metric_name] = self.metric_history[metric_name][-self.max_history_size:]
                
                # Call callbacks
                for callback in self.metric_callbacks.values():
                    try:
                        callback(metric_name, metric_value)
                    except Exception as e:
                        self.logger.error(f"Metric callback error: {e}")
                
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to record metric {metric_name}: {e}")
            return False
    
    def get_metric(self, metric_id: str) -> Optional[PerformanceMetric]:
        """Get metric by ID."""
        return self.metrics.get(metric_id)
    
    def get_metrics_by_type(self, metric_type: MetricType) -> List[PerformanceMetric]:
        """Get all metrics of a specific type."""
        return [m for m in self.metrics.values() if m.metric_type == metric_type]
    
    def update_metric(self, metric_id: str, updates: Dict[str, Any]) -> bool:
        """Update metric properties."""
        try:
            if metric_id not in self.metrics:
                self.logger.error(f"Metric not found: {metric_id}")
                return False
            
            metric = self.metrics[metric_id]
            for key, value in updates.items():
                if hasattr(metric, key):
                    setattr(metric, key, value)
            
            metric.updated_at = datetime.now()
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update metric: {e}")
            return False
    
    def remove_metric(self, metric_id: str) -> bool:
        """Remove a metric."""
        try:
            with self._metric_lock:
                if metric_id in self.metrics:
                    del self.metrics[metric_id]
                    if metric_id in self.metric_history:
                        del self.metric_history[metric_id]
                    self.logger.info(f"Removed metric: {metric_id}")
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove metric: {e}")
            return False
    
    def register_callback(self, callback_id: str, callback: Callable) -> bool:
        """Register a metric callback."""
        try:
            self.metric_callbacks[callback_id] = callback
            return True
        except Exception as e:
            self.logger.error(f"Failed to register callback: {e}")
            return False
    
    def get_metric_history(self, metric_name: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get metric history."""
        history = self.metric_history.get(metric_name, [])
        if limit:
            return history[-limit:]
        return history
    
    def get_all_metrics(self) -> List[PerformanceMetric]:
        """Get all metrics."""
        return list(self.metrics.values())
    
    def clear_metrics(self) -> None:
        """Clear all metrics and history."""
        with self._metric_lock:
            self.metrics.clear()
            self.metric_history.clear()
            self.logger.info("All metrics cleared")


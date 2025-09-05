"""
Performance Monitor - V2 Compliant Module
========================================

Handles performance monitoring and metrics collection.
Extracted from enhanced_integration_orchestrator.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import time
import threading
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import logging

from ..integration_models import (
    IntegrationPerformanceMetrics, IntegrationPerformanceReport,
    create_performance_metrics, create_performance_report
)


class PerformanceMonitor:
    """
    Monitor for integration performance metrics and reporting.
    
    Handles real-time monitoring, metrics collection, and performance analysis.
    """
    
    def __init__(self, config):
        """Initialize performance monitor."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Monitoring state
        self.is_monitoring = False
        self.monitoring_thread: Optional[threading.Thread] = None
        
        # Metrics
        self.metrics = create_performance_metrics()
        self.metrics_history: List[IntegrationPerformanceMetrics] = []
        self.current_report: Optional[IntegrationPerformanceReport] = None
        
        # Performance tracking
        self.operations_count = 0
        self.last_reset_time = datetime.now()
    
    def start_monitoring(self):
        """Start performance monitoring thread."""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        self.logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring."""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5.0)
        self.logger.info("Performance monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.is_monitoring:
            try:
                # Capture current metrics
                current_metrics = self._capture_current_metrics()
                
                # Store in history
                self.metrics_history.append(current_metrics)
                
                # Trim history if needed
                if len(self.metrics_history) > self.config.metric_history_size:
                    self.metrics_history = self.metrics_history[-self.config.metric_history_size//2:]
                
                # Reset operations counter for next interval
                self.operations_count = 0
                
                time.sleep(self.config.performance_check_interval)
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5.0)
    
    def _capture_current_metrics(self) -> IntegrationPerformanceMetrics:
        """Capture current performance metrics."""
        current_metrics = create_performance_metrics()
        current_metrics.timestamp = datetime.now()
        current_metrics.operations_per_second = self._calculate_operations_per_second()
        current_metrics.average_latency_ms = self.metrics.average_latency_ms
        current_metrics.success_rate = self.metrics.success_rate
        current_metrics.error_rate = self.metrics.error_rate
        current_metrics.efficiency_score = self._calculate_efficiency_score()
        current_metrics.resource_utilization = self.metrics.resource_utilization.copy()
        current_metrics.active_integrations = self.metrics.active_integrations
        current_metrics.queue_size = self.metrics.queue_size
        
        return current_metrics
    
    def _calculate_operations_per_second(self) -> float:
        """Calculate operations per second."""
        now = datetime.now()
        time_diff = (now - self.last_reset_time).total_seconds()
        
        if time_diff == 0:
            return 0.0
        
        ops_per_sec = self.operations_count / time_diff
        self.last_reset_time = now
        return ops_per_sec
    
    def _calculate_efficiency_score(self) -> float:
        """Calculate overall efficiency score."""
        if self.metrics.average_latency_ms == 0:
            return 1.0
        
        # Simple efficiency calculation
        latency_score = max(0, 1 - (self.metrics.average_latency_ms / self.config.max_latency_ms))
        throughput_score = min(1, self.metrics.operations_per_second / self.config.min_throughput_ops_sec)
        
        return (latency_score + throughput_score + self.metrics.success_rate) / 3.0
    
    def record_operation(self, success: bool = True, latency_ms: float = 0.0):
        """Record a single operation."""
        self.operations_count += 1
        
        # Update success rate
        if success:
            self.metrics.successful_operations += 1
        else:
            self.metrics.failed_operations += 1
        
        # Update latency
        if latency_ms > 0:
            self._update_average_latency(latency_ms)
        
        # Update success rate
        total_operations = self.metrics.successful_operations + self.metrics.failed_operations
        if total_operations > 0:
            self.metrics.success_rate = (self.metrics.successful_operations / total_operations) * 100
            self.metrics.error_rate = (self.metrics.failed_operations / total_operations) * 100
    
    def _update_average_latency(self, latency_ms: float):
        """Update average latency using exponential moving average."""
        if self.metrics.average_latency_ms == 0:
            self.metrics.average_latency_ms = latency_ms
        else:
            alpha = 0.1  # Smoothing factor
            self.metrics.average_latency_ms = (
                alpha * latency_ms + (1 - alpha) * self.metrics.average_latency_ms
            )
    
    def update_queue_size(self, size: int):
        """Update current queue size."""
        self.metrics.queue_size = size
    
    def update_active_integrations(self, count: int):
        """Update active integrations count."""
        self.metrics.active_integrations = count
    
    def update_resource_utilization(self, resource_type: str, utilization: float):
        """Update resource utilization for specific type."""
        self.metrics.resource_utilization[resource_type] = utilization
    
    def get_current_metrics(self) -> IntegrationPerformanceMetrics:
        """Get current performance metrics."""
        return self.metrics
    
    def get_metrics_history(self) -> List[IntegrationPerformanceMetrics]:
        """Get metrics history."""
        return self.metrics_history.copy()
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        return {
            "current_metrics": self.metrics.to_dict(),
            "history_size": len(self.metrics_history),
            "monitoring_active": self.is_monitoring,
            "efficiency_score": self._calculate_efficiency_score()
        }
    
    def create_performance_report(self, report_id: str) -> IntegrationPerformanceReport:
        """Create new performance report."""
        self.current_report = create_performance_report(report_id)
        return self.current_report
    
    def finalize_performance_report(self):
        """Finalize current performance report."""
        if self.current_report:
            self.current_report.end_time = datetime.now()
            self.current_report.final_metrics = self.metrics
            self.logger.info(f"Performance report finalized: {self.current_report.report_id}")
    
    def get_performance_trends(self, hours: int = 1) -> Dict[str, Any]:
        """Get performance trends over specified hours."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_metrics = [
            m for m in self.metrics_history 
            if m.timestamp >= cutoff_time
        ]
        
        if not recent_metrics:
            return {"trend": "no_data", "message": "No recent metrics available"}
        
        # Calculate trends
        ops_trend = self._calculate_trend([m.operations_per_second for m in recent_metrics])
        latency_trend = self._calculate_trend([m.average_latency_ms for m in recent_metrics])
        success_trend = self._calculate_trend([m.success_rate for m in recent_metrics])
        
        return {
            "trend": "stable",
            "operations_per_second": ops_trend,
            "latency_ms": latency_trend,
            "success_rate": success_trend,
            "data_points": len(recent_metrics)
        }
    
    def _calculate_trend(self, values: List[float]) -> Dict[str, float]:
        """Calculate trend for a list of values."""
        if len(values) < 2:
            return {"current": values[0] if values else 0, "change": 0}
        
        current = values[-1]
        previous = values[0]
        change = ((current - previous) / previous * 100) if previous != 0 else 0
        
        return {
            "current": current,
            "change": change,
            "trend": "increasing" if change > 5 else "decreasing" if change < -5 else "stable"
        }
    
    def reset_metrics(self):
        """Reset all performance metrics."""
        self.metrics = create_performance_metrics()
        self.operations_count = 0
        self.last_reset_time = datetime.now()
        self.logger.info("Performance metrics reset")

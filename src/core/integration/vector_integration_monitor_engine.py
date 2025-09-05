#!/usr/bin/env python3
"""
Vector Integration Monitor Engine - V2 Compliant
================================================

Core engine for vector integration monitoring operations.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactoring)
Created: 2025-01-27
Purpose: Modular engine for vector integration monitoring
"""

import time
import threading
import logging
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from collections import deque
from .vector_integration_models import PerformanceAlert, PerformanceMetrics, IntegrationConfig, AlertLevel


class VectorIntegrationMonitorEngine:
    """Core engine for vector integration monitoring operations."""
    
    def __init__(self, config: Optional[IntegrationConfig] = None):
        """Initialize the vector integration monitor engine."""
        self.config = config or IntegrationConfig()
        self.logger = logging.getLogger(__name__)
        self.metrics_history: deque = deque(maxlen=1000)
        self.alerts: List[PerformanceAlert] = []
        self.monitoring_active = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.alert_callbacks: List[Callable] = []
    
    def start_monitoring(self) -> None:
        """Start the monitoring process."""
        if self.monitoring_active:
            self.logger.warning("Monitoring already active")
            return
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Vector integration monitoring started")
    
    def stop_monitoring(self) -> None:
        """Stop the monitoring process."""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        self.logger.info("Vector integration monitoring stopped")
    
    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring_active:
            try:
                # Collect metrics
                metrics = self._collect_metrics()
                self.metrics_history.append(metrics)
                
                # Check for alerts
                self._check_alerts(metrics)
                
                # Sleep between monitoring cycles
                time.sleep(self.config.monitoring_interval)
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(1.0)
    
    def _collect_metrics(self) -> PerformanceMetrics:
        """Collect current performance metrics."""
        return PerformanceMetrics(
            timestamp=datetime.now(),
            response_time=0.1,  # Simulated
            throughput=100,     # Simulated
            error_rate=0.01,    # Simulated
            memory_usage=50.0   # Simulated
        )
    
    def _check_alerts(self, metrics: PerformanceMetrics) -> None:
        """Check metrics against alert thresholds."""
        # Check response time threshold
        if metrics.response_time > self.config.response_time_threshold:
            alert = PerformanceAlert(
                level=AlertLevel.WARNING,
                message=f"High response time: {metrics.response_time}s",
                timestamp=datetime.now(),
                metric_name="response_time",
                metric_value=metrics.response_time
            )
            self._trigger_alert(alert)
        
        # Check error rate threshold
        if metrics.error_rate > self.config.error_rate_threshold:
            alert = PerformanceAlert(
                level=AlertLevel.ERROR,
                message=f"High error rate: {metrics.error_rate}",
                timestamp=datetime.now(),
                metric_name="error_rate",
                metric_value=metrics.error_rate
            )
            self._trigger_alert(alert)
    
    def _trigger_alert(self, alert: PerformanceAlert) -> None:
        """Trigger an alert and notify callbacks."""
        self.alerts.append(alert)
        self.logger.warning(f"Alert triggered: {alert.message}")
        
        # Notify callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                self.logger.error(f"Error in alert callback: {e}")
    
    def add_alert_callback(self, callback: Callable) -> None:
        """Add an alert callback function."""
        self.alert_callbacks.append(callback)
    
    def get_recent_metrics(self, count: int = 10) -> List[PerformanceMetrics]:
        """Get recent performance metrics."""
        return list(self.metrics_history)[-count:]
    
    def get_active_alerts(self) -> List[PerformanceAlert]:
        """Get active alerts."""
        return [alert for alert in self.alerts if alert.is_active()]
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status."""
        return {
            "monitoring_active": self.monitoring_active,
            "metrics_collected": len(self.metrics_history),
            "active_alerts": len(self.get_active_alerts()),
            "total_alerts": len(self.alerts)
        }

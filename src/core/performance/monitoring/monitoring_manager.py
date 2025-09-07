#!/usr/bin/env python3
"""
Performance Monitoring Manager - V2 Modular Architecture
=======================================================

Handles all performance monitoring operations.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import time
import random
from typing import Dict, List, Optional, Any
from datetime import datetime

from .monitoring_types import MetricData, MetricType, MonitoringConfig, CollectionResult


logger = logging.getLogger(__name__)


class MonitoringManager:
    """
    Monitoring Manager - Single responsibility: Manage performance monitoring
    
    Handles all monitoring operations including:
    - Metrics collection and storage
    - Health status monitoring
    - Alert management
    - Performance tracking
    """

    def __init__(self):
        """Initialize monitoring manager"""
        self.logger = logging.getLogger(f"{__name__}.MonitoringManager")
        
        # Metrics storage
        self.metrics_history: List[MetricData] = []
        self.current_metrics: Dict[str, Any] = {}
        
        # Alerts
        self.alerts: List[str] = []
        self.max_alerts = 1000
        
        # Health tracking
        self.health_status = "healthy"
        self.last_health_check = datetime.now()
        self.health_check_interval = 60  # seconds
        
        # Collection statistics
        self.total_collections = 0
        self.successful_collections = 0
        self.failed_collections = 0
        
        self.logger.info("✅ Monitoring Manager initialized successfully")

    def collect_system_metrics(self) -> Dict[str, Any]:
        """Collect current system performance metrics"""
        try:
            self.total_collections += 1
            
            # Collect various system metrics
            metrics = {}
            
            # CPU metrics
            metrics["cpu_usage_percent"] = self._collect_cpu_metrics()
            metrics["cpu_temperature_celsius"] = self._collect_cpu_temperature()
            
            # Memory metrics
            metrics["memory_usage_percent"] = self._collect_memory_metrics()
            metrics["memory_available_mb"] = self._collect_memory_available()
            
            # Disk metrics
            metrics["disk_usage_percent"] = self._collect_disk_metrics()
            metrics["disk_io_mbps"] = self._collect_disk_io()
            
            # Network metrics
            metrics["network_bandwidth_mbps"] = self._collect_network_metrics()
            metrics["network_latency_ms"] = self._collect_network_latency()
            
            # Application metrics
            metrics["active_connections"] = self._collect_connection_metrics()
            metrics["response_time_ms"] = self._collect_response_time()
            
            # Store current metrics
            self.current_metrics = metrics.copy()
            
            # Add to history
            for metric_name, value in metrics.items():
                metric_data = MetricData(
                    name=metric_name,
                    value=value,
                    timestamp=datetime.now().isoformat(),
                    type=MetricType.SYSTEM,
                    status="active"
                )
                self.metrics_history.append(metric_data)
            
            # Limit history size
            if len(self.metrics_history) > 10000:
                self.metrics_history = self.metrics_history[-5000:]
            
            self.successful_collections += 1
            self.logger.debug(f"✅ Collected {len(metrics)} system metrics")
            
            return metrics
            
        except Exception as e:
            self.failed_collections += 1
            self.logger.error(f"Failed to collect system metrics: {e}")
            return {}

    def _collect_cpu_metrics(self) -> float:
        """Collect CPU usage metrics"""
        try:
            # Simulate CPU usage collection
            return random.uniform(20.0, 85.0)
        except Exception as e:
            self.logger.error(f"Failed to collect CPU metrics: {e}")
            return 0.0

    def _collect_cpu_temperature(self) -> float:
        """Collect CPU temperature metrics"""
        try:
            # Simulate CPU temperature collection
            return random.uniform(45.0, 75.0)
        except Exception as e:
            self.logger.error(f"Failed to collect CPU temperature: {e}")
            return 0.0

    def _collect_memory_metrics(self) -> float:
        """Collect memory usage metrics"""
        try:
            # Simulate memory usage collection
            return random.uniform(30.0, 80.0)
        except Exception as e:
            self.logger.error(f"Failed to collect memory metrics: {e}")
            return 0.0

    def _collect_memory_available(self) -> float:
        """Collect available memory metrics"""
        try:
            # Simulate available memory collection
            return random.uniform(1024.0, 8192.0)
        except Exception as e:
            self.logger.error(f"Failed to collect available memory: {e}")
            return 0.0

    def _collect_disk_metrics(self) -> float:
        """Collect disk usage metrics"""
        try:
            # Simulate disk usage collection
            return random.uniform(40.0, 90.0)
        except Exception as e:
            self.logger.error(f"Failed to collect disk metrics: {e}")
            return 0.0

    def _collect_disk_io(self) -> float:
        """Collect disk I/O metrics"""
        try:
            # Simulate disk I/O collection
            return random.uniform(10.0, 100.0)
        except Exception as e:
            self.logger.error(f"Failed to collect disk I/O: {e}")
            return 0.0

    def _collect_network_metrics(self) -> float:
        """Collect network bandwidth metrics"""
        try:
            # Simulate network bandwidth collection
            return random.uniform(50.0, 500.0)
        except Exception as e:
            self.logger.error(f"Failed to collect network metrics: {e}")
            return 0.0

    def _collect_network_latency(self) -> float:
        """Collect network latency metrics"""
        try:
            # Simulate network latency collection
            return random.uniform(5.0, 50.0)
        except Exception as e:
            self.logger.error(f"Failed to collect network latency: {e}")
            return 0.0

    def _collect_connection_metrics(self) -> int:
        """Collect connection metrics"""
        try:
            # Simulate connection count collection
            return random.randint(10, 200)
        except Exception as e:
            self.logger.error(f"Failed to collect connection metrics: {e}")
            return 0

    def _collect_response_time(self) -> float:
        """Collect response time metrics"""
        try:
            # Simulate response time collection
            return random.uniform(50.0, 300.0)
        except Exception as e:
            self.logger.error(f"Failed to collect response time: {e}")
            return 0.0

    def add_metric(self, name: str, value: Any) -> None:
        """Add a custom metric"""
        try:
            metric_data = MetricData(
                name=name,
                value=value,
                timestamp=datetime.now().isoformat(),
                type=MetricType.CUSTOM,
                status="active"
            )
            self.metrics_history.append(metric_data)
            self.current_metrics[name] = value
            
        except Exception as e:
            self.logger.error(f"Failed to add metric {name}: {e}")

    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        return self.current_metrics.copy()

    def get_metrics_history(self) -> List[MetricData]:
        """Get metrics history"""
        return self.metrics_history.copy()

    def get_metric_by_name(self, name: str) -> Optional[MetricData]:
        """Get metric by name from history"""
        for metric in reversed(self.metrics_history):
            if metric.name == name:
                return metric
        return None

    def get_metrics_by_type(self, metric_type: MetricType) -> List[MetricData]:
        """Get metrics by type"""
        return [metric for metric in self.metrics_history if metric.type == metric_type]

    def get_recent_metrics(self, count: int = 100) -> List[MetricData]:
        """Get recent metrics"""
        return self.metrics_history[-count:] if self.metrics_history else []

    def add_alert(self, message: str) -> None:
        """Add a new alert"""
        try:
            timestamp = datetime.now().isoformat()
            alert = f"[{timestamp}] {message}"
            
            self.alerts.append(alert)
            
            # Limit alerts
            if len(self.alerts) > self.max_alerts:
                self.alerts = self.alerts[-self.max_alerts//2:]
            
            self.logger.warning(f"Alert added: {message}")
            
        except Exception as e:
            self.logger.error(f"Failed to add alert: {e}")

    def get_alerts(self) -> List[str]:
        """Get all alerts"""
        return self.alerts.copy()

    def get_recent_alerts(self, count: int = 50) -> List[str]:
        """Get recent alerts"""
        return self.alerts[-count:] if self.alerts else []

    def clear_alerts(self) -> None:
        """Clear all alerts"""
        self.alerts.clear()
        self.logger.info("✅ All alerts cleared")

    def get_health_status(self) -> Dict[str, Any]:
        """Get monitoring health status"""
        try:
            current_time = datetime.now()
            
            # Check if health check is needed
            if (current_time - self.last_health_check).total_seconds() > self.health_check_interval:
                self._update_health_status()
                self.last_health_check = current_time
            
            return {
                "status": self.health_status,
                "last_check": self.last_health_check.isoformat(),
                "total_collections": self.total_collections,
                "successful_collections": self.successful_collections,
                "failed_collections": self.failed_collections,
                "success_rate": round(self.successful_collections / max(self.total_collections, 1), 3),
                "active_metrics": len(self.current_metrics),
                "total_alerts": len(self.alerts),
                "metrics_history_size": len(self.metrics_history)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get health status: {e}")
            return {"status": "error", "error": str(e)}

    def _update_health_status(self) -> None:
        """Update health status based on current conditions"""
        try:
            # Check collection success rate
            if self.total_collections > 0:
                success_rate = self.successful_collections / self.total_collections
                
                if success_rate < 0.5:
                    self.health_status = "critical"
                elif success_rate < 0.8:
                    self.health_status = "warning"
                elif success_rate < 0.95:
                    self.health_status = "degraded"
                else:
                    self.health_status = "healthy"
            
            # Check alert count
            if len(self.alerts) > 100:
                if self.health_status == "healthy":
                    self.health_status = "warning"
                elif self.health_status == "degraded":
                    self.health_status = "critical"
            
            # Check metrics history size
            if len(self.metrics_history) > 8000:
                if self.health_status == "healthy":
                    self.health_status = "warning"
            
        except Exception as e:
            self.logger.error(f"Failed to update health status: {e}")
            self.health_status = "error"

    def clear_metrics(self) -> None:
        """Clear all metrics"""
        self.metrics_history.clear()
        self.current_metrics.clear()
        self.total_collections = 0
        self.successful_collections = 0
        self.failed_collections = 0
        self.logger.info("✅ All metrics cleared")

    def export_metrics(self, format: str = "json") -> str:
        """Export metrics in specified format"""
        try:
            if format.lower() == "json":
                import json
                return json.dumps({
                    "export_timestamp": datetime.now().isoformat(),
                    "total_metrics": len(self.metrics_history),
                    "current_metrics": self.current_metrics,
                    "recent_metrics": [metric.__dict__ for metric in self.metrics_history[-100:]],
                    "health_status": self.get_health_status()
                }, indent=2)
            else:
                return f"Export format {format} not supported"
                
        except Exception as e:
            self.logger.error(f"Failed to export metrics: {e}")
            return f"Export failed: {e}"

    def get_statistics(self) -> Dict[str, Any]:
        """Get monitoring statistics"""
        try:
            return {
                "total_collections": self.total_collections,
                "successful_collections": self.successful_collections,
                "failed_collections": self.failed_collections,
                "success_rate": round(self.successful_collections / max(self.total_collections, 1), 3),
                "total_metrics": len(self.metrics_history),
                "current_metrics_count": len(self.current_metrics),
                "total_alerts": len(self.alerts),
                "health_status": self.health_status,
                "last_health_check": self.last_health_check.isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get statistics: {e}")
            return {"error": str(e)}

    def reset(self) -> None:
        """Reset monitoring manager to initial state"""
        try:
            self.clear_metrics()
            self.clear_alerts()
            self.health_status = "healthy"
            self.last_health_check = datetime.now()
            self.logger.info("✅ Monitoring Manager reset to initial state")
            
        except Exception as e:
            self.logger.error(f"Failed to reset monitoring manager: {e}")

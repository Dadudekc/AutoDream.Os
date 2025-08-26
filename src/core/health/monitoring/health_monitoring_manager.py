#!/usr/bin/env python3
"""
Health Monitoring Manager - V2 Modular Architecture
==================================================

Handles health metric collection and monitoring operations.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import time
import psutil
from typing import Dict, List, Optional, Any
from datetime import datetime
from threading import Thread, Lock

from ..types.health_types import HealthMetric, HealthLevel


logger = logging.getLogger(__name__)


class HealthMonitoringManager:
    """
    Health Monitoring Manager - Single responsibility: Monitor health metrics
    
    Handles all health monitoring operations including:
    - System metric collection
    - Metric storage and management
    - Health level calculation
    - Trend analysis
    """

    def __init__(self):
        """Initialize health monitoring manager"""
        self.logger = logging.getLogger(f"{__name__}.HealthMonitoringManager")
        
        # Metric storage
        self.health_metrics: Dict[str, HealthMetric] = {}
        self.metric_history: Dict[str, List[Dict[str, Any]]] = {}
        
        # Monitoring state
        self.monitoring_active = False
        self.monitoring_interval = 30  # seconds
        self.monitoring_thread: Optional[Thread] = None
        
        # Thread safety
        self._lock = Lock()
        
        # Setup default metrics
        self._setup_default_metrics()
        
        self.logger.info("✅ Health Monitoring Manager initialized successfully")

    def _setup_default_metrics(self):
        """Setup default health metrics"""
        try:
            # System metrics
            self.health_metrics["cpu_usage"] = HealthMetric(
                name="cpu_usage",
                value=0.0,
                unit="%",
                threshold_min=0.0,
                threshold_max=80.0,
                current_level=HealthLevel.EXCELLENT,
                timestamp=datetime.now().isoformat(),
                trend="stable",
                description="CPU usage percentage"
            )
            
            self.health_metrics["memory_usage"] = HealthMetric(
                name="memory_usage",
                value=0.0,
                unit="%",
                threshold_min=0.0,
                threshold_max=85.0,
                current_level=HealthLevel.EXCELLENT,
                timestamp=datetime.now().isoformat(),
                trend="stable",
                description="Memory usage percentage"
            )
            
            self.health_metrics["disk_usage"] = HealthMetric(
                name="disk_usage",
                value=0.0,
                unit="%",
                threshold_min=0.0,
                threshold_max=90.0,
                current_level=HealthLevel.EXCELLENT,
                timestamp=datetime.now().isoformat(),
                trend="stable",
                description="Disk usage percentage"
            )
            
            self.health_metrics["network_bytes_sent"] = HealthMetric(
                name="network_bytes_sent",
                value=0.0,
                unit="bytes",
                threshold_min=0.0,
                threshold_max=None,
                current_level=HealthLevel.EXCELLENT,
                timestamp=datetime.now().isoformat(),
                trend="stable",
                description="Network bytes sent"
            )
            
            self.health_metrics["network_bytes_recv"] = HealthMetric(
                name="network_bytes_recv",
                value=0.0,
                unit="bytes",
                threshold_min=0.0,
                threshold_max=None,
                current_level=HealthLevel.EXCELLENT,
                timestamp=datetime.now().isoformat(),
                trend="stable",
                description="Network bytes received"
            )
            
            # Initialize history for each metric
            for metric_name in self.health_metrics:
                self.metric_history[metric_name] = []
                
        except Exception as e:
            self.logger.error(f"Failed to setup default metrics: {e}")

    def start_monitoring(self, interval: Optional[int] = None):
        """Start health monitoring"""
        try:
            if self.monitoring_active:
                self.logger.info("Health monitoring already active")
                return
            
            if interval:
                self.monitoring_interval = interval
            
            self.monitoring_active = True
            
            # Start monitoring thread
            self.monitoring_thread = Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            
            self.logger.info(f"✅ Health monitoring started with {self.monitoring_interval}s interval")
            
        except Exception as e:
            self.logger.error(f"Failed to start health monitoring: {e}")

    def stop_monitoring(self):
        """Stop health monitoring"""
        try:
            self.monitoring_active = False
            if self.monitoring_thread:
                self.monitoring_thread.join(timeout=5.0)
            self.logger.info("✅ Health monitoring stopped")
        except Exception as e:
            self.logger.error(f"Failed to stop health monitoring: {e}")

    def _monitoring_loop(self):
        """Main health monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect system metrics
                self._collect_system_metrics()
                
                # Wait for next interval
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                self.logger.error(f"Health monitoring error: {e}")
                time.sleep(5)

    def _collect_system_metrics(self):
        """Collect system health metrics"""
        try:
            with self._lock:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                self._update_metric("cpu_usage", cpu_percent)
                
                # Memory usage
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                self._update_metric("memory_usage", memory_percent)
                
                # Disk usage
                try:
                    disk = psutil.disk_usage('/')
                    disk_percent = (disk.used / disk.total) * 100
                    self._update_metric("disk_usage", disk_percent)
                except Exception:
                    pass  # Skip disk metrics if not accessible
                
                # Network metrics
                try:
                    network = psutil.net_io_counters()
                    self._update_metric("network_bytes_sent", network.bytes_sent)
                    self._update_metric("network_bytes_recv", network.bytes_recv)
                except Exception:
                    pass
                    
        except Exception as e:
            self.logger.error(f"Failed to collect system metrics: {e}")

    def _update_metric(self, metric_name: str, value: float):
        """Update a health metric"""
        try:
            if metric_name in self.health_metrics:
                metric = self.health_metrics[metric_name]
                
                # Calculate trend
                old_value = metric.value
                if value > old_value:
                    trend = "increasing"
                elif value < old_value:
                    trend = "decreasing"
                else:
                    trend = "stable"
                
                # Update metric
                metric.value = value
                metric.timestamp = datetime.now().isoformat()
                metric.trend = trend
                
                # Store in history
                history_entry = {
                    "value": value,
                    "timestamp": metric.timestamp,
                    "trend": trend
                }
                self.metric_history[metric_name].append(history_entry)
                
                # Keep only last 1000 entries
                if len(self.metric_history[metric_name]) > 1000:
                    self.metric_history[metric_name] = self.metric_history[metric_name][-1000:]
                
        except Exception as e:
            self.logger.error(f"Failed to update metric {metric_name}: {e}")

    def get_metric(self, metric_name: str) -> Optional[HealthMetric]:
        """Get a specific health metric"""
        try:
            with self._lock:
                return self.health_metrics.get(metric_name)
        except Exception as e:
            self.logger.error(f"Failed to get metric {metric_name}: {e}")
            return None

    def get_all_metrics(self) -> Dict[str, HealthMetric]:
        """Get all health metrics"""
        try:
            with self._lock:
                return self.health_metrics.copy()
        except Exception as e:
            self.logger.error(f"Failed to get all metrics: {e}")
            return {}

    def get_metric_history(self, metric_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get metric history"""
        try:
            with self._lock:
                if metric_name in self.metric_history:
                    return self.metric_history[metric_name][-limit:]
                return []
        except Exception as e:
            self.logger.error(f"Failed to get metric history for {metric_name}: {e}")
            return []

    def add_custom_metric(self, metric: HealthMetric) -> bool:
        """Add a custom health metric"""
        try:
            with self._lock:
                self.health_metrics[metric.name] = metric
                self.metric_history[metric.name] = []
                self.logger.info(f"Added custom metric: {metric.name}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to add custom metric {metric.name}: {e}")
            return False

    def remove_metric(self, metric_name: str) -> bool:
        """Remove a health metric"""
        try:
            with self._lock:
                if metric_name in self.health_metrics:
                    del self.health_metrics[metric_name]
                    del self.metric_history[metric_name]
                    self.logger.info(f"Removed metric: {metric_name}")
                    return True
                return False
        except Exception as e:
            self.logger.error(f"Failed to remove metric {metric_name}: {e}")
            return False

    def clear_metrics(self):
        """Clear all metrics and history"""
        try:
            with self._lock:
                self.health_metrics.clear()
                self.metric_history.clear()
                self._setup_default_metrics()
                self.logger.info("✅ All metrics cleared and reset to defaults")
        except Exception as e:
            self.logger.error(f"Failed to clear metrics: {e}")

    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get monitoring status"""
        try:
            return {
                "monitoring_active": self.monitoring_active,
                "monitoring_interval": self.monitoring_interval,
                "total_metrics": len(self.health_metrics),
                "total_history_entries": sum(len(history) for history in self.metric_history.values()),
                "last_update": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Failed to get monitoring status: {e}")
            return {"error": str(e)}

    def cleanup(self):
        """Cleanup resources"""
        try:
            self.stop_monitoring()
            self.clear_metrics()
            self.logger.info("✅ Health Monitoring Manager cleanup completed")
        except Exception as e:
            self.logger.error(f"Health Monitoring Manager cleanup failed: {e}")


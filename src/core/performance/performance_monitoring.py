#!/usr/bin/env python3
"""
Performance Monitoring Manager - Metric Collection and Monitoring
==============================================================

Handles performance metric collection, monitoring, and real-time tracking.
Follows V2 standards: ≤400 LOC, SRP, OOP design.

Author: Agent-1 (Phase 3 Modularization)
License: MIT
"""

import logging
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

from .performance_models import PerformanceMetric, MetricType, ResourceUtilization


class PerformanceMonitoringManager:
    """
    Performance Monitoring Manager - Handles metric collection and monitoring
    
    Single Responsibility: Collect, monitor, and track performance metrics
    across all system components in real-time.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.PerformanceMonitoringManager")
        
        # Monitoring state
        self.monitoring_active = False
        self.monitoring_thread: Optional[threading.Thread] = None
        self.monitoring_interval = 5.0  # seconds
        
        # Metric collection
        self.metrics_buffer: List[PerformanceMetric] = []
        self.metrics_lock = threading.Lock()
        
        # Resource tracking
        self.resource_utilization: Dict[str, ResourceUtilization] = {}
        self.resource_lock = threading.Lock()
        
        # Performance counters
        self.total_metrics_collected = 0
        self.metrics_collection_errors = 0
        self.last_collection_time: Optional[datetime] = None
        
        self.logger.info("Performance Monitoring Manager initialized")
    
    def start_monitoring(self) -> bool:
        """Start performance monitoring"""
        try:
            if self.monitoring_active:
                self.logger.warning("Monitoring is already active")
                return True
            
            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(
                target=self._monitoring_loop,
                daemon=True,
                name="PerformanceMonitoring"
            )
            self.monitoring_thread.start()
            
            self.logger.info("✅ Performance monitoring started")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start monitoring: {e}")
            return False
    
    def stop_monitoring(self) -> bool:
        """Stop performance monitoring"""
        try:
            if not self.monitoring_active:
                self.logger.warning("Monitoring is not active")
                return True
            
            self.monitoring_active = False
            
            if self.monitoring_thread and self.monitoring_thread.is_alive():
                self.monitoring_thread.join(timeout=5.0)
            
            self.logger.info("✅ Performance monitoring stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop monitoring: {e}")
            return False
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                start_time = time.time()
                
                # Collect system metrics
                self._collect_system_metrics()
                
                # Collect resource utilization
                self._collect_resource_utilization()
                
                # Update collection time
                self.last_collection_time = datetime.now()
                
                # Sleep for remaining interval
                elapsed = time.time() - start_time
                sleep_time = max(0, self.monitoring_interval - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                self.metrics_collection_errors += 1
                time.sleep(1.0)  # Brief pause on error
    
    def _collect_system_metrics(self):
        """Collect system performance metrics"""
        try:
            metrics = []
            
            # CPU metrics
            cpu_metrics = self._collect_cpu_metrics()
            metrics.extend(cpu_metrics)
            
            # Memory metrics
            memory_metrics = self._collect_memory_metrics()
            metrics.extend(memory_metrics)
            
            # Disk metrics
            disk_metrics = self._collect_disk_metrics()
            metrics.extend(disk_metrics)
            
            # Network metrics
            network_metrics = self._collect_network_metrics()
            metrics.extend(network_metrics)
            
            # Add to buffer
            with self.metrics_lock:
                self.metrics_buffer.extend(metrics)
                self.total_metrics_collected += len(metrics)
            
            self.logger.debug(f"Collected {len(metrics)} system metrics")
            
        except Exception as e:
            self.logger.error(f"Failed to collect system metrics: {e}")
            self.metrics_collection_errors += 1
    
    def _collect_cpu_metrics(self) -> List[PerformanceMetric]:
        """Collect CPU performance metrics"""
        try:
            import psutil
            
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            metrics = [
                PerformanceMetric(
                    name="cpu_usage_percent",
                    value=cpu_percent,
                    unit="%",
                    metric_type=MetricType.GAUGE,
                    timestamp=datetime.now(),
                    labels={"type": "system", "component": "cpu"},
                    description="Current CPU usage percentage"
                ),
                PerformanceMetric(
                    name="cpu_count",
                    value=cpu_count,
                    unit="cores",
                    metric_type=MetricType.GAUGE,
                    timestamp=datetime.now(),
                    labels={"type": "system", "component": "cpu"},
                    description="Number of CPU cores"
                )
            ]
            
            if cpu_freq:
                metrics.append(PerformanceMetric(
                    name="cpu_frequency_mhz",
                    value=cpu_freq.current,
                    unit="MHz",
                    metric_type=MetricType.GAUGE,
                    timestamp=datetime.now(),
                    labels={"type": "system", "component": "cpu"},
                    description="Current CPU frequency"
                ))
            
            return metrics
            
        except ImportError:
            self.logger.warning("psutil not available - using mock CPU metrics")
            return [
                PerformanceMetric(
                    name="cpu_usage_percent",
                    value=50.0,  # Mock value
                    unit="%",
                    metric_type=MetricType.GAUGE,
                    timestamp=datetime.now(),
                    labels={"type": "system", "component": "cpu"},
                    description="Mock CPU usage percentage"
                )
            ]
        except Exception as e:
            self.logger.error(f"Failed to collect CPU metrics: {e}")
            return []
    
    def _collect_memory_metrics(self) -> List[PerformanceMetric]:
        """Collect memory performance metrics"""
        try:
            import psutil
            
            memory = psutil.virtual_memory()
            
            return [
                PerformanceMetric(
                    name="memory_usage_percent",
                    value=memory.percent,
                    unit="%",
                    metric_type=MetricType.GAUGE,
                    timestamp=datetime.now(),
                    labels={"type": "system", "component": "memory"},
                    description="Current memory usage percentage"
                ),
                PerformanceMetric(
                    name="memory_available_gb",
                    value=memory.available / (1024**3),
                    unit="GB",
                    metric_type=MetricType.GAUGE,
                    timestamp=datetime.now(),
                    labels={"type": "system", "component": "memory"},
                    description="Available memory in GB"
                ),
                PerformanceMetric(
                    name="memory_total_gb",
                    value=memory.total / (1024**3),
                    unit="GB",
                    metric_type=MetricType.GAUGE,
                    timestamp=datetime.now(),
                    labels={"type": "system", "component": "memory"},
                    description="Total memory in GB"
                )
            ]
            
        except ImportError:
            self.logger.warning("psutil not available - using mock memory metrics")
            return [
                PerformanceMetric(
                    name="memory_usage_percent",
                    value=65.0,  # Mock value
                    unit="%",
                    metric_type=MetricType.GAUGE,
                    timestamp=datetime.now(),
                    labels={"type": "system", "component": "memory"},
                    description="Mock memory usage percentage"
                )
            ]
        except Exception as e:
            self.logger.error(f"Failed to collect memory metrics: {e}")
            return []
    
    def _collect_disk_metrics(self) -> List[PerformanceMetric]:
        """Collect disk performance metrics"""
        try:
            import psutil
            
            disk = psutil.disk_usage('/')
            
            return [
                PerformanceMetric(
                    name="disk_usage_percent",
                    value=disk.percent,
                    unit="%",
                    metric_type=MetricType.GAUGE,
                    timestamp=datetime.now(),
                    labels={"type": "system", "component": "disk"},
                    description="Current disk usage percentage"
                ),
                PerformanceMetric(
                    name="disk_free_gb",
                    value=disk.free / (1024**3),
                    unit="GB",
                    metric_type=MetricType.GAUGE,
                    timestamp=datetime.now(),
                    labels={"type": "system", "component": "disk"},
                    description="Free disk space in GB"
                )
            ]
            
        except ImportError:
            self.logger.warning("psutil not available - using mock disk metrics")
            return [
                PerformanceMetric(
                    name="disk_usage_percent",
                    value=45.0,  # Mock value
                    unit="%",
                    metric_type=MetricType.GAUGE,
                    timestamp=datetime.now(),
                    labels={"type": "system", "component": "disk"},
                    description="Mock disk usage percentage"
                )
            ]
        except Exception as e:
            self.logger.error(f"Failed to collect disk metrics: {e}")
            return []
    
    def _collect_network_metrics(self) -> List[PerformanceMetric]:
        """Collect network performance metrics"""
        try:
            import psutil
            
            network = psutil.net_io_counters()
            
            return [
                PerformanceMetric(
                    name="network_bytes_sent",
                    value=network.bytes_sent,
                    unit="bytes",
                    metric_type=MetricType.COUNTER,
                    timestamp=datetime.now(),
                    labels={"type": "system", "component": "network"},
                    description="Total bytes sent over network"
                ),
                PerformanceMetric(
                    name="network_bytes_recv",
                    value=network.bytes_recv,
                    unit="bytes",
                    metric_type=MetricType.COUNTER,
                    timestamp=datetime.now(),
                    labels={"type": "system", "component": "network"},
                    description="Total bytes received over network"
                )
            ]
            
        except ImportError:
            self.logger.warning("psutil not available - using mock network metrics")
            return [
                PerformanceMetric(
                    name="network_bytes_sent",
                    value=1024,  # Mock value
                    unit="bytes",
                    metric_type=MetricType.COUNTER,
                    timestamp=datetime.now(),
                    labels={"type": "system", "component": "network"},
                    description="Mock network bytes sent"
                )
            ]
        except Exception as e:
            self.logger.error(f"Failed to collect network metrics: {e}")
            return []
    
    def _collect_resource_utilization(self):
        """Collect resource utilization metrics"""
        try:
            with self.resource_lock:
                for resource_name, resource in self.resource_utilization.items():
                    # Update utilization percentage
                    if resource.max_capacity > 0:
                        resource.utilization_percentage = (resource.current_usage / resource.max_capacity) * 100
                        resource.last_updated = datetime.now()
                        
                        # Update status based on utilization
                        if resource.utilization_percentage >= 90:
                            resource.status = "critical"
                        elif resource.utilization_percentage >= 75:
                            resource.status = "warning"
                        elif resource.utilization_percentage >= 50:
                            resource.status = "moderate"
                        else:
                            resource.status = "normal"
                            
        except Exception as e:
            self.logger.error(f"Failed to collect resource utilization: {e}")
    
    def collect_metrics(self) -> List[PerformanceMetric]:
        """Collect all available metrics"""
        try:
            with self.metrics_lock:
                metrics = self.metrics_buffer.copy()
                self.metrics_buffer.clear()
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to collect metrics: {e}")
            return []
    
    def add_custom_metric(
        self,
        name: str,
        value: float,
        unit: str,
        metric_type: MetricType,
        labels: Dict[str, str],
        description: str
    ) -> bool:
        """Add a custom performance metric"""
        try:
            metric = PerformanceMetric(
                name=name,
                value=value,
                unit=unit,
                metric_type=metric_type,
                timestamp=datetime.now(),
                labels=labels,
                description=description
            )
            
            with self.metrics_lock:
                self.metrics_buffer.append(metric)
                self.total_metrics_collected += 1
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add custom metric: {e}")
            return False
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get monitoring system status"""
        return {
            "monitoring_active": self.monitoring_active,
            "monitoring_interval": self.monitoring_interval,
            "total_metrics_collected": self.total_metrics_collected,
            "metrics_collection_errors": self.metrics_collection_errors,
            "last_collection_time": self.last_collection_time.isoformat() if self.last_collection_time else None,
            "metrics_buffer_size": len(self.metrics_buffer),
            "resource_count": len(self.resource_utilization)
        }
    
    def set_monitoring_interval(self, interval: float) -> bool:
        """Set monitoring interval in seconds"""
        try:
            if interval < 1.0:
                self.logger.warning("Monitoring interval must be at least 1 second")
                return False
            
            self.monitoring_interval = interval
            self.logger.info(f"Monitoring interval set to {interval} seconds")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to set monitoring interval: {e}")
            return False

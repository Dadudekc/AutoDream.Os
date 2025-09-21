"""
V3-006 Performance Monitoring Core System
Real-time performance metrics collection and monitoring
"""

import time
import psutil
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class MetricType(Enum):
    """Types of performance metrics"""
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    DISK_IO = "disk_io"
    NETWORK_IO = "network_io"
    DATABASE_QUERY_TIME = "db_query_time"
    API_RESPONSE_TIME = "api_response_time"
    CUSTOM = "custom"

@dataclass
class PerformanceMetric:
    """Performance metric data structure"""
    metric_type: MetricType
    value: float
    timestamp: datetime
    source: str
    tags: Dict[str, str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = {}

class PerformanceCollector:
    """Core performance metrics collector"""
    
    def __init__(self, collection_interval: float = 1.0):
        self.collection_interval = collection_interval
        self.metrics: List[PerformanceMetric] = []
        self.is_running = False
        self.collection_thread = None
        self.max_metrics = 10000  # Keep last 10k metrics
        
    def start_collection(self):
        """Start continuous performance collection"""
        if self.is_running:
            return
            
        self.is_running = True
        self.collection_thread = threading.Thread(target=self._collection_loop)
        self.collection_thread.daemon = True
        self.collection_thread.start()
        
    def stop_collection(self):
        """Stop performance collection"""
        self.is_running = False
        if self.collection_thread:
            self.collection_thread.join()
            
    def _collection_loop(self):
        """Main collection loop"""
        while self.is_running:
            try:
                self._collect_system_metrics()
                self._collect_database_metrics()
                self._collect_application_metrics()
                time.sleep(self.collection_interval)
            except Exception as e:
                print(f"Performance collection error: {e}")
                
    def _collect_system_metrics(self):
        """Collect system-level performance metrics"""
        now = datetime.now()
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=0.1)
        self._add_metric(MetricType.CPU_USAGE, cpu_percent, now, "system")
        
        # Memory usage
        memory = psutil.virtual_memory()
        self._add_metric(MetricType.MEMORY_USAGE, memory.percent, now, "system")
        
        # Disk I/O
        disk_io = psutil.disk_io_counters()
        if disk_io:
            self._add_metric(MetricType.DISK_IO, disk_io.read_bytes, now, "system", {"type": "read"})
            self._add_metric(MetricType.DISK_IO, disk_io.write_bytes, now, "system", {"type": "write"})
            
        # Network I/O
        net_io = psutil.net_io_counters()
        if net_io:
            self._add_metric(MetricType.NETWORK_IO, net_io.bytes_sent, now, "system", {"type": "sent"})
            self._add_metric(MetricType.NETWORK_IO, net_io.bytes_recv, now, "system", {"type": "received"})
            
    def _collect_database_metrics(self):
        """Collect database performance metrics"""
        # Placeholder for database metrics
        # In real implementation, this would connect to database monitoring
        pass
        
    def _collect_application_metrics(self):
        """Collect application-specific metrics"""
        # Placeholder for application metrics
        # In real implementation, this would collect custom app metrics
        pass
        
    def _add_metric(self, metric_type: MetricType, value: float, timestamp: datetime, 
                   source: str, tags: Dict[str, str] = None):
        """Add metric to collection"""
        metric = PerformanceMetric(
            metric_type=metric_type,
            value=value,
            timestamp=timestamp,
            source=source,
            tags=tags or {}
        )
        
        self.metrics.append(metric)
        
        # Keep only recent metrics
        if len(self.metrics) > self.max_metrics:
            self.metrics = self.metrics[-self.max_metrics:]
            
    def get_metrics(self, metric_type: Optional[MetricType] = None, 
                   source: Optional[str] = None, 
                   time_range: Optional[timedelta] = None) -> List[PerformanceMetric]:
        """Get filtered metrics"""
        filtered_metrics = self.metrics
        
        if metric_type:
            filtered_metrics = [m for m in filtered_metrics if m.metric_type == metric_type]
            
        if source:
            filtered_metrics = [m for m in filtered_metrics if m.source == source]
            
        if time_range:
            cutoff = datetime.now() - time_range
            filtered_metrics = [m for m in filtered_metrics if m.timestamp >= cutoff]
            
        return filtered_metrics
        
    def get_current_performance(self) -> Dict[str, Any]:
        """Get current performance snapshot"""
        recent_metrics = self.get_metrics(time_range=timedelta(minutes=1))
        
        performance = {
            "timestamp": datetime.now().isoformat(),
            "cpu_usage": 0.0,
            "memory_usage": 0.0,
            "disk_io_read": 0.0,
            "disk_io_write": 0.0,
            "network_sent": 0.0,
            "network_received": 0.0
        }
        
        for metric in recent_metrics:
            if metric.metric_type == MetricType.CPU_USAGE:
                performance["cpu_usage"] = metric.value
            elif metric.metric_type == MetricType.MEMORY_USAGE:
                performance["memory_usage"] = metric.value
            elif metric.metric_type == MetricType.DISK_IO:
                if metric.tags.get("type") == "read":
                    performance["disk_io_read"] = metric.value
                elif metric.tags.get("type") == "write":
                    performance["disk_io_write"] = metric.value
            elif metric.metric_type == MetricType.NETWORK_IO:
                if metric.tags.get("type") == "sent":
                    performance["network_sent"] = metric.value
                elif metric.tags.get("type") == "received":
                    performance["network_received"] = metric.value
                    
        return performance

class PerformanceMonitor:
    """Main performance monitoring system"""
    
    def __init__(self):
        self.collector = PerformanceCollector()
        self.alerts = []
        self.thresholds = {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "disk_io": 1000000,  # 1MB/s
            "network_io": 10000000  # 10MB/s
        }
        
    def start_monitoring(self):
        """Start performance monitoring"""
        self.collector.start_collection()
        print("Performance monitoring started")
        
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.collector.stop_collection()
        print("Performance monitoring stopped")
        
    def check_alerts(self) -> List[Dict[str, Any]]:
        """Check for performance alerts"""
        current = self.collector.get_current_performance()
        new_alerts = []
        
        if current["cpu_usage"] > self.thresholds["cpu_usage"]:
            new_alerts.append({
                "type": "high_cpu",
                "value": current["cpu_usage"],
                "threshold": self.thresholds["cpu_usage"],
                "timestamp": datetime.now().isoformat()
            })
            
        if current["memory_usage"] > self.thresholds["memory_usage"]:
            new_alerts.append({
                "type": "high_memory",
                "value": current["memory_usage"],
                "threshold": self.thresholds["memory_usage"],
                "timestamp": datetime.now().isoformat()
            })
            
        self.alerts.extend(new_alerts)
        return new_alerts
        
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        current = self.collector.get_current_performance()
        recent_alerts = self.check_alerts()
        
        return {
            "current_performance": current,
            "recent_alerts": recent_alerts,
            "total_alerts": len(self.alerts),
            "monitoring_status": "active" if self.collector.is_running else "inactive",
            "metrics_collected": len(self.collector.metrics)
        }

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

def start_performance_monitoring():
    """Start global performance monitoring"""
    performance_monitor.start_monitoring()

def stop_performance_monitoring():
    """Stop global performance monitoring"""
    performance_monitor.stop_monitoring()

def get_performance_summary() -> Dict[str, Any]:
    """Get current performance summary"""
    return performance_monitor.get_performance_summary()

if __name__ == "__main__":
    # Start monitoring for testing
    start_performance_monitoring()
    time.sleep(10)  # Monitor for 10 seconds
    summary = get_performance_summary()
    print(f"Performance Summary: {summary}")
    stop_performance_monitoring()



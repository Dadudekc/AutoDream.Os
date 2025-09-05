"""
Performance Monitoring System - KISS Simplified
===============================================

Simplified performance monitoring system.
KISS PRINCIPLE: Keep It Simple, Stupid - removed overengineering.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-2 - Architecture & Design Specialist
License: MIT
"""

import time
import psutil
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import logging


@dataclass
class PerformanceMetric:
    """Simple performance metric."""
    name: str
    value: float
    timestamp: datetime
    category: str = "general"
    unit: str = "ms"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
            "category": self.category,
            "unit": self.unit
        }


@dataclass
class PerformanceReport:
    """Simple performance report."""
    report_id: str
    timestamp: datetime
    metrics: List[PerformanceMetric]
    summary: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "report_id": self.report_id,
            "timestamp": self.timestamp.isoformat(),
            "metrics": [metric.to_dict() for metric in self.metrics],
            "summary": self.summary
        }


class PerformanceMonitoringSystem:
    """
    KISS Simplified Performance Monitoring System.
    
    Removed overengineering - focuses on essential monitoring only.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize simplified monitoring system."""
        self.logger = logger or logging.getLogger(__name__)
        self.metrics_history: List[PerformanceMetric] = []
        self.is_monitoring = False
        self.monitoring_interval = 5.0  # seconds
    
    def start_monitoring(self) -> bool:
        """Start performance monitoring."""
        try:
            if self.is_monitoring:
                return True
            
            self.is_monitoring = True
            self.logger.info("Performance monitoring started")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start monitoring: {e}")
            return False
    
    def stop_monitoring(self) -> bool:
        """Stop performance monitoring."""
        try:
            self.is_monitoring = False
            self.logger.info("Performance monitoring stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop monitoring: {e}")
            return False
    
    def collect_metrics(self) -> List[PerformanceMetric]:
        """Collect current performance metrics."""
        try:
            metrics = []
            current_time = datetime.now()
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            metrics.append(PerformanceMetric(
                name="cpu_usage",
                value=cpu_percent,
                timestamp=current_time,
                category="system",
                unit="percent"
            ))
            
            # Memory usage
            memory = psutil.virtual_memory()
            metrics.append(PerformanceMetric(
                name="memory_usage",
                value=memory.percent,
                timestamp=current_time,
                category="system",
                unit="percent"
            ))
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            metrics.append(PerformanceMetric(
                name="disk_usage",
                value=disk_percent,
                timestamp=current_time,
                category="system",
                unit="percent"
            ))
            
            # Store metrics
            self.metrics_history.extend(metrics)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to collect metrics: {e}")
            return []
    
    def generate_report(self) -> PerformanceReport:
        """Generate performance report."""
        try:
            # Collect current metrics
            current_metrics = self.collect_metrics()
            
            # Generate report
            report_id = f"perf_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Simple summary
            summary = f"Performance report with {len(current_metrics)} metrics"
            if current_metrics:
                cpu_metric = next((m for m in current_metrics if m.name == "cpu_usage"), None)
                if cpu_metric:
                    summary += f" - CPU: {cpu_metric.value:.1f}%"
            
            report = PerformanceReport(
                report_id=report_id,
                timestamp=datetime.now(),
                metrics=current_metrics,
                summary=summary
            )
            
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate report: {e}")
            return PerformanceReport(
                report_id=f"error_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                timestamp=datetime.now(),
                metrics=[],
                summary=f"Error generating report: {str(e)}"
            )
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status."""
        try:
            return {
                "is_monitoring": self.is_monitoring,
                "metrics_count": len(self.metrics_history),
                "monitoring_interval": self.monitoring_interval,
                "status": "active" if self.is_monitoring else "stopped"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get metrics summary."""
        try:
            if not self.metrics_history:
                return {"message": "No metrics collected"}
            
            # Simple summary
            latest_metrics = self.metrics_history[-10:]  # Last 10 metrics
            
            summary = {
                "total_metrics": len(self.metrics_history),
                "latest_metrics": len(latest_metrics),
                "monitoring_active": self.is_monitoring
            }
            
            # Add latest values if available
            if latest_metrics:
                cpu_metrics = [m for m in latest_metrics if m.name == "cpu_usage"]
                if cpu_metrics:
                    summary["latest_cpu"] = cpu_metrics[-1].value
                
                memory_metrics = [m for m in latest_metrics if m.name == "memory_usage"]
                if memory_metrics:
                    summary["latest_memory"] = memory_metrics[-1].value
            
            return summary
            
        except Exception as e:
            return {"error": str(e)}
    
    def cleanup(self) -> None:
        """Cleanup monitoring resources."""
        try:
            self.stop_monitoring()
            self.metrics_history.clear()
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")


# Factory function for backward compatibility
def create_performance_monitoring_system(logger: Optional[logging.Logger] = None) -> PerformanceMonitoringSystem:
    """Create a performance monitoring system instance."""
    return PerformanceMonitoringSystem(logger)

def get_performance_monitor() -> PerformanceMonitoringSystem:
    """Get performance monitor instance."""
    return create_performance_monitoring_system()
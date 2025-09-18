#!/usr/bin/env python3
"""
Thea Monitoring System - Comprehensive Monitoring and Logging
============================================================

Advanced monitoring and logging system for Thea autonomous operations.
Tracks performance, errors, and system health for 24/7 operation.

Features:
- Real-time performance monitoring
- Comprehensive activity logging
- System health tracking
- Performance metrics collection
- Alert system for critical issues
- Historical data analysis

Usage:
    from src.services.thea.thea_monitoring_system import TheaMonitoringSystem
    
    monitor = TheaMonitoringSystem()
    monitor.start_monitoring()
"""

import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from threading import Thread, Event
import psutil


@dataclass
class PerformanceMetrics:
    """Performance metrics for Thea operations."""
    timestamp: str
    operation: str
    duration: float
    success: bool
    memory_usage: float
    cpu_usage: float
    response_length: int
    error_message: Optional[str] = None


@dataclass
class SystemHealth:
    """System health status."""
    timestamp: str
    browser_running: bool
    cookies_valid: bool
    memory_usage: float
    cpu_usage: float
    disk_usage: float
    network_connected: bool
    last_activity: Optional[str] = None


class TheaMonitoringSystem:
    """Comprehensive monitoring system for Thea autonomous operations."""
    
    def __init__(self, 
                 log_dir: str = "logs/thea_monitoring",
                 metrics_retention_days: int = 7,
                 health_check_interval: int = 60):
        """
        Initialize the monitoring system.
        
        Args:
            log_dir: Directory for storing monitoring logs
            metrics_retention_days: Days to retain performance metrics
            health_check_interval: Health check interval in seconds
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.metrics_retention_days = metrics_retention_days
        self.health_check_interval = health_check_interval
        
        # Data storage
        self.performance_metrics: List[PerformanceMetrics] = []
        self.system_health_history: List[SystemHealth] = []
        self.activity_log: List[Dict[str, Any]] = []
        
        # Monitoring state
        self.monitoring_active = False
        self.monitoring_thread = None
        self.stop_event = Event()
        
        # Alert thresholds
        self.alert_thresholds = {
            "memory_usage_percent": 80.0,
            "cpu_usage_percent": 80.0,
            "disk_usage_percent": 90.0,
            "error_rate_percent": 20.0,
            "response_time_seconds": 120.0
        }
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup monitoring system logging."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"thea_monitoring_{timestamp}.log"
        
        self.monitor_logger = logging.getLogger("thea_monitoring")
        self.monitor_logger.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.monitor_logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.monitor_logger.addHandler(console_handler)
        
        self.monitor_logger.info("🔍 Thea Monitoring System initialized")
    
    def start_monitoring(self):
        """Start the monitoring system."""
        if self.monitoring_active:
            self.monitor_logger.warning("Monitoring already active")
            return
        
        self.monitoring_active = True
        self.stop_event.clear()
        
        self.monitoring_thread = Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        self.monitor_logger.info("🚀 Monitoring system started")
    
    def stop_monitoring(self):
        """Stop the monitoring system."""
        if not self.monitoring_active:
            return
        
        self.monitoring_active = False
        self.stop_event.set()
        
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        self.monitor_logger.info("🛑 Monitoring system stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop."""
        while not self.stop_event.is_set():
            try:
                # Collect system health
                health = self._collect_system_health()
                self.system_health_history.append(health)
                
                # Check for alerts
                self._check_alerts(health)
                
                # Cleanup old data
                self._cleanup_old_data()
                
                # Wait for next check
                self.stop_event.wait(self.health_check_interval)
                
            except Exception as e:
                self.monitor_logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5)
    
    def _collect_system_health(self) -> SystemHealth:
        """Collect current system health metrics."""
        try:
            # System metrics
            memory = psutil.virtual_memory()
            cpu = psutil.cpu_percent(interval=1)
            disk = psutil.disk_usage('/')
            
            # Network connectivity (simple check)
            network_connected = self._check_network_connectivity()
            
            # Browser and cookie status (would need integration with Thea system)
            browser_running = self._check_browser_status()
            cookies_valid = self._check_cookie_status()
            
            # Last activity
            last_activity = None
            if self.activity_log:
                last_activity = self.activity_log[-1].get('timestamp')
            
            return SystemHealth(
                timestamp=datetime.now().isoformat(),
                browser_running=browser_running,
                cookies_valid=cookies_valid,
                memory_usage=memory.percent,
                cpu_usage=cpu,
                disk_usage=disk.percent,
                network_connected=network_connected,
                last_activity=last_activity
            )
            
        except Exception as e:
            self.monitor_logger.error(f"Error collecting system health: {e}")
            return SystemHealth(
                timestamp=datetime.now().isoformat(),
                browser_running=False,
                cookies_valid=False,
                memory_usage=0.0,
                cpu_usage=0.0,
                disk_usage=0.0,
                network_connected=False
            )
    
    def _check_network_connectivity(self) -> bool:
        """Check network connectivity."""
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False
    
    def _check_browser_status(self) -> bool:
        """Check if browser is running."""
        try:
            # Check for Chrome/Chromium processes
            for proc in psutil.process_iter(['pid', 'name']):
                if 'chrome' in proc.info['name'].lower():
                    return True
            return False
        except Exception:
            return False
    
    def _check_cookie_status(self) -> bool:
        """Check if cookies are valid."""
        try:
            cookie_file = Path("thea_cookies.json")
            if not cookie_file.exists():
                return False
            
            # Check if cookie file is recent (within last 24 hours)
            file_age = time.time() - cookie_file.stat().st_mtime
            return file_age < 86400  # 24 hours
        except Exception:
            return False
    
    def _check_alerts(self, health: SystemHealth):
        """Check for alert conditions."""
        alerts = []
        
        if health.memory_usage > self.alert_thresholds["memory_usage_percent"]:
            alerts.append(f"High memory usage: {health.memory_usage:.1f}%")
        
        if health.cpu_usage > self.alert_thresholds["cpu_usage_percent"]:
            alerts.append(f"High CPU usage: {health.cpu_usage:.1f}%")
        
        if health.disk_usage > self.alert_thresholds["disk_usage_percent"]:
            alerts.append(f"High disk usage: {health.disk_usage:.1f}%")
        
        if not health.network_connected:
            alerts.append("Network connectivity lost")
        
        if not health.browser_running:
            alerts.append("Browser not running")
        
        if not health.cookies_valid:
            alerts.append("Cookies invalid or expired")
        
        # Check error rate
        if len(self.performance_metrics) > 10:
            recent_metrics = self.performance_metrics[-10:]
            error_rate = sum(1 for m in recent_metrics if not m.success) / len(recent_metrics) * 100
            if error_rate > self.alert_thresholds["error_rate_percent"]:
                alerts.append(f"High error rate: {error_rate:.1f}%")
        
        # Log alerts
        for alert in alerts:
            self.monitor_logger.warning(f"🚨 ALERT: {alert}")
    
    def _cleanup_old_data(self):
        """Clean up old monitoring data."""
        cutoff_date = datetime.now() - timedelta(days=self.metrics_retention_days)
        cutoff_str = cutoff_date.isoformat()
        
        # Cleanup performance metrics
        self.performance_metrics = [
            m for m in self.performance_metrics 
            if m.timestamp > cutoff_str
        ]
        
        # Cleanup system health history
        self.system_health_history = [
            h for h in self.system_health_history 
            if h.timestamp > cutoff_str
        ]
        
        # Cleanup activity log
        self.activity_log = [
            a for a in self.activity_log 
            if a.get('timestamp', '') > cutoff_str
        ]
    
    def log_operation(self, 
                     operation: str,
                     duration: float,
                     success: bool,
                     response_length: int = 0,
                     error_message: Optional[str] = None):
        """Log a Thea operation."""
        try:
            # Get system metrics
            memory = psutil.virtual_memory()
            cpu = psutil.cpu_percent()
            
            metric = PerformanceMetrics(
                timestamp=datetime.now().isoformat(),
                operation=operation,
                duration=duration,
                success=success,
                memory_usage=memory.percent,
                cpu_usage=cpu,
                response_length=response_length,
                error_message=error_message
            )
            
            self.performance_metrics.append(metric)
            
            # Log activity
            activity = {
                "timestamp": datetime.now().isoformat(),
                "operation": operation,
                "duration": duration,
                "success": success,
                "response_length": response_length
            }
            self.activity_log.append(activity)
            
            # Log to file
            if success:
                self.monitor_logger.info(f"✅ {operation} completed in {duration:.2f}s")
            else:
                self.monitor_logger.error(f"❌ {operation} failed: {error_message}")
                
        except Exception as e:
            self.monitor_logger.error(f"Error logging operation: {e}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary statistics."""
        if not self.performance_metrics:
            return {"total_operations": 0}
        
        total_ops = len(self.performance_metrics)
        successful_ops = sum(1 for m in self.performance_metrics if m.success)
        error_rate = (total_ops - successful_ops) / total_ops * 100
        
        avg_duration = sum(m.duration for m in self.performance_metrics) / total_ops
        avg_response_length = sum(m.response_length for m in self.performance_metrics) / total_ops
        
        # Recent performance (last 10 operations)
        recent_metrics = self.performance_metrics[-10:] if len(self.performance_metrics) >= 10 else self.performance_metrics
        recent_avg_duration = sum(m.duration for m in recent_metrics) / len(recent_metrics)
        
        return {
            "total_operations": total_ops,
            "successful_operations": successful_ops,
            "error_rate_percent": error_rate,
            "average_duration_seconds": avg_duration,
            "average_response_length": avg_response_length,
            "recent_average_duration_seconds": recent_avg_duration,
            "last_operation": self.performance_metrics[-1].timestamp if self.performance_metrics else None
        }
    
    def get_system_health_summary(self) -> Dict[str, Any]:
        """Get current system health summary."""
        if not self.system_health_history:
            return {"status": "no_data"}
        
        latest_health = self.system_health_history[-1]
        
        return {
            "timestamp": latest_health.timestamp,
            "browser_running": latest_health.browser_running,
            "cookies_valid": latest_health.cookies_valid,
            "memory_usage_percent": latest_health.memory_usage,
            "cpu_usage_percent": latest_health.cpu_usage,
            "disk_usage_percent": latest_health.disk_usage,
            "network_connected": latest_health.network_connected,
            "last_activity": latest_health.last_activity,
            "status": "healthy" if all([
                latest_health.browser_running,
                latest_health.cookies_valid,
                latest_health.network_connected,
                latest_health.memory_usage < 80,
                latest_health.cpu_usage < 80
            ]) else "degraded"
        }
    
    def export_data(self, output_file: Optional[str] = None) -> str:
        """Export monitoring data to JSON file."""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.log_dir / f"thea_monitoring_export_{timestamp}.json"
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "performance_metrics": [asdict(m) for m in self.performance_metrics],
            "system_health_history": [asdict(h) for h in self.system_health_history],
            "activity_log": self.activity_log,
            "performance_summary": self.get_performance_summary(),
            "system_health_summary": self.get_system_health_summary()
        }
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.monitor_logger.info(f"📊 Monitoring data exported to {output_file}")
        return str(output_file)


# Convenience functions
def create_monitoring_system(**kwargs) -> TheaMonitoringSystem:
    """Create a monitoring system with default settings."""
    return TheaMonitoringSystem(**kwargs)


if __name__ == "__main__":
    # Example usage
    print("📊 V2_SWARM Thea Monitoring System")
    print("=" * 40)
    
    monitor = create_monitoring_system()
    print("✅ Monitoring system created")
    
    # Start monitoring
    monitor.start_monitoring()
    print("🚀 Monitoring started")
    
    # Simulate some operations
    monitor.log_operation("test_message", 2.5, True, 150)
    monitor.log_operation("test_message_2", 1.8, False, 0, "Network error")
    
    # Get summaries
    print("📈 Performance Summary:", monitor.get_performance_summary())
    print("🏥 System Health:", monitor.get_system_health_summary())
    
    # Export data
    export_file = monitor.export_data()
    print(f"📊 Data exported to: {export_file}")
    
    # Stop monitoring
    monitor.stop_monitoring()
    print("🛑 Monitoring stopped")

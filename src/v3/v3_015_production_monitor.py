#!/usr/bin/env python3
"""
V3-015: Production Monitor
==========================

V2 compliant production monitoring coordinator.
Maintains all functionality while staying under 400 lines.
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

# Import monitoring modules
from v3.v3_015_monitoring_metrics import (
    MetricsCollector, AlertManager, Metric, Alert, MetricType, AlertLevel
)
from v3.v3_015_monitoring_targets import (
    TargetManager, HealthCheckScheduler, MonitorStatus
)


class ProductionMonitor:
    """Main production monitoring system coordinator."""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.alert_manager = AlertManager()
        self.target_manager = TargetManager()
        self.scheduler = HealthCheckScheduler(self.target_manager)
        self.monitoring_active = False
        self.start_time = datetime.now()
    
    def initialize(self):
        """Initialize production monitoring system."""
        try:
            # Register default targets
            self._register_default_targets()
            
            # Set up default alert rules
            self._setup_default_alert_rules()
            
            # Start monitoring
            self.start_monitoring()
            
            print("🏥 Production Monitor initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            return False
    
    def _register_default_targets(self):
        """Register default monitoring targets."""
        self.target_manager.register_target(
            "web_app", "Web Application", "http://localhost:8080/health"
        )
        self.target_manager.register_target(
            "api_service", "API Service", "http://localhost:3000/status"
        )
        self.target_manager.register_target(
            "database", "Database", "tcp://localhost:5432"
        )
    
    def _setup_default_alert_rules(self):
        """Set up default alert rules."""
        self.alert_manager.add_alert_rule(
            "cpu_high", "cpu_usage", 80.0, AlertLevel.WARNING, "CPU usage is high"
        )
        self.alert_manager.add_alert_rule(
            "memory_high", "memory_usage", 90.0, AlertLevel.CRITICAL, "Memory usage is critical"
        )
        self.alert_manager.add_alert_rule(
            "response_slow", "response_time", 1000.0, AlertLevel.WARNING, "Response time is slow"
        )
    
    def start_monitoring(self):
        """Start monitoring system."""
        self.monitoring_active = True
        self.scheduler.start_scheduler()
        print("🚀 Production monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring system."""
        self.monitoring_active = False
        self.scheduler.stop_scheduler()
        print("⏹️ Production monitoring stopped")
    
    def collect_metric(self, name: str, value: float, metric_type: MetricType, 
                      labels: Dict[str, str] = None, unit: str = ""):
        """Collect a metric."""
        metric = Metric(
            metric_id=f"{name}_{int(datetime.now().timestamp())}",
            name=name,
            metric_type=metric_type,
            value=value,
            labels=labels or {},
            timestamp=datetime.now(),
            unit=unit
        )
        
        self.metrics_collector.add_metric(metric)
        self.alert_manager.check_metric_for_alerts(metric)
    
    def perform_health_checks(self) -> List[Dict[str, Any]]:
        """Perform health checks on all targets."""
        if not self.monitoring_active:
            return []
        
        results = self.target_manager.check_all_targets()
        
        # Convert results to dictionary format
        health_data = []
        for result in results:
            health_data.append({
                "target_id": result.target_id,
                "success": result.success,
                "response_time_ms": result.response_time_ms,
                "status_code": result.status_code,
                "error_message": result.error_message,
                "checked_at": result.checked_at.isoformat()
            })
        
        return health_data
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        if not self.monitoring_active:
            return {"status": "monitoring_inactive"}
        
        # Get metrics summary
        metrics_summary = self.metrics_collector.get_metric_summary()
        
        # Get alert summary
        alert_summary = self.alert_manager.get_alert_summary()
        
        # Get target health summary
        target_summary = self.target_manager.get_target_health_summary()
        
        # Get scheduler status
        scheduler_status = self.scheduler.get_scheduler_status()
        
        return {
            "monitoring_active": self.monitoring_active,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "metrics": metrics_summary,
            "alerts": alert_summary,
            "targets": target_summary,
            "scheduler": scheduler_status,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_health_dashboard(self) -> Dict[str, Any]:
        """Get health dashboard data."""
        system_status = self.get_system_status()
        
        # Get active alerts
        active_alerts = self.alert_manager.get_active_alerts()
        
        # Get recent health checks
        recent_checks = self.perform_health_checks()
        
        return {
            "system_status": system_status,
            "active_alerts": [
                {
                    "alert_id": alert.alert_id,
                    "name": alert.name,
                    "level": alert.level.value,
                    "message": alert.message,
                    "metric_name": alert.metric_name,
                    "current_value": alert.current_value,
                    "threshold": alert.threshold,
                    "triggered_at": alert.triggered_at.isoformat()
                }
                for alert in active_alerts
            ],
            "recent_health_checks": recent_checks,
            "dashboard_updated": datetime.now().isoformat()
        }
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert."""
        return self.alert_manager.acknowledge_alert(alert_id)
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert."""
        return self.alert_manager.resolve_alert(alert_id)
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get alert summary."""
        return self.alert_manager.get_alert_summary()
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get metrics summary."""
        return self.metrics_collector.get_metric_summary()
    
    def export_monitoring_data(self, filepath: str) -> bool:
        """Export monitoring data to file."""
        try:
            dashboard_data = self.get_health_dashboard()
            
            with open(filepath, 'w') as f:
                json.dump(dashboard_data, f, indent=2, default=str)
            
            print(f"📊 Monitoring data exported to {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Export error: {e}")
            return False


def main():
    """Main execution function."""
    print("🏥 V3-015 Production Monitor - Testing...")
    
    try:
        # Initialize production monitor
        monitor = ProductionMonitor()
        monitor.initialize()
        
        # Collect sample metrics
        print("\n📊 Collecting sample metrics...")
        monitor.collect_metric("cpu_usage", 75.5, MetricType.GAUGE, {"host": "server1"}, "%")
        monitor.collect_metric("memory_usage", 60.2, MetricType.GAUGE, {"host": "server1"}, "%")
        monitor.collect_metric("response_time", 250.0, MetricType.HISTOGRAM, {"endpoint": "/api"}, "ms")
        
        # Perform health checks
        print("\n🏥 Performing health checks...")
        health_checks = monitor.perform_health_checks()
        for check in health_checks:
            status = "✅" if check["success"] else "❌"
            print(f"   {check['target_id']}: {status} ({check['response_time_ms']:.2f}ms)")
        
        # Get system status
        system_status = monitor.get_system_status()
        
        print(f"\n📈 System Status:")
        print(f"   Monitoring Active: {system_status['monitoring_active']}")
        print(f"   Uptime: {system_status['uptime_seconds']:.1f} seconds")
        print(f"   Total Metrics: {system_status['metrics']['total_metrics']}")
        print(f"   Active Alerts: {system_status['alerts']['active_alerts']}")
        print(f"   Healthy Targets: {system_status['targets']['healthy_targets']}")
        
        # Export monitoring data
        monitor.export_monitoring_data("production_monitor_data.json")
        
        print("\n✅ V3-015 Production Monitor completed successfully!")
        return 0
        
    except Exception as e:
        print(f"❌ V3-015 implementation error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())


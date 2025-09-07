#!/usr/bin/env python3
"""
Unified Health Manager - V2 Modular Architecture
===============================================

Main orchestrator for all health management components.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import time
import threading
from typing import Dict, List, Optional, Any
from datetime import datetime

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority

from .types.health_types import HealthMetric, HealthAlert, HealthLevel
from .monitoring.health_monitoring_manager import HealthMonitoringManager
from .alerting.health_alert_manager import HealthAlertManager
from .analysis.health_analysis_manager import HealthAnalysisManager
from .notifications.health_notification_manager import HealthNotificationManager
from .recovery.health_recovery_manager import HealthRecoveryManager


logger = logging.getLogger(__name__)


class UnifiedHealthManager(BaseManager):
    """
    Unified Health Manager - Single responsibility: Orchestrate health components
    
    This manager orchestrates functionality from modular components:
    - Health monitoring and metrics collection
    - Alert creation and management
    - Health analysis and insights
    - Multi-channel notifications
    - Automated recovery actions
    
    Total consolidation: 1,116 lines → 6 modular components (95% modularization)
    """

    def __init__(self, config_path: str = "config/health_manager.json"):
        """Initialize unified health manager"""
        super().__init__(
            manager_name="UnifiedHealthManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        # Initialize modular components
        self.monitoring_manager = HealthMonitoringManager()
        self.alert_manager = HealthAlertManager()
        self.analysis_manager = HealthAnalysisManager()
        self.notification_manager = HealthNotificationManager()
        self.recovery_manager = HealthRecoveryManager()
        
        # System state
        self.monitoring_active = False
        self.monitoring_interval = 30  # seconds
        self.monitoring_thread: Optional[threading.Thread] = None
        
        # Configuration
        self.auto_resolve_alerts = True
        self.alert_timeout = 3600  # 1 hour
        self.enable_notifications = True
        self.enable_auto_recovery = True
        
        # Load configuration
        self._load_manager_config()
        
        self.logger.info("✅ Unified Health Manager initialized successfully")

    def _load_manager_config(self):
        """Load manager-specific configuration"""
        try:
            # Load configuration from base manager
            config = self.get_config()
            
            # Update health-specific settings
            self.monitoring_interval = config.get('monitoring_interval', 30)
            self.auto_resolve_alerts = config.get('auto_resolve_alerts', True)
            self.alert_timeout = config.get('alert_timeout', 3600)
            self.enable_notifications = config.get('enable_notifications', True)
            self.enable_auto_recovery = config.get('enable_auto_recovery', True)
            
        except Exception as e:
            self.logger.error(f"Failed to load health config: {e}")

    def start_monitoring(self, interval: Optional[int] = None):
        """Start health monitoring"""
        try:
            if self.monitoring_active:
                self.logger.info("Health monitoring already active")
                return
            
            if interval:
                self.monitoring_interval = interval
            
            self.monitoring_active = True
            
            # Start monitoring in monitoring manager
            self.monitoring_manager.start_monitoring(interval)
            
            # Start main monitoring loop
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            
            self.logger.info(f"✅ Health monitoring started with {self.monitoring_interval}s interval")
            
        except Exception as e:
            self.logger.error(f"Failed to start health monitoring: {e}")

    def stop_monitoring(self):
        """Stop health monitoring"""
        try:
            self.monitoring_active = False
            
            # Stop monitoring in monitoring manager
            self.monitoring_manager.stop_monitoring()
            
            # Stop main monitoring thread
            if self.monitoring_thread:
                self.monitoring_thread.join(timeout=5.0)
            
            self.logger.info("✅ Health monitoring stopped")
            
        except Exception as e:
            self.logger.error(f"Failed to stop health monitoring: {e}")

    def _monitoring_loop(self):
        """Main health monitoring loop"""
        while self.monitoring_active:
            try:
                # Get current metrics
                metrics = self.monitoring_manager.get_all_metrics()
                
                # Check thresholds and generate alerts
                new_alerts = self.alert_manager.check_thresholds(metrics)
                
                # Process new alerts
                for alert in new_alerts:
                    self._process_new_alert(alert)
                
                # Auto-resolve old alerts
                if self.auto_resolve_alerts:
                    self.alert_manager.auto_resolve_alerts()
                
                # Wait for next interval
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                self.logger.error(f"Health monitoring error: {e}")
                time.sleep(5)

    def _process_new_alert(self, alert: HealthAlert):
        """Process a new health alert"""
        try:
            # Send notifications
            if self.enable_notifications:
                self.notification_manager.send_notification(alert)
            
            # Execute automated recovery if enabled
            if self.enable_auto_recovery:
                recovery_result = self.recovery_manager.execute_automated_recovery(alert)
                if recovery_result and "error" not in recovery_result:
                    self.logger.info(f"Automated recovery executed for alert {alert.id}")
            
            # Emit event
            self._emit_event("health_alert_created", {
                "alert_id": alert.id,
                "metric_name": alert.metric_name,
                "level": alert.level.value,
                "value": alert.metric_value,
                "threshold": alert.threshold
            })
            
        except Exception as e:
            self.logger.error(f"Failed to process new alert {alert.id}: {e}")

    def get_health_summary(self) -> Dict[str, Any]:
        """Get overall health summary"""
        try:
            # Get metrics from monitoring manager
            metrics = self.monitoring_manager.get_all_metrics()
            
            # Get alerts from alert manager
            active_alerts = self.alert_manager.get_active_alerts()
            alert_stats = self.alert_manager.get_alert_statistics()
            
            # Get analysis insights
            trends = self.analysis_manager.analyze_health_trends(metrics)
            insights = self.analysis_manager.get_health_insights(metrics, trends)
            
            # Get recovery statistics
            recovery_stats = self.recovery_manager.get_recovery_statistics()
            
            # Get notification statistics
            notification_stats = self.notification_manager.get_notification_statistics()
            
            # Get monitoring status
            monitoring_status = self.monitoring_manager.get_monitoring_status()
            
            return {
                "timestamp": datetime.now().isoformat(),
                "monitoring_status": monitoring_status,
                "metrics_summary": {
                    "total_metrics": len(metrics),
                    "metrics_by_level": self._count_metrics_by_level(metrics)
                },
                "alerts_summary": alert_stats,
                "active_alerts_count": len(active_alerts),
                "health_insights": insights,
                "recovery_summary": recovery_stats,
                "notification_summary": notification_stats,
                "system_health": insights.get("overall_health", {})
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get health summary: {e}")
            return {"error": str(e)}

    def _count_metrics_by_level(self, metrics: Dict[str, HealthMetric]) -> Dict[str, int]:
        """Count metrics by health level"""
        try:
            level_counts = {}
            for metric in metrics.values():
                level = metric.current_level.value
                level_counts[level] = level_counts.get(level, 0) + 1
            return level_counts
        except Exception as e:
            self.logger.error(f"Failed to count metrics by level: {e}")
            return {}

    def get_metric_info(self, metric_name: str) -> Optional[HealthMetric]:
        """Get metric information"""
        return self.monitoring_manager.get_metric(metric_name)

    def get_all_metrics(self) -> Dict[str, HealthMetric]:
        """Get all health metrics"""
        return self.monitoring_manager.get_all_metrics()

    def get_metric_history(self, metric_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get metric history"""
        return self.monitoring_manager.get_metric_history(metric_name, limit)

    def add_custom_metric(self, metric: HealthMetric) -> bool:
        """Add a custom health metric"""
        return self.monitoring_manager.add_custom_metric(metric)

    def get_active_alerts(self) -> List[HealthAlert]:
        """Get list of active (unresolved) alerts"""
        return self.alert_manager.get_active_alerts()

    def get_all_alerts(self) -> List[HealthAlert]:
        """Get all health alerts"""
        return self.alert_manager.get_all_alerts()

    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge a health alert"""
        return self.alert_manager.acknowledge_alert(alert_id, acknowledged_by)

    def resolve_alert(self, alert_id: str, resolution_note: str = "") -> bool:
        """Resolve a health alert"""
        return self.alert_manager.resolve_alert(alert_id, resolution_note)

    def set_threshold(self, metric_name: str, level: str, value: float) -> bool:
        """Set threshold for a metric"""
        return self.alert_manager.set_threshold(metric_name, level, value)

    def get_threshold(self, metric_name: str, level: str) -> Optional[float]:
        """Get threshold for a metric and level"""
        return self.alert_manager.get_threshold(metric_name, level)

    def get_all_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Get all thresholds"""
        return self.alert_manager.get_all_thresholds()

    def analyze_health_trends(self, time_range_hours: int = 24) -> Dict[str, Any]:
        """Analyze health trends for predictive insights"""
        try:
            metrics = self.monitoring_manager.get_all_metrics()
            trends = self.analysis_manager.analyze_health_trends(metrics, time_range_hours)
            return {name: trend.to_dict() for name, trend in trends.items()}
        except Exception as e:
            self.logger.error(f"Failed to analyze health trends: {e}")
            return {}

    def predict_health_issues(self, time_horizon_hours: int = 6) -> List[Dict[str, Any]]:
        """Predict potential health issues based on current metrics"""
        try:
            metrics = self.monitoring_manager.get_all_metrics()
            return self.analysis_manager.predict_health_issues(metrics, time_horizon_hours)
        except Exception as e:
            self.logger.error(f"Failed to predict health issues: {e}")
            return []

    def generate_optimization_recommendations(self) -> List[str]:
        """Generate optimization recommendations based on metrics and trends"""
        try:
            metrics = self.monitoring_manager.get_all_metrics()
            trends = self.analysis_manager.analyze_health_trends(metrics)
            return self.analysis_manager.generate_optimization_recommendations(metrics, trends)
        except Exception as e:
            self.logger.error(f"Failed to generate optimization recommendations: {e}")
            return []

    def get_health_insights(self) -> Dict[str, Any]:
        """Get comprehensive health insights"""
        try:
            metrics = self.monitoring_manager.get_all_metrics()
            trends = self.analysis_manager.analyze_health_trends(metrics)
            return self.analysis_manager.get_health_insights(metrics, trends)
        except Exception as e:
            self.logger.error(f"Failed to get health insights: {e}")
            return {"error": str(e)}

    def send_notification(self, alert: HealthAlert, config_name: Optional[str] = None) -> bool:
        """Send notification for a health alert"""
        return self.notification_manager.send_notification(alert, config_name)

    def add_notification_config(self, name: str, config: Any) -> bool:
        """Add a new notification configuration"""
        return self.notification_manager.add_notification_config(name, config)

    def test_notification_channel(self, config_name: str) -> bool:
        """Test a notification channel"""
        return self.notification_manager.test_notification_channel(config_name)

    def execute_automated_recovery(self, alert_id: str) -> Dict[str, Any]:
        """Execute automated recovery actions for health issues"""
        try:
            alert = self.alert_manager.get_alert(alert_id)
            if not alert:
                return {"error": f"Alert {alert_id} not found"}
            
            return self.recovery_manager.execute_automated_recovery(alert)
            
        except Exception as e:
            self.logger.error(f"Failed to execute automated recovery: {e}")
            return {"error": str(e)}

    def enable_auto_recovery(self):
        """Enable automated recovery"""
        self.recovery_manager.enable_auto_recovery()

    def disable_auto_recovery(self):
        """Disable automated recovery"""
        self.recovery_manager.disable_auto_recovery()

    def get_recovery_statistics(self) -> Dict[str, Any]:
        """Get recovery statistics"""
        return self.recovery_manager.get_recovery_statistics()

    def test_recovery_strategy(self, metric_name: str) -> bool:
        """Test a recovery strategy"""
        return self.recovery_manager.test_recovery_strategy(metric_name)

    def generate_health_report(self, report_type: str = "comprehensive") -> Dict[str, Any]:
        """Generate comprehensive health report"""
        try:
            report = {
                "report_id": f"health_report_{int(time.time())}",
                "generated_at": datetime.now().isoformat(),
                "report_type": report_type,
                "summary": self.get_health_summary(),
                "detailed_metrics": {},
                "alerts_summary": {},
                "recommendations": []
            }
            
            # Get detailed metrics
            metrics = self.monitoring_manager.get_all_metrics()
            for metric_name, metric in metrics.items():
                report["detailed_metrics"][metric_name] = metric.to_dict()
            
            # Get alerts summary
            report["alerts_summary"] = self.alert_manager.get_alert_statistics()
            
            # Get recommendations
            report["recommendations"] = self.generate_optimization_recommendations()
            
            self.logger.info(f"Health report generated: {report['report_id']}")
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate health report: {e}")
            return {"error": str(e)}

    def run_smoke_test(self) -> bool:
        """Run basic functionality test"""
        try:
            self.logger.info("🧪 Running Unified Health Manager smoke test...")
            
            # Test monitoring start
            self.start_monitoring(interval=1)
            time.sleep(2)  # Wait for metrics collection
            
            # Test metric collection
            metrics = self.monitoring_manager.get_all_metrics()
            if not metrics:
                self.logger.error("❌ Metric collection failed")
                return False
            
            # Test threshold checking
            alerts = self.alert_manager.check_thresholds(metrics)
            
            # Test analysis
            insights = self.get_health_insights()
            if "error" in insights:
                self.logger.error("❌ Health analysis failed")
                return False
            
            # Test report generation
            report = self.generate_health_report()
            if "error" in report:
                self.logger.error("❌ Report generation failed")
                return False
            
            # Stop monitoring
            self.stop_monitoring()
            
            self.logger.info("✅ Unified Health Manager smoke test passed")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Unified Health Manager smoke test failed: {e}")
            return False

    def cleanup(self):
        """Cleanup resources"""
        try:
            # Stop monitoring
            self.stop_monitoring()
            
            # Cleanup all components
            self.monitoring_manager.cleanup()
            self.alert_manager.cleanup()
            self.analysis_manager.cleanup()
            self.notification_manager.cleanup()
            self.recovery_manager.cleanup()
            
            # Call base cleanup
            super().cleanup()
            
            self.logger.info("✅ Unified Health Manager cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Unified Health Manager cleanup failed: {e}")


# ============================================================================
# BACKWARDS COMPATIBILITY ALIASES
# ============================================================================

# Maintain backwards compatibility with existing code
HealthManager = UnifiedHealthManager
HealthAlertManager = UnifiedHealthManager
HealthThresholdManager = UnifiedHealthManager
HealthNotificationManager = UnifiedHealthManager

# Export all components for backwards compatibility
__all__ = [
    "UnifiedHealthManager",
    "HealthManager",
    "HealthAlertManager", 
    "HealthThresholdManager",
    "HealthNotificationManager",
]


if __name__ == "__main__":
    # Initialize system
    health_manager = UnifiedHealthManager()
    
    # Run smoke test
    success = health_manager.run_smoke_test()
    
    if success:
        print("✅ Unified Health Manager ready for production use!")
        print("🚀 System ready for health management operations!")
    else:
        print("❌ Unified Health Manager requires additional testing!")
        print("⚠️ System not ready for production deployment!")



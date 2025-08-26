#!/usr/bin/env python3
"""
Performance Alert Manager - V2 Core Performance System
======================================================

Handles performance alerting and notification management.
Follows Single Responsibility Principle - alert management only.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable

from src.utils.stability_improvements import stability_manager, safe_import
from .alert_core import AlertSeverity, AlertType, PerformanceAlert
from .performance_monitor import PerformanceMonitor


class AlertManager:
    """
    Performance alert management and notification system
    
    Responsibilities:
    - Manage alert storage and retrieval
    - Handle alert notifications and escalation
    - Track alert history and resolution
    """
    
    def __init__(self):
        self.alerts: Dict[str, PerformanceAlert] = {}
        self.alert_handlers: Dict[AlertSeverity, List[Callable]] = {
            severity: [] for severity in AlertSeverity
        }
        
        self.logger = logging.getLogger(f"{__name__}.AlertManager")
        self.performance_monitor = PerformanceMonitor()
    
    def check_benchmark_for_alerts(self, benchmark) -> List[PerformanceAlert]:
        """Check a benchmark result for alert conditions"""
        try:
            alerts = self.performance_monitor.check_benchmark_for_alerts(benchmark)
            
            # Store and trigger alerts
            for alert in alerts:
                self._store_and_trigger_alert(alert)
            
            return alerts
            
        except Exception as e:
            self.logger.error(f"Failed to check benchmark for alerts: {e}")
            return []
    
    def register_alert_handler(self, severity: AlertSeverity, handler: Callable[[PerformanceAlert], None]) -> None:
        """Register an alert handler for a specific severity level"""
        try:
            self.alert_handlers[severity].append(handler)
            self.logger.info(f"Registered alert handler for {severity.value} alerts")
            
        except Exception as e:
            self.logger.error(f"Failed to register alert handler: {e}")
    
    def trigger_alert(self, alert: PerformanceAlert) -> bool:
        """Trigger an alert and notify handlers"""
        try:
            # Call registered handlers for this severity level
            handlers = self.alert_handlers.get(alert.severity, [])
            
            for handler in handlers:
                try:
                    handler(alert)
                except Exception as e:
                    self.logger.error(f"Alert handler failed: {e}")
            
            # Also call handlers for higher severity levels if this is critical
            if alert.severity == AlertSeverity.CRITICAL:
                for severity in [AlertSeverity.HIGH, AlertSeverity.MEDIUM, AlertSeverity.LOW]:
                    for handler in self.alert_handlers.get(severity, []):
                        try:
                            handler(alert)
                        except Exception as e:
                            self.logger.error(f"Escalated alert handler failed: {e}")
            
            self.logger.info(f"Triggered alert: {alert.alert_id} ({alert.severity.value})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to trigger alert: {e}")
            return False
    
    def resolve_alert(self, alert_id: str, resolution_note: str = "") -> bool:
        """Mark an alert as resolved"""
        try:
            alert = self.alerts.get(alert_id)
            if not alert:
                self.logger.warning(f"Alert not found: {alert_id}")
                return False
            
            alert.is_resolved = True
            alert.resolved_at = datetime.now().isoformat()
            alert.metadata["resolution_note"] = resolution_note
            
            self.logger.info(f"Resolved alert: {alert_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to resolve alert: {e}")
            return False
    
    def get_active_alerts(self) -> List[PerformanceAlert]:
        """Get all active (unresolved) alerts"""
        return [alert for alert in self.alerts.values() if not alert.is_resolved]
    
    def get_alerts_by_severity(self, severity: AlertSeverity) -> List[PerformanceAlert]:
        """Get alerts filtered by severity"""
        return [alert for alert in self.alerts.values() if alert.severity == severity]
    
    def get_alerts_by_type(self, alert_type: AlertType) -> List[PerformanceAlert]:
        """Get alerts filtered by type"""
        return [alert for alert in self.alerts.values() if alert.alert_type == alert_type]
    
    def get_recent_alerts(self, hours: int = 24) -> List[PerformanceAlert]:
        """Get alerts from the last N hours"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            cutoff_str = cutoff_time.isoformat()
            
            return [
                alert for alert in self.alerts.values()
                if alert.triggered_at >= cutoff_str
            ]
            
        except Exception as e:
            self.logger.error(f"Failed to get recent alerts: {e}")
            return []
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get summary of all alerts"""
        try:
            total_alerts = len(self.alerts)
            active_alerts = len(self.get_active_alerts())
            
            # Count by severity
            severity_counts = {}
            for severity in AlertSeverity:
                severity_counts[severity.value] = len(self.get_alerts_by_severity(severity))
            
            # Count by type
            type_counts = {}
            for alert_type in AlertType:
                type_counts[alert_type.value] = len(self.get_alerts_by_type(alert_type))
            
            # Recent activity
            recent_alerts = len(self.get_recent_alerts(24))
            
            return {
                "total_alerts": total_alerts,
                "active_alerts": active_alerts,
                "resolved_alerts": total_alerts - active_alerts,
                "alerts_by_severity": severity_counts,
                "alerts_by_type": type_counts,
                "recent_alerts_24h": recent_alerts,
                "alert_rate": recent_alerts / 24.0,  # alerts per hour
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get alert summary: {e}")
            return {"error": str(e)}
    
    def _store_and_trigger_alert(self, alert: PerformanceAlert) -> None:
        """Store an alert and trigger notifications"""
        try:
            self.alerts[alert.alert_id] = alert
            self.trigger_alert(alert)
            
        except Exception as e:
            self.logger.error(f"Failed to store and trigger alert: {e}")
    
    def clear_alerts(self) -> None:
        """Clear all stored alerts"""
        self.alerts.clear()
        self.logger.info("Cleared all alerts")
    
    def clear_resolved_alerts(self) -> int:
        """Clear resolved alerts and return count of cleared alerts"""
        try:
            resolved_count = 0
            alert_ids_to_remove = []
            
            for alert_id, alert in self.alerts.items():
                if alert.is_resolved:
                    alert_ids_to_remove.append(alert_id)
                    resolved_count += 1
            
            for alert_id in alert_ids_to_remove:
                del self.alerts[alert_id]
            
            self.logger.info(f"Cleared {resolved_count} resolved alerts")
            return resolved_count
            
        except Exception as e:
            self.logger.error(f"Failed to clear resolved alerts: {e}")
            return 0

#!/usr/bin/env python3
"""
Health Alert Manager - V2 Modular Architecture
=============================================

Handles health alert creation, management, and threshold checking.
Follows V2 standards: OOP design, SRP, BaseManager inheritance.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import time
from typing import Any, Dict, List, Optional
from datetime import datetime

from ...base_manager import BaseManager
from ...base import ConfigMixin, LoggingMixin, ValidationMixin
from ..types.health_types import HealthAlert, AlertType, HealthLevel, HealthMetric
from .alert_config import DEFAULT_THRESHOLDS


class HealthAlertManager(LoggingMixin, ConfigMixin, ValidationMixin, BaseManager):
    """Health Alert Manager - inherits from BaseManager for unified lifecycle management"""
    
    def __init__(self):
        super().__init__(
            manager_id="health_alert_manager",
            name="Health Alert Manager",
            description="Manages health alerts and threshold monitoring"
        )
        
        self.health_alerts: Dict[str, HealthAlert] = {}
        self.thresholds: Dict[str, Dict[str, float]] = DEFAULT_THRESHOLDS.copy()
        self.auto_resolve_enabled = True
        self.alert_timeout = 3600
        self.max_alerts = 1000
        self.logger.info("✅ Health Alert Manager initialized successfully")

    # ============================================================================
    # LIFECYCLE HOOKS - Required by BaseManager
    # ============================================================================
    
    def _on_start(self) -> bool:
        try:
            self.logger.info("Starting Health Alert Manager...")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start Health Alert Manager: {e}")
            return False
    
    def _on_stop(self):
        try:
            self.logger.info("Stopping Health Alert Manager...")
            self.clear_alerts()
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
    
    def _on_heartbeat(self):
        try:
            if self.auto_resolve_enabled:
                self.auto_resolve_alerts()
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
    
    def _on_initialize_resources(self) -> bool:
        try:
            self.thresholds = DEFAULT_THRESHOLDS.copy()
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False
    
    def _on_cleanup_resources(self):
        try:
            self.clear_alerts()
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
    
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        try:
            self.logger.warning(f"Recovery attempt for {context}: {error}")
            return True
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False

    # ============================================================================
    # CORE HEALTH ALERT FUNCTIONALITY
    # ============================================================================

    def set_threshold(self, metric_name: str, level: str, value: float) -> bool:
        try:
            if metric_name not in self.thresholds:
                self.thresholds[metric_name] = {}
            self.thresholds[metric_name][level] = value
            self.logger.info(f"Threshold set for {metric_name}.{level}: {value}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to set threshold for {metric_name}.{level}: {e}")
            return False

    def get_threshold(self, metric_name: str, level: str) -> Optional[float]:
        return self.thresholds.get(metric_name, {}).get(level)

    def get_all_thresholds(self) -> Dict[str, Dict[str, float]]:
        return self.thresholds.copy()

    def check_thresholds(self, metrics: Dict[str, HealthMetric]) -> List[HealthAlert]:
        try:
            new_alerts = []
            for metric_name, metric in metrics.items():
                if metric_name not in self.thresholds:
                    continue
                
                thresholds = self.thresholds[metric_name]
                value = metric.value
                
                for level_name, threshold_value in thresholds.items():
                    if value >= threshold_value:
                        alert_exists = any(
                            alert.metric_name == metric_name and 
                            alert.threshold == threshold_value and 
                            not alert.resolved
                            for alert in self.health_alerts.values()
                        )
                        
                        if not alert_exists:
                            alert = self._create_alert(metric_name, value, threshold_value, level_name)
                            if alert:
                                new_alerts.append(alert)
                        break
            
            return new_alerts
        except Exception as e:
            self.logger.error(f"Failed to check thresholds: {e}")
            return []

    def _create_alert(self, metric_name: str, value: float, threshold: float, level_name: str) -> Optional[HealthAlert]:
        try:
            alert_id = f"alert_{metric_name}_{int(time.time())}"
            
            alert_type_map = {
                "warning": AlertType.WARNING,
                "critical": AlertType.ERROR,
                "emergency": AlertType.CRITICAL
            }
            health_level_map = {
                "warning": HealthLevel.WARNING,
                "critical": HealthLevel.CRITICAL,
                "emergency": HealthLevel.EMERGENCY
            }
            
            alert = HealthAlert(
                id=alert_id,
                type=alert_type_map.get(level_name, AlertType.WARNING),
                level=health_level_map.get(level_name, HealthLevel.WARNING),
                component=metric_name,
                message=f"{metric_name} exceeded {level_name} threshold: {value} >= {threshold}",
                metric_name=metric_name,
                metric_value=value,
                threshold=threshold,
                timestamp=datetime.now().isoformat(),
                acknowledged=False,
                acknowledged_by=None,
                acknowledged_at=None,
                resolved=False,
                resolved_at=None,
                metadata={"threshold_level": level_name}
            )
            
            self.health_alerts[alert_id] = alert
            
            if len(self.health_alerts) > self.max_alerts:
                self._cleanup_old_alerts()
            
            self.logger.warning(f"Health alert created: {metric_name} = {value} (threshold: {threshold})")
            return alert
        except Exception as e:
            self.logger.error(f"Failed to create alert: {e}")
            return None

    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        try:
            if alert_id not in self.health_alerts:
                self.logger.warning(f"Alert not found: {alert_id}")
                return False
            
            alert = self.health_alerts[alert_id]
            alert.acknowledged = True
            alert.acknowledged_by = acknowledged_by
            alert.acknowledged_at = datetime.now().isoformat()
            
            self.logger.info(f"Alert {alert_id} acknowledged by {acknowledged_by}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to acknowledge alert {alert_id}: {e}")
            return False

    def resolve_alert(self, alert_id: str, resolution_note: str = "") -> bool:
        try:
            if alert_id not in self.health_alerts:
                self.logger.warning(f"Alert not found: {alert_id}")
                return False
            
            alert = self.health_alerts[alert_id]
            alert.resolved = True
            alert.resolved_at = datetime.now().isoformat()
            
            if resolution_note:
                alert.message += f" - RESOLVED: {resolution_note}"
            
            self.logger.info(f"Alert {alert_id} resolved: {resolution_note}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to resolve alert {alert_id}: {e}")
            return False

    def get_alert(self, alert_id: str) -> Optional[HealthAlert]:
        return self.health_alerts.get(alert_id)

    def get_active_alerts(self) -> List[HealthAlert]:
        return [alert for alert in self.health_alerts.values() if not alert.resolved]

    def get_all_alerts(self) -> List[HealthAlert]:
        return list(self.health_alerts.values())

    def auto_resolve_alerts(self):
        try:
            current_time = datetime.now()
            alerts_to_resolve = []
            
            for alert_id, alert in self.health_alerts.items():
                if alert.resolved:
                    continue
                
                alert_time = datetime.fromisoformat(alert.timestamp)
                time_diff = (current_time - alert_time).total_seconds()
                
                if time_diff > self.alert_timeout:
                    alerts_to_resolve.append(alert_id)
            
            for alert_id in alerts_to_resolve:
                self.resolve_alert(alert_id, "Auto-resolved after timeout")
        except Exception as e:
            self.logger.error(f"Failed to auto-resolve alerts: {e}")

    def _cleanup_old_alerts(self):
        try:
            resolved_alerts = [
                alert_id for alert_id, alert in self.health_alerts.items()
                if alert.resolved
            ]
            
            if len(resolved_alerts) > self.max_alerts // 2:
                alerts_to_remove = resolved_alerts[self.max_alerts // 2:]
                for alert_id in alerts_to_remove:
                    del self.health_alerts[alert_id]
                self.logger.info(f"Cleaned up {len(alerts_to_remove)} old resolved alerts")
        except Exception as e:
            self.logger.error(f"Failed to cleanup old alerts: {e}")

    def get_alert_statistics(self) -> Dict[str, Any]:
        try:
            total_alerts = len(self.health_alerts)
            active_alerts = len([a for a in self.health_alerts.values() if not a.resolved])
            acknowledged_alerts = len([a for a in self.health_alerts.values() if a.acknowledged and not a.resolved])
            resolved_alerts = len([a for a in self.health_alerts.values() if a.resolved])
            
            level_counts = {}
            type_counts = {}
            for alert in self.health_alerts.values():
                level = alert.level.value
                alert_type = alert.type.value
                level_counts[level] = level_counts.get(level, 0) + 1
                type_counts[alert_type] = type_counts.get(alert_type, 0) + 1
            
            return {
                "total_alerts": total_alerts,
                "active_alerts": active_alerts,
                "acknowledged_alerts": acknowledged_alerts,
                "resolved_alerts": resolved_alerts,
                "level_distribution": level_counts,
                "type_distribution": type_counts,
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Failed to get alert statistics: {e}")
            return {"error": str(e)}

    def clear_alerts(self):
        try:
            self.health_alerts.clear()
            self.logger.info("✅ All alerts cleared")
        except Exception as e:
            self.logger.error(f"Failed to clear alerts: {e}")

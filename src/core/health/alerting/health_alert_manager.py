#!/usr/bin/env python3
"""
Health Alert Manager - V2 Modular Architecture
=============================================

Handles health alert creation, management, and threshold checking.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
from threading import Lock

from ..types.health_types import HealthAlert, AlertType, HealthLevel, HealthMetric


logger = logging.getLogger(__name__)


class HealthAlertManager:
    """
    Health Alert Manager - Single responsibility: Manage health alerts
    
    Handles all health alert operations including:
    - Alert creation and management
    - Threshold checking
    - Alert lifecycle management
    - Alert statistics and reporting
    """

    def __init__(self):
        """Initialize health alert manager"""
        self.logger = logging.getLogger(f"{__name__}.HealthAlertManager")
        
        # Alert storage
        self.health_alerts: Dict[str, HealthAlert] = {}
        
        # Thresholds
        self.thresholds: Dict[str, Dict[str, float]] = {}
        
        # Configuration
        self.auto_resolve_alerts = True
        self.alert_timeout = 3600  # 1 hour
        self.max_alerts = 1000
        
        # Thread safety
        self._lock = Lock()
        
        # Setup default thresholds
        self._setup_default_thresholds()
        
        self.logger.info("✅ Health Alert Manager initialized successfully")

    def _setup_default_thresholds(self):
        """Setup default health thresholds"""
        try:
            self.thresholds = {
                "cpu_usage": {"warning": 70.0, "critical": 90.0, "emergency": 95.0},
                "memory_usage": {"warning": 75.0, "critical": 90.0, "emergency": 95.0},
                "disk_usage": {"warning": 80.0, "critical": 90.0, "emergency": 95.0},
                "response_time": {"warning": 2.0, "critical": 5.0, "emergency": 10.0},
                "error_rate": {"warning": 5.0, "critical": 15.0, "emergency": 25.0}
            }
        except Exception as e:
            self.logger.error(f"Failed to setup default thresholds: {e}")

    def set_threshold(self, metric_name: str, level: str, value: float) -> bool:
        """Set threshold for a metric"""
        try:
            with self._lock:
                if metric_name not in self.thresholds:
                    self.thresholds[metric_name] = {}
                
                self.thresholds[metric_name][level] = value
                
                self.logger.info(f"Threshold set for {metric_name}.{level}: {value}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to set threshold for {metric_name}.{level}: {e}")
            return False

    def get_threshold(self, metric_name: str, level: str) -> Optional[float]:
        """Get threshold for a metric and level"""
        try:
            with self._lock:
                return self.thresholds.get(metric_name, {}).get(level)
        except Exception as e:
            self.logger.error(f"Failed to get threshold for {metric_name}.{level}: {e}")
            return None

    def get_all_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Get all thresholds"""
        try:
            with self._lock:
                return self.thresholds.copy()
        except Exception as e:
            self.logger.error(f"Failed to get all thresholds: {e}")
            return {}

    def check_thresholds(self, metrics: Dict[str, HealthMetric]) -> List[HealthAlert]:
        """Check metrics against thresholds and generate alerts"""
        try:
            new_alerts = []
            
            with self._lock:
                for metric_name, metric in metrics.items():
                    if metric_name not in self.thresholds:
                        continue
                    
                    thresholds = self.thresholds[metric_name]
                    value = metric.value
                    
                    # Check each threshold level
                    for level_name, threshold_value in thresholds.items():
                        if value >= threshold_value:
                            # Check if alert already exists
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
                            
                            break  # Only create one alert per metric
            
            return new_alerts
                
        except Exception as e:
            self.logger.error(f"Failed to check thresholds: {e}")
            return []

    def _create_alert(self, metric_name: str, value: float, threshold: float, level_name: str) -> Optional[HealthAlert]:
        """Create a new health alert"""
        try:
            alert_id = f"alert_{metric_name}_{int(time.time())}"
            
            # Map threshold level to alert type
            alert_type_map = {
                "warning": AlertType.WARNING,
                "critical": AlertType.ERROR,
                "emergency": AlertType.CRITICAL
            }
            
            alert_type = alert_type_map.get(level_name, AlertType.WARNING)
            
            # Map threshold level to health level
            health_level_map = {
                "warning": HealthLevel.WARNING,
                "critical": HealthLevel.CRITICAL,
                "emergency": HealthLevel.EMERGENCY
            }
            
            health_level = health_level_map.get(level_name, HealthLevel.WARNING)
            
            alert = HealthAlert(
                id=alert_id,
                type=alert_type,
                level=health_level,
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
            
            with self._lock:
                self.health_alerts[alert_id] = alert
                
                # Cleanup old alerts if limit exceeded
                if len(self.health_alerts) > self.max_alerts:
                    self._cleanup_old_alerts()
            
            self.logger.warning(f"Health alert created: {metric_name} = {value} (threshold: {threshold})")
            return alert
                
        except Exception as e:
            self.logger.error(f"Failed to create alert: {e}")
            return None

    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge a health alert"""
        try:
            with self._lock:
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
        """Resolve a health alert"""
        try:
            with self._lock:
                if alert_id not in self.health_alerts:
                    self.logger.warning(f"Alert not found: {alert_id}")
                    return False
                
                alert = self.health_alerts[alert_id]
                alert.resolved = True
                alert.resolved_at = datetime.now().isoformat()
                
                # Update message with resolution note
                if resolution_note:
                    alert.message += f" - RESOLVED: {resolution_note}"
                
                self.logger.info(f"Alert {alert_id} resolved: {resolution_note}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to resolve alert {alert_id}: {e}")
            return False

    def get_alert(self, alert_id: str) -> Optional[HealthAlert]:
        """Get a specific health alert"""
        try:
            with self._lock:
                return self.health_alerts.get(alert_id)
        except Exception as e:
            self.logger.error(f"Failed to get alert {alert_id}: {e}")
            return None

    def get_active_alerts(self) -> List[HealthAlert]:
        """Get list of active (unresolved) alerts"""
        try:
            with self._lock:
                return [
                    alert for alert in self.health_alerts.values()
                    if not alert.resolved
                ]
        except Exception as e:
            self.logger.error(f"Failed to get active alerts: {e}")
            return []

    def get_all_alerts(self) -> List[HealthAlert]:
        """Get all health alerts"""
        try:
            with self._lock:
                return list(self.health_alerts.values())
        except Exception as e:
            self.logger.error(f"Failed to get all alerts: {e}")
            return []

    def auto_resolve_alerts(self):
        """Auto-resolve old alerts"""
        try:
            current_time = datetime.now()
            alerts_to_resolve = []
            
            with self._lock:
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
        """Clean up old resolved alerts"""
        try:
            with self._lock:
                resolved_alerts = [
                    alert_id for alert_id, alert in self.health_alerts.items()
                    if alert.resolved
                ]
                
                # Keep only recent resolved alerts
                if len(resolved_alerts) > self.max_alerts // 2:
                    alerts_to_remove = resolved_alerts[self.max_alerts // 2:]
                    for alert_id in alerts_to_remove:
                        del self.health_alerts[alert_id]
                    
                    self.logger.info(f"Cleaned up {len(alerts_to_remove)} old resolved alerts")
                    
        except Exception as e:
            self.logger.error(f"Failed to cleanup old alerts: {e}")

    def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alert statistics"""
        try:
            with self._lock:
                total_alerts = len(self.health_alerts)
                active_alerts = len([a for a in self.health_alerts.values() if not a.resolved])
                acknowledged_alerts = len([a for a in self.health_alerts.values() if a.acknowledged and not a.resolved])
                resolved_alerts = len([a for a in self.health_alerts.values() if a.resolved])
                
                # Count alerts by level
                level_counts = {}
                for alert in self.health_alerts.values():
                    level = alert.level.value
                    level_counts[level] = level_counts.get(level, 0) + 1
                
                # Count alerts by type
                type_counts = {}
                for alert in self.health_alerts.values():
                    alert_type = alert.type.value
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
        """Clear all alerts"""
        try:
            with self._lock:
                self.health_alerts.clear()
                self.logger.info("✅ All alerts cleared")
        except Exception as e:
            self.logger.error(f"Failed to clear alerts: {e}")

    def cleanup(self):
        """Cleanup resources"""
        try:
            self.clear_alerts()
            self.logger.info("✅ Health Alert Manager cleanup completed")
        except Exception as e:
            self.logger.error(f"Health Alert Manager cleanup failed: {e}")



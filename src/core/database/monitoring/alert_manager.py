#!/usr/bin/env python3
"""
V3-003: Database Alert Manager
=============================

Alert management component for database monitoring system.
V2 Compliant: ≤400 lines, single responsibility, KISS principle.
"""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class Alert:
    alert_id: str
    metric_name: str
    alert_level: AlertLevel
    message: str
    threshold: float
    current_value: float
    timestamp: datetime
    resolved: bool = False


@dataclass
class MetricThreshold:
    metric_name: str
    warning_threshold: float
    critical_threshold: float
    unit: str = ""
    description: str = ""


class AlertManager:
    """Database alert management component."""
    
    def __init__(self):
        """Initialize alert manager."""
        self.alerts: List[Alert] = []
        self.thresholds: Dict[str, MetricThreshold] = {}
        self._initialize_default_thresholds()
        logger.info("🚨 Alert Manager initialized")
    
    async def check_metrics_for_alerts(self, metrics: List[Any]) -> List[Alert]:
        """Check metrics against thresholds and generate alerts."""
        try:
            new_alerts = []
            
            for metric in metrics:
                if metric.metric_name in self.thresholds:
                    threshold = self.thresholds[metric.metric_name]
                    
                    # Check critical threshold
                    if metric.value >= threshold.critical_threshold:
                        alert = await self._create_alert(metric, AlertLevel.CRITICAL, threshold.critical_threshold)
                        new_alerts.append(alert)
                    # Check warning threshold
                    elif metric.value >= threshold.warning_threshold:
                        alert = await self._create_alert(metric, AlertLevel.WARNING, threshold.warning_threshold)
                        new_alerts.append(alert)
            
            # Add new alerts to the list
            self.alerts.extend(new_alerts)
            
            return new_alerts
            
        except Exception as e:
            logger.error(f"❌ Error checking metrics for alerts: {e}")
            return []
    
    async def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert."""
        try:
            for alert in self.alerts:
                if alert.alert_id == alert_id:
                    alert.resolved = True
                    logger.info(f"✅ Alert resolved: {alert_id}")
                    return True
            
            logger.warning(f"⚠️ Alert not found: {alert_id}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error resolving alert: {e}")
            return False
    
    async def get_active_alerts(self) -> List[Alert]:
        """Get all active (unresolved) alerts."""
        try:
            return [alert for alert in self.alerts if not alert.resolved]
        except Exception as e:
            logger.error(f"❌ Error getting active alerts: {e}")
            return []
    
    async def get_alerts_by_level(self, level: AlertLevel) -> List[Alert]:
        """Get alerts by level."""
        try:
            return [alert for alert in self.alerts if alert.alert_level == level and not alert.resolved]
        except Exception as e:
            logger.error(f"❌ Error getting alerts by level: {e}")
            return []
    
    async def get_alert_summary(self) -> Dict[str, Any]:
        """Get alert summary statistics."""
        try:
            active_alerts = await self.get_active_alerts()
            
            summary = {
                "total_alerts": len(self.alerts),
                "active_alerts": len(active_alerts),
                "resolved_alerts": len([a for a in self.alerts if a.resolved]),
                "alerts_by_level": {
                    level.value: len([a for a in active_alerts if a.alert_level == level])
                    for level in AlertLevel
                },
                "recent_alerts": sorted(self.alerts, key=lambda x: x.timestamp, reverse=True)[:10]
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Error getting alert summary: {e}")
            return {"error": str(e)}
    
    async def cleanup_old_alerts(self, hours: int = 24) -> int:
        """Clean up old resolved alerts."""
        try:
            cutoff_time = datetime.now(timezone.utc).replace(hour=datetime.now().hour - hours)
            
            old_alerts = [
                alert for alert in self.alerts 
                if alert.resolved and alert.timestamp < cutoff_time
            ]
            
            for alert in old_alerts:
                self.alerts.remove(alert)
            
            logger.info(f"✅ Cleaned up {len(old_alerts)} old alerts")
            return len(old_alerts)
            
        except Exception as e:
            logger.error(f"❌ Error cleaning up old alerts: {e}")
            return 0
    
    async def _create_alert(self, metric: Any, level: AlertLevel, threshold: float) -> Alert:
        """Create an alert for a metric."""
        try:
            alert_id = f"alert_{metric.metric_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            alert = Alert(
                alert_id=alert_id,
                metric_name=metric.metric_name,
                alert_level=level,
                message=f"{metric.metric_name} exceeded {level.value} threshold",
                threshold=threshold,
                current_value=metric.value,
                timestamp=datetime.now(timezone.utc)
            )
            
            logger.warning(f"⚠️ Alert created: {alert.message}")
            return alert
            
        except Exception as e:
            logger.error(f"❌ Error creating alert: {e}")
            raise
    
    def _initialize_default_thresholds(self):
        """Initialize default metric thresholds."""
        default_thresholds = [
            MetricThreshold("connection_count", 80, 95, "connections", "Active connections"),
            MetricThreshold("cpu_usage", 70, 90, "%", "CPU usage"),
            MetricThreshold("memory_usage", 80, 95, "%", "Memory usage"),
            MetricThreshold("disk_usage", 85, 95, "%", "Disk usage"),
            MetricThreshold("query_duration", 1000, 5000, "ms", "Query duration"),
            MetricThreshold("lock_wait_time", 100, 1000, "ms", "Lock wait time")
        ]
        
        for threshold in default_thresholds:
            self.thresholds[threshold.metric_name] = threshold
    
    def add_threshold(self, threshold: MetricThreshold):
        """Add a new metric threshold."""
        try:
            self.thresholds[threshold.metric_name] = threshold
            logger.info(f"✅ Added threshold for metric: {threshold.metric_name}")
        except Exception as e:
            logger.error(f"❌ Error adding threshold: {e}")
    
    def remove_threshold(self, metric_name: str) -> bool:
        """Remove a metric threshold."""
        try:
            if metric_name in self.thresholds:
                del self.thresholds[metric_name]
                logger.info(f"✅ Removed threshold for metric: {metric_name}")
                return True
            else:
                logger.warning(f"⚠️ Threshold not found for metric: {metric_name}")
                return False
        except Exception as e:
            logger.error(f"❌ Error removing threshold: {e}")
            return False
    
    def get_thresholds(self) -> Dict[str, MetricThreshold]:
        """Get all metric thresholds."""
        return self.thresholds
    
    def update_threshold(self, metric_name: str, warning_threshold: float, critical_threshold: float):
        """Update an existing threshold."""
        try:
            if metric_name in self.thresholds:
                self.thresholds[metric_name].warning_threshold = warning_threshold
                self.thresholds[metric_name].critical_threshold = critical_threshold
                logger.info(f"✅ Updated threshold for metric: {metric_name}")
            else:
                logger.warning(f"⚠️ Threshold not found for metric: {metric_name}")
        except Exception as e:
            logger.error(f"❌ Error updating threshold: {e}")


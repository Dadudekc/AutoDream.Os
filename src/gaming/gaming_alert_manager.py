"""
Gaming Alert Manager

Manages alerts and notifications for gaming and entertainment systems,
providing real-time monitoring and alert handling capabilities.

Author: Agent-6 - Gaming & Entertainment Specialist
"""

import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels for gaming systems."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertType(Enum):
    """Types of alerts for gaming and entertainment systems."""
    PERFORMANCE = "performance"
    SYSTEM_HEALTH = "system_health"
    USER_ENGAGEMENT = "user_engagement"
    GAME_STATE = "game_state"
    ENTERTAINMENT_SYSTEM = "entertainment_system"
    INTEGRATION_ERROR = "integration_error"


@dataclass
class GamingAlert:
    """Represents a gaming system alert."""
    id: str
    type: AlertType
    severity: AlertSeverity
    message: str
    timestamp: datetime
    source: str
    metadata: Dict[str, Any]
    acknowledged: bool = False
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None


class GamingAlertManager:
    """
    Manages alerts for gaming and entertainment systems.
    
    Provides comprehensive alert handling including creation, acknowledgment,
    resolution, and monitoring capabilities.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the gaming alert manager."""
        self.config = config or {}
        self.alerts: Dict[str, GamingAlert] = {}
        self.alert_counters = {
            alert_type: 0 for alert_type in AlertType
        }
        self.severity_thresholds = {
            AlertSeverity.LOW: 10,
            AlertSeverity.MEDIUM: 5,
            AlertSeverity.HIGH: 3,
            AlertSeverity.CRITICAL: 1
        }
        self._initialize_resources()
    
    def _initialize_resources(self):
        """Initialize alert manager resources."""
        logger.info("Initializing Gaming Alert Manager resources")
        self._load_alert_history()
        self._setup_monitoring()
    
    def _load_alert_history(self):
        """Load alert history from persistent storage."""
        try:
            # Load from file or database
            logger.info("Loading alert history")
        except Exception as e:
            logger.warning(f"Could not load alert history: {e}")
    
    def _setup_monitoring(self):
        """Setup monitoring for gaming systems."""
        logger.info("Setting up gaming system monitoring")
    
    def create_alert(
        self,
        alert_type: AlertType,
        severity: AlertSeverity,
        message: str,
        source: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> GamingAlert:
        """
        Create a new gaming alert.
        
        Args:
            alert_type: Type of alert
            severity: Alert severity level
            message: Alert message
            source: Source system
            metadata: Additional alert metadata
            
        Returns:
            Created GamingAlert instance
        """
        alert_id = f"gaming_alert_{int(time.time())}_{len(self.alerts)}"
        
        alert = GamingAlert(
            id=alert_id,
            type=alert_type,
            severity=severity,
            message=message,
            timestamp=datetime.now(),
            source=source,
            metadata=metadata or {}
        )
        
        self.alerts[alert_id] = alert
        self.alert_counters[alert_type] += 1
        
        logger.info(f"Created gaming alert: {alert_id} - {message}")
        return alert
    
    def check_performance_alerts(self, performance_metrics: Dict[str, Any]) -> List[GamingAlert]:
        """
        Check for performance-related alerts based on metrics.
        
        Args:
            performance_metrics: Current performance metrics
            
        Returns:
            List of created performance alerts
        """
        alerts = []
        
        # Check FPS performance
        fps = performance_metrics.get('fps', 0)
        if fps < 30:
            severity = AlertSeverity.CRITICAL if fps < 15 else AlertSeverity.HIGH
            alert = self.create_alert(
                AlertType.PERFORMANCE,
                severity,
                f"Low FPS detected: {fps} FPS",
                "performance_monitor",
                {"fps": fps, "threshold": 30}
            )
            alerts.append(alert)
        
        # Check memory usage
        memory_usage = performance_metrics.get('memory_usage', 0)
        if memory_usage > 80:
            severity = AlertSeverity.CRITICAL if memory_usage > 95 else AlertSeverity.HIGH
            alert = self.create_alert(
                AlertType.PERFORMANCE,
                severity,
                f"High memory usage: {memory_usage}%",
                "performance_monitor",
                {"memory_usage": memory_usage, "threshold": 80}
            )
            alerts.append(alert)
        
        # Check CPU usage
        cpu_usage = performance_metrics.get('cpu_usage', 0)
        if cpu_usage > 90:
            alert = self.create_alert(
                AlertType.PERFORMANCE,
                AlertSeverity.HIGH,
                f"High CPU usage: {cpu_usage}%",
                "performance_monitor",
                {"cpu_usage": cpu_usage, "threshold": 90}
            )
            alerts.append(alert)
        
        return alerts
    
    def check_system_health_alerts(self, health_metrics: Dict[str, Any]) -> List[GamingAlert]:
        """
        Check for system health alerts.
        
        Args:
            health_metrics: Current system health metrics
            
        Returns:
            List of created health alerts
        """
        alerts = []
        
        # Check disk space
        disk_usage = health_metrics.get('disk_usage', 0)
        if disk_usage > 85:
            alert = self.create_alert(
                AlertType.SYSTEM_HEALTH,
                AlertSeverity.MEDIUM,
                f"Low disk space: {100 - disk_usage}% free",
                "system_monitor",
                {"disk_usage": disk_usage, "threshold": 85}
            )
            alerts.append(alert)
        
        # Check network connectivity
        network_status = health_metrics.get('network_status', 'unknown')
        if network_status != 'connected':
            alert = self.create_alert(
                AlertType.SYSTEM_HEALTH,
                AlertSeverity.HIGH,
                f"Network connectivity issue: {network_status}",
                "network_monitor",
                {"network_status": network_status}
            )
            alerts.append(alert)
        
        return alerts
    
    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """
        Acknowledge an alert.
        
        Args:
            alert_id: ID of the alert to acknowledge
            acknowledged_by: User/agent acknowledging the alert
            
        Returns:
            True if alert was acknowledged, False otherwise
        """
        if alert_id not in self.alerts:
            logger.warning(f"Alert {alert_id} not found")
            return False
        
        alert = self.alerts[alert_id]
        alert.acknowledged = True
        alert.metadata['acknowledged_by'] = acknowledged_by
        alert.metadata['acknowledged_at'] = datetime.now().isoformat()
        
        logger.info(f"Alert {alert_id} acknowledged by {acknowledged_by}")
        return True
    
    def resolve_alert(self, alert_id: str, resolved_by: str, resolution_notes: str = "") -> bool:
        """
        Resolve an alert.
        
        Args:
            alert_id: ID of the alert to resolve
            resolved_by: User/agent resolving the alert
            resolution_notes: Notes about the resolution
            
        Returns:
            True if alert was resolved, False otherwise
        """
        if alert_id not in self.alerts:
            logger.warning(f"Alert {alert_id} not found")
            return False
        
        alert = self.alerts[alert_id]
        alert.resolved = True
        alert.resolved_at = datetime.now()
        alert.resolved_by = resolved_by
        alert.metadata['resolution_notes'] = resolution_notes
        
        logger.info(f"Alert {alert_id} resolved by {resolved_by}")
        return True
    
    def get_active_alerts(self, alert_type: Optional[AlertType] = None) -> List[GamingAlert]:
        """
        Get all active (unresolved) alerts.
        
        Args:
            alert_type: Optional filter by alert type
            
        Returns:
            List of active alerts
        """
        active_alerts = [
            alert for alert in self.alerts.values()
            if not alert.resolved
        ]
        
        if alert_type:
            active_alerts = [
                alert for alert in active_alerts
                if alert.type == alert_type
            ]
        
        return active_alerts
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all alerts.
        
        Returns:
            Dictionary containing alert summary statistics
        """
        total_alerts = len(self.alerts)
        active_alerts = len(self.get_active_alerts())
        resolved_alerts = total_alerts - active_alerts
        
        alerts_by_type = {}
        alerts_by_severity = {}
        
        for alert in self.alerts.values():
            # Count by type
            alert_type = alert.type.value
            alerts_by_type[alert_type] = alerts_by_type.get(alert_type, 0) + 1
            
            # Count by severity
            severity = alert.severity.value
            alerts_by_severity[severity] = alerts_by_severity.get(severity, 0) + 1
        
        return {
            "total_alerts": total_alerts,
            "active_alerts": active_alerts,
            "resolved_alerts": resolved_alerts,
            "alerts_by_type": alerts_by_type,
            "alerts_by_severity": alerts_by_severity,
            "alert_counters": self.alert_counters
        }
    
    def clear_resolved_alerts(self, older_than_days: int = 30) -> int:
        """
        Clear resolved alerts older than specified days.
        
        Args:
            older_than_days: Remove alerts resolved more than this many days ago
            
        Returns:
            Number of alerts cleared
        """
        cutoff_time = datetime.now().timestamp() - (older_than_days * 24 * 60 * 60)
        
        alerts_to_remove = [
            alert_id for alert_id, alert in self.alerts.items()
            if alert.resolved and alert.resolved_at and alert.resolved_at.timestamp() < cutoff_time
        ]
        
        for alert_id in alerts_to_remove:
            del self.alerts[alert_id]
        
        logger.info(f"Cleared {len(alerts_to_remove)} resolved alerts")
        return len(alerts_to_remove)
    
    def set_alert_threshold(self, alert_type: AlertType, severity: AlertSeverity, threshold: int):
        """
        Set threshold for alert severity levels.
        
        Args:
            alert_type: Type of alert
            severity: Severity level
            threshold: Threshold value
        """
        self.severity_thresholds[severity] = threshold
        logger.info(f"Set threshold for {alert_type.value} {severity.value}: {threshold}")
    
    def export_alerts(self, filepath: str) -> bool:
        """
        Export alerts to JSON file.
        
        Args:
            filepath: Path to export file
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            export_data = {
                "alerts": [asdict(alert) for alert in self.alerts.values()],
                "summary": self.get_alert_summary(),
                "export_timestamp": datetime.now().isoformat()
            }
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"Exported alerts to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to export alerts: {e}")
            return False

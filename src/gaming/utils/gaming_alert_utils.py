"""
Gaming Alert Utilities

Utility functions for gaming alert handling and processing.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Mission: V2 Compliance Emergency Re-Onboarding - Phase 2 Remediation
Status: V2_COMPLIANCE_REMEDIATION_ACTIVE
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from ..models.gaming_alert_models import (
    GamingAlert, AlertType, AlertSeverity, 
    PerformanceMetrics, SystemHealthMetrics, AlertSummary
)

logger = logging.getLogger(__name__)


def create_alert_id(prefix: str = "gaming_alert") -> str:
    """Create a unique alert ID."""
    timestamp = int(datetime.now().timestamp())
    return f"{prefix}_{timestamp}"


def check_fps_performance(fps: float) -> Optional[tuple[AlertSeverity, str]]:
    """Check FPS performance and return alert details if needed."""
    if fps < 15:
        return AlertSeverity.CRITICAL, f"Critical FPS: {fps} FPS"
    elif fps < 30:
        return AlertSeverity.HIGH, f"Low FPS: {fps} FPS"
    return None


def check_memory_performance(memory_usage: float) -> Optional[tuple[AlertSeverity, str]]:
    """Check memory usage and return alert details if needed."""
    if memory_usage > 95:
        return AlertSeverity.CRITICAL, f"Critical memory usage: {memory_usage}%"
    elif memory_usage > 80:
        return AlertSeverity.HIGH, f"High memory usage: {memory_usage}%"
    return None


def check_cpu_performance(cpu_usage: float) -> Optional[tuple[AlertSeverity, str]]:
    """Check CPU usage and return alert details if needed."""
    if cpu_usage > 90:
        return AlertSeverity.HIGH, f"High CPU usage: {cpu_usage}%"
    return None


def check_disk_health(disk_usage: float) -> Optional[tuple[AlertSeverity, str]]:
    """Check disk usage and return alert details if needed."""
    if disk_usage > 85:
        return AlertSeverity.MEDIUM, f"Low disk space: {100 - disk_usage}% free"
    return None


def check_network_health(network_status: str) -> Optional[tuple[AlertSeverity, str]]:
    """Check network status and return alert details if needed."""
    if network_status != 'connected':
        return AlertSeverity.HIGH, f"Network connectivity issue: {network_status}"
    return None


def generate_performance_alerts(metrics: PerformanceMetrics) -> List[tuple[AlertType, AlertSeverity, str, Dict[str, Any]]]:
    """Generate performance alerts based on metrics."""
    alerts = []
    
    # Check FPS
    fps_alert = check_fps_performance(metrics.fps)
    if fps_alert:
        severity, message = fps_alert
        alerts.append((
            AlertType.PERFORMANCE,
            severity,
            message,
            {"fps": metrics.fps, "threshold": 30}
        ))
    
    # Check memory
    memory_alert = check_memory_performance(metrics.memory_usage)
    if memory_alert:
        severity, message = memory_alert
        alerts.append((
            AlertType.PERFORMANCE,
            severity,
            message,
            {"memory_usage": metrics.memory_usage, "threshold": 80}
        ))
    
    # Check CPU
    cpu_alert = check_cpu_performance(metrics.cpu_usage)
    if cpu_alert:
        severity, message = cpu_alert
        alerts.append((
            AlertType.PERFORMANCE,
            severity,
            message,
            {"cpu_usage": metrics.cpu_usage, "threshold": 90}
        ))
    
    return alerts


def generate_health_alerts(metrics: SystemHealthMetrics) -> List[tuple[AlertType, AlertSeverity, str, Dict[str, Any]]]:
    """Generate system health alerts based on metrics."""
    alerts = []
    
    # Check disk
    disk_alert = check_disk_health(metrics.disk_usage)
    if disk_alert:
        severity, message = disk_alert
        alerts.append((
            AlertType.SYSTEM_HEALTH,
            severity,
            message,
            {"disk_usage": metrics.disk_usage, "threshold": 85}
        ))
    
    # Check network
    network_alert = check_network_health(metrics.network_status)
    if network_alert:
        severity, message = network_alert
        alerts.append((
            AlertType.SYSTEM_HEALTH,
            severity,
            message,
            {"network_status": metrics.network_status}
        ))
    
    return alerts


def calculate_alert_summary(alerts: Dict[str, GamingAlert]) -> AlertSummary:
    """Calculate alert summary statistics."""
    total_alerts = len(alerts)
    active_alerts = len([a for a in alerts.values() if not a.resolved])
    resolved_alerts = total_alerts - active_alerts
    
    alerts_by_type = {}
    alerts_by_severity = {}
    
    for alert in alerts.values():
        # Count by type
        alert_type = alert.type.value
        alerts_by_type[alert_type] = alerts_by_type.get(alert_type, 0) + 1
        
        # Count by severity
        severity = alert.severity.value
        alerts_by_severity[severity] = alerts_by_severity.get(severity, 0) + 1
    
    # Calculate alert counters by type
    alert_counters = {}
    for alert in alerts.values():
        alert_type = alert.type.value
        alert_counters[alert_type] = alert_counters.get(alert_type, 0) + 1
    
    return AlertSummary(
        total_alerts=total_alerts,
        active_alerts=active_alerts,
        resolved_alerts=resolved_alerts,
        alerts_by_type=alerts_by_type,
        alerts_by_severity=alerts_by_severity,
        alert_counters=alert_counters
    )


def export_alerts_to_json(alerts: Dict[str, GamingAlert], filepath: str) -> bool:
    """Export alerts to JSON file."""
    try:
        export_data = {
            "alerts": [alert.__dict__ for alert in alerts.values()],
            "summary": calculate_alert_summary(alerts).__dict__,
            "export_timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        logger.info(f"Exported alerts to {filepath}")
        return True
    except Exception as e:
        logger.error(f"Failed to export alerts: {e}")
        return False


def clear_old_resolved_alerts(alerts: Dict[str, GamingAlert], older_than_days: int = 30) -> int:
    """Clear resolved alerts older than specified days."""
    cutoff_time = datetime.now().timestamp() - (older_than_days * 24 * 60 * 60)
    
    alerts_to_remove = [
        alert_id for alert_id, alert in alerts.items()
        if alert.resolved and alert.resolved_at and alert.resolved_at.timestamp() < cutoff_time
    ]
    
    for alert_id in alerts_to_remove:
        del alerts[alert_id]
    
    logger.info(f"Cleared {len(alerts_to_remove)} resolved alerts")
    return len(alerts_to_remove)


__all__ = [
    "create_alert_id",
    "check_fps_performance",
    "check_memory_performance", 
    "check_cpu_performance",
    "check_disk_health",
    "check_network_health",
    "generate_performance_alerts",
    "generate_health_alerts",
    "calculate_alert_summary",
    "export_alerts_to_json",
    "clear_old_resolved_alerts"
]

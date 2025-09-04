"""
Gaming Alert Handlers

Extracted handler functions for gaming alert system to achieve V2 compliance.
Contains performance monitoring, system health monitoring, and alert processing handlers.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Implementation - Gaming Infrastructure Refactoring
"""


logger = logging.getLogger(__name__)


def handle_performance_alerts(manager, performance_metrics: Dict[str, Any]) -> List:
    """
    Handle performance-related alerts based on metrics.
    
    Args:
        manager: GamingAlertManager instance
        performance_metrics: Current performance metrics
        
    Returns:
        List of created performance alerts
    """
    alerts = []
    
    # Check FPS performance
    fps = performance_metrics.get('fps', 0)
    if fps < 30:
        severity = AlertSeverity.CRITICAL if fps < 15 else AlertSeverity.HIGH
        alert = manager.create_alert(
            AlertType.PERFORMANCE,
            severity,
            format_alert_message(AlertType.PERFORMANCE, severity, {"fps": fps, "threshold": 30}),
            "performance_monitor",
            {"fps": fps, "threshold": 30}
        )
        alerts.append(alert)
    
    # Check memory usage
    memory_usage = performance_metrics.get('memory_usage', 0)
    if memory_usage > 80:
        severity = AlertSeverity.CRITICAL if memory_usage > 95 else AlertSeverity.HIGH
        alert = manager.create_alert(
            AlertType.PERFORMANCE,
            severity,
            format_alert_message(AlertType.PERFORMANCE, severity, {"memory_usage": memory_usage, "threshold": 80}),
            "performance_monitor",
            {"memory_usage": memory_usage, "threshold": 80}
        )
        alerts.append(alert)
    
    # Check CPU usage
    cpu_usage = performance_metrics.get('cpu_usage', 0)
    if cpu_usage > 90:
        alert = manager.create_alert(
            AlertType.PERFORMANCE,
            AlertSeverity.HIGH,
            format_alert_message(AlertType.PERFORMANCE, AlertSeverity.HIGH, {"cpu_usage": cpu_usage, "threshold": 90}),
            "performance_monitor",
            {"cpu_usage": cpu_usage, "threshold": 90}
        )
        alerts.append(alert)
    
    return alerts


def handle_system_health_alerts(manager, health_metrics: Dict[str, Any]) -> List:
    """
    Handle system health alerts.
    
    Args:
        manager: GamingAlertManager instance
        health_metrics: Current system health metrics
        
    Returns:
        List of created health alerts
    """
    alerts = []
    
    # Check disk space
    disk_usage = health_metrics.get('disk_usage', 0)
    if disk_usage > 85:
        alert = manager.create_alert(
            AlertType.SYSTEM_HEALTH,
            AlertSeverity.MEDIUM,
            format_alert_message(AlertType.SYSTEM_HEALTH, AlertSeverity.MEDIUM, {"disk_usage": disk_usage, "threshold": 85}),
            "system_monitor",
            {"disk_usage": disk_usage, "threshold": 85}
        )
        alerts.append(alert)
    
    # Check network connectivity
    network_status = health_metrics.get('network_status', 'unknown')
    if network_status != 'connected':
        alert = manager.create_alert(
            AlertType.SYSTEM_HEALTH,
            AlertSeverity.HIGH,
            format_alert_message(AlertType.SYSTEM_HEALTH, AlertSeverity.HIGH, {"network_status": network_status}),
            "network_monitor",
            {"network_status": network_status}
        )
        alerts.append(alert)
    
    return alerts


def handle_alert_acknowledgment(manager, alert_id: str, acknowledged_by: str) -> bool:
    """
    Handle alert acknowledgment.
    
    Args:
        manager: GamingAlertManager instance
        alert_id: ID of the alert to acknowledge
        acknowledged_by: User/agent acknowledging the alert
        
    Returns:
        True if alert was acknowledged, False otherwise
    """
    if alert_id not in manager.alerts:
        get_logger(__name__).warning(f"Alert {alert_id} not found")
        return False
    
    alert = manager.alerts[alert_id]
    alert.acknowledged = True
    alert.metadata['acknowledged_by'] = acknowledged_by
    alert.metadata['acknowledged_at'] = manager._get_current_timestamp()
    
    get_logger(__name__).info(f"Alert {alert_id} acknowledged by {acknowledged_by}")
    return True


def handle_alert_resolution(manager, alert_id: str, resolved_by: str, resolution_notes: str = "") -> bool:
    """
    Handle alert resolution.
    
    Args:
        manager: GamingAlertManager instance
        alert_id: ID of the alert to resolve
        resolved_by: User/agent resolving the alert
        resolution_notes: Notes about the resolution
        
    Returns:
        True if alert was resolved, False otherwise
    """
    if alert_id not in manager.alerts:
        get_logger(__name__).warning(f"Alert {alert_id} not found")
        return False
    
    alert = manager.alerts[alert_id]
    alert.resolved = True
    alert.resolved_at = manager._get_current_timestamp()
    alert.resolved_by = resolved_by
    alert.metadata['resolution_notes'] = resolution_notes
    
    get_logger(__name__).info(f"Alert {alert_id} resolved by {resolved_by}")
    return True

#!/usr/bin/env python3
"""
Health Monitor - Agent Cellphone V2
===================================

Real-time connector health monitoring system with proactive alerts.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import logging
from typing import Dict, List, Optional, Any, Callable

from ..status.status_core import LiveStatusSystem
from ..health_models import HealthAlert

# Import the modular components
from .health_monitor_core import HealthMonitorCore
from .health_monitor_alerts import HealthChecker, AlertLevel
from .health_monitor_reports import HealthReporter


class HealthMonitor:
    """
    Real-time health monitoring system for connectors and services
    Now uses modular architecture for better maintainability
    """

    def __init__(self, update_interval: float = 10.0):
        self.logger = logging.getLogger(f"{__name__}.HealthMonitor")
        self.update_interval = update_interval
        
        # Use the modular components
        self.core_monitor = HealthMonitorCore(update_interval)
        self.health_checker = HealthChecker()
        self.health_reporter = HealthReporter()
        
        # Integration with status system
        self.status_system: Optional[LiveStatusSystem] = None

    def set_status_system(self, status_system: LiveStatusSystem):
        """Set the status system for integration"""
        self.status_system = status_system
        self.health_checker.set_status_system(status_system)

    def register_component(
        self, component_id: str, health_checker: Callable[[], Dict[str, float]]
    ):
        """Register a component for health monitoring"""
        self.core_monitor.register_component(component_id, health_checker)

    def unregister_component(self, component_id: str):
        """Unregister a component from health monitoring"""
        self.core_monitor.unregister_component(component_id)

    def start_monitoring(self):
        """Start health monitoring"""
        self.core_monitor.start_monitoring()

    def stop_monitoring(self):
        """Stop health monitoring"""
        self.core_monitor.stop_monitoring()

    def get_component_health(self, component_id: str) -> Optional[Dict[str, Any]]:
        """Get health status for a specific component"""
        return self.core_monitor.get_component_health(component_id)

    def get_all_health_status(self) -> Dict[str, Dict[str, Any]]:
        """Get health status for all components"""
        return self.core_monitor.get_all_health_status()

    def get_health_alerts(self, include_resolved: bool = False) -> List[Dict[str, Any]]:
        """Get current health alerts"""
        return self.core_monitor.get_health_alerts(include_resolved)

    def add_alert_callback(self, callback: Callable[[HealthAlert], None]):
        """Add callback for health alerts"""
        self.core_monitor.add_alert_callback(callback)

    def remove_alert_callback(self, callback: Callable[[HealthAlert], None]):
        """Remove alert callback"""
        self.core_monitor.remove_alert_callback(callback)

    def acknowledge_alert(self, alert_id: str):
        """Acknowledge a health alert"""
        self.core_monitor.acknowledge_alert(alert_id)

    def resolve_alert(self, alert_id: str):
        """Mark an alert as resolved"""
        self.core_monitor.resolve_alert(alert_id)

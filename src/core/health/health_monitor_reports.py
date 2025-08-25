#!/usr/bin/env python3
"""
Health Monitor Reports - Agent Cellphone V2
==========================================

Reporting and history utilities for the health monitoring system.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import time
import logging
from typing import Dict, List, Optional, Any, Callable

from src.utils.stability_improvements import stability_manager, safe_import
from ..health_models import (
    HealthStatus,
    HealthMetricType,
    AlertSeverity,
    HealthMetric,
    HealthSnapshot,
    HealthAlert,
    HealthThreshold,
    HealthReport,
    HealthCheck,
    HealthCheckResult,
)


class HealthReporter:
    """
    Health reporting and history functionality
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.HealthReporter")
        
        # Health history tracking
        self.health_history: Dict[str, List[Dict[str, Any]]] = {}
        
        # Alert callbacks
        self.alert_callbacks: List[Callable[[HealthAlert], None]] = []

    def register_component(self, component_id: str):
        """Register a component for health reporting"""
        self.health_history[component_id] = []

    def unregister_component(self, component_id: str):
        """Unregister a component from health reporting"""
        if component_id in self.health_history:
            del self.health_history[component_id]

    def save_health_history(self):
        """Save health history for trending analysis"""
        current_time = time.time()

        # This method will be called by the monitor with access to current metrics
        # The actual implementation will be coordinated with the HealthChecker
        pass

    def add_alert_callback(self, callback: Callable[[HealthAlert], None]):
        """Add callback for health alerts"""
        self.alert_callbacks.append(callback)

    def remove_alert_callback(self, callback: Callable[[HealthAlert], None]):
        """Remove alert callback"""
        if callback in self.alert_callbacks:
            self.alert_callbacks.remove(callback)

    def acknowledge_alert(self, alert_id: str):
        """Acknowledge a health alert"""
        # This will be coordinated with the HealthChecker
        pass

    def resolve_alert(self, alert_id: str):
        """Mark an alert as resolved"""
        current_time = time.time()
        # This will be coordinated with the HealthChecker
        pass

    def get_component_health(self, component_id: str) -> Optional[Dict[str, Any]]:
        """Get health status for a specific component"""
        # This will be coordinated with the HealthChecker
        # For now, return None as the actual implementation needs coordination
        return None

    def get_all_health_status(self) -> Dict[str, Dict[str, Any]]:
        """Get health status for all components"""
        # This will be coordinated with the HealthChecker
        # For now, return empty dict as the actual implementation needs coordination
        return {}

    def get_health_alerts(self, include_resolved: bool = False) -> List[Dict[str, Any]]:
        """Get current health alerts"""
        # This will be coordinated with the HealthChecker
        # For now, return empty list as the actual implementation needs coordination
        return []

    def _get_overall_status(self, health_score: float) -> HealthStatus:
        """Get overall health status from score"""
        if health_score >= 0.8:
            return HealthStatus.EXCELLENT
        elif health_score >= 0.6:
            return HealthStatus.GOOD
        elif health_score >= 0.4:
            return HealthStatus.WARNING
        elif health_score >= 0.2:
            return HealthStatus.CRITICAL
        else:
            return HealthStatus.FAILED

    def get_health_history(self, component_id: str) -> List[Dict[str, Any]]:
        """Get health history for a specific component"""
        return self.health_history.get(component_id, [])

    def get_all_health_history(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get health history for all components"""
        return self.health_history

    def clear_health_history(self, component_id: Optional[str] = None):
        """Clear health history for a component or all components"""
        if component_id:
            if component_id in self.health_history:
                self.health_history[component_id] = []
        else:
            self.health_history.clear()

    def export_health_data(self, component_id: Optional[str] = None) -> Dict[str, Any]:
        """Export health data for analysis"""
        if component_id:
            return {
                "component_id": component_id,
                "history": self.health_history.get(component_id, []),
                "exported_at": time.time()
            }
        else:
            return {
                "all_components": self.health_history,
                "exported_at": time.time()
            }

    def get_health_summary(self) -> Dict[str, Any]:
        """Get a summary of all health data"""
        total_components = len(self.health_history)
        total_history_entries = sum(len(history) for history in self.health_history.values())
        
        return {
            "total_components": total_components,
            "total_history_entries": total_history_entries,
            "components_with_history": [
                comp_id for comp_id, history in self.health_history.items() 
                if len(history) > 0
            ],
            "summary_generated_at": time.time()
        }

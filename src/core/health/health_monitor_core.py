#!/usr/bin/env python3
"""
Health Monitor Core - Agent Cellphone V2
========================================

Core monitoring functionality for the health monitoring system.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import time
import threading
import logging
from typing import Dict, List, Optional, Any, Callable

from src.utils.stability_improvements import stability_manager, safe_import
from .health_monitor_alerts import HealthChecker
from .health_monitor_reports import HealthReporter


class HealthMonitorCore:
    """
    Core health monitoring system for connectors and services
    """

    def __init__(self, update_interval: float = 10.0):
        self.logger = logging.getLogger(f"{__name__}.HealthMonitorCore")
        self.update_interval = update_interval
        self.is_active = False

        # Core components
        self.health_checker = HealthChecker()
        self.health_reporter = HealthReporter()

        # Monitoring thread
        self.monitor_thread: Optional[threading.Thread] = None
        self.monitor_lock = threading.RLock()

        # Health check functions
        self.health_checkers: Dict[str, Callable[[], Dict[str, float]]] = {}

    def register_component(
        self, component_id: str, health_checker: Callable[[], Dict[str, float]]
    ):
        """Register a component for health monitoring"""
        with self.monitor_lock:
            self.health_checkers[component_id] = health_checker
            self.health_checker.register_component(component_id)
            self.health_reporter.register_component(component_id)

        self.logger.info(f"Registered component for health monitoring: {component_id}")

    def unregister_component(self, component_id: str):
        """Unregister a component from health monitoring"""
        with self.monitor_lock:
            if component_id in self.health_checkers:
                del self.health_checkers[component_id]
            self.health_checker.unregister_component(component_id)
            self.health_reporter.unregister_component(component_id)

        self.logger.info(
            f"Unregistered component from health monitoring: {component_id}"
        )

    def start_monitoring(self):
        """Start health monitoring"""
        if self.is_active:
            return

        self.is_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

        self.logger.info("Health monitoring started")

    def stop_monitoring(self):
        """Stop health monitoring"""
        self.is_active = False

        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)

        self.logger.info("Health monitoring stopped")

    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_active:
            try:
                self._perform_health_checks()
                self.health_checker.update_health_scores()
                self.health_checker.check_alert_conditions()
                self.health_reporter.save_health_history()
                time.sleep(self.update_interval)
            except Exception as e:
                self.logger.error(f"Health monitoring error: {e}")
                time.sleep(10)  # Recovery pause

    def _perform_health_checks(self):
        """Perform health checks on all registered components"""
        with self.monitor_lock:
            for component_id, health_checker in self.health_checkers.items():
                try:
                    metrics_data = health_checker()
                    self.health_checker.update_component_metrics(component_id, metrics_data)
                except Exception as e:
                    self.logger.error(f"Health check failed for {component_id}: {e}")
                    self.health_checker.mark_component_failed(component_id, str(e))

    def get_component_health(self, component_id: str) -> Optional[Dict[str, Any]]:
        """Get health status for a specific component"""
        return self.health_reporter.get_component_health(component_id)

    def get_all_health_status(self) -> Dict[str, Dict[str, Any]]:
        """Get health status for all components"""
        return self.health_reporter.get_all_health_status()

    def get_health_alerts(self, include_resolved: bool = False) -> List[Dict[str, Any]]:
        """Get current health alerts"""
        return self.health_reporter.get_health_alerts(include_resolved)

    def add_alert_callback(self, callback: Callable[[Any], None]):
        """Add callback for health alerts"""
        self.health_reporter.add_alert_callback(callback)

    def remove_alert_callback(self, callback: Callable[[Any], None]):
        """Remove alert callback"""
        self.health_reporter.remove_alert_callback(callback)

    def acknowledge_alert(self, alert_id: str):
        """Acknowledge a health alert"""
        self.health_reporter.acknowledge_alert(alert_id)

    def resolve_alert(self, alert_id: str):
        """Mark an alert as resolved"""
        self.health_reporter.resolve_alert(alert_id)


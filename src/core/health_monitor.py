#!/usr/bin/env python3
"""
Health Monitor - Agent Cellphone V2
===================================

Real-time connector health monitoring system with proactive alerts.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import time
import json
import threading
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from .status.status_core import LiveStatusSystem
from .status.status_types import StatusEventType, StatusEvent
from .monitor.monitor_alerts import AlertLevel
from .health_models import (
    HealthStatus, HealthMetricType, AlertSeverity,
    HealthMetric, HealthSnapshot, HealthAlert,
    HealthThreshold, HealthReport, HealthCheck, HealthCheckResult
)


# Health models now imported from unified health_models


class HealthMonitor:
    """
    Real-time health monitoring system for connectors and services
    """
    
    def __init__(self, update_interval: float = 10.0):
        self.logger = logging.getLogger(f"{__name__}.HealthMonitor")
        self.update_interval = update_interval
        self.is_active = False
        
        # Health tracking
        self.health_metrics: Dict[str, Dict[str, HealthMetric]] = {}
        self.health_scores: Dict[str, float] = {}
        self.health_history: Dict[str, List[Dict[str, Any]]] = {}
        
        # Alerting system
        self.alerts: List[HealthAlert] = []
        self.alert_callbacks: List[Callable[[HealthAlert], None]] = []
        
        # Monitoring thread
        self.monitor_thread: Optional[threading.Thread] = None
        self.monitor_lock = threading.RLock()
        
        # Integration with status system
        self.status_system: Optional[LiveStatusSystem] = None
        
        # Health check functions
        self.health_checkers: Dict[str, Callable[[], Dict[str, float]]] = {}
        
        # Configuration
        self.health_thresholds = {
            "response_time": {"warning": 1000.0, "critical": 5000.0},  # ms
            "error_rate": {"warning": 0.05, "critical": 0.20},  # percentage
            "availability": {"warning": 0.95, "critical": 0.80},  # percentage
            "throughput": {"warning": 100.0, "critical": 50.0},  # requests/sec
            "memory_usage": {"warning": 0.80, "critical": 0.95},  # percentage
            "cpu_usage": {"warning": 0.70, "critical": 0.90}  # percentage
        }
        
    def set_status_system(self, status_system: LiveStatusSystem):
        """Set the status system for integration"""
        self.status_system = status_system
        
    def register_component(self, component_id: str, health_checker: Callable[[], Dict[str, float]]):
        """Register a component for health monitoring"""
        with self.monitor_lock:
            self.health_checkers[component_id] = health_checker
            self.health_metrics[component_id] = {}
            self.health_scores[component_id] = 1.0
            self.health_history[component_id] = []
            
        self.logger.info(f"Registered component for health monitoring: {component_id}")
        
    def unregister_component(self, component_id: str):
        """Unregister a component from health monitoring"""
        with self.monitor_lock:
            if component_id in self.health_checkers:
                del self.health_checkers[component_id]
            if component_id in self.health_metrics:
                del self.health_metrics[component_id]
            if component_id in self.health_scores:
                del self.health_scores[component_id]
            if component_id in self.health_history:
                del self.health_history[component_id]
                
        self.logger.info(f"Unregistered component from health monitoring: {component_id}")
        
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
                self._update_health_scores()
                self._check_alert_conditions()
                self._save_health_history()
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
                    self._update_component_metrics(component_id, metrics_data)
                except Exception as e:
                    self.logger.error(f"Health check failed for {component_id}: {e}")
                    self._mark_component_failed(component_id, str(e))
                    
    def _update_component_metrics(self, component_id: str, metrics_data: Dict[str, float]):
        """Update health metrics for a component"""
        if component_id not in self.health_metrics:
            return
            
        current_time = time.time()
        
        for metric_name, value in metrics_data.items():
            if metric_name not in self.health_metrics[component_id]:
                # Create new metric
                thresholds = self.health_thresholds.get(metric_name, {"warning": 100.0, "critical": 200.0})
                metric = HealthMetric(
                    name=metric_name,
                    value=value,
                    unit=self._get_metric_unit(metric_name),
                    threshold_warning=thresholds["warning"],
                    threshold_critical=thresholds["critical"],
                    timestamp=current_time
                )
                self.health_metrics[component_id][metric_name] = metric
            else:
                # Update existing metric
                metric = self.health_metrics[component_id][metric_name]
                metric.trend.append(metric.value)
                if len(metric.trend) > 10:  # Keep last 10 values
                    metric.trend.pop(0)
                metric.value = value
                metric.timestamp = current_time
                
    def _mark_component_failed(self, component_id: str, error_message: str):
        """Mark a component as failed"""
        with self.monitor_lock:
            if component_id in self.health_metrics:
                for metric in self.health_metrics[component_id].values():
                    metric.value = metric.threshold_critical * 1.5  # Mark as critical
                    
            self.health_scores[component_id] = 0.0
            
        # Create alert
        self._create_alert(component_id, "health_check", AlertLevel.CRITICAL, 
                          f"Component health check failed: {error_message}")
                          
    def _update_health_scores(self):
        """Update overall health scores for all components"""
        with self.monitor_lock:
            for component_id in self.health_metrics:
                if component_id not in self.health_scores:
                    self.health_scores[component_id] = 1.0
                    
                metrics = self.health_metrics[component_id]
                if not metrics:
                    continue
                    
                # Calculate weighted health score
                total_weight = 0
                weighted_score = 0
                
                for metric in metrics.values():
                    weight = self._get_metric_weight(metric.name)
                    status = metric.get_status()
                    
                    if status == HealthStatus.EXCELLENT:
                        score = 1.0
                    elif status == HealthStatus.GOOD:
                        score = 0.8
                    elif status == HealthStatus.WARNING:
                        score = 0.5
                    elif status == HealthStatus.CRITICAL:
                        score = 0.2
                    else:
                        score = 0.0
                        
                    weighted_score += score * weight
                    total_weight += weight
                    
                if total_weight > 0:
                    self.health_scores[component_id] = weighted_score / total_weight
                    
    def _check_alert_conditions(self):
        """Check for alert conditions and create alerts"""
        with self.monitor_lock:
            for component_id, metrics in self.health_metrics.items():
                for metric_name, metric in metrics.items():
                    status = metric.get_status()
                    
                    if status in [HealthStatus.WARNING, HealthStatus.CRITICAL]:
                        alert_level = AlertLevel.CRITICAL if status == HealthStatus.CRITICAL else AlertLevel.WARNING
                        message = f"{metric_name} is {status.value}: {metric.value}{metric.unit}"
                        
                        # Check if alert already exists
                        existing_alert = self._find_existing_alert(component_id, metric_name)
                        if not existing_alert:
                            self._create_alert(component_id, metric_name, alert_level, message)
                            
    def _create_alert(self, component_id: str, metric_name: str, alert_level: AlertLevel, message: str):
        """Create a new health alert"""
        alert = HealthAlert(
            alert_id=f"alert_{int(time.time())}_{component_id}_{metric_name}",
            component_id=component_id,
            metric_name=metric_name,
            alert_level=alert_level,
            message=message,
            timestamp=time.time()
        )
        
        self.alerts.append(alert)
        
        # Notify callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                self.logger.error(f"Alert callback failed: {e}")
                
        # Integrate with status system
        if self.status_system:
            self.status_system._create_status_event(
                StatusEventType.HEALTH_ALERT,
                component_id,
                message,
                {"alert_level": alert_level.value, "metric": metric_name},
                "high" if alert_level in [AlertLevel.ERROR, AlertLevel.CRITICAL] else "medium"
            )
            
        self.logger.warning(f"Health alert created: {component_id} - {message}")
        
    def _find_existing_alert(self, component_id: str, metric_name: str) -> Optional[HealthAlert]:
        """Find existing alert for component and metric"""
        for alert in self.alerts:
            if (alert.component_id == component_id and 
                alert.metric_name == metric_name and 
                not alert.is_acknowledged):
                return alert
        return None
        
    def _save_health_history(self):
        """Save health history for trending analysis"""
        current_time = time.time()
        
        with self.monitor_lock:
            for component_id, metrics in self.health_metrics.items():
                if component_id not in self.health_history:
                    self.health_history[component_id] = []
                    
                history_entry = {
                    "timestamp": current_time,
                    "health_score": self.health_scores.get(component_id, 0.0),
                    "metrics": {name: {"value": metric.value, "status": metric.get_status().value}
                               for name, metric in metrics.items()}
                }
                
                self.health_history[component_id].append(history_entry)
                
                # Keep last 1000 entries
                if len(self.health_history[component_id]) > 1000:
                    self.health_history[component_id] = self.health_history[component_id][-1000:]
                    
    def _get_metric_unit(self, metric_name: str) -> str:
        """Get unit for a metric"""
        units = {
            "response_time": "ms",
            "error_rate": "%",
            "availability": "%",
            "throughput": "req/s",
            "memory_usage": "%",
            "cpu_usage": "%"
        }
        return units.get(metric_name, "")
        
    def _get_metric_weight(self, metric_name: str) -> float:
        """Get weight for a metric in health score calculation"""
        weights = {
            "response_time": 0.25,
            "error_rate": 0.30,
            "availability": 0.25,
            "throughput": 0.10,
            "memory_usage": 0.05,
            "cpu_usage": 0.05
        }
        return weights.get(metric_name, 0.1)
        
    def add_alert_callback(self, callback: Callable[[HealthAlert], None]):
        """Add callback for health alerts"""
        self.alert_callbacks.append(callback)
        
    def remove_alert_callback(self, callback: Callable[[HealthAlert], None]):
        """Remove alert callback"""
        if callback in self.alert_callbacks:
            self.alert_callbacks.remove(callback)
            
    def acknowledge_alert(self, alert_id: str):
        """Acknowledge a health alert"""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.is_acknowledged = True
                break
                
    def resolve_alert(self, alert_id: str):
        """Mark an alert as resolved"""
        current_time = time.time()
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolved_at = current_time
                break
                
    def get_component_health(self, component_id: str) -> Optional[Dict[str, Any]]:
        """Get health status for a specific component"""
        with self.monitor_lock:
            if component_id not in self.health_metrics:
                return None
                
            metrics = self.health_metrics[component_id]
            health_score = self.health_scores.get(component_id, 0.0)
            
            return {
                "component_id": component_id,
                "health_score": health_score,
                "overall_status": self._get_overall_status(health_score),
                "metrics": {name: {
                    "value": metric.value,
                    "unit": metric.unit,
                    "status": metric.get_status().value,
                    "thresholds": {
                        "warning": metric.threshold_warning,
                        "critical": metric.threshold_critical
                    }
                } for name, metric in metrics.items()},
                "last_updated": max(metric.timestamp for metric in metrics.values()) if metrics else 0
            }
            
    def get_all_health_status(self) -> Dict[str, Dict[str, Any]]:
        """Get health status for all components"""
        return {component_id: self.get_component_health(component_id)
                for component_id in self.health_metrics.keys()}
                
    def get_health_alerts(self, include_resolved: bool = False) -> List[Dict[str, Any]]:
        """Get current health alerts"""
        alerts = []
        for alert in self.alerts:
            if include_resolved or not alert.resolved_at:
                alerts.append({
                    "alert_id": alert.alert_id,
                    "component_id": alert.component_id,
                    "metric_name": alert.metric_name,
                    "alert_level": alert.alert_level.value,
                    "message": alert.message,
                    "timestamp": alert.timestamp,
                    "is_acknowledged": alert.is_acknowledged,
                    "resolved_at": alert.resolved_at
                })
        return alerts
        
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

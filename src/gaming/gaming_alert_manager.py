#!/usr/bin/env python3
"""
Gaming Alert Manager - Agent Cellphone V2

Manages gaming-specific alerts and integrates with core alert infrastructure.
Provides gaming performance alerts, system health notifications, and alert routing.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3C - Gaming Systems Integration
V2 Standards: ≤200 LOC, SRP, OOP principles, BaseManager inheritance
"""

import logging
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json

# Core infrastructure imports
from src.core.performance.alerts import AlertSeverity, AlertType
from src.core.base_manager import BaseManager, ManagerStatus, ManagerPriority


@dataclass
class GamingAlert:
    """Gaming-specific alert definition"""
    alert_id: str
    alert_type: str
    severity: AlertSeverity
    message: str
    system_id: str
    game_context: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    acknowledged: bool = False
    resolved: bool = False
    resolution_note: Optional[str] = None


class GamingAlertManager(BaseManager):
    """
    Gaming Alert Manager - TASK 3C
    
    Manages gaming alerts and integrates with:
    - Core alert management system
    - Performance monitoring alerts
    - System health notifications
    - Alert routing and escalation
    
    Now inherits from BaseManager for unified functionality
    """
    
    def __init__(self):
        """Initialize gaming alert manager with BaseManager"""
        super().__init__(
            manager_id="gaming_alert_manager",
            name="Gaming Alert Manager",
            description="Manages gaming-specific alerts and notifications"
        )
        
        # Alert tracking
        self.active_alerts: Dict[str, GamingAlert] = {}
        self.alert_history: List[GamingAlert] = []
        self.alert_counters: Dict[str, int] = {}
        
        # Alert thresholds
        self.alert_thresholds = {
            "frame_rate": {"warning": 30.0, "error": 15.0, "critical": 5.0},
            "response_time": {"warning": 100.0, "error": 200.0, "critical": 500.0},
            "memory_usage": {"warning": 2048.0, "error": 4096.0, "critical": 8192.0},
            "system_health": {"warning": 80.0, "error": 60.0, "critical": 40.0}
        }
        
        self.logger.info("Gaming Alert Manager initialized for TASK 3C")
    
    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize gaming alert system"""
        try:
            self.logger.info("Starting Gaming Alert Manager...")
            
            # Initialize alert tracking
            self.active_alerts.clear()
            self.alert_history.clear()
            self.alert_counters.clear()
            
            # Load default thresholds
            self._load_default_thresholds()
            
            self.logger.info("Gaming Alert Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Gaming Alert Manager: {e}")
            return False
    
    def _on_stop(self):
        """Cleanup gaming alert system"""
        try:
            self.logger.info("Stopping Gaming Alert Manager...")
            
            # Save alert history
            self._save_alert_history()
            
            # Clear active alerts
            self.active_alerts.clear()
            
            self.logger.info("Gaming Alert Manager stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to stop Gaming Alert Manager: {e}")
    
    def _on_heartbeat(self):
        """Gaming alert manager heartbeat"""
        try:
            # Check for stale alerts
            self._check_stale_alerts()
            
            # Update metrics
            self.record_operation("heartbeat", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)
    
    def _on_initialize_resources(self) -> bool:
        """Initialize gaming alert resources"""
        try:
            # Initialize alert storage
            self.active_alerts = {}
            self.alert_history = []
            self.alert_counters = {}
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Cleanup gaming alert resources"""
        try:
            # Clear alert data
            self.active_alerts.clear()
            self.alert_history.clear()
            self.alert_counters.clear()
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
    
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors"""
        try:
            self.logger.info(f"Attempting recovery for {context}")
            
            # Reset alert state
            self.active_alerts.clear()
            self.alert_counters.clear()
            
            # Reload thresholds
            self._load_default_thresholds()
            
            self.logger.info("Recovery successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False
    
    # ============================================================================
    # Gaming Alert Management Methods
    # ============================================================================
    
    def create_alert(self, alert_type: str, severity: str, message: str, 
                    system_id: str, game_context: Dict[str, Any]) -> GamingAlert:
        """Create a new gaming alert"""
        try:
            alert_id = f"gaming_{alert_type}_{int(time.time())}"
            severity_enum = AlertSeverity(severity.upper())
            
            alert = GamingAlert(
                alert_id=alert_id,
                alert_type=alert_type,
                severity=severity_enum,
                message=message,
                system_id=system_id,
                game_context=game_context
            )
            
            # Store alert
            self.active_alerts[alert_id] = alert
            self.alert_history.append(alert)
            
            # Update counters
            if alert_type not in self.alert_counters:
                self.alert_counters[alert_type] = 0
            self.alert_counters[alert_type] += 1
            
            # Record operation
            self.record_operation("create_alert", True, 0.0)
            
            self.logger.warning(f"Created {severity} gaming alert: {message}")
            return alert
            
        except Exception as e:
            self.logger.error(f"Failed to create gaming alert: {e}")
            self.record_operation("create_alert", False, 0.0)
            return None
    
    def check_performance_alerts(self, system_id: str, metrics: Dict[str, Any]) -> List[GamingAlert]:
        """Check performance metrics for alert conditions"""
        try:
            alerts = []
            
            # Check frame rate
            if "frame_rate" in metrics:
                frame_rate = metrics["frame_rate"]
                if frame_rate < self.alert_thresholds["frame_rate"]["critical"]:
                    alert = self.create_alert(
                        "frame_rate", "critical",
                        f"Critical frame rate: {frame_rate}fps for {system_id}",
                        system_id, {"frame_rate": frame_rate, "threshold": self.alert_thresholds["frame_rate"]["critical"]}
                    )
                    if alert:
                        alerts.append(alert)
                elif frame_rate < self.alert_thresholds["frame_rate"]["error"]:
                    alert = self.create_alert(
                        "frame_rate", "error",
                        f"Low frame rate: {frame_rate}fps for {system_id}",
                        system_id, {"frame_rate": frame_rate, "threshold": self.alert_thresholds["frame_rate"]["error"]}
                    )
                    if alert:
                        alerts.append(alert)
                elif frame_rate < self.alert_thresholds["frame_rate"]["warning"]:
                    alert = self.create_alert(
                        "frame_rate", "warning",
                        f"Suboptimal frame rate: {frame_rate}fps for {system_id}",
                        system_id, {"frame_rate": frame_rate, "threshold": self.alert_thresholds["frame_rate"]["warning"]}
                    )
                    if alert:
                        alerts.append(alert)
            
            # Check response time
            if "response_time" in metrics:
                response_time = metrics["response_time"]
                if response_time > self.alert_thresholds["response_time"]["critical"]:
                    alert = self.create_alert(
                        "response_time", "critical",
                        f"Critical response time: {response_time}ms for {system_id}",
                        system_id, {"response_time": response_time, "threshold": self.alert_thresholds["response_time"]["critical"]}
                    )
                    if alert:
                        alerts.append(alert)
                elif response_time > self.alert_thresholds["response_time"]["error"]:
                    alert = self.create_alert(
                        "response_time", "error",
                        f"High response time: {response_time}ms for {system_id}",
                        system_id, {"response_time": response_time, "threshold": self.alert_thresholds["response_time"]["error"]}
                    )
                    if alert:
                        alerts.append(alert)
                elif response_time > self.alert_thresholds["response_time"]["warning"]:
                    alert = self.create_alert(
                        "response_time", "warning",
                        f"Elevated response time: {response_time}ms for {system_id}",
                        system_id, {"response_time": response_time, "threshold": self.alert_thresholds["response_time"]["warning"]}
                    )
                    if alert:
                        alerts.append(alert)
            
            # Check memory usage
            if "memory_usage" in metrics:
                memory_usage = metrics["memory_usage"]
                if memory_usage > self.alert_thresholds["memory_usage"]["critical"]:
                    alert = self.create_alert(
                        "memory_usage", "critical",
                        f"Critical memory usage: {memory_usage}MB for {system_id}",
                        system_id, {"memory_usage": memory_usage, "threshold": self.alert_thresholds["memory_usage"]["critical"]}
                    )
                    if alert:
                        alerts.append(alert)
                elif memory_usage > self.alert_thresholds["memory_usage"]["error"]:
                    alert = self.create_alert(
                        "memory_usage", "error",
                        f"High memory usage: {memory_usage}MB for {system_id}",
                        system_id, {"memory_usage": memory_usage, "threshold": self.alert_thresholds["memory_usage"]["error"]}
                    )
                    if alert:
                        alerts.append(alert)
                elif memory_usage > self.alert_thresholds["memory_usage"]["warning"]:
                    alert = self.create_alert(
                        "memory_usage", "warning",
                        f"Elevated memory usage: {memory_usage}MB for {system_id}",
                        system_id, {"memory_usage": memory_usage, "threshold": self.alert_thresholds["memory_usage"]["warning"]}
                    )
                    if alert:
                        alerts.append(alert)
            
            # Record operation
            self.record_operation("check_performance_alerts", True, 0.0)
            
            return alerts
            
        except Exception as e:
            self.logger.error(f"Failed to check performance alerts: {e}")
            self.record_operation("check_performance_alerts", False, 0.0)
            return []
    
    def check_system_health_alerts(self, system_id: str, health_score: float) -> Optional[GamingAlert]:
        """Check system health for alert conditions"""
        try:
            if health_score < self.alert_thresholds["system_health"]["critical"]:
                alert = self.create_alert(
                    "system_health", "critical",
                    f"Critical system health: {health_score}% for {system_id}",
                    system_id, {"health_score": health_score, "threshold": self.alert_thresholds["system_health"]["critical"]}
                )
            elif health_score < self.alert_thresholds["system_health"]["error"]:
                alert = self.create_alert(
                    "system_health", "error",
                    f"Poor system health: {health_score}% for {system_id}",
                    system_id, {"health_score": health_score, "threshold": self.alert_thresholds["system_health"]["error"]}
                )
            elif health_score < self.alert_thresholds["system_health"]["warning"]:
                alert = self.create_alert(
                    "system_health", "warning",
                    f"Degraded system health: {health_score}% for {system_id}",
                    system_id, {"health_score": health_score, "threshold": self.alert_thresholds["system_health"]["warning"]}
                )
            else:
                alert = None
            
            # Record operation
            self.record_operation("check_system_health_alerts", True, 0.0)
            
            return alert
            
        except Exception as e:
            self.logger.error(f"Failed to check system health alerts: {e}")
            self.record_operation("check_system_health_alerts", False, 0.0)
            return None
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge a gaming alert"""
        try:
            if alert_id not in self.active_alerts:
                self.logger.warning(f"Alert not found: {alert_id}")
                return False
            
            alert = self.active_alerts[alert_id]
            alert.acknowledged = True
            
            # Record operation
            self.record_operation("acknowledge_alert", True, 0.0)
            
            self.logger.info(f"Acknowledged gaming alert: {alert_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to acknowledge alert {alert_id}: {e}")
            self.record_operation("acknowledge_alert", False, 0.0)
            return False
    
    def resolve_alert(self, alert_id: str, resolution_note: str = "") -> bool:
        """Resolve a gaming alert"""
        try:
            if alert_id not in self.active_alerts:
                self.logger.warning(f"Alert not found: {alert_id}")
                return False
            
            alert = self.active_alerts[alert_id]
            alert.resolved = True
            alert.resolution_note = resolution_note
            
            # Move to history
            self.alert_history.append(alert)
            del self.active_alerts[alert_id]
            
            # Record operation
            self.record_operation("resolve_alert", True, 0.0)
            
            self.logger.info(f"Resolved gaming alert: {alert_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to resolve alert {alert_id}: {e}")
            self.record_operation("resolve_alert", False, 0.0)
            return False
    
    def get_active_alerts(self, system_id: Optional[str] = None, 
                         severity: Optional[AlertSeverity] = None) -> List[GamingAlert]:
        """Get active gaming alerts"""
        try:
            alerts = list(self.active_alerts.values())
            
            # Filter by system ID
            if system_id:
                alerts = [a for a in alerts if a.system_id == system_id]
            
            # Filter by severity
            if severity:
                alerts = [a for a in alerts if a.severity == severity]
            
            # Record operation
            self.record_operation("get_active_alerts", True, 0.0)
            
            return alerts
            
        except Exception as e:
            self.logger.error(f"Failed to get active alerts: {e}")
            self.record_operation("get_active_alerts", False, 0.0)
            return []
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get gaming alert summary"""
        try:
            total_alerts = len(self.alert_history)
            active_alerts = len(self.active_alerts)
            
            # Count by severity
            severity_counts = {}
            for alert in self.active_alerts.values():
                severity = alert.severity.value
                if severity not in severity_counts:
                    severity_counts[severity] = 0
                severity_counts[severity] += 1
            
            # Count by type
            type_counts = {}
            for alert in self.active_alerts.values():
                alert_type = alert.alert_type
                if alert_type not in type_counts:
                    type_counts[alert_type] = 0
                type_counts[alert_type] += 1
            
            # Count by system
            system_counts = {}
            for alert in self.active_alerts.values():
                system = alert.system_id
                if system not in system_counts:
                    system_counts[system] = 0
                system_counts[system] += 1
            
            summary = {
                "total_alerts": total_alerts,
                "active_alerts": active_alerts,
                "resolved_alerts": total_alerts - active_alerts,
                "alerts_by_severity": severity_counts,
                "alerts_by_type": type_counts,
                "alerts_by_system": system_counts,
                "alert_counters": self.alert_counters
            }
            
            # Record operation
            self.record_operation("get_alert_summary", True, 0.0)
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to get alert summary: {e}")
            self.record_operation("get_alert_summary", False, 0.0)
            return {"error": str(e)}
    
    def clear_resolved_alerts(self) -> int:
        """Clear resolved alerts from history"""
        try:
            resolved_count = 0
            alerts_to_remove = []
            
            for alert in self.alert_history:
                if alert.resolved:
                    alerts_to_remove.append(alert)
                    resolved_count += 1
            
            for alert in alerts_to_remove:
                self.alert_history.remove(alert)
            
            # Record operation
            self.record_operation("clear_resolved_alerts", True, 0.0)
            
            self.logger.info(f"Cleared {resolved_count} resolved gaming alerts")
            return resolved_count
            
        except Exception as e:
            self.logger.error(f"Failed to clear resolved alerts: {e}")
            self.record_operation("clear_resolved_alerts", False, 0.0)
            return 0
    
    def set_alert_threshold(self, metric: str, severity: str, value: float):
        """Set alert threshold for a metric"""
        try:
            if metric not in self.alert_thresholds:
                self.alert_thresholds[metric] = {}
            
            self.alert_thresholds[metric][severity] = value
            
            # Record operation
            self.record_operation("set_alert_threshold", True, 0.0)
            
            self.logger.info(f"Set {metric} {severity} threshold to {value}")
            
        except Exception as e:
            self.logger.error(f"Failed to set alert threshold: {e}")
            self.record_operation("set_alert_threshold", False, 0.0)
    
    def get_alert_thresholds(self) -> Dict[str, Any]:
        """Get current alert thresholds"""
        try:
            thresholds = self.alert_thresholds.copy()
            
            # Record operation
            self.record_operation("get_alert_thresholds", True, 0.0)
            
            return thresholds
            
        except Exception as e:
            self.logger.error(f"Failed to get alert thresholds: {e}")
            self.record_operation("get_alert_thresholds", False, 0.0)
            return {}
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _load_default_thresholds(self):
        """Load default alert thresholds"""
        try:
            # Default thresholds are already set in __init__
            self.logger.debug("Default thresholds loaded")
            
        except Exception as e:
            self.logger.error(f"Failed to load default thresholds: {e}")
    
    def _save_alert_history(self):
        """Save alert history to persistent storage"""
        try:
            # Create persistence directory if it doesn't exist
            persistence_dir = Path("data/persistent/gaming_alerts")
            persistence_dir.mkdir(parents=True, exist_ok=True)
            
            # Prepare data for persistence
            alert_data = {
                "active_alerts": {k: v.__dict__ for k, v in self.active_alerts.items()},
                "alert_history": [alert.__dict__ for alert in self.alert_history],
                "alert_thresholds": self.alert_thresholds,
                "timestamp": datetime.now().isoformat(),
                "manager_id": self.manager_id,
                "version": "2.0.0"
            }
            
            # Save to JSON file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"gaming_alerts_data_{timestamp}.json"
            filepath = persistence_dir / filename
            
            with open(filepath, 'w') as f:
                json.dump(alert_data, f, indent=2, default=str)
            
            # Keep only the latest 5 backup files
            self._cleanup_old_backups(persistence_dir, "gaming_alerts_data_*.json", 5)
            
            self.logger.info(f"Alert history saved to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to save alert history: {e}")
            # Fallback to basic logging if persistence fails
            self.logger.warning("Persistence failed, data only logged in memory")
    
    def _cleanup_old_backups(self, directory: Path, pattern: str, keep_count: int):
        """Clean up old backup files, keeping only the specified number"""
        try:
            files = list(directory.glob(pattern))
            if len(files) > keep_count:
                # Sort by modification time (oldest first)
                files.sort(key=lambda x: x.stat().st_mtime)
                # Remove oldest files
                for old_file in files[:-keep_count]:
                    old_file.unlink()
                    self.logger.debug(f"Removed old backup: {old_file}")
        except Exception as e:
            self.logger.warning(f"Failed to cleanup old backups: {e}")
    
    def _check_stale_alerts(self):
        """Check for stale alerts that need attention"""
        try:
            current_time = time.time()
            stale_threshold = 3600  # 1 hour
            
            for alert_id, alert in list(self.active_alerts.items()):
                alert_timestamp = float(alert.timestamp.split('T')[0].replace('-', ''))
                if current_time - alert_timestamp > stale_threshold:
                    self.logger.warning(f"Stale alert detected: {alert_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to check stale alerts: {e}")


#!/usr/bin/env python3
"""
Emergency Detector - Component of Emergency Response System
=========================================================

Responsible for detecting system failures and emergency conditions.
Extracted from EmergencyResponseSystem to follow Single Responsibility Principle.

Author: Agent-7 (Class Hierarchy Refactoring)
Contract: MODULAR-002: Class Hierarchy Refactoring (400 pts)
License: MIT
"""

import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from ..base_manager import BaseManager
from ..health.types.health_types import HealthAlert, HealthLevel
from ..health.monitoring.health_monitoring_manager import HealthMonitoringManager
from ..health.alerting.health_alert_manager import HealthAlertManager


logger = logging.getLogger(__name__)


@dataclass
class FailureThreshold:
    """Failure detection threshold configuration"""
    name: str
    value: Any
    operator: str  # 'gt', 'lt', 'eq', 'gte', 'lte'
    description: str
    critical: bool = False


@dataclass
class FailureDetection:
    """Failure detection result"""
    threshold_name: str
    current_value: Any
    threshold_value: Any
    triggered: bool
    severity: str
    timestamp: datetime
    description: str


class EmergencyDetector(BaseManager):
    """
    Emergency Detector - Single responsibility: Failure detection and monitoring
    
    This component is responsible for:
    - Monitoring system health metrics
    - Detecting threshold violations
    - Triggering emergency alerts
    - Providing failure analysis
    """

    def __init__(self, config_path: str = "config/emergency_detector.json"):
        """Initialize emergency detector"""
        super().__init__(
            manager_name="EmergencyDetector",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        # Health monitoring integration
        self.health_monitor: Optional[HealthMonitoringManager] = None
        self.health_alerts: Optional[HealthAlertManager] = None
        
        # Failure detection thresholds
        self.failure_thresholds: Dict[str, FailureThreshold] = {}
        
        # Detection state
        self.detection_active = False
        self.last_detection_run: Optional[datetime] = None
        self.detection_history: List[FailureDetection] = []
        
        # Load configuration and setup
        self._load_detector_config()
        self._setup_default_thresholds()
        
        self.logger.info("✅ Emergency Detector initialized successfully")

    def _load_detector_config(self):
        """Load detector configuration"""
        try:
            config = self.get_config()
            
            # Load custom thresholds if available
            if 'custom_thresholds' in config:
                for threshold_data in config['custom_thresholds']:
                    threshold = FailureThreshold(**threshold_data)
                    self.failure_thresholds[threshold.name] = threshold
            
        except Exception as e:
            self.logger.error(f"Failed to load detector config: {e}")

    def _setup_default_thresholds(self):
        """Setup default failure detection thresholds"""
        self.failure_thresholds = {
            "contract_availability": FailureThreshold(
                name="contract_availability",
                value=30,
                operator="lt",
                description="Minimum contracts available",
                critical=True
            ),
            "agent_idle_time": FailureThreshold(
                name="agent_idle_time",
                value=900,  # 15 minutes in seconds
                operator="gt",
                description="Maximum agent idle time",
                critical=False
            ),
            "system_response_time": FailureThreshold(
                name="system_response_time",
                value=5000,  # 5 seconds in milliseconds
                operator="gt",
                description="Maximum system response time",
                critical=False
            ),
            "error_rate": FailureThreshold(
                name="error_rate",
                value=0.20,  # 20% error rate threshold
                operator="gt",
                description="Maximum error rate",
                critical=True
            ),
            "health_score": FailureThreshold(
                name="health_score",
                value=0.70,  # 70% health score threshold
                operator="lt",
                description="Minimum system health score",
                critical=True
            )
        }

    def set_health_integration(self, health_monitor: HealthMonitoringManager, 
                              health_alerts: HealthAlertManager):
        """Set health monitoring integration"""
        self.health_monitor = health_monitor
        self.health_alerts = health_alerts
        self.logger.info("✅ Health monitoring integration configured")

    def add_threshold(self, threshold: FailureThreshold):
        """Add a custom failure threshold"""
        self.failure_thresholds[threshold.name] = threshold
        self.logger.info(f"✅ Added failure threshold: {threshold.name}")

    def remove_threshold(self, threshold_name: str):
        """Remove a failure threshold"""
        if threshold_name in self.failure_thresholds:
            del self.failure_thresholds[threshold_name]
            self.logger.info(f"✅ Removed failure threshold: {threshold_name}")

    def run_detection(self) -> List[FailureDetection]:
        """Run failure detection analysis"""
        if not self.detection_active:
            self.logger.warning("⚠️ Detection not active")
            return []

        try:
            self.last_detection_run = datetime.now()
            detections = []
            
            # Check each threshold
            for threshold_name, threshold in self.failure_thresholds.items():
                detection = self._check_threshold(threshold)
                if detection:
                    detections.append(detection)
                    self.detection_history.append(detection)
                    
                    # Trigger health alert if critical
                    if threshold.critical and detection.triggered:
                        self._trigger_critical_alert(detection)
            
            # Update metrics
            self.record_metric("detection_runs", 1)
            self.record_metric("failures_detected", len([d for d in detections if d.triggered]))
            
            return detections
            
        except Exception as e:
            self.logger.error(f"Failed to run detection: {e}")
            return []

    def _check_threshold(self, threshold: FailureThreshold) -> Optional[FailureDetection]:
        """Check if a specific threshold is violated"""
        try:
            current_value = self._get_current_value(threshold.name)
            
            if current_value is None:
                return None
            
            # Determine if threshold is triggered
            triggered = self._evaluate_threshold(current_value, threshold)
            
            # Determine severity
            severity = "CRITICAL" if threshold.critical else "WARNING"
            
            detection = FailureDetection(
                threshold_name=threshold.name,
                current_value=current_value,
                threshold_value=threshold.value,
                triggered=triggered,
                severity=severity,
                timestamp=datetime.now(),
                description=threshold.description
            )
            
            return detection
            
        except Exception as e:
            self.logger.error(f"Failed to check threshold {threshold.name}: {e}")
            return None

    def _get_current_value(self, threshold_name: str) -> Optional[Any]:
        """Get current value for a specific threshold"""
        try:
            if threshold_name == "contract_availability":
                return self._get_available_contract_count()
            elif threshold_name == "agent_idle_time":
                return self._get_max_agent_idle_time()
            elif threshold_name == "system_response_time":
                return self._get_system_response_time()
            elif threshold_name == "error_rate":
                return self._get_system_error_rate()
            elif threshold_name == "health_score":
                return self._get_system_health_score()
            else:
                self.logger.warning(f"Unknown threshold: {threshold_name}")
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to get current value for {threshold_name}: {e}")
            return None

    def _evaluate_threshold(self, current_value: Any, threshold: FailureThreshold) -> bool:
        """Evaluate if threshold is violated based on operator"""
        try:
            if threshold.operator == "gt":
                return current_value > threshold.value
            elif threshold.operator == "lt":
                return current_value < threshold.value
            elif threshold.operator == "eq":
                return current_value == threshold.value
            elif threshold.operator == "gte":
                return current_value >= threshold.value
            elif threshold.operator == "lte":
                return current_value <= threshold.value
            else:
                self.logger.warning(f"Unknown operator: {threshold.operator}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to evaluate threshold: {e}")
            return False

    def _trigger_critical_alert(self, detection: FailureDetection):
        """Trigger a critical health alert"""
        try:
            if self.health_alerts:
                alert = HealthAlert(
                    level=HealthLevel.CRITICAL,
                    message=f"Critical failure detected: {detection.description}",
                    source="EmergencyDetector",
                    details={
                        "threshold": detection.threshold_name,
                        "current_value": detection.current_value,
                        "threshold_value": detection.threshold_value,
                        "timestamp": detection.timestamp.isoformat()
                    }
                )
                self.health_alerts.raise_alert(alert)
                self.logger.warning(f"🚨 Critical alert triggered: {detection.description}")
                
        except Exception as e:
            self.logger.error(f"Failed to trigger critical alert: {e}")

    def _get_available_contract_count(self) -> int:
        """Get count of available contracts"""
        try:
            # This would integrate with the contract system
            # For now, return placeholder value
            return 50  # Placeholder
            
        except Exception as e:
            self.logger.error(f"Failed to get contract count: {e}")
            return 0

    def _get_max_agent_idle_time(self) -> int:
        """Get maximum agent idle time in seconds"""
        try:
            # This would integrate with agent monitoring
            # For now, return placeholder value
            return 0  # Placeholder
            
        except Exception as e:
            self.logger.error(f"Failed to get agent idle time: {e}")
            return 0

    def _get_system_response_time(self) -> int:
        """Get system response time in milliseconds"""
        try:
            # This would integrate with performance monitoring
            # For now, return placeholder value
            return 100  # Placeholder
            
        except Exception as e:
            self.logger.error(f"Failed to get system response time: {e}")
            return 100

    def _get_system_error_rate(self) -> float:
        """Get system error rate as percentage"""
        try:
            # This would integrate with error monitoring
            # For now, return placeholder value
            return 0.05  # 5% placeholder
            
        except Exception as e:
            self.logger.error(f"Failed to get system error rate: {e}")
            return 0.05

    def _get_system_health_score(self) -> float:
        """Get overall system health score"""
        try:
            if self.health_monitor:
                health_summary = self.health_monitor.get_health_summary()
                return health_summary.get("overall_health_score", 1.0)
            else:
                return 1.0  # Default healthy score
                
        except Exception as e:
            self.logger.error(f"Failed to get health score: {e}")
            return 1.0

    def start_detection(self):
        """Start continuous failure detection"""
        self.detection_active = True
        self.logger.info("✅ Failure detection started")

    def stop_detection(self):
        """Stop continuous failure detection"""
        self.detection_active = False
        self.logger.info("⏹️ Failure detection stopped")

    def get_detection_status(self) -> Dict[str, Any]:
        """Get current detection status"""
        return {
            "detection_active": self.detection_active,
            "last_detection_run": self.last_detection_run.isoformat() if self.last_detection_run else None,
            "total_thresholds": len(self.failure_thresholds),
            "total_detections": len(self.detection_history),
            "critical_thresholds": len([t for t in self.failure_thresholds.values() if t.critical])
        }

    def get_detection_history(self) -> List[Dict[str, Any]]:
        """Get detection history"""
        return [
            {
                "threshold_name": d.threshold_name,
                "current_value": d.current_value,
                "threshold_value": d.threshold_value,
                "triggered": d.triggered,
                "severity": d.severity,
                "timestamp": d.timestamp.isoformat(),
                "description": d.description
            }
            for d in self.detection_history
        ]

    def health_check(self) -> Dict[str, Any]:
        """Health check for the emergency detector"""
        try:
            return {
                "is_healthy": True,
                "detection_active": self.detection_active,
                "total_thresholds": len(self.failure_thresholds),
                "total_detections": len(self.detection_history),
                "last_detection": self.last_detection_run.isoformat() if self.last_detection_run else None,
                "health_monitor_connected": self.health_monitor is not None,
                "health_alerts_connected": self.health_alerts is not None
            }
            
        except Exception as e:
            return {
                "is_healthy": False,
                "error": str(e)
            }


# Export the main class
__all__ = ["EmergencyDetector", "FailureThreshold", "FailureDetection"]

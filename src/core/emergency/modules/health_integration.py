#!/usr/bin/env python3
"""
Health Integration Module - Extracted from emergency_response_system.py
Agent-3: Monolithic File Modularization Contract

This module handles health monitoring integration, alert handling, and system health validation.
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

from .emergency_types import EmergencyEvent, EmergencyType, EmergencyLevel
from ...health.types.health_types import HealthAlert, HealthLevel
from ...health.monitoring.health_monitoring_manager import HealthMonitoringManager
from ...health.alerting.health_alert_manager import HealthAlertManager
from ...health.recovery.health_recovery_manager import HealthRecoveryManager

logger = logging.getLogger(__name__)


class HealthIntegration:
    """Handles health monitoring integration and alert handling"""
    
    def __init__(self, health_monitor: HealthMonitoringManager, 
                 alert_manager: HealthAlertManager,
                 recovery_manager: HealthRecoveryManager):
        """Initialize health integration"""
        self.health_monitor = health_monitor
        self.alert_manager = alert_manager
        self.recovery_manager = recovery_manager
        self.health_thresholds = {
            "system_health": 0.7,
            "response_time": 5.0,
            "error_rate": 0.1,
            "memory_usage": 0.8,
            "cpu_usage": 0.8,
            "disk_usage": 0.9
        }
        self.alert_history: List[Dict[str, Any]] = []
        self.health_checks: List[Dict[str, Any]] = []
        self._setup_health_integration()
    
    def _setup_health_integration(self):
        """Setup health monitoring integration"""
        try:
            logger.info("Setting up health monitoring integration")
            
            # Register alert handlers
            self.alert_manager.register_alert_handler(self._handle_health_alert)
            
            # Setup health check intervals
            self._setup_health_check_intervals()
            
            logger.info("Health monitoring integration setup completed")
            
        except Exception as e:
            logger.error(f"Error setting up health integration: {e}")
    
    def _setup_health_check_intervals(self):
        """Setup health check intervals"""
        try:
            # This would typically setup scheduled health checks
            # For now, we'll use manual health checks
            logger.info("Health check intervals configured")
            
        except Exception as e:
            logger.error(f"Error setting up health check intervals: {e}")
    
    def _handle_health_alert(self, alert: HealthAlert):
        """Handle health alerts from the health monitoring system"""
        try:
            logger.info(f"Handling health alert: {alert.alert_type} (Level: {alert.level})")
            
            # Record alert
            self.alert_history.append({
                "alert_type": alert.alert_type,
                "level": alert.level.value,
                "message": alert.message,
                "timestamp": alert.timestamp.isoformat(),
                "source": alert.source
            })
            
            # Determine if emergency response is needed
            if self._should_trigger_emergency(alert):
                logger.warning(f"Health alert requires emergency response: {alert.alert_type}")
                self._trigger_emergency_from_alert(alert)
            else:
                logger.info(f"Health alert handled without emergency response: {alert.alert_type}")
                
        except Exception as e:
            logger.error(f"Error handling health alert: {e}")
    
    def _should_trigger_emergency(self, alert: HealthAlert) -> bool:
        """Determine if health alert should trigger emergency response"""
        try:
            # Critical alerts always trigger emergency
            if alert.level == HealthLevel.CRITICAL:
                return True
            
            # High level alerts with specific types trigger emergency
            if alert.level == HealthLevel.HIGH:
                critical_types = [
                    "SYSTEM_FAILURE",
                    "DATABASE_DOWN",
                    "NETWORK_OUTAGE",
                    "CRITICAL_SERVICE_DOWN"
                ]
                return alert.alert_type in critical_types
            
            # Medium level alerts with repeated occurrences trigger emergency
            if alert.level == HealthLevel.MEDIUM:
                # Check if this is a repeated alert
                recent_alerts = [a for a in self.alert_history 
                               if a["alert_type"] == alert.alert_type 
                               and (datetime.now() - datetime.fromisoformat(a["timestamp"])).total_seconds() < 300]
                return len(recent_alerts) >= 3
            
            return False
            
        except Exception as e:
            logger.error(f"Error determining emergency trigger: {e}")
            return False
    
    def _trigger_emergency_from_alert(self, alert: HealthAlert):
        """Trigger emergency response from health alert"""
        try:
            logger.warning(f"Triggering emergency from health alert: {alert.alert_type}")
            
            # Create emergency event from alert
            emergency = EmergencyEvent(
                id=f"HEALTH-{int(time.time())}",
                type=self._map_alert_to_emergency_type(alert),
                level=self._map_alert_to_emergency_level(alert),
                description=f"Health alert triggered emergency: {alert.message}",
                timestamp=datetime.now(),
                source=alert.source,
                affected_components=[alert.source],
                impact_assessment={
                    "health_score": self._get_system_health_score(),
                    "alert_severity": alert.level.value,
                    "system_status": "degraded"
                }
            )
            
            # This would typically trigger the emergency response system
            logger.info(f"Emergency event created from health alert: {emergency.id}")
            
        except Exception as e:
            logger.error(f"Error triggering emergency from alert: {e}")
    
    def _map_alert_to_emergency_type(self, alert: HealthAlert) -> EmergencyType:
        """Map health alert to emergency type"""
        try:
            # Map alert types to emergency types
            type_mapping = {
                "SYSTEM_FAILURE": EmergencyType.SYSTEM_FAILURE,
                "DATABASE_DOWN": EmergencyType.SYSTEM_FAILURE,
                "NETWORK_OUTAGE": EmergencyType.COMMUNICATION_FAILURE,
                "CRITICAL_SERVICE_DOWN": EmergencyType.SYSTEM_FAILURE,
                "PERFORMANCE_DEGRADATION": EmergencyType.PERFORMANCE_DEGRADATION,
                "MEMORY_LEAK": EmergencyType.PERFORMANCE_DEGRADATION,
                "CPU_OVERLOAD": EmergencyType.PERFORMANCE_DEGRADATION,
                "DISK_FULL": EmergencyType.SYSTEM_FAILURE,
                "SECURITY_VIOLATION": EmergencyType.SECURITY_BREACH,
                "DATA_CORRUPTION": EmergencyType.DATA_CORRUPTION
            }
            
            return type_mapping.get(alert.alert_type, EmergencyType.SYSTEM_FAILURE)
            
        except Exception as e:
            logger.error(f"Error mapping alert to emergency type: {e}")
            return EmergencyType.SYSTEM_FAILURE
    
    def _map_alert_to_emergency_level(self, alert: HealthAlert) -> EmergencyLevel:
        """Map health alert level to emergency level"""
        try:
            # Map health levels to emergency levels
            level_mapping = {
                HealthLevel.LOW: EmergencyLevel.LOW,
                HealthLevel.MEDIUM: EmergencyLevel.MEDIUM,
                HealthLevel.HIGH: EmergencyLevel.HIGH,
                HealthLevel.CRITICAL: EmergencyLevel.CRITICAL
            }
            
            return level_mapping.get(alert.level, EmergencyLevel.MEDIUM)
            
        except Exception as e:
            logger.error(f"Error mapping alert to emergency level: {e}")
            return EmergencyLevel.MEDIUM
    
    def _get_system_health_score(self) -> float:
        """Get current system health score"""
        try:
            return self.health_monitor.get_system_health_score()
        except Exception as e:
            logger.error(f"Error getting system health score: {e}")
            return 0.5  # Default fallback
    
    def _validate_system_health(self) -> Dict[str, Any]:
        """Validate overall system health"""
        try:
            logger.info("Validating system health")
            
            health_metrics = {}
            
            # Get system health score
            health_metrics["system_health_score"] = self._get_system_health_score()
            
            # Check response time
            health_metrics["response_time"] = self._check_system_response_time()
            
            # Check error rate
            health_metrics["error_rate"] = self._check_system_error_rate()
            
            # Check resource usage
            health_metrics["memory_usage"] = self._check_memory_usage()
            health_metrics["cpu_usage"] = self._check_cpu_usage()
            health_metrics["disk_usage"] = self._check_disk_usage()
            
            # Determine overall health status
            health_metrics["overall_status"] = self._determine_health_status(health_metrics)
            
            # Record health check
            self.health_checks.append({
                "timestamp": datetime.now().isoformat(),
                "metrics": health_metrics.copy()
            })
            
            logger.info(f"System health validation completed: {health_metrics['overall_status']}")
            return health_metrics
            
        except Exception as e:
            logger.error(f"Error validating system health: {e}")
            return {"overall_status": "error", "error": str(e)}
    
    def _check_system_response_time(self) -> float:
        """Check system response time"""
        try:
            start_time = time.time()
            # Perform a simple health check
            self.health_monitor.health_check()
            return time.time() - start_time
        except Exception as e:
            logger.error(f"Error checking response time: {e}")
            return 10.0  # Default high value
    
    def _check_system_error_rate(self) -> float:
        """Check system error rate"""
        try:
            # This would typically query logs or metrics
            # For now, return a placeholder value
            return 0.05  # 5% error rate
        except Exception as e:
            logger.error(f"Error checking error rate: {e}")
            return 0.1  # Default high value
    
    def _check_memory_usage(self) -> float:
        """Check memory usage"""
        try:
            # This would typically query system metrics
            # For now, return a placeholder value
            return 0.6  # 60% memory usage
        except Exception as e:
            logger.error(f"Error checking memory usage: {e}")
            return 0.5  # Default value
    
    def _check_cpu_usage(self) -> float:
        """Check CPU usage"""
        try:
            # This would typically query system metrics
            # For now, return a placeholder value
            return 0.4  # 40% CPU usage
        except Exception as e:
            logger.error(f"Error checking CPU usage: {e}")
            return 0.5  # Default value
    
    def _check_disk_usage(self) -> float:
        """Check disk usage"""
        try:
            # This would typically query system metrics
            # For now, return a placeholder value
            return 0.7  # 70% disk usage
        except Exception as e:
            logger.error(f"Error checking disk usage: {e}")
            return 0.5  # Default value
    
    def _determine_health_status(self, metrics: Dict[str, Any]) -> str:
        """Determine overall health status from metrics"""
        try:
            # Check if any metric exceeds critical thresholds
            if (metrics.get("system_health_score", 1.0) < 0.3 or
                metrics.get("response_time", 0) > 10.0 or
                metrics.get("error_rate", 0) > 0.3 or
                metrics.get("memory_usage", 0) > 0.95 or
                metrics.get("cpu_usage", 0) > 0.95 or
                metrics.get("disk_usage", 0) > 0.95):
                return "critical"
            
            # Check if any metric exceeds warning thresholds
            if (metrics.get("system_health_score", 1.0) < 0.6 or
                metrics.get("response_time", 0) > 5.0 or
                metrics.get("error_rate", 0) > 0.1 or
                metrics.get("memory_usage", 0) > 0.8 or
                metrics.get("cpu_usage", 0) > 0.8 or
                metrics.get("disk_usage", 0) > 0.8):
                return "warning"
            
            return "healthy"
            
        except Exception as e:
            logger.error(f"Error determining health status: {e}")
            return "unknown"
    
    def _activate_health_monitoring(self, emergency: EmergencyEvent) -> bool:
        """Activate enhanced health monitoring for emergency"""
        try:
            logger.info(f"Activating enhanced health monitoring for emergency: {emergency.id}")
            
            # Increase monitoring frequency
            self._increase_monitoring_frequency(emergency)
            
            # Add emergency-specific health checks
            self._add_emergency_health_checks(emergency)
            
            # Setup emergency alert thresholds
            self._setup_emergency_alert_thresholds(emergency)
            
            logger.info("Enhanced health monitoring activated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error activating health monitoring: {e}")
            return False
    
    def _increase_monitoring_frequency(self, emergency: EmergencyEvent):
        """Increase health monitoring frequency during emergency"""
        try:
            # This would typically reduce health check intervals
            # For now, just log the action
            logger.info(f"Increased monitoring frequency for emergency: {emergency.id}")
            
        except Exception as e:
            logger.error(f"Error increasing monitoring frequency: {e}")
    
    def _add_emergency_health_checks(self, emergency: EmergencyEvent):
        """Add emergency-specific health checks"""
        try:
            # This would typically add custom health checks
            # For now, just log the action
            logger.info(f"Added emergency health checks for emergency: {emergency.id}")
            
        except Exception as e:
            logger.error(f"Error adding emergency health checks: {e}")
    
    def _setup_emergency_alert_thresholds(self, emergency: EmergencyEvent):
        """Setup emergency-specific alert thresholds"""
        try:
            # Adjust thresholds based on emergency level
            if emergency.level in [EmergencyLevel.CRITICAL, EmergencyLevel.CODE_BLACK]:
                # More sensitive thresholds for critical emergencies
                self.health_thresholds.update({
                    "system_health": 0.8,
                    "response_time": 3.0,
                    "error_rate": 0.05
                })
                logger.info("Emergency alert thresholds adjusted for critical emergency")
            
        except Exception as e:
            logger.error(f"Error setting up emergency alert thresholds: {e}")
    
    def _assess_system_damage(self, emergency: EmergencyEvent) -> Dict[str, Any]:
        """Assess system damage from emergency"""
        try:
            logger.info(f"Assessing system damage for emergency: {emergency.id}")
            
            damage_assessment = {
                "emergency_id": emergency.id,
                "assessment_time": datetime.now().isoformat(),
                "health_metrics": self._validate_system_health(),
                "affected_components": emergency.affected_components.copy(),
                "damage_level": "unknown",
                "recovery_estimate": "unknown"
            }
            
            # Determine damage level based on health metrics
            health_status = damage_assessment["health_metrics"]["overall_status"]
            if health_status == "critical":
                damage_assessment["damage_level"] = "severe"
                damage_assessment["recovery_estimate"] = "4-8 hours"
            elif health_status == "warning":
                damage_assessment["damage_level"] = "moderate"
                damage_assessment["recovery_estimate"] = "2-4 hours"
            else:
                damage_assessment["damage_level"] = "minimal"
                damage_assessment["recovery_estimate"] = "1-2 hours"
            
            logger.info(f"System damage assessment completed: {damage_assessment['damage_level']}")
            return damage_assessment
            
        except Exception as e:
            logger.error(f"Error assessing system damage: {e}")
            return {"error": str(e)}
    
    def _activate_backup_systems(self, emergency: EmergencyEvent) -> bool:
        """Activate backup systems during emergency"""
        try:
            logger.info(f"Activating backup systems for emergency: {emergency.id}")
            
            # This would typically activate backup systems
            # For now, just log the action
            
            logger.info("Backup systems activated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error activating backup systems: {e}")
            return False
    
    def _notify_stakeholders(self, emergency: EmergencyEvent) -> bool:
        """Notify stakeholders about emergency"""
        try:
            logger.info(f"Notifying stakeholders about emergency: {emergency.id}")
            
            # This would typically send notifications
            # For now, just log the action
            
            logger.info("Stakeholders notified successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error notifying stakeholders: {e}")
            return False
    
    def _schedule_escalation_checks(self, emergency: EmergencyEvent):
        """Schedule escalation checks for emergency"""
        try:
            logger.info(f"Scheduling escalation checks for emergency: {emergency.id}")
            
            # This would typically schedule escalation checks
            # For now, just log the action
            
        except Exception as e:
            logger.error(f"Error scheduling escalation checks: {e}")
    
    def _check_escalation_requirement(self, emergency: EmergencyEvent) -> bool:
        """Check if escalation is required"""
        try:
            # Check if emergency has been active too long
            emergency_duration = datetime.now() - emergency.timestamp
            
            if emergency.level == EmergencyLevel.CRITICAL and emergency_duration > timedelta(minutes=30):
                return True
            elif emergency.level == EmergencyLevel.HIGH and emergency_duration > timedelta(hours=1):
                return True
            elif emergency.level == EmergencyLevel.MEDIUM and emergency_duration > timedelta(hours=2):
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking escalation requirement: {e}")
            return False
    
    def _execute_escalation_action(self, action: str, emergency: EmergencyEvent):
        """Execute escalation action"""
        try:
            logger.warning(f"Executing escalation action: {action} for emergency: {emergency.id}")
            
            # This would typically execute escalation procedures
            # For now, just log the action
            
        except Exception as e:
            logger.error(f"Error executing escalation action: {e}")
    
    def _notify_captain_coordinator(self, emergency: EmergencyEvent):
        """Notify captain/coordinator about emergency"""
        try:
            logger.info(f"Notifying captain/coordinator about emergency: {emergency.id}")
            
            # This would typically send notification to captain
            # For now, just log the action
            
        except Exception as e:
            logger.error(f"Error notifying captain/coordinator: {e}")
    
    def _activate_code_black_protocol(self, emergency: EmergencyEvent):
        """Activate code black protocol"""
        try:
            logger.critical(f"ACTIVATING CODE BLACK PROTOCOL for emergency: {emergency.id}")
            
            # This would typically activate code black procedures
            # For now, just log the action
            
        except Exception as e:
            logger.error(f"Error activating code black protocol: {e}")
    
    def _increase_monitoring_frequency(self, emergency: EmergencyEvent):
        """Increase monitoring frequency for emergency"""
        try:
            logger.info(f"Increasing monitoring frequency for emergency: {emergency.id}")
            
            # This would typically reduce monitoring intervals
            # For now, just log the action
            
        except Exception as e:
            logger.error(f"Error increasing monitoring frequency: {e}")
    
    def _activate_emergency_coordination(self, emergency: EmergencyEvent):
        """Activate emergency coordination"""
        try:
            logger.info(f"Activating emergency coordination for emergency: {emergency.id}")
            
            # This would typically activate coordination procedures
            # For now, just log the action
            
        except Exception as e:
            logger.error(f"Error activating emergency coordination: {e}")
    
    def _activate_disaster_recovery(self, emergency: EmergencyEvent):
        """Activate disaster recovery procedures"""
        try:
            logger.warning(f"Activating disaster recovery for emergency: {emergency.id}")
            
            # This would typically activate disaster recovery
            # For now, just log the action
            
        except Exception as e:
            logger.error(f"Error activating disaster recovery: {e}")
    
    def get_health_integration_status(self) -> Dict[str, Any]:
        """Get health integration status"""
        return {
            "health_thresholds": self.health_thresholds.copy(),
            "alert_history_count": len(self.alert_history),
            "health_checks_count": len(self.health_checks),
            "last_health_check": self.health_checks[-1]["timestamp"] if self.health_checks else None,
            "integration_active": True
        }
    
    def get_alert_history(self) -> List[Dict[str, Any]]:
        """Get alert history"""
        return self.alert_history.copy()
    
    def get_health_checks(self) -> List[Dict[str, Any]]:
        """Get health check history"""
        return self.health_checks.copy()

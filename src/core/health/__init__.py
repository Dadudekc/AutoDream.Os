#!/usr/bin/env python3
"""
Health Package - V2 Modular Architecture
=======================================

Unified health management system with modular components.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

# Main unified system
from .unified_health_manager import UnifiedHealthManager

# Core types
from .types.health_types import (
    HealthLevel, AlertType, NotificationChannel, HealthMetric, 
    HealthAlert, NotificationConfig, HealthThreshold, HealthTrend, RecoveryAction
)

# Modular components
from .monitoring.health_monitoring_manager import HealthMonitoringManager
from .alerting.health_alert_manager import HealthAlertManager
from .analysis.health_analysis_manager import HealthAnalysisManager
from .notifications.health_notification_manager import HealthNotificationManager
from .recovery.health_recovery_manager import HealthRecoveryManager

# Backwards compatibility aliases
HealthManager = UnifiedHealthManager
HealthAlertManager = UnifiedHealthManager
HealthThresholdManager = UnifiedHealthManager
HealthNotificationManager = UnifiedHealthManager

__all__ = [
    # Main system
    "UnifiedHealthManager",
    
    # Core types
    "HealthLevel",
    "AlertType", 
    "NotificationChannel",
    "HealthMetric",
    "HealthAlert",
    "NotificationConfig",
    "HealthThreshold",
    "HealthTrend",
    "RecoveryAction",
    
    # Modular components
    "HealthMonitoringManager",
    "HealthAlertManager",
    "HealthAnalysisManager",
    "HealthNotificationManager",
    "HealthRecoveryManager",
    
    # Backwards compatibility
    "HealthManager",
    "HealthAlertManager",
    "HealthThresholdManager",
    "HealthNotificationManager",
]

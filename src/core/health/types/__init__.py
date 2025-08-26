#!/usr/bin/env python3
"""
Health Types Package - V2 Modular Architecture
=============================================

Core data structures for health management system.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .health_types import (
    HealthLevel,
    AlertType,
    NotificationChannel,
    HealthMetric,
    HealthAlert,
    NotificationConfig,
    HealthThreshold,
    HealthTrend,
    RecoveryAction
)

__all__ = [
    "HealthLevel",
    "AlertType",
    "NotificationChannel", 
    "HealthMetric",
    "HealthAlert",
    "NotificationConfig",
    "HealthThreshold",
    "HealthTrend",
    "RecoveryAction"
]


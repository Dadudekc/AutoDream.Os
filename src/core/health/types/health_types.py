#!/usr/bin/env python3
"""
Health Types - V2 Modular Architecture
=====================================

Core data structures for health management system.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class HealthLevel(Enum):
    """Health levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class AlertType(Enum):
    """Alert types"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class NotificationChannel(Enum):
    """Notification channels"""
    EMAIL = "email"
    SMS = "sms"
    WEBHOOK = "webhook"
    SLACK = "slack"
    DISCORD = "discord"
    LOG = "log"


@dataclass
class HealthMetric:
    """Health metric definition"""
    name: str
    value: float
    unit: str
    threshold_min: Optional[float]
    threshold_max: Optional[float]
    current_level: HealthLevel
    timestamp: str
    trend: str  # increasing, decreasing, stable
    description: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metric to dictionary"""
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "threshold_min": self.threshold_min,
            "threshold_max": self.threshold_max,
            "current_level": self.current_level.value,
            "timestamp": self.timestamp,
            "trend": self.trend,
            "description": self.description
        }


@dataclass
class HealthAlert:
    """Health alert definition"""
    id: str
    type: AlertType
    level: HealthLevel
    component: str
    message: str
    metric_name: str
    metric_value: float
    threshold: float
    timestamp: str
    acknowledged: bool
    acknowledged_by: Optional[str]
    acknowledged_at: Optional[str]
    resolved: bool
    resolved_at: Optional[str]
    metadata: Dict[str, Any]
    
    def is_active(self) -> bool:
        """Check if alert is active (not resolved)"""
        return not self.resolved
    
    def is_acknowledged(self) -> bool:
        """Check if alert is acknowledged"""
        return self.acknowledged
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary"""
        return {
            "id": self.id,
            "type": self.type.value,
            "level": self.level.value,
            "component": self.component,
            "message": self.message,
            "metric_name": self.metric_name,
            "metric_value": self.metric_value,
            "threshold": self.threshold,
            "timestamp": self.timestamp,
            "acknowledged": self.acknowledged,
            "acknowledged_by": self.acknowledged_by,
            "acknowledged_at": self.acknowledged_at,
            "resolved": self.resolved,
            "resolved_at": self.resolved_at,
            "metadata": self.metadata
        }


@dataclass
class NotificationConfig:
    """Notification configuration"""
    channel: NotificationChannel
    enabled: bool
    recipients: List[str]
    config: Dict[str, Any]
    schedule: Dict[str, Any]  # time windows, frequency
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "channel": self.channel.value,
            "enabled": self.enabled,
            "recipients": self.recipients,
            "config": self.config,
            "schedule": self.schedule
        }


@dataclass
class HealthThreshold:
    """Health threshold definition"""
    metric_name: str
    warning_value: float
    critical_value: float
    emergency_value: Optional[float] = None
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert threshold to dictionary"""
        return {
            "metric_name": self.metric_name,
            "warning_value": self.warning_value,
            "critical_value": self.critical_value,
            "emergency_value": self.emergency_value,
            "description": self.description
        }


@dataclass
class HealthTrend:
    """Health trend analysis result"""
    metric_name: str
    current_value: float
    previous_value: float
    change_percent: float
    trend_direction: str  # increasing, decreasing, stable
    trend_strength: str   # strong, moderate, weak
    prediction_hours: int
    confidence: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert trend to dictionary"""
        return {
            "metric_name": self.metric_name,
            "current_value": self.current_value,
            "previous_value": self.previous_value,
            "change_percent": self.change_percent,
            "trend_direction": self.trend_direction,
            "trend_strength": self.trend_strength,
            "prediction_hours": self.prediction_hours,
            "confidence": self.confidence
        }


@dataclass
class RecoveryAction:
    """Recovery action definition"""
    action_id: str
    action_name: str
    target_metric: str
    target_value: float
    current_value: float
    status: str  # pending, executing, completed, failed
    execution_time: Optional[float] = None
    result: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert action to dictionary"""
        return {
            "action_id": self.action_id,
            "action_name": self.action_name,
            "target_metric": self.target_metric,
            "target_value": self.target_value,
            "current_value": self.current_value,
            "status": self.status,
            "execution_time": self.execution_time,
            "result": self.result,
            "metadata": self.metadata
        }


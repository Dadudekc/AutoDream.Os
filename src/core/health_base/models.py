#!/usr/bin/env python3
"""
Health Threshold Models - Agent_Cellphone_V2

Extracted models and enums for health threshold management.
Part of the HealthThresholdManager refactoring for SRP compliance.

Author: Agent-7 (Refactoring Specialist)
License: MIT
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any


class HealthMetricType(Enum):
    """Types of health metrics"""

    RESPONSE_TIME = "response_time"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    ERROR_RATE = "error_rate"
    TASK_COMPLETION_RATE = "task_completion_rate"
    HEARTBEAT_FREQUENCY = "heartbeat_frequency"
    CONTRACT_SUCCESS_RATE = "contract_success_rate"
    COMMUNICATION_LATENCY = "communication_latency"


@dataclass
class HealthThreshold:
    """Health threshold configuration"""

    metric_type: str
    warning_threshold: float
    critical_threshold: float
    unit: str
    description: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "metric_type": self.metric_type,
            "warning_threshold": self.warning_threshold,
            "critical_threshold": self.critical_threshold,
            "unit": self.unit,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HealthThreshold":
        """Create from dictionary"""
        return cls(**data)


@dataclass
class ThresholdOperation:
    """Record of threshold operations"""

    timestamp: str
    operation: str
    metric_type: str
    success: bool
    warning_threshold: float = 0.0
    critical_threshold: float = 0.0
    unit: str = ""
    details: Dict[str, Any] = None

    def __post_init__(self):
        if self.details is None:
            self.details = {}


@dataclass
class ValidationOperation:
    """Record of threshold validation operations"""

    timestamp: str
    metric_type: str
    value: float
    status: str
    threshold: Dict[str, Any]
    details: Dict[str, Any] = None

    def __post_init__(self):
        if self.details is None:
            self.details = {}


@dataclass
class ConfigurationChange:
    """Record of configuration changes"""

    timestamp: str
    operation: str
    metric_type: str
    success: bool
    details: Dict[str, Any] = None

    def __post_init__(self):
        if self.details is None:
            self.details = {}

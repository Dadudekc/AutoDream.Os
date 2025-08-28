#!/usr/bin/env python3
"""
Monitoring Types - V2 Modular Architecture
==========================================

Data structures for performance monitoring.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

from src.services.metrics_definitions import MetricType


class MetricStatus(Enum):
    """Metric collection status."""
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    TIMEOUT = "timeout"


@dataclass
class MetricData:
    """Single metric data point."""
    name: str
    value: float
    unit: str
    metric_type: MetricType
    timestamp: datetime
    source: str
    status: MetricStatus = MetricStatus.SUCCESS
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metric to dictionary."""
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "metric_type": self.metric_type.value,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "status": self.status.value,
            "metadata": self.metadata
        }


@dataclass
class MonitoringConfig:
    """Monitoring system configuration."""
    collection_interval: int = 30  # seconds
    retention_period: int = 86400  # seconds (24 hours)
    max_data_points: int = 10000
    cleanup_interval: int = 3600  # seconds (1 hour)
    enabled_collectors: List[str] = field(default_factory=lambda: ["system", "application"])
    
    # System metrics settings
    collect_cpu: bool = True
    collect_memory: bool = True
    collect_disk: bool = True
    collect_network: bool = True
    
    # Application metrics settings
    collect_process_metrics: bool = True
    collect_request_metrics: bool = True
    collect_response_time_metrics: bool = True
    collect_error_metrics: bool = True
    
    def is_collector_enabled(self, collector_name: str) -> bool:
        """Check if a specific collector is enabled."""
        return collector_name in self.enabled_collectors
    
    def validate_config(self) -> List[str]:
        """Validate monitoring configuration."""
        errors = []
        if self.collection_interval <= 0:
            errors.append("Collection interval must be positive")
        if self.retention_period <= 0:
            errors.append("Retention period must be positive")
        if self.max_data_points <= 0:
            errors.append("Max data points must be positive")
        if self.cleanup_interval <= 0:
            errors.append("Cleanup interval must be positive")
        return errors


@dataclass
class CollectionResult:
    """Result of a metrics collection operation."""
    collector_name: str
    timestamp: datetime
    metrics_collected: int
    status: MetricStatus
    duration_ms: float
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_successful(self) -> bool:
        """Check if collection was successful."""
        return self.status == MetricStatus.SUCCESS
    
    def has_errors(self) -> bool:
        """Check if collection had errors."""
        return len(self.errors) > 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "collector_name": self.collector_name,
            "timestamp": self.timestamp.isoformat(),
            "metrics_collected": self.metrics_collected,
            "status": self.status.value,
            "duration_ms": self.duration_ms,
            "errors": self.errors,
            "metadata": self.metadata
        }

"""
Integration Models
=================

Data models and enums for integration coordination.
"""

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Any, Dict, List, Optional


class IntegrationType(Enum):
    """Types of integrations."""
    VECTOR_DATABASE = "vector_database"
    MESSAGING = "messaging"
    DATA_PROCESSING = "data_processing"
    CONFIGURATION = "configuration"
    LOGGING = "logging"


class OptimizationLevel(Enum):
    """Optimization levels."""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    MAXIMUM = "maximum"


@dataclass
class IntegrationMetrics:
    """Metrics for integration performance."""
    integration_type: IntegrationType
    total_operations: int
    average_response_time: float
    success_rate: float
    cache_hit_rate: float
    throughput: float
    error_count: int
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class OptimizationConfig:
    """Configuration for unified integration optimization."""
    enable_vector_optimization: bool = True
    enable_messaging_optimization: bool = True
    enable_data_processing_optimization: bool = True
    optimization_level: OptimizationLevel = OptimizationLevel.INTERMEDIATE
    enable_cross_system_coordination: bool = True
    enable_performance_monitoring: bool = True
    monitoring_interval_seconds: int = 60
    enable_auto_optimization: bool = True


@dataclass
class PerformanceReport:
    """Performance report data structure."""
    overall_metrics: Dict[str, Any]
    integration_metrics: Dict[str, Dict[str, Any]]
    optimization_status: Dict[str, bool]
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class OptimizationRecommendation:
    """Optimization recommendation data structure."""
    integration: str
    issue: str
    current_value: str
    recommendation: str
    priority: str

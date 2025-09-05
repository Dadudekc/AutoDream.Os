"""
Integration Models Core - KISS Simplified
=========================================

Core data models for integration coordination.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined data modeling.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

# Import enums from dedicated module for V2 compliance micro-refactoring
from .enums import (
    IntegrationType,
    OptimizationLevel,
    IntegrationStatus,
    IntegrationPriority,
    IntegrationMode
)


@dataclass
class IntegrationMetrics:
    """Integration performance metrics."""
    integration_type: IntegrationType
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0
    max_response_time: float = 0.0
    min_response_time: float = 0.0
    throughput: float = 0.0
    error_rate: float = 0.0
    last_updated: datetime = None


@dataclass
class OptimizationConfig:
    """Configuration for integration optimization."""
    integration_type: IntegrationType
    optimization_level: OptimizationLevel
    target_response_time: float = 1.0
    max_concurrent_requests: int = 100
    cache_enabled: bool = True
    monitoring_enabled: bool = True
    retry_attempts: int = 3
    timeout_seconds: int = 30
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class PerformanceReport:
    """Performance analysis report."""
    report_id: str
    integration_type: IntegrationType
    period_start: datetime
    period_end: datetime
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0
    p95_response_time: float = 0.0
    p99_response_time: float = 0.0
    throughput: float = 0.0
    error_rate: float = 0.0
    recommendations: List[str] = None
    created_at: datetime = None

    def __post_init__(self):
        if self.recommendations is None:
            self.recommendations = []
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class OptimizationRecommendation:
    """Integration optimization recommendation."""
    recommendation_id: str
    integration_type: IntegrationType
    priority: IntegrationPriority
    title: str
    description: str
    expected_improvement: float = 0.0
    implementation_effort: str = "medium"
    risk_level: str = "low"
    prerequisites: List[str] = None
    created_at: datetime = None

    def __post_init__(self):
        if self.prerequisites is None:
            self.prerequisites = []
        if self.created_at is None:
            self.created_at = datetime.now()

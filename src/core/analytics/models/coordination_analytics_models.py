#!/usr/bin/env python3
"""
Coordination Analytics Models - V2 Compliance Module
===================================================

Data models for coordination analytics operations.
Extracted from coordination_analytics_orchestrator.py for V2 compliance.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class AnalyticsMetric(Enum):
    """Analytics metric types."""

    EFFICIENCY = "efficiency"
    THROUGHPUT = "throughput"
    SUCCESS_RATE = "success_rate"
    RESPONSE_TIME = "response_time"
    COORDINATION_QUALITY = "coordination_quality"
    SWARM_HEALTH = "swarm_health"


class OptimizationRecommendation(Enum):
    """Optimization recommendation types."""

    ROUTE_OPTIMIZATION = "route_optimization"
    BATCH_PROCESSING = "batch_processing"
    PRIORITY_QUEUING = "priority_queuing"
    LOAD_BALANCING = "load_balancing"
    CACHING = "caching"
    RETRY_STRATEGY = "retry_strategy"


@dataclass
class CoordinationAnalyticsData:
    """Coordination analytics data structure."""

    timestamp: datetime
    efficiency_score: float
    throughput: int
    success_rate: float
    average_response_time: float
    coordination_quality: float
    swarm_health: float
    active_agents: int
    total_tasks: int
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of key metrics."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "efficiency_score": self.efficiency_score,
            "success_rate": self.success_rate,
            "active_agents": self.active_agents,
            "total_tasks": self.total_tasks,
            "recommendations_count": len(self.recommendations),
        }


@dataclass
class AnalyticsReport:
    """Analytics report structure."""

    report_id: str
    generated_at: datetime
    data: CoordinationAnalyticsData
    trends: Dict[str, Any]
    recommendations: List[str]
    summary: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "report_id": self.report_id,
            "generated_at": self.generated_at.isoformat(),
            "data": self.data.to_dict(),
            "trends": self.trends,
            "recommendations": self.recommendations,
            "summary": self.summary,
        }


@dataclass
class AnalyticsConfig:
    """Analytics configuration."""

    enable_real_time_monitoring: bool = True
    analysis_interval_seconds: int = 60
    history_retention_hours: int = 24
    target_efficiency: float = 0.45
    enable_recommendations: bool = True
    cache_ttl_seconds: int = 300

    def validate(self) -> None:
        """Validate configuration."""
        if self.analysis_interval_seconds < 1:
            raise ValueError("Analysis interval must be at least 1 second")
        if self.history_retention_hours < 1:
            raise ValueError("History retention must be at least 1 hour")
        if not 0 <= self.target_efficiency <= 1:
            raise ValueError("Target efficiency must be between 0 and 1")
        if self.cache_ttl_seconds < 1:
            raise ValueError("Cache TTL must be at least 1 second")

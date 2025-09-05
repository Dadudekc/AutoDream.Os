"""
Integration Core Models - V2 Compliance Module
==============================================

Core integration data models.

V2 Compliance: < 300 lines, single responsibility, core models.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, Any, List
from datetime import datetime


@dataclass
class IntegrationMetrics:
    """Integration performance metrics."""
    total_integrations: int
    successful_integrations: int
    failed_integrations: int
    average_response_time: float
    last_updated: datetime


@dataclass
class OptimizationConfig:
    """Integration optimization configuration."""
    enable_caching: bool
    max_retries: int
    timeout_seconds: int
    batch_size: int


@dataclass
class PerformanceReport:
    """Integration performance report."""
    report_id: str
    metrics: IntegrationMetrics
    recommendations: List[str]
    generated_at: datetime


@dataclass
class OptimizationRecommendation:
    """Integration optimization recommendation."""
    recommendation_id: str
    title: str
    description: str
    priority: str
    estimated_impact: str

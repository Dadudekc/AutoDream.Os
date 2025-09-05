#!/usr/bin/env python3
"""
Vector Enhanced Contracts Extended Models - V2 Compliance Module
================================================================

Extended data models for vector enhanced contracts operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List
from datetime import datetime


@dataclass
class PerformanceMetrics:
    """Performance metrics structure."""
    
    agent_id: str
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    average_completion_time: float = 0.0
    success_rate: float = 0.0
    quality_score: float = 0.0
    efficiency_score: float = 0.0
    collaboration_score: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "average_completion_time": self.average_completion_time,
            "success_rate": self.success_rate,
            "quality_score": self.quality_score,
            "efficiency_score": self.efficiency_score,
            "collaboration_score": self.collaboration_score,
            "last_updated": self.last_updated.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class PerformanceTrend:
    """Performance trend analysis."""
    
    agent_id: str
    trend_type: str
    trend_direction: str  # "improving", "declining", "stable"
    trend_strength: float  # 0.0 to 1.0
    key_factors: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    confidence: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "trend_type": self.trend_type,
            "trend_direction": self.trend_direction,
            "trend_strength": self.trend_strength,
            "key_factors": self.key_factors,
            "recommendations": self.recommendations,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class OptimizationResult:
    """Optimization result structure."""
    
    optimization_id: str
    optimization_type: str
    before_metrics: Dict[str, Any] = field(default_factory=dict)
    after_metrics: Dict[str, Any] = field(default_factory=dict)
    improvement_percentage: float = 0.0
    recommendations: List[str] = field(default_factory=list)
    implementation_effort: str = "medium"
    expected_impact: str = "medium"
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "optimization_id": self.optimization_id,
            "optimization_type": self.optimization_type,
            "before_metrics": self.before_metrics,
            "after_metrics": self.after_metrics,
            "improvement_percentage": self.improvement_percentage,
            "recommendations": self.recommendations,
            "implementation_effort": self.implementation_effort,
            "expected_impact": self.expected_impact,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }

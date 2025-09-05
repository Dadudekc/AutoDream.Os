#!/usr/bin/env python3
"""
Pattern Analysis Models Extended - V2 Compliance Module
=======================================================

Extended data models for pattern analysis operations.
Extracted from models.py for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist
License: MIT
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
from enum import Enum
import uuid

from .models_core import (
    PatternType, RecommendationType, ImpactLevel,
    MissionPattern, PatternCorrelation, MissionContext, StrategicRecommendation
)


@dataclass
class PatternAnalysisResult:
    """Pattern analysis result data."""
    analysis_id: str
    pattern_type: PatternType
    analysis_timestamp: datetime
    patterns_analyzed: int
    correlations_found: int
    recommendations_generated: int
    analysis_duration: float
    confidence_score: float
    summary: str
    detailed_findings: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "analysis_id": self.analysis_id,
            "pattern_type": self.pattern_type.value,
            "analysis_timestamp": self.analysis_timestamp.isoformat(),
            "patterns_analyzed": self.patterns_analyzed,
            "correlations_found": self.correlations_found,
            "recommendations_generated": self.recommendations_generated,
            "analysis_duration": self.analysis_duration,
            "confidence_score": self.confidence_score,
            "summary": self.summary,
            "detailed_findings": self.detailed_findings
        }


@dataclass
class PerformanceMetrics:
    """Performance metrics data."""
    metrics_id: str
    agent_id: str
    mission_id: str
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    execution_time: float
    success_rate: float
    error_count: int
    throughput: float
    latency: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "metrics_id": self.metrics_id,
            "agent_id": self.agent_id,
            "mission_id": self.mission_id,
            "timestamp": self.timestamp.isoformat(),
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
            "execution_time": self.execution_time,
            "success_rate": self.success_rate,
            "error_count": self.error_count,
            "throughput": self.throughput,
            "latency": self.latency
        }


@dataclass
class ResourceUtilization:
    """Resource utilization data."""
    utilization_id: str
    agent_id: str
    resource_type: str
    utilization_percent: float
    peak_usage: float
    average_usage: float
    timestamp: datetime
    duration: float
    efficiency_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "utilization_id": self.utilization_id,
            "agent_id": self.agent_id,
            "resource_type": self.resource_type,
            "utilization_percent": self.utilization_percent,
            "peak_usage": self.peak_usage,
            "average_usage": self.average_usage,
            "timestamp": self.timestamp.isoformat(),
            "duration": self.duration,
            "efficiency_score": self.efficiency_score
        }


@dataclass
class TimingPattern:
    """Timing pattern data."""
    timing_id: str
    agent_id: str
    operation_type: str
    start_time: datetime
    end_time: datetime
    duration: float
    frequency: float
    pattern_type: str
    efficiency_rating: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timing_id": self.timing_id,
            "agent_id": self.agent_id,
            "operation_type": self.operation_type,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration": self.duration,
            "frequency": self.frequency,
            "pattern_type": self.pattern_type,
            "efficiency_rating": self.efficiency_rating
        }


@dataclass
class CoordinationPattern:
    """Coordination pattern data."""
    coordination_id: str
    agent_a_id: str
    agent_b_id: str
    coordination_type: str
    success_rate: float
    communication_frequency: float
    response_time: float
    timestamp: datetime
    effectiveness_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "coordination_id": self.coordination_id,
            "agent_a_id": self.agent_a_id,
            "agent_b_id": self.agent_b_id,
            "coordination_type": self.coordination_type,
            "success_rate": self.success_rate,
            "communication_frequency": self.communication_frequency,
            "response_time": self.response_time,
            "timestamp": self.timestamp.isoformat(),
            "effectiveness_score": self.effectiveness_score
        }


def create_analysis_id() -> str:
    """Create unique analysis ID."""
    return f"analysis_{uuid.uuid4().hex[:12]}"


def create_metrics_id() -> str:
    """Create unique metrics ID."""
    return f"metrics_{uuid.uuid4().hex[:12]}"


def create_utilization_id() -> str:
    """Create unique utilization ID."""
    return f"util_{uuid.uuid4().hex[:12]}"


def create_timing_id() -> str:
    """Create unique timing ID."""
    return f"timing_{uuid.uuid4().hex[:12]}"


def create_coordination_id() -> str:
    """Create unique coordination ID."""
    return f"coord_{uuid.uuid4().hex[:12]}"

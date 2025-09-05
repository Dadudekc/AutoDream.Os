"""
Pattern Analysis Core Models
============================

Core data structures and enums for pattern analysis operations.
V2 Compliance: < 100 lines, single responsibility, core data modeling.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import uuid


class PatternType(Enum):
    """Pattern type."""
    PERFORMANCE = "performance"
    COORDINATION = "coordination"
    EFFICIENCY = "efficiency"
    RESOURCE = "resource"
    TIMING = "timing"
    SEQUENCE = "sequence"


class RecommendationType(Enum):
    """Recommendation type."""
    OPTIMIZATION = "optimization"
    COORDINATION = "coordination"
    RESOURCE_ALLOCATION = "resource_allocation"
    TIMING_ADJUSTMENT = "timing_adjustment"
    PROCESS_IMPROVEMENT = "process_improvement"


class ImpactLevel(Enum):
    """Impact level."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AnalysisStatus(Enum):
    """Analysis status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class MissionPattern:
    """Mission pattern data."""
    pattern_id: str
    name: str
    description: str
    pattern_type: PatternType
    frequency: float
    confidence: float
    context: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


@dataclass
class PatternCorrelation:
    """Pattern correlation data."""
    correlation_id: str
    pattern1_id: str
    pattern2_id: str
    correlation_score: float
    significance: float
    relationship_type: str
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class MissionContext:
    """Mission context data."""
    context_id: str
    mission_id: str
    phase: str
    priority: str
    resources: Dict[str, Any]
    constraints: List[str]
    objectives: List[str]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
"""
Strategic Oversight Core Models
===============================

Core data structures and enums for strategic oversight operations.
V2 Compliance: < 150 lines, single responsibility, core data modeling.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import uuid


class InsightType(Enum):
    """Insight type."""
    PERFORMANCE = "performance"
    COORDINATION = "coordination"
    EFFICIENCY = "efficiency"
    RESOURCE = "resource"
    TIMING = "timing"
    PATTERN = "pattern"


class ConfidenceLevel(Enum):
    """Confidence level."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class ImpactLevel(Enum):
    """Impact level."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MissionStatus(Enum):
    """Mission status."""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PriorityLevel(Enum):
    """Priority level."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


@dataclass
class StrategicInsight:
    """Strategic insight data."""
    insight_id: str
    title: str
    description: str
    insight_type: InsightType
    confidence_level: ConfidenceLevel
    impact_level: ImpactLevel
    context: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


@dataclass
class MissionObjective:
    """Mission objective data."""
    objective_id: str
    mission_id: str
    title: str
    description: str
    priority: PriorityLevel
    status: MissionStatus
    target_date: Optional[datetime]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class ResourceAllocation:
    """Resource allocation data."""
    allocation_id: str
    resource_type: str
    allocated_amount: float
    used_amount: float
    available_amount: float
    efficiency_score: float
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
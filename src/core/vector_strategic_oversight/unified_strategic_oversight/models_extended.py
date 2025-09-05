#!/usr/bin/env python3
"""
Strategic Oversight Models Extended - V2 Compliance Module
=========================================================

Extended data models for vector strategic oversight operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum
import uuid
from .models_core import InsightType, ConfidenceLevel, ImpactLevel, MissionStatus


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ActionType(Enum):
    """Action types."""
    IMMEDIATE = "immediate"
    SCHEDULED = "scheduled"
    MONITORING = "monitoring"
    INVESTIGATION = "investigation"


@dataclass
class StrategicAlert:
    """Strategic alert data."""
    alert_id: str
    alert_type: str
    severity: AlertSeverity
    title: str
    description: str
    source_agent: str
    target_agents: List[str]
    created_at: datetime
    resolved_at: Optional[datetime] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.target_agents is None:
            self.target_agents = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class StrategicAction:
    """Strategic action data."""
    action_id: str
    action_type: ActionType
    title: str
    description: str
    assigned_agent: str
    priority: int
    status: str
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.metadata is None:
            self.metadata = {}


@dataclass
class StrategicReport:
    """Strategic report data."""
    report_id: str
    report_type: str
    title: str
    content: str
    author_agent: str
    created_at: datetime
    updated_at: datetime
    target_agents: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.target_agents is None:
            self.target_agents = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class StrategicMetrics:
    """Strategic metrics data."""
    metrics_id: str
    period_start: datetime
    period_end: datetime
    total_insights: int
    total_alerts: int
    total_actions: int
    success_rate: float
    efficiency_score: float
    coordination_score: float
    created_at: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.metadata is None:
            self.metadata = {}


@dataclass
class StrategicConfiguration:
    """Strategic configuration data."""
    config_id: str
    config_name: str
    config_value: Any
    config_type: str
    description: str
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.metadata is None:
            self.metadata = {}


@dataclass
class StrategicEvent:
    """Strategic event data."""
    event_id: str
    event_type: str
    event_name: str
    description: str
    source_agent: str
    timestamp: datetime
    severity: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.metadata is None:
            self.metadata = {}


@dataclass
class StrategicPattern:
    """Strategic pattern data."""
    pattern_id: str
    pattern_name: str
    pattern_type: str
    description: str
    frequency: int
    confidence: float
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.metadata is None:
            self.metadata = {}


@dataclass
class StrategicTrend:
    """Strategic trend data."""
    trend_id: str
    trend_name: str
    trend_direction: str
    trend_strength: float
    confidence: float
    data_points: int
    time_window: int
    created_at: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.metadata is None:
            self.metadata = {}

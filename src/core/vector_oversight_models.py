#!/usr/bin/env python3
"""
Vector Database Strategic Oversight Models - V2 Compliant
=========================================================

Data models for vector database strategic oversight system.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactoring)
Created: 2025-01-27
Purpose: Modular data models for strategic oversight
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class StrategicOversightReport:
    """Comprehensive strategic oversight report."""
    
    report_id: str
    generated_at: datetime = field(default_factory=datetime.now)
    mission_status: Dict[str, Any] = field(default_factory=dict)
    agent_capabilities: Dict[str, Any] = field(default_factory=dict)
    emergency_status: Dict[str, Any] = field(default_factory=dict)
    pattern_analysis: Dict[str, Any] = field(default_factory=dict)
    strategic_recommendations: List[Dict[str, Any]] = field(default_factory=list)
    success_predictions: Dict[str, float] = field(default_factory=dict)
    risk_assessment: Dict[str, Any] = field(default_factory=dict)
    intervention_history: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SwarmCoordinationInsight:
    """Swarm coordination insight structure."""
    
    insight_type: str
    mission_context: str
    insight_content: str
    confidence_level: float
    recommended_actions: List[str] = field(default_factory=list)
    expected_impact: str = "medium"
    generated_at: datetime = field(default_factory=datetime.now)


@dataclass
class MissionContext:
    """Mission context for strategic oversight."""
    
    mission_id: str
    mission_type: str
    priority: str
    assigned_agents: List[str] = field(default_factory=list)
    status: str = "active"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class AgentCapability:
    """Agent capability tracking."""
    
    agent_id: str
    capabilities: List[str] = field(default_factory=list)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.now)

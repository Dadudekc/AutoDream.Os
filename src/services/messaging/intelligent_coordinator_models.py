#!/usr/bin/env python3
"""
Intelligent Coordinator Models
============================

Data models for intelligent agent coordination system.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class CoordinationTask:
    """Task coordination data model."""
    task: str
    required_skills: List[str]
    priority: str = "NORMAL"
    deadline: Optional[str] = None
    dependencies: List[str] = None


@dataclass
class AgentProfile:
    """Agent profile data model."""
    agent_id: str
    skills: List[str]
    availability: str
    performance_score: float
    current_load: int


@dataclass
class CoordinationPlan:
    """Coordination plan data model."""
    task: str
    assigned_agents: List[str]
    coordination_strategy: str
    estimated_duration: str
    success_probability: float


@dataclass
class CoordinationResult:
    """Coordination result data model."""
    success: bool
    assigned_agents: List[str]
    coordination_plan: CoordinationPlan
    execution_time: float
    performance_metrics: Dict[str, Any]


@dataclass
class SwarmIntelligence:
    """Swarm intelligence data model."""
    patterns: List[Dict[str, Any]]
    expert_agents: List[str]
    success_rate: float
    recommendations: List[str]


@dataclass
class TaskRouting:
    """Task routing data model."""
    task_id: str
    target_agent: str
    routing_strategy: str
    priority: str
    estimated_completion: str


@dataclass
class PerformanceMetrics:
    """Performance metrics data model."""
    coordination_success_rate: float
    average_response_time: float
    agent_utilization: Dict[str, float]
    task_completion_rate: float
    swarm_efficiency: float

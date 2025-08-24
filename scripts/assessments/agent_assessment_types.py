#!/usr/bin/env python3
"""
Agent Assessment Types - Agent Cellphone V2
==========================================

Data types and enums for agent assessment system.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class AssessmentStatus(Enum):
    """Assessment status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class IntegrationPriority(Enum):
    """Integration priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class WebIntegrationType(Enum):
    """Web integration types"""
    API_ENDPOINTS = "api_endpoints"
    WEBHOOKS = "webhooks"
    WEBSOCKETS = "websockets"
    HTTP_CLIENT = "http_client"
    BROWSER_AUTOMATION = "browser_automation"
    UI_TESTING = "ui_testing"


@dataclass
class AgentAssessmentResult:
    """Individual agent assessment result"""
    agent_id: str
    agent_name: str
    assessment_status: AssessmentStatus
    web_integration_score: float
    integration_requirements: List[str]
    current_capabilities: List[str]
    missing_features: List[str]
    priority: IntegrationPriority
    estimated_effort_hours: int
    dependencies: List[str]
    last_assessed: datetime
    notes: str = ""
    recommendations: List[str] = field(default_factory=list)


@dataclass
class IntegrationRequirement:
    """Web integration requirement specification"""
    requirement_id: str
    requirement_type: WebIntegrationType
    description: str
    priority: IntegrationPriority
    complexity: str
    estimated_hours: int
    dependencies: List[str]
    agent_dependencies: List[str]
    status: str = "pending"


@dataclass
class AssessmentSummary:
    """Overall assessment summary"""
    timestamp: datetime
    total_agents: int
    assessed_agents: int
    overall_status: AssessmentStatus
    critical_requirements: int
    high_priority_requirements: int
    total_estimated_hours: int
    completion_percentage: float
    next_steps: List[str]
    risk_factors: List[str]


@dataclass
class AgentConfiguration:
    """Agent configuration data"""
    agent_id: str
    agent_name: str
    agent_type: str
    current_location: str
    capabilities: List[str]
    limitations: List[str]
    integration_status: str
    last_updated: datetime
    configuration_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AssessmentConfiguration:
    """Assessment configuration settings"""
    assessment_id: str
    assessment_name: str
    target_agents: List[str]
    assessment_criteria: List[str]
    priority_threshold: IntegrationPriority
    max_assessment_time_minutes: int
    include_dependencies: bool
    generate_reports: bool
    output_format: str = "json"
    log_level: str = "INFO"


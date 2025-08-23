#!/usr/bin/env python3
"""
Unified Agent Models - Consolidated Agent Data Structures

This module provides unified agent models to eliminate duplication.
Follows Single Responsibility Principle - only agent data structures.
Architecture: Single Responsibility Principle - agent models only
LOC: Target 200 lines (under 300 limit)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from enum import Enum


class AgentRole(Enum):
    """Unified agent role definitions"""

    # System roles
    SYSTEM_COORDINATOR = "System Coordinator & Project Manager"
    TECHNICAL_ARCHITECT = "Technical Architect & Developer"
    DATA_ENGINEER = "Data Engineer & Analytics Specialist"
    DEVOPS_ENGINEER = "DevOps Engineer & Infrastructure Specialist"
    AI_ML_ENGINEER = "AI/ML Engineer & Algorithm Specialist"
    FRONTEND_DEVELOPER = "Frontend Developer & UI/UX Specialist"
    BACKEND_DEVELOPER = "Backend Developer & API Specialist"
    QA_SPECIALIST = "Quality Assurance & Testing Specialist"

    # Functional roles
    COORDINATOR = "coordinator"
    WORKER = "worker"
    MONITOR = "monitor"
    ANALYST = "analyst"
    SPECIALIST = "specialist"


class AgentStatus(Enum):
    """Agent status definitions"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    BUSY = "busy"
    IDLE = "idle"
    ERROR = "error"
    OFFLINE = "offline"


class AgentCapability(Enum):
    """Agent capability types"""

    SYSTEM_ACCESS = "system_access"
    COMMUNICATION = "communication"
    TASK_EXECUTION = "task_execution"
    COORDINATION = "coordination"
    MONITORING = "monitoring"
    ANALYSIS = "analysis"
    DEVELOPMENT = "development"
    TESTING = "testing"
    DEPLOYMENT = "deployment"


@dataclass
class AgentCapabilityDefinition:
    """Agent capability definition"""

    capability_id: str
    name: str
    description: str
    capability_type: AgentCapability
    permissions: List[str]
    dependencies: List[str]
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class AgentRoleDefinition:
    """Unified agent role definition"""

    role_id: str
    name: str
    description: str
    capabilities: List[str]
    required_training: List[str]
    permissions: List[str]
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class AgentResponsibilities:
    """Agent responsibilities structure"""

    role: str
    emoji: str
    key_responsibilities: List[str]
    leadership: str
    onboarding_path: str
    priority_docs: List[str]


@dataclass
class AgentInfo:
    """Comprehensive agent information"""

    agent_id: str
    name: str
    role: AgentRole
    status: AgentStatus
    capabilities: List[AgentCapability]
    responsibilities: AgentResponsibilities
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=lambda: __import__("time").time())
    last_active: float = field(default_factory=lambda: __import__("time").time())


@dataclass
class RoleAssignment:
    """Agent role assignment record"""

    agent_id: str
    role_id: str
    assigned_at: float
    assigned_by: str
    status: str  # "active", "suspended", "revoked"
    metadata: Optional[Dict[str, Any]] = None

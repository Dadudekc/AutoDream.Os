#!/usr/bin/env python3
"""
DevOps Workflow Models - V2 Compliant
=====================================

Data models for DevOps workflow system.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactoring)
Created: 2025-01-27
Purpose: Modular data models for DevOps workflows
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class WorkflowType(Enum):
    """Workflow type enumeration."""
    CI_CD = "ci_cd"
    CI_BASIC = "ci_basic"
    DEPLOYMENT = "deployment"
    TESTING = "testing"
    SECURITY = "security"


class WorkflowStatus(Enum):
    """Workflow status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    DEPRECATED = "deprecated"


@dataclass
class WorkflowStep:
    """Workflow step data structure."""
    name: str
    type: str
    command: str
    timeout: int = 300
    retry_count: int = 0
    dependencies: List[str] = field(default_factory=list)
    environment: Dict[str, str] = field(default_factory=dict)


@dataclass
class WorkflowConfig:
    """Workflow configuration data structure."""
    workflow_id: str
    name: str
    description: str
    type: WorkflowType
    status: WorkflowStatus
    steps: List[WorkflowStep] = field(default_factory=list)
    triggers: List[str] = field(default_factory=list)
    environment: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class WorkflowExecution:
    """Workflow execution tracking."""
    execution_id: str
    workflow_id: str
    status: str
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    logs: List[str] = field(default_factory=list)
    error_message: Optional[str] = None

#!/usr/bin/env python3
"""Contract models and enums for contract management."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from .agent_manager import AgentCapability


class ContractPriority(Enum):
    """Contract priority levels"""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class ContractStatus(Enum):
    """Contract lifecycle states"""

    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    APPROVED = "approved"


class AssignmentStrategy(Enum):
    """Strategies for assigning contracts to agents"""

    SKILL_MATCH = "skill_match"
    LOAD_BALANCE = "load_balance"
    PRIORITY_FIRST = "priority_first"
    ROUND_ROBIN = "round_robin"
    EXPERT_OPINION = "expert_opinion"


class ContractType(Enum):
    """Supported contract categories"""

    TASK_ASSIGNMENT = "task_assignment"
    AGENT_RESPONSE = "agent_response"
    COLLABORATION = "collaboration"
    SERVICE_AGREEMENT = "service_agreement"


@dataclass
class Contract:
    """Contract definition"""

    contract_id: str
    title: str
    description: str
    priority: ContractPriority
    status: ContractStatus
    required_capabilities: List[AgentCapability]
    estimated_duration: int  # hours
    assigned_agent: Optional[str]
    created_at: str
    assigned_at: Optional[str]
    completed_at: Optional[str]
    metadata: Dict[str, Any]
    contract_type: Optional[ContractType] = None
    parties: Optional[List[Dict[str, Any]]] = None
    terms: Optional[Dict[str, Any]] = None
    validation_results: Optional[List[Any]] = None


@dataclass
class AssignmentResult:
    """Result of assigning a contract to an agent"""

    assignment_id: str
    contract_id: str
    agent_id: str
    strategy: AssignmentStrategy
    confidence_score: float
    assignment_timestamp: str
    metadata: Dict[str, Any]


@dataclass
class ContractTemplate:
    """Template for standardized contract creation"""

    template_id: str
    name: str
    description: str
    contract_type: ContractType
    default_terms: Dict[str, Any]
    required_fields: List[str]
    validation_rules: Dict[str, Any]
    created_at: str
    updated_at: str

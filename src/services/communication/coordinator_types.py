#!/usr/bin/env python3
"""
Communication Coordinator Types - V2 Standards Compliant
Contains all data models and enums for the communication coordination system
Follows V2 coding standards: ≤100 LOC, clean data models
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional


class CommunicationMode(Enum):
    """Enhanced communication modes from V1"""
    HIERARCHICAL = "hierarchical"  # Top-down coordination
    COLLABORATIVE = "collaborative"  # Peer-to-peer collaboration
    DEMOCRATIC = "democratic"  # Voting-based decisions
    EMERGENCY = "emergency"  # Crisis response mode
    INNOVATION = "innovation"  # Creative problem solving
    PRESIDENTIAL = "presidential"  # Presidential captaincy mode


class TaskPriority(Enum):
    """Task priority levels from V1"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"
    PRESIDENTIAL = "presidential"


class TaskStatus(Enum):
    """Task status states from V1"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    REVIEW = "review"
    COMPLETED = "completed"
    FAILED = "failed"


class CaptaincyTerm(Enum):
    """Presidential captaincy terms from V1"""
    CAMPAIGN_TERM = "campaign_term"  # Task-list based term
    ELECTION_PHASE = "election_phase"  # Election and voting phase
    TRANSITION_PHASE = "transition_phase"  # Handoff between captains


class MessageType(Enum):
    """Message types for coordination"""
    TASK_ASSIGNMENT = "task_assignment"
    STATUS_UPDATE = "status_update"
    COORDINATION = "coordination"
    EMERGENCY = "emergency"
    BROADCAST = "broadcast"
    PRIVATE = "private"


@dataclass
class CoordinationTask:
    """Task structure from V1"""
    task_id: str
    title: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    assigned_agents: List[str]
    dependencies: List[str]
    created_at: datetime
    due_date: Optional[datetime]
    estimated_hours: float
    actual_hours: float
    progress_percentage: float
    tags: List[str]


@dataclass
class CoordinationMessage:
    """Message structure for coordination"""
    message_id: str
    sender_id: str
    recipient_ids: List[str]
    message_type: MessageType
    content: str
    timestamp: datetime
    priority: TaskPriority
    metadata: dict


@dataclass
class AgentCapability:
    """Agent capability definition"""
    agent_id: str
    capabilities: List[str]
    specializations: List[str]
    availability: bool
    current_load: int
    max_capacity: int


@dataclass
class CoordinationSession:
    """Coordination session for group activities"""
    session_id: str
    mode: CommunicationMode
    participants: List[str]
    start_time: datetime
    end_time: Optional[datetime]
    agenda: List[str]
    decisions: List[dict]

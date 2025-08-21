#!/usr/bin/env python3
"""
Shared Enums Module
===================

This module contains common enum definitions used across multiple modules
to eliminate duplication and ensure consistency.
"""

from enum import Enum


class MessagePriority(Enum):
    """Message priority levels for routing and processing."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class MessageStatus(Enum):
    """Message status states."""
    PENDING = "pending"
    READ = "read"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class MessageType(Enum):
    """Types of messages supported by the system."""
    TEXT = "text"
    TASK = "task"
    NOTIFICATION = "notification"
    COMMAND = "command"
    RESPONSE = "response"
    ERROR = "error"
    CONTRACT_ASSIGNMENT = "contract_assignment"
    STATUS_UPDATE = "status_update"
    COORDINATION = "coordination"
    EMERGENCY = "emergency"
    HEARTBEAT = "heartbeat"
    SYSTEM_COMMAND = "system_command"


class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatus(Enum):
    """Individual task status"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    RETRYING = "retrying"
    CANCELLED = "cancelled"


class WorkflowStatus(Enum):
    """Workflow execution status"""
    CREATED = "created"
    PLANNING = "planning"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RECOVERING = "recovering"
    INITIALIZING = "initializing"
    INITIALIZED = "initialized"
    ACTIVE = "active"
    WAITING_FOR_AI = "waiting_for_ai"
    PROCESSING_RESPONSE = "processing_response"
    OPTIMIZING = "optimizing"
    SCALING = "scaling"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"


class WorkflowType(Enum):
    """Workflow types"""
    SEQUENTIAL = "sequential"          # Tasks execute in order
    PARALLEL = "parallel"              # Tasks execute simultaneously
    CONDITIONAL = "conditional"        # Tasks execute based on conditions
    LOOP = "loop"                      # Tasks repeat based on conditions
    PARALLEL_BATCH = "parallel_batch"  # Tasks execute in parallel batches
    PIPELINE = "pipeline"              # Tasks form a processing pipeline


class AgentStatus(Enum):
    """Agent status states"""
    OFFLINE = "offline"
    ONLINE = "online"
    BUSY = "busy"
    IDLE = "idle"
    ERROR = "error"
    RECOVERING = "recovering"


class AgentCapability(Enum):
    """Agent capability types"""
    TASK_EXECUTION = "task_execution"
    DECISION_MAKING = "decision_making"
    COMMUNICATION = "communication"
    DATA_PROCESSING = "data_processing"
    MONITORING = "monitoring"
    REPORTING = "reporting"

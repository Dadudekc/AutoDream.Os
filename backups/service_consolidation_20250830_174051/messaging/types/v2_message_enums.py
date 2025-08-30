#!/usr/bin/env python3
"""
V2Message Enums - Agent Cellphone V2
====================================

Clean, focused enums extracted from comprehensive system.
Follows V2 standards: OOP, SRP, clean production-grade code.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from enum import Enum


class V2MessageType(Enum):
    """Message types for V2 system"""
    TASK_ASSIGNMENT = "task_assignment"
    STATUS_UPDATE = "status_update"
    COORDINATION = "coordination"
    BROADCAST = "broadcast"
    ONBOARDING_PHASE = "onboarding_phase"
    SYSTEM = "system"
    ALERT = "alert"
    WORKFLOW_UPDATE = "workflow_update"
    TASK = "task"
    RESPONSE = "response"
    VALIDATION = "validation"
    FEEDBACK = "feedback"
    TEXT = "text"
    NOTIFICATION = "notification"
    COMMAND = "command"
    ERROR = "error"
    CONTRACT_ASSIGNMENT = "contract_assignment"
    EMERGENCY = "emergency"
    HEARTBEAT = "heartbeat"
    SYSTEM_COMMAND = "system_command"
    ONBOARDING_START = "onboarding_start"
    ONBOARDING_COMPLETE = "onboarding_complete"
    TASK_CREATED = "task_created"
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    AGENT_REGISTRATION = "agent_registration"
    AGENT_STATUS = "agent_status"
    AGENT_HEALTH = "agent_health"
    AGENT_CAPABILITY_UPDATE = "agent_capability_update"
    WORKFLOW_STATUS = "workflow_status"
    WORKFLOW_COMMAND = "workflow_command"
    WORKFLOW_RESPONSE = "workflow_response"
    METRICS_UPDATE = "metrics_update"
    PERFORMANCE_ALERT = "performance_alert"
    SYSTEM_HEALTH = "system_health"
    CAPACITY_ALERT = "capacity_alert"
    TASK_COORDINATION = "task_coordination"
    TASK_DEPENDENCY = "task_dependency"
    TASK_RESOURCE = "task_resource"
    TASK_SCHEDULE = "task_schedule"
    AGENT_COORDINATION = "agent_coordination"
    AGENT_SYNC = "agent_sync"
    AGENT_LOAD_BALANCE = "agent_load_balance"
    AGENT_FAILOVER = "agent_failover"
    SYSTEM_MAINTENANCE = "system_maintenance"
    SYSTEM_UPDATE = "system_update"
    SYSTEM_ROLLBACK = "system_rollback"
    SYSTEM_BACKUP = "system_backup"
    DATA_SYNC = "data_sync"
    DATA_BACKUP = "data_backup"
    DATA_RESTORE = "data_restore"


class V2MessagePriority(Enum):
    """Message priority levels"""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    URGENT = 3
    CRITICAL = 4


class V2MessageStatus(Enum):
    """Message status values"""
    PENDING = "pending"
    QUEUED = "queued"
    SENDING = "sending"
    SENT = "sent"
    DELIVERED = "delivered"
    ACKNOWLEDGED = "acknowledged"
    READ = "read"
    FAILED = "failed"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

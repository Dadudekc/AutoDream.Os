"""Shared enums used by the lightweight message router."""

from enum import Enum


class MessageType(Enum):
    CONTRACT_ASSIGNMENT = "contract_assignment"
    STATUS_UPDATE = "status_update"
    COORDINATION = "coordination"
    EMERGENCY = "emergency"
    HEARTBEAT = "heartbeat"
    SYSTEM_COMMAND = "system_command"


class MessagePriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class MessageStatus(Enum):
    PENDING = "pending"
    DELIVERED = "delivered"
    FAILED = "failed"
    EXPIRED = "expired"

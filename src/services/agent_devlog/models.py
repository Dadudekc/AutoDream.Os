#!/usr/bin/env python3
"""
Agent Devlog Models
==================

Data models for Agent Devlog Posting Service
V2 Compliant: ≤400 lines, focused data structures
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class DevlogStatus(Enum):
    """Devlog status enumeration"""

    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"
    FAILED = "failed"
    PENDING = "pending"


class DevlogType(Enum):
    """Devlog type enumeration"""

    ACTION = "action"
    STATUS_UPDATE = "status_update"
    ERROR_REPORT = "error_report"
    COORDINATION = "coordination"
    TESTING = "testing"


@dataclass
class DevlogEntry:
    """Devlog entry structure"""

    agent_id: str
    action: str
    status: DevlogStatus
    details: str
    timestamp: str
    devlog_type: DevlogType
    metadata: dict[str, Any]


@dataclass
class AgentInfo:
    """Agent information structure"""

    agent_id: str
    role: str
    status: str
    capabilities: list[str]
    last_active: str


@dataclass
class DevlogStats:
    """Devlog statistics structure"""

    total_devlogs: int
    agent_counts: dict[str, int]
    status_counts: dict[str, int]
    type_counts: dict[str, int]
    recent_activity: list[str]


@dataclass
class SearchResult:
    """Search result structure"""

    query: str
    results: list[DevlogEntry]
    total_matches: int
    search_time: float
    filters_applied: dict[str, Any]


@dataclass
class DevlogConfig:
    """Devlog configuration structure"""

    devlogs_directory: str
    max_file_size: int
    retention_days: int
    backup_enabled: bool
    compression_enabled: bool
    vectorization_enabled: bool

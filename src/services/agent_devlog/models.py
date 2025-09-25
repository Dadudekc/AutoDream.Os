#!/usr/bin/env python3
"""
Agent Devlog Models
==================

Data models for Agent Devlog Posting Service
V2 Compliant: ≤400 lines, focused data structures
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


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
    metadata: Dict[str, Any]


@dataclass
class AgentInfo:
    """Agent information structure"""
    agent_id: str
    role: str
    status: str
    capabilities: List[str]
    last_active: str


@dataclass
class DevlogStats:
    """Devlog statistics structure"""
    total_devlogs: int
    agent_counts: Dict[str, int]
    status_counts: Dict[str, int]
    type_counts: Dict[str, int]
    recent_activity: List[str]


@dataclass
class SearchResult:
    """Search result structure"""
    query: str
    results: List[DevlogEntry]
    total_matches: int
    search_time: float
    filters_applied: Dict[str, Any]


@dataclass
class DevlogConfig:
    """Devlog configuration structure"""
    devlogs_directory: str
    max_file_size: int
    retention_days: int
    backup_enabled: bool
    compression_enabled: bool
    vectorization_enabled: bool
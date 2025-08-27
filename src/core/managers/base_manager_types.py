#!/usr/bin/env python3
"""
Base Manager Types - Agent Cellphone V2
=======================================

Data models and enums for the base manager system.
Extracted from base_manager.py to follow Single Responsibility Principle.

**Author:** Agent-3 (Integration & Testing)
**Created:** Current Sprint
**Status:** ACTIVE - REFACTORING IN PROGRESS
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional


class ManagerStatus(Enum):
    """Unified manager status states"""
    OFFLINE = "offline"
    ONLINE = "online"
    BUSY = "busy"
    IDLE = "idle"
    ERROR = "error"
    RECOVERING = "recovering"
    MAINTENANCE = "maintenance"
    INITIALIZING = "initializing"
    SHUTTING_DOWN = "shutting_down"


class ManagerPriority(Enum):
    """Unified manager priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5


@dataclass
class ManagerMetrics:
    """Unified manager performance metrics"""
    manager_id: str
    uptime_seconds: float = 0.0
    operations_processed: int = 0
    errors_count: int = 0
    last_operation: Optional[datetime] = None
    performance_score: float = 0.0
    resource_usage: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class ManagerConfig:
    """Unified manager configuration"""
    manager_id: str
    name: str
    description: str
    enabled: bool = True
    auto_start: bool = True
    heartbeat_interval: int = 30
    max_retries: int = 3
    timeout_seconds: int = 60
    log_level: str = "INFO"
    config_file: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

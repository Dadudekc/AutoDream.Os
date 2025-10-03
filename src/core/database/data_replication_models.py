"""
Data Replication System Models - V2 Compliant
=============================================

Data models for replication system.
V2 Compliance: ≤400 lines, ≤5 classes, KISS principle
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class ReplicationStatus(Enum):
    """Replication status enumeration."""

    ACTIVE = "active"
    PAUSED = "paused"
    FAILED = "failed"
    SYNCING = "syncing"
    CONFLICT = "conflict"


@dataclass
class ReplicationConfig:
    """Replication configuration."""

    source_db: str
    target_db: str
    tables: list[str]
    batch_size: int = 1000
    sync_interval: int = 60


@dataclass
class ReplicationRecord:
    """Replication record data structure."""

    id: str
    table_name: str
    operation: str
    data: dict[str, Any]
    timestamp: datetime
    source_node: str
    checksum: str


@dataclass
class ReplicationMetrics:
    """Replication metrics data structure."""

    records_synced: int
    conflicts_resolved: int
    sync_duration: float
    last_sync_time: datetime
    status: ReplicationStatus
    error_count: int = 0


@dataclass
class SyncResult:
    """Synchronization result."""

    success: bool
    records_processed: int
    conflicts_found: int
    errors: list[str]
    duration: float

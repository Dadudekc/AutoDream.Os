#!/usr/bin/env python3
"""
Integrity Types - Agent Cellphone V2
====================================

Defines integrity-related enums and dataclasses.
Follows Single Responsibility Principle with 50 LOC limit.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional


class IntegrityCheckType(Enum):
    """Types of integrity checks"""

    CHECKSUM = "checksum"
    HASH_CHAIN = "hash_chain"
    TIMESTAMP = "timestamp"
    SIZE_VERIFICATION = "size_verification"
    VERSION_CONTROL = "version_control"


class RecoveryStrategy(Enum):
    """Data recovery strategies"""

    BACKUP_RESTORE = "backup_restore"
    CHECKSUM_MATCH = "checksum_match"
    TIMESTAMP_ROLLBACK = "timestamp_rollback"
    VERSION_ROLLBACK = "version_rollback"
    MANUAL_RECOVERY = "manual_recovery"


class IntegrityLevel(Enum):
    """Integrity verification levels"""

    BASIC = "basic"  # Simple checksum
    ADVANCED = "advanced"  # Hash + timestamp
    CRITICAL = "critical"  # Full integrity chain


@dataclass
class IntegrityCheck:
    """Data integrity check result"""

    check_id: str
    data_id: str
    check_type: IntegrityCheckType
    timestamp: float
    passed: bool
    details: Dict[str, Any]
    recovery_attempted: bool
    recovery_successful: bool


@dataclass
class IntegrityViolation:
    """Data integrity violation details"""

    violation_id: str
    data_id: str
    violation_type: str
    severity: str
    timestamp: float
    description: str
    affected_data: Dict[str, Any]
    suggested_recovery: RecoveryStrategy


@dataclass
class IntegrityConfig:
    """Integrity verification configuration"""

    check_interval: int
    recovery_enabled: bool
    alert_on_violation: bool
    auto_recovery: bool
    max_recovery_attempts: int

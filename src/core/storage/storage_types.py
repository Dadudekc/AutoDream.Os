#!/usr/bin/env python3
"""
Storage Types - Agent Cellphone V2
==================================

Defines storage-related enums and dataclasses.
Follows V2 standards: ≤50 LOC, SRP, OOP principles.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any


class StorageType(Enum):
    """Types of persistent storage"""

    FILE_BASED = "file_based"
    DATABASE = "database"
    HYBRID = "hybrid"


class DataIntegrityLevel(Enum):
    """Data integrity verification levels"""

    BASIC = "basic"  # Simple checksum
    ADVANCED = "advanced"  # Hash + timestamp
    CRITICAL = "critical"  # Full integrity chain


class BackupStrategy(Enum):
    """Backup strategies for data protection"""

    INCREMENTAL = "incremental"
    FULL = "full"
    DIFFERENTIAL = "differential"


class CompressionType(Enum):
    """Data compression types"""

    NONE = "none"
    GZIP = "gzip"
    LZMA = "lzma"
    ZSTD = "zstd"


@dataclass
class StorageMetadata:
    """Storage metadata for data integrity"""

    data_id: str
    timestamp: float
    checksum: str
    size: int
    version: int
    integrity_level: DataIntegrityLevel
    backup_count: int
    last_backup: Optional[float]
    compression_type: CompressionType
    encryption_enabled: bool


@dataclass
class StorageConfig:
    """Storage configuration parameters"""

    storage_type: StorageType
    base_path: str
    max_file_size: int
    compression_enabled: bool
    encryption_enabled: bool
    backup_retention_days: int
    integrity_check_interval: int
    auto_backup_enabled: bool


@dataclass
class StorageStats:
    """Storage system statistics"""

    total_data_entries: int
    total_storage_size: int
    storage_type: StorageType
    integrity_level: DataIntegrityLevel
    backup_count: int
    last_backup_timestamp: Optional[float]
    compression_ratio: float
    error_count: int

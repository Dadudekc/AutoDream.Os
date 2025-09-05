#!/usr/bin/env python3
"""
Utility System Models - V2 Compliance Module
===========================================

Data models and enums for utility system operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Callable
from datetime import datetime
from pathlib import Path


class UtilityOperationType(Enum):
    """Types of utility operations."""
    PATH_RESOLUTION = "path_resolution"
    STRING_MANIPULATION = "string_manipulation"
    DATA_TRANSFORMATION = "data_transformation"
    FILE_OPERATION = "file_operation"
    DIRECTORY_OPERATION = "directory_operation"
    VALIDATION = "validation"
    BACKUP = "backup"
    RESTORE = "restore"


class UtilityStatus(Enum):
    """Status of utility operations."""
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    SKIPPED = "skipped"


@dataclass
class UtilityOperation:
    """Represents a utility operation."""
    
    operation_id: str
    operation_type: UtilityOperationType
    input_data: Any
    output_data: Any = None
    status: UtilityStatus = UtilityStatus.SUCCESS
    error_message: Optional[str] = None
    execution_time_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UtilityConfig:
    """Configuration for utility system operations."""
    
    default_encoding: str = "utf-8"
    max_file_size_mb: int = 100
    backup_enabled: bool = True
    backup_directory: str = "backups"
    validation_enabled: bool = True
    logging_enabled: bool = True
    performance_monitoring: bool = True
    cache_enabled: bool = True
    cache_size_mb: int = 50
    timeout_seconds: int = 30


@dataclass
class UtilityMetrics:
    """Metrics for utility system performance."""
    
    total_operations: int = 0
    successful_operations: int = 0
    failed_operations: int = 0
    average_execution_time_ms: float = 0.0
    total_execution_time_ms: float = 0.0
    operations_by_type: Dict[str, int] = field(default_factory=dict)
    error_count_by_type: Dict[str, int] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "total_operations": self.total_operations,
            "successful_operations": self.successful_operations,
            "failed_operations": self.failed_operations,
            "average_execution_time_ms": self.average_execution_time_ms,
            "total_execution_time_ms": self.total_execution_time_ms,
            "operations_by_type": self.operations_by_type,
            "error_count_by_type": self.error_count_by_type,
            "last_updated": self.last_updated.isoformat()
        }


@dataclass
class FileOperationResult:
    """Result of file operation."""
    
    success: bool
    file_path: Union[str, Path]
    operation_type: str
    bytes_processed: int = 0
    error_message: Optional[str] = None
    execution_time_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StringOperationResult:
    """Result of string operation."""
    
    success: bool
    input_string: str
    output_string: str
    operation_type: str
    characters_processed: int = 0
    error_message: Optional[str] = None
    execution_time_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PathOperationResult:
    """Result of path operation."""
    
    success: bool
    input_path: Union[str, Path]
    output_path: Union[str, Path]
    operation_type: str
    path_exists: bool = False
    error_message: Optional[str] = None
    execution_time_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

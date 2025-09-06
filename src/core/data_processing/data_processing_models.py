#!/usr/bin/env python3
"""
Data Processing Models - V2 Compliance Module
============================================

Data models and enums for data processing operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pathlib import Path


class ProcessingType(Enum):
    """Types of data processing operations."""

    CSV = "csv"
    JSON = "json"
    SQLITE = "sqlite"
    HTTP = "http"
    VALIDATION = "validation"
    CLEANING = "cleaning"


class ProcessingStatus(Enum):
    """Status of processing operations."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ProcessingConfig:
    """Configuration for data processing operations."""

    enable_pandas: bool = True
    enable_numpy: bool = True
    enable_requests: bool = True
    default_encoding: str = "utf-8"
    max_file_size_mb: int = 100
    timeout_seconds: int = 30
    retry_attempts: int = 3
    log_level: str = "INFO"


@dataclass
class ProcessingResult:
    """Result of data processing operation."""

    success: bool
    data: Optional[Any] = None
    error_message: Optional[str] = None
    processing_time: float = 0.0
    records_processed: int = 0
    file_size_bytes: int = 0


@dataclass
class DataValidationResult:
    """Result of data validation operation."""

    is_valid: bool
    missing_fields: List[str] = None
    invalid_fields: List[str] = None
    validation_errors: List[str] = None
    total_records: int = 0
    valid_records: int = 0

    def __post_init__(self):
        if self.missing_fields is None:
            self.missing_fields = []
        if self.invalid_fields is None:
            self.invalid_fields = []
        if self.validation_errors is None:
            self.validation_errors = []


@dataclass
class FileProcessingInfo:
    """Information about file processing operation."""

    file_path: Union[str, Path]
    file_type: str
    file_size_bytes: int
    records_count: int
    processing_time: float
    success: bool
    error_message: Optional[str] = None


@dataclass
class DatabaseConnectionInfo:
    """Information about database connection."""

    db_path: Union[str, Path]
    connection_type: str
    is_connected: bool
    last_query_time: Optional[float] = None
    query_count: int = 0
    error_message: Optional[str] = None

#!/usr/bin/env python3
"""
Database Schema Test Models
===========================

Data models for database schema implementation tests.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TestDatabaseConfig:
    """Test database configuration."""
    db_path: str
    schema_version: str
    test_mode: bool = True


@dataclass
class TestSchemaData:
    """Test schema data model."""
    table_name: str
    columns: List[str]
    data: List[Dict[str, Any]]
    constraints: List[str] = None


@dataclass
class TestResult:
    """Test result data model."""
    test_name: str
    success: bool
    error_message: Optional[str] = None
    execution_time: float = 0.0
    data_count: int = 0


@dataclass
class TestValidationResult:
    """Test validation result data model."""
    validation_type: str
    passed: bool
    details: Dict[str, Any]
    recommendations: List[str] = None


@dataclass
class TestPerformanceMetrics:
    """Test performance metrics data model."""
    query_time: float
    memory_usage: float
    disk_usage: float
    connection_count: int


@dataclass
class TestSchemaInfo:
    """Test schema information data model."""
    schema_name: str
    version: str
    tables: List[str]
    indexes: List[str]
    triggers: List[str]

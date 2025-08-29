#!/usr/bin/env python3
"""
Data Source Models - Core data structures
=========================================

Defines the core data models for the unified data source
consolidation system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from .types import DataSourceType, DataType, DataPriority, DataAccessPattern


@dataclass
class DataSource:
    """Unified data source definition"""
    id: str
    name: str
    type: DataSourceType
    data_type: DataType
    location: str
    priority: DataPriority = DataPriority.NORMAL
    enabled: bool = True
    last_updated: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    validation_rules: Dict[str, Any] = field(default_factory=dict)
    access_patterns: List[str] = field(default_factory=list)
    original_service: str = ""
    migration_status: str = "pending"


@dataclass
class DataRecord:
    """Unified data record structure"""
    id: str
    source_id: str
    data: Dict[str, Any]
    timestamp: datetime
    version: str = "1.0"
    metadata: Dict[str, Any] = field(default_factory=dict)
    validation_status: str = "pending"
    quality_score: Optional[float] = None


@dataclass
class DataValidationRule:
    """Data validation rule definition"""
    id: str
    name: str
    rule_type: str
    parameters: Dict[str, Any]
    enabled: bool = True
    priority: int = 1
    description: str = ""


@dataclass
class DataSourceMapping:
    """Mapping between old and new data sources"""
    old_source: str
    new_source: str
    migration_path: str
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


@dataclass
class DataConsolidationReport:
    """Report of data source consolidation"""
    total_sources: int
    consolidated_sources: int
    remaining_sources: int
    migration_progress: float
    issues_found: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)

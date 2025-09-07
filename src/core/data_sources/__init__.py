"""
Data Sources Package - Unified SSOT-compliant data management
============================================================

This package provides unified data source management, eliminating
SSOT violations and creating a single authoritative data architecture.

Modules:
- types: Data source types and enums
- models: Core data models and structures  
- manager: Main data source manager
- validation: Data validation rules
- migration: Data source migration utilities
"""

from .types import DataSourceType, DataType, DataPriority
from .models import DataSource, DataRecord, DataValidationRule
from .manager import UnifiedDataSourceManager
from .validation import DataValidator
from .migration import DataSourceMigrator

__all__ = [
    'DataSourceType', 'DataType', 'DataPriority',
    'DataSource', 'DataRecord', 'DataValidationRule', 
    'UnifiedDataSourceManager', 'DataValidator', 'DataSourceMigrator'
]

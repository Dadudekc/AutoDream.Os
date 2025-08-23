#!/usr/bin/env python3
"""
Storage Package - Agent Cellphone V2
====================================

Refactored storage system with modular architecture.
All modules comply with 200 LOC standard.
"""

from .storage_types import (
    StorageType,
    DataIntegrityLevel,
    BackupStrategy,
    StorageMetadata,
    StorageConfig,
)

from .storage_core import PersistentDataStorage
from .storage_integration import UnifiedStorageSystem

# Backward compatibility - maintain original interface
__all__ = [
    # Types
    "StorageType",
    "DataIntegrityLevel",
    "BackupStrategy",
    "StorageMetadata",
    "StorageConfig",
    # Core classes
    "PersistentDataStorage",
    "UnifiedStorageSystem",
    # Legacy alias for backward compatibility
    "PersistentDataStorage as Storage",  # Maintains original import
]

# Version information
__version__ = "2.0.0"
__author__ = "Agent-4 (Quality Assurance Specialist)"
__description__ = "Refactored storage system meeting 200 LOC standards"

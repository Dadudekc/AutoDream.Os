#!/usr/bin/env python3
"""
File Operations Package - V2 Compliant
=====================================

Modularized file operations system extracted from consolidated_file_operations.py
for V2 compliance (≤400 lines per module).

Modules:
- file_metadata: File metadata operations and analysis
- file_serialization: JSON/YAML serialization and file I/O
- file_backup: File backup and restore operations

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from .file_backup import BackupResult, FileBackupOperations, ScanResult
from .file_metadata import DirectoryInfo, FileInfo, FileMetadataOperations
from .file_serialization import FileSerializationOperations

__all__ = [
    # Metadata classes
    "FileInfo",
    "DirectoryInfo",
    "FileMetadataOperations",
    # Serialization classes
    "FileSerializationOperations",
    # Backup classes
    "BackupResult",
    "ScanResult",
    "FileBackupOperations",
]

__version__ = "1.0.0"
__author__ = "Agent-3 (Infrastructure & DevOps Specialist)"


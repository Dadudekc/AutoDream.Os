#!/usr/bin/env python3
"""
File Locking Package - V2 Compliance Module
==========================================

Modular file locking system for V2 compliance.
Replaces monolithic file_lock.py.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from .file_locking_models import (
    LockConfig,
    LockInfo,
    LockStatus,
    LockResult,
    LockMetrics,
)
from .file_locking_engine import FileLockEngine
from .file_locking_manager import FileLockManager
from .file_locking_orchestrator import (
    get_file_lock_manager,
    create_file_lock,
    acquire_lock,
    release_lock,
    is_locked,
    cleanup_stale_locks,
    get_lock_metrics,
)

__all__ = [
    'LockConfig',
    'LockInfo',
    'LockStatus',
    'LockResult',
    'LockMetrics',
    'FileLockEngine',
    'FileLockManager',
    'get_file_lock_manager',
    'create_file_lock',
    'acquire_lock',
    'release_lock',
    'is_locked',
    'cleanup_stale_locks',
    'get_lock_metrics',
]

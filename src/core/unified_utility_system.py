#!/usr/bin/env python3
"""
Unified Utility System - V2 Compliance Redirect
==============================================

V2 compliance redirect to modular utility system.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

# V2 COMPLIANCE REDIRECT - see utility_system package

from .utility_system import (
    UtilityOperation,
    UtilityConfig,
    UtilityMetrics,
    UtilityOperationType,
    UtilityStatus,
    UnifiedUtilitySystem,
    get_unified_utility,
    get_project_root,
    format_string,
    sanitize_string,
    validate_string,
    transform_data,
    read_file,
    write_file,
    create_directory,
    copy_file,
    move_file,
    delete_file,
    get_file_size,
    get_file_extension,
    normalize_path,
    resolve_path,
    get_relative_path,
    ensure_directory_exists,
    get_directory_contents,
    get_file_hash,
    backup_file,
    restore_file,
    get_utility_metrics,
)

# Re-export for backward compatibility
__all__ = [
    'UtilityOperation',
    'UtilityConfig',
    'UtilityMetrics',
    'UtilityOperationType',
    'UtilityStatus',
    'UnifiedUtilitySystem',
    'get_unified_utility',
    'get_project_root',
    'format_string',
    'sanitize_string',
    'validate_string',
    'transform_data',
    'read_file',
    'write_file',
    'create_directory',
    'copy_file',
    'move_file',
    'delete_file',
    'get_file_size',
    'get_file_extension',
    'normalize_path',
    'resolve_path',
    'get_relative_path',
    'ensure_directory_exists',
    'get_directory_contents',
    'get_file_hash',
    'backup_file',
    'restore_file',
    'get_utility_metrics',
]

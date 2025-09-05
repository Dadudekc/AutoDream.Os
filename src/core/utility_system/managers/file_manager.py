#!/usr/bin/env python3
"""
File Manager - V2 Compliance Redirect
=====================================

V2 compliance redirect to modular file manager system.
Refactored from 358-line monolithic file into focused modules.

Author: Agent-8 (SSOT & System Integration Specialist) - V2 Compliance Refactoring
Original: Agent-5 - Business Intelligence Specialist
License: MIT
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .file_manager_v2 import (
    FileManager,
    FileOperationConfig,
    create_file_manager,
    get_file_manager
)

# Re-export for backward compatibility
__all__ = [
    'FileManager',
    'FileOperationConfig',
    'create_file_manager',
    'get_file_manager'
]

"""
Utility System Package
=====================

KISS Simplified utility system package.
Restored after deletion to maintain functionality.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Restoration
License: MIT
"""

from .managers.file_manager import FileManager, create_file_manager, get_file_manager

__all__ = [
    'FileManager',
    'create_file_manager',
    'get_file_manager'
]

"""
File Operations Package
=======================

Modular file operations handlers for V2 compliance.
Extracted from file_manager.py for improved maintainability.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

from .file_reader import FileReader
from .file_writer import FileWriter
from .file_operations import FileOperations

__all__ = [
    'FileReader',
    'FileWriter',
    'FileOperations'
]

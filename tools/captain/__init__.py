"""
Captain Tools Package
====================

Integrated Captain tools for role/mode management, agent oversight,
and system coordination.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

from .role_manager import RoleManager
from .mode_manager import ModeManager
from .cli import main as cli_main

__all__ = ['RoleManager', 'ModeManager', 'cli_main']
__version__ = '1.0.0'
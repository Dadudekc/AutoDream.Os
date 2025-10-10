"""
DreamVault - AI Training & Memory Intelligence System.

V2 Compliance: Ported from DreamVault repository
Author: Agent-7 - Repository Cloning Specialist
License: MIT
"""

from .config import Config
from .database import DatabaseConnection as Database

# Schema module - import full module, not specific class
from . import schema

__all__ = [
    'Config',
    'Database',
    'schema',
]


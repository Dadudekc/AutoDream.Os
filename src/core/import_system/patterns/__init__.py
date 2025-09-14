"""
Import Pattern Definitions
=========================

This module contains import pattern definitions and utilities for the import system.
"""

from .module_patterns import ModuleImportPattern
from .package_patterns import PackageImportPattern

__all__ = [
    'ModuleImportPattern',
    'PackageImportPattern'
]


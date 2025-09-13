"""
Core messaging systems registry and health checking.

This module provides the Single Source of Truth (SSOT) for all 19 messaging systems
in the Agent Cellphone V2 repository, with health checking and CLI tools.
"""

from .registry_loader import SystemSpec, load_registry, resolve, iter_specs
from .health_check import check_imports, assert_all_importable

__all__ = [
    "SystemSpec",
    "load_registry",
    "resolve",
    "iter_specs",
    "check_imports",
    "assert_all_importable"
]

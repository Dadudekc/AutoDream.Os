#!/usr/bin/env python3
"""
Repository System Package - V2 Unified Architecture
==================================================

CONSOLIDATED repository system - single RepositorySystemManager replaces 16 separate files.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from ..managers.repository_system_manager import (
    RepositorySystemManager,
    RepositoryMetadata,
    TechnologyStack,
    AnalysisResult,
    DiscoveryConfig,
    DiscoveryStatus,
    TechnologyType
)

from .access import is_repository, list_files
from .sync import fetch, get_status
from .audit import audit_repository

__version__ = "2.0.0"
__author__ = "V2 SWARM CAPTAIN"
__license__ = "MIT"

__all__ = [
    "RepositorySystemManager",
    "RepositoryMetadata", 
    "TechnologyStack",
    "AnalysisResult",
    "DiscoveryConfig",
    "DiscoveryStatus",
    "TechnologyType",
    "is_repository",
    "list_files",
    "fetch",
    "get_status",
    "audit_repository"
]

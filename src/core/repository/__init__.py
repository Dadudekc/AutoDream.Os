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
    "TechnologyType"
]

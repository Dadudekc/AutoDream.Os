#!/usr/bin/env python3
"""
Repository Scanner Package
==========================

A comprehensive repository scanning and analysis system with:
- Repository discovery
- Technology stack detection
- Architecture analysis
- Security assessment
- Performance metrics
- Report generation

Author: Agent-1 (Performance & Health Systems)
License: MIT
"""

from .discovery_engine import RepositoryDiscoveryEngine, DiscoveryConfig
from .technology_detector import TechnologyDetector, TechnologyStack
from .analysis_engine import RepositoryAnalysisEngine, AnalysisResult
from .report_generator import RepositoryReportGenerator
from .repository_metadata import RepositoryMetadata, RepositoryMetadataManager
from .report_export import ReportExportManager
from .technology_database import TechnologyDatabase
from .version_detector import VersionDetector
from .repository_scanner import RepositoryScanner

__version__ = "2.0.0"
__author__ = "Agent-1 (Performance & Health Systems)"
__license__ = "MIT"

__all__ = [
    "RepositoryDiscoveryEngine",
    "DiscoveryConfig",
    "TechnologyDetector",
    "TechnologyStack",
    "RepositoryAnalysisEngine",
    "AnalysisResult",
    "RepositoryReportGenerator",
    "RepositoryMetadata",
    "RepositoryMetadataManager",
    "ReportExportManager",
    "TechnologyDatabase",
    "VersionDetector",
    "RepositoryScanner",
]

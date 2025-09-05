#!/usr/bin/env python3
"""
Architecture Analysis Tools Refactored - V2 Compliance Module
=============================================================

Main refactored entry point for architecture analysis tools.

Author: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

# Import models
from .analysis_tools_models import (
    ArchitecturePattern,
    FileAnalysis,
    DuplicateFile,
    RefactoringSuggestion,
    AnalysisReport
)

# Import core functionality
from .analysis_tools_core import ArchitectureAnalyzer

# Re-export all components for backward compatibility
__all__ = [
    'ArchitecturePattern',
    'FileAnalysis',
    'DuplicateFile',
    'RefactoringSuggestion',
    'AnalysisReport',
    'ArchitectureAnalyzer'
]

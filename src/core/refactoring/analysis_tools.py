#!/usr/bin/env python3
"""
Architecture Analysis Tools - KISS Simplified
=============================================

Backward compatibility wrapper for architecture analysis tools.

Author: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

# Import all components from refactored modules
from .analysis_tools_refactored import *

# Re-export all components for backward compatibility
__all__ = [
    'ArchitecturePattern',
    'FileAnalysis',
    'DuplicateFile',
    'RefactoringSuggestion',
    'AnalysisReport',
    'ArchitectureAnalyzer'
]
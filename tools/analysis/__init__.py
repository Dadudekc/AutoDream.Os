"""
V2 Compliance Analysis Tool Package
==================================

Modular V2 compliance analysis tools for the Agent Cellphone V2 project.

Components:
- core: Core analysis functions
- violations: Violation detection and reporting
- refactor: Refactoring suggestions and planning
- cli: Command-line interface

Usage:
    from tools.analysis import AnalysisCore, ViolationDetector, RefactorPlanner
"""

from .core import AnalysisCore, should_exclude_file, count_lines
from .violations import ViolationDetector, format_violations_text
from .refactor import RefactorPlanner, generate_refactor_suggestions, format_refactor_report
from .cli import main

__all__ = [
    "AnalysisCore",
    "ViolationDetector", 
    "RefactorPlanner",
    "should_exclude_file",
    "count_lines",
    "format_violations_text",
    "generate_refactor_suggestions",
    "format_refactor_report",
    "main"
]

__version__ = "2.0.0"
__author__ = "V2_SWARM Agent-4 (Captain)"
__description__ = "V2 Compliant Analysis Tool Package"



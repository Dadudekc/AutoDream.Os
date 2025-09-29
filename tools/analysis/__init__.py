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

from .cli import main
from .core import AnalysisCore, count_lines, should_exclude_file
from .refactor import RefactorPlanner, format_refactor_report, generate_refactor_suggestions
from .violations import ViolationDetector, format_violations_text

__all__ = [
    "AnalysisCore",
    "ViolationDetector",
    "RefactorPlanner",
    "should_exclude_file",
    "count_lines",
    "format_violations_text",
    "generate_refactor_suggestions",
    "format_refactor_report",
    "main",
]

__version__ = "2.0.0"
__author__ = "V2_SWARM Agent-4 (Captain)"
__description__ = "V2 Compliant Analysis Tool Package"

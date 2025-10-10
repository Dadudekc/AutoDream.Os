#!/usr/bin/env python3
"""
Complexity Analyzer - Intelligent Quality Automation
====================================================
AST-based complexity analysis for Python code.
Refactored for V2 compliance (<400 lines).

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
Refactored: Agent-5 (V2 Compliance)
License: MIT
"""

# Backward compatibility - re-export from modular components
from .complexity_analyzer_core import (
    ComplexityAnalysisService,
    ComplexityAnalyzer,
    ComplexityMetrics,
    ComplexityReport,
    ComplexityViolation,
    CognitiveComplexityVisitor,
    CyclomaticComplexityVisitor,
)
from .complexity_analyzer_cli import main

__all__ = [
    "ComplexityAnalyzer",
    "ComplexityAnalysisService",
    "ComplexityMetrics",
    "ComplexityReport",
    "ComplexityViolation",
    "CyclomaticComplexityVisitor",
    "CognitiveComplexityVisitor",
    "main",
]

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Architectural Patterns Test Module
==================================

Modularized architectural patterns testing suite.
Replaces the original test_architectural_patterns_comprehensive_agent2.py (580 lines)
with 3 V2-compliant modules (≤400 lines each).

Modules:
- test_solid_principles.py: SOLID principles validation tests
- test_design_patterns.py: Design pattern implementation tests
- test_architecture_validation.py: Architecture validation and quality assurance tests

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from .test_solid_principles import TestSOLIDPrinciplesComprehensive
from .test_design_patterns import TestDesignPatternsComprehensive
from .test_architecture_validation import TestArchitectureValidationComprehensive

__version__ = "2.0.0"
__author__ = "Agent-2 (Architecture & Design Specialist)"

__all__ = [
    "TestSOLIDPrinciplesComprehensive",
    "TestDesignPatternsComprehensive",
    "TestArchitectureValidationComprehensive"
]

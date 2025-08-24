#!/usr/bin/env python3
"""
Duplication Detection Package - Agent Cellphone V2
=================================================

Advanced duplication detection system broken into modular components.
Follows V2 standards: ≤200 LOC per file, OOP design, SRP compliance.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .duplication_types import DuplicationIssue, CodeBlock
from .duplication_detector import DuplicationDetector
from .code_analyzer import CodeAnalyzer
from .duplication_reporter import DuplicationReporter

__all__ = [
    'DuplicationIssue',
    'CodeBlock', 
    'DuplicationDetector',
    'CodeAnalyzer',
    'DuplicationReporter'
]


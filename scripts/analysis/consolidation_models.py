#!/usr/bin/env python3
"""
Consolidation Models - Logic Consolidation System
===============================================

Models and data structures for the logic consolidation system.

Author: Agent-8 (Integration Enhancement Optimization Manager)
License: MIT
"""



@dataclass
class LogicPattern:
    """Logic pattern definition extracted from source files."""
    name: str
    file_path: str
    line_number: int
    function_type: str  # validate, process, initialize, cleanup, etc.
    signature: str
    docstring: str = ""
    complexity: int = 0

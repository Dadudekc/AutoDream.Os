#!/usr/bin/env python3
"""
Refactoring Models - Data Structures for Refactoring Analysis
==============================================================

Data models for refactoring suggestion engine.
Extracted from refactoring_suggestion_engine.py for V2 compliance.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
License: MIT
"""

from dataclasses import dataclass, field


@dataclass
class CodeEntity:
    """Represents a code entity (class, function, etc.)."""

    entity_type: str  # "class", "function", "import", "constant"
    name: str
    start_line: int
    end_line: int
    line_count: int
    dependencies: list[str] = field(default_factory=list)
    complexity: int = 0
    category: str = "general"  # "model", "util", "service", "repository", etc.


@dataclass
class ModuleSuggestion:
    """Suggested module extraction."""

    module_name: str
    purpose: str
    entities: list[CodeEntity]
    estimated_lines: int
    priority: int  # 1=high, 2=medium, 3=low


@dataclass
class RefactoringSuggestion:
    """Complete refactoring suggestion for a file."""

    file_path: str
    violation_type: str
    current_lines: int
    target_lines: int
    confidence: float
    reasoning: str
    modules: list[ModuleSuggestion]
    estimated_main_lines: int
    import_changes: str
    will_be_compliant: bool
    total_lines_after: int

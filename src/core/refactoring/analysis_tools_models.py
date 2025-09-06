#!/usr/bin/env python3
"""
Architecture Analysis Tools Models - V2 Compliance Module
=========================================================

Data models for architecture analysis tools.

Author: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple


@dataclass
class ArchitecturePattern:
    """Represents an identified architecture pattern - simplified."""

    name: str
    pattern_type: str
    files: List[str]
    confidence: float
    description: str


@dataclass
class FileAnalysis:
    """Analysis results for a single file - simplified."""

    file_path: str
    line_count: int
    classes: List[str]
    functions: List[str]
    imports: List[str]
    complexity_score: float
    v2_compliance: bool


@dataclass
class DuplicateFile:
    """Represents duplicate file information - simplified."""

    original_file: str
    duplicate_files: List[str]
    similarity_score: float


@dataclass
class RefactoringSuggestion:
    """Represents a refactoring suggestion - simplified."""

    file_path: str
    suggestion_type: str
    description: str
    priority: str
    estimated_effort: str


@dataclass
class AnalysisReport:
    """Complete analysis report - simplified."""

    total_files: int
    v2_compliant_files: int
    patterns_found: List[ArchitecturePattern]
    duplicates_found: List[DuplicateFile]
    suggestions: List[RefactoringSuggestion]
    overall_complexity: float
    v2_compliance_percentage: float

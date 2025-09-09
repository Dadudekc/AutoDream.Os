#!/usr/bin/env python3
"""
Architecture Analysis Tools Models - V2 Compliance Module
=========================================================

Data models for architecture analysis tools.

Author: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

from dataclasses import dataclass


@dataclass
class ArchitecturePattern:
    """Represents an identified architecture pattern - simplified."""

    name: str
    pattern_type: str
    files: list[str]
    confidence: float
    description: str


@dataclass
class FileAnalysis:
    """Analysis results for a single file - simplified."""

    file_path: str
    line_count: int
    classes: list[str]
    functions: list[str]
    imports: list[str]
    complexity_score: float
    v2_compliance: bool


@dataclass
class DuplicateFile:
    """Represents duplicate file information - simplified."""

    original_file: str
    duplicate_files: list[str]
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
    patterns_found: list[ArchitecturePattern]
    duplicates_found: list[DuplicateFile]
    suggestions: list[RefactoringSuggestion]
    overall_complexity: float
    v2_compliance_percentage: float

"""Unified access to refactoring analysis tools."""

from .duplicate_analysis import DuplicateFile, find_duplicate_files
from .file_analysis import FileAnalysis, analyze_file_for_extraction
from .pattern_detection import ArchitecturePattern, analyze_architecture_patterns

__all__ = [
    "FileAnalysis",
    "analyze_file_for_extraction",
    "DuplicateFile",
    "find_duplicate_files",
    "ArchitecturePattern",
    "analyze_architecture_patterns",
]

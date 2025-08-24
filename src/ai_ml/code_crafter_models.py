"""Data models used by the modular CodeCrafter system."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class CodeGenerationRequest:
    """Request describing the code to generate."""

    description: str
    language: str = "python"


@dataclass
class CodeGenerationResult:
    """Result of a successful code generation run."""

    code: str
    path: Optional[Path] = None


@dataclass
class CodeAnalysis:
    """Very small placeholder for code analysis results.

    The original project exposed a rich :class:`CodeAnalysis` model.  The
    refactored system keeps a lightweight version so existing imports remain
    valid.  Only a handful of fields are required for the tests in this kata
    and additional fields can be added incrementally as needed.
    """

    file_path: str
    complexity_score: float = 0.0
    maintainability_index: float = 0.0
    code_smells: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    security_issues: List[str] = field(default_factory=list)
    performance_issues: List[str] = field(default_factory=list)
    documentation_coverage: float = 0.0
    test_coverage: float = 0.0


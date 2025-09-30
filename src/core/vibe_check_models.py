"""
Vibe Check Models - Data structures for vibe check analysis.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .design_authority import DecisionSeverity


class VibeCheckResult(Enum):
    """Result of vibe check analysis."""

    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"


@dataclass
class VibeViolation:
    """Represents a vibe check violation."""

    file_path: str
    line_number: int
    violation_type: str
    description: str
    severity: DecisionSeverity
    suggestion: str
    code_snippet: str = ""


@dataclass
class VibeCheckReport:
    """Comprehensive vibe check report."""

    result: VibeCheckResult
    total_files: int
    violations: list[VibeViolation]
    summary: dict[str, Any]
    timestamp: str
    agent_author: str = ""

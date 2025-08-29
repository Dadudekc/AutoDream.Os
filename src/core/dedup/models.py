"""Data models for deduplication system."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class DuplicationType(Enum):
    """Types of code duplication."""

    EXACT_MATCH = "exact_match"
    NEAR_DUPLICATE = "near_duplicate"
    FUNCTION_DUPLICATE = "function_duplicate"
    CLASS_DUPLICATE = "class_duplicate"
    PATTERN_DUPLICATE = "pattern_duplicate"
    STRUCTURAL_DUPLICATE = "structural_duplicate"
    LOGIC_DUPLICATE = "logic_duplicate"


class DuplicationSeverity(Enum):
    """Duplication severity levels."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class DuplicationInstance:
    """Represents a single duplication instance."""

    id: str
    duplication_type: DuplicationType
    severity: DuplicationSeverity
    similarity_score: float
    lines_count: int
    locations: List[Dict[str, Any]]
    code_snippet: str
    hash_value: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DuplicationGroup:
    """Represents a group of related duplications."""

    id: str
    duplication_type: DuplicationType
    instances: List[DuplicationInstance]
    total_duplication: int
    consolidation_priority: DuplicationSeverity
    suggested_consolidation: str
    estimated_effort: str
    metadata: Dict[str, Any] = field(default_factory=dict)
